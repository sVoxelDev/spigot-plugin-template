#!/usr/bin/env python3
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import time
import urllib.request
import uuid
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".template"
USER_AGENT = "paper-plugin-template/6 (https://github.com/sVoxelDev/spigot-plugin-template)"


def run(args, *, capture=False, check=True, timeout=600):
    result = subprocess.run([str(arg) for arg in args], cwd=ROOT, text=True,
                            stdout=subprocess.PIPE if capture else None,
                            stderr=subprocess.PIPE if capture else None, timeout=timeout)
    if check and result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(map(str, args[:3]))}\n"
                           + (result.stdout or "") + (result.stderr or ""))
    return result


def config():
    return json.loads((ROOT / "template.json").read_text())


def properties():
    return dict(line.strip().split("=", 1) for line in (ROOT / "gradle.properties").read_text().splitlines()
                if "=" in line and not line.lstrip().startswith("#"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


@contextlib.contextmanager
def project_lock():
    STATE.mkdir(exist_ok=True)
    with (STATE / "project.lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another template command is changing this checkout. Use an isolated checkout.") from None
        yield


def docker_ready():
    if not shutil.which("docker"):
        raise RuntimeError("Install Docker Engine or Docker Desktop, then run ./template doctor.")
    run(["docker", "info"], capture=True, timeout=30)


def doctor():
    docker_ready()
    result = {
        "python": sys.version.split()[0],
        "docker": json.loads(run(["docker", "version", "--format", "{{json .}}"], capture=True).stdout),
        "platform": run(["docker", "info", "--format", "{{.OSType}}/{{.Architecture}}"], capture=True).stdout.strip(),
        "profiles": config()["servers"],
        "free_disk_gib": round(shutil.disk_usage(ROOT).free / 1024**3, 1),
    }
    print(json.dumps(result, indent=2))


def build(tasks=None):
    docker_ready()
    cache = ROOT / ".gradle-user-home"
    cache.mkdir(exist_ok=True)
    command = ["docker", "run", "--rm", "--user", f"{os.getuid()}:{os.getgid()}",
               "--mount", f"type=bind,src={ROOT},dst=/workspace", "--workdir", "/workspace",
               "--env", "GRADLE_USER_HOME=/workspace/.gradle-user-home",
               "--env", "JAVA_TOOL_OPTIONS=-Djava.util.prefs.userRoot=/tmp/paper-plugin-prefs", config()["build_image"],
               "./gradlew", "--no-daemon", "--console=plain"]
    run(command + (tasks or ["build"]))


def artifact():
    props = properties()
    jar = ROOT / "build/libs" / f"{props['pluginName']}-{props['version']}.jar"
    source_descriptor = (ROOT / "src/main/resources/plugin.yml").read_text()
    entrypoint = re.search(r"^main:\s*(.+?)\s*$", source_descriptor, re.MULTILINE)
    if not entrypoint:
        raise RuntimeError("Source descriptor must declare a main entrypoint.")
    main_class = entrypoint.group(1).strip("'\"")
    for key, value in props.items():
        main_class = main_class.replace("${" + key + "}", value)
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        descriptor = archive.read("plugin.yml").decode()
        for key, value in {"name": props["pluginName"], "version": props["version"],
                           "main": main_class, "api-version": props["apiVersion"]}.items():
            if not re.search(rf"^{re.escape(key)}: ['\"]?{re.escape(value)}['\"]?$", descriptor, re.MULTILINE):
                raise RuntimeError(f"Packaged descriptor has the wrong {key}.")
        if main_class.replace(".", "/") + ".class" not in names:
            raise RuntimeError("Packaged entrypoint class is missing from the jar.")
        forbidden = [name for name in names if name.startswith(("org/bukkit/", "io/papermc/paper/",
                      "org/junit/", "org/mockbukkit/")) or name.endswith("Test.class")]
        if forbidden or "${" in descriptor:
            raise RuntimeError(f"Jar contains test/server classes or unexpanded metadata: {forbidden}")
        default_config = archive.read("config.yml").decode()
        enabled = re.search(r"^\s*enabled:\s*(true|false)\s*$", default_config, re.MULTILINE)
        if not enabled:
            raise RuntimeError("The example contract requires a boolean greeting.enabled default.")
    return jar, enabled.group(1) == "true"


def request_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def paper_jar(profile):
    pin = config()["servers"][profile]
    target = STATE / "downloads" / f"paper-{pin['version']}-{pin['build']}.jar"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and digest(target) == pin["sha256"]:
        return target
    temporary = target.with_suffix(".download")
    print(f"Downloading Paper {pin['version']} build {pin['build']} ({pin['channel']})", flush=True)
    request = urllib.request.Request(pin["url"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as stream:
            shutil.copyfileobj(response, stream)
        if digest(temporary) != pin["sha256"]:
            raise RuntimeError("Paper download checksum differs from template.json. Refusing to run it.")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return target


def container_details(name):
    return json.loads(run(["docker", "inspect", name], capture=True).stdout)[0]


def owned_container(name):
    details = container_details(name)
    if details["Config"].get("Labels", {}).get("paper-template.checkout") != str(ROOT):
        raise RuntimeError(f"Container {name} belongs to another checkout.")
    return details


def server_start(name, data, jar, profile, *, publish=None, online=True):
    if run(["docker", "inspect", name], capture=True, check=False).returncode == 0:
        raise RuntimeError(f"Container {name} already exists. Inspect it before starting another server.")
    data.mkdir(parents=True, exist_ok=True)
    server = paper_jar(profile)
    command = ["docker", "run", "--detach", "--name", name,
               "--label", f"paper-template.checkout={ROOT}",
               "--mount", f"type=bind,src={data},dst=/data",
               "--mount", f"type=bind,src={jar},dst=/plugins/{jar.name},readonly",
               "--mount", f"type=bind,src={server},dst=/server/paper.jar,readonly"]
    env = {
        "EULA": "TRUE", "TYPE": "PAPER", "PAPER_CUSTOM_JAR": "/server/paper.jar",
        "VERSION": config()["servers"][profile]["version"], "SKIP_DOWNLOAD_DEFAULTS": "TRUE",
        "UID": str(os.getuid()), "GID": str(os.getgid()), "MEMORY": "2G",
        "ONLINE_MODE": str(online).upper(), "ENABLE_RCON": "TRUE", "RCON_PASSWORD": secrets.token_urlsafe(24),
        "VIEW_DISTANCE": "3", "SIMULATION_DISTANCE": "3", "MAX_PLAYERS": "8",
        "GENERATE_STRUCTURES": "FALSE", "LEVEL_TYPE": "minecraft:flat",
        "GENERATOR_SETTINGS": json.dumps({"layers": [{"block": "minecraft:bedrock", "height": 1},
            {"block": "minecraft:dirt", "height": 2}, {"block": "minecraft:grass_block", "height": 1}],
            "biome": "minecraft:plains", "structure_overrides": []}),
        "SPAWN_PROTECTION": "0", "ENABLE_QUERY": "FALSE", "ENABLE_ROLLING_LOGS": "true",
    }
    if not online:
        env["JVM_OPTS"] = "-Dpaper.disableStartupVersionCheck"
    for key, value in env.items():
        command.extend(["--env", f"{key}={value}"])
    if publish:
        command.extend(["--publish", f"{publish}:25565"])
    command.append(config()["server_image"])
    try:
        run(command, capture=True)
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        inspection = run(["docker", "inspect", name], capture=True, check=False)
        if inspection.returncode == 0:
            details = owned_container(name)
            if not details["State"]["Running"]:
                run(["docker", "rm", name], capture=True)
        raise


def wait_server(name, timeout):
    deadline = time.monotonic() + timeout
    next_update = 0
    while time.monotonic() < deadline:
        state = container_details(name)["State"]
        if not state["Running"]:
            raise RuntimeError(f"Server exited with code {state['ExitCode']} before becoming healthy.")
        if state.get("Health", {}).get("Status") == "healthy":
            return
        if time.monotonic() >= next_update:
            print(f"Waiting for {name} to become healthy...", flush=True)
            next_update = time.monotonic() + 30
        time.sleep(2)
    raise RuntimeError(f"Server did not become healthy within {timeout} seconds.")


def rcon(name, command):
    owned_container(name)
    return run(["docker", "exec", name, "rcon-cli", command], capture=True, timeout=30).stdout.strip()


def log_errors(log, *, expected_invalid=False):
    errors = []
    for line in log.splitlines():
        if re.search(r"\b(ERROR|SEVERE)\b|Error occurred while|Could not load|Exception|Caused by:|command not found", line):
            if expected_invalid and "Invalid configuration:" in line:
                continue
            errors.append(line)
    return errors


def validate_server(profile, report_dir, jar, default_enabled, timeout):
    props = properties()
    name = "paper-validate-" + uuid.uuid4().hex[:12]
    data = report_dir / profile / "data"
    report = {"profile": profile, "pin": config()["servers"][profile], "checks": [], "status": "running",
              "startup_update_check": False}
    phase = "fresh"
    phase_logs = []
    started = False

    def expect(command, expected):
        response = rcon(name, command)
        report["checks"].append({"phase": phase, "command": command, "response": response, "expected": expected})
        if expected not in response:
            raise RuntimeError(f"{profile}: {command!r} returned {response!r}; expected {expected!r}.")

    def status(enabled):
        expect(props["commandName"] + " status", f"{props['pluginName']} v{props['version']}. Greeting: {'enabled' if enabled else 'disabled'}.")

    def capture_logs(expected_invalid=False):
        log = run(["docker", "logs", name], capture=True, check=False)
        content = log.stdout + log.stderr
        path = report_dir / profile / f"{phase}.log"
        path.write_text(content)
        phase_logs.append(path.name)
        errors = log_errors(content, expected_invalid=expected_invalid)
        if errors:
            raise RuntimeError(f"Server log contains errors. See {path}: {errors[:3]}")
        if f"Disabling {props['pluginName']} v{props['version']}" not in content:
            raise RuntimeError(f"Plugin did not disable cleanly. See {path}.")
        return content

    def stop_and_capture(expected_invalid=False):
        owned_container(name)
        run(["docker", "stop", "--time", "60", name], capture=True, timeout=90)
        details = container_details(name)
        if details["State"]["ExitCode"] != 0:
            raise RuntimeError(f"Unclean server shutdown: exit {details['State']['ExitCode']}.")
        return capture_logs(expected_invalid)

    def remove():
        owned_container(name)
        run(["docker", "rm", name], capture=True)

    try:
        server_start(name, data, jar, profile, online=False)
        started = True
        wait_server(name, timeout)
        details = container_details(name)
        report["image_id"] = details["Image"]
        report["java"] = run(["docker", "exec", name, "java", "-version"], capture=True).stderr.strip()
        startup_log = run(["docker", "logs", name], capture=True)
        startup = startup_log.stdout + startup_log.stderr
        version_pattern = rf"Loading Paper {re.escape(report['pin']['version'])}-{report['pin']['build']}[- ]"
        if not re.search(version_pattern, startup):
            raise RuntimeError("Startup log does not identify the pinned Paper version/build.")
        report["checks"].append({"phase": phase, "check": "actual Paper version/build", "expected": version_pattern})
        expect("version " + props["pluginName"], props["version"])
        status(default_enabled)
        expect(props["commandName"], f"Usage: /{props['commandName']}")
        expect(props["commandName"] + " info", "Only players can use this command.")
        plugin_config = data / "plugins" / props["pluginName"] / "config.yml"
        if not plugin_config.is_file():
            raise RuntimeError("Fresh install did not create config.yml.")
        phase = "reload"
        custom = "greeting:\n  enabled: false\n  message: 'Hello, {player}. Custom configuration!'\n"
        plugin_config.write_text(custom)
        expect(props["commandName"] + " reload", "Configuration reloaded.")
        status(False)
        plugin_config.write_text("greeting: [broken\n")
        expect(props["commandName"] + " reload", "Configuration was not reloaded:")
        status(False)
        plugin_config.write_text("greeting:\n  enabled: 'false'\n  message: 'Wrong type'\n")
        expect(props["commandName"] + " reload", "greeting.enabled must be true or false")
        status(False)
        plugin_config.write_text(custom)
        stop_and_capture()
        remove()
        started = False
        phase = "restart"
        server_start(name, data, jar, profile, online=False)
        started = True
        wait_server(name, timeout)
        status(False)
        if plugin_config.read_text() != custom:
            raise RuntimeError("Restart overwrote the custom configuration.")
        expect(props["commandName"] + " reload", "Configuration reloaded.")
        stop_and_capture()
        remove()
        started = False
        phase = "invalid-startup"
        plugin_config.write_text("greeting:\n  enabled: false\n  message: ''\n")
        server_start(name, data, jar, profile, online=False)
        started = True
        wait_server(name, timeout)
        expect("plugins", props["pluginName"])
        startup_log = run(["docker", "logs", name], capture=True)
        content = startup_log.stdout + startup_log.stderr
        if f"Disabling {props['pluginName']} v{props['version']}" not in content:
            raise RuntimeError("Invalid configuration did not disable the plugin before shutdown.")
        if "Invalid configuration: greeting.message must be a nonempty string" not in content:
            raise RuntimeError("Invalid startup did not explain its configuration error.")
        report["checks"].append({"phase": phase, "check": "invalid configuration disables the plugin", "before_shutdown": True, "result": "passed"})
        stop_and_capture(expected_invalid=True)
        remove()
        started = False
        phase = "recovery"
        plugin_config.write_text("greeting:\n  enabled: true\n  message: 'Recovered, {player}!'\n")
        server_start(name, data, jar, profile, online=False)
        started = True
        wait_server(name, timeout)
        status(True)
        stop_and_capture()
        report["status"] = "passed"
    except Exception as exception:
        report["status"] = "failed"
        report["error"] = str(exception)
        raise
    finally:
        if started:
            run(["docker", "stop", "--time", "60", name], capture=True, check=False, timeout=90)
            log = run(["docker", "logs", name], capture=True, check=False)
            (report_dir / profile / "final.log").write_text(log.stdout + log.stderr)
            run(["docker", "rm", name], capture=True, check=False)
        report["logs"] = phase_logs
        write_json(report_dir / profile / "results.json", report)
    print(f"PASS: Paper {report['pin']['version']} ({report['pin']['channel']}), {len(report['checks'])} checks", flush=True)
    return report


def validate(args):
    run_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    directory = ROOT / "build/validation" / run_id
    profiles = args.profile or list(config()["servers"])
    report = {"status": "running", "started_at": run_id,
              "build_skipped": args.skip_build, "server_image": config()["server_image"], "servers": []}
    try:
        docker_ready()
        if not args.skip_build:
            build()
        run([sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-v"])
        jar, default_enabled = artifact()
        directory.mkdir(parents=True)
        snapshot = directory / jar.name
        shutil.copy2(jar, snapshot)
        report.update({"jar": snapshot.name, "jar_sha256": digest(snapshot)})
        for profile in profiles:
            try:
                report["servers"].append(validate_server(profile, directory, snapshot, default_enabled, args.timeout))
            except Exception:
                profile_report = directory / profile / "results.json"
                if profile_report.exists():
                    report["servers"].append(json.loads(profile_report.read_text()))
                raise
        report["status"] = "passed"
    except Exception as exception:
        report["status"] = "failed"
        report["error"] = str(exception)
        raise
    finally:
        write_json(directory / "results.json", report)
        write_json(ROOT / "build/validation/latest.json", {"report": str(directory.relative_to(ROOT)), "status": report["status"]})
        print(f"Validation evidence: {directory}", flush=True)


def initialize(args):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{1,63}", args.name):
        raise RuntimeError("Plugin name must be 2-64 letters, digits, or underscores, starting with a letter.")
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*){2,}", args.package):
        raise RuntimeError("Package must have at least three lowercase Java identifiers, e.g. io.github.alex.welcome.")
    if any(part in JAVA_KEYWORDS for part in args.package.split(".")):
        raise RuntimeError("Package segments must not be Java keywords.")
    if not re.fullmatch(r"[a-z][a-z0-9_-]{1,31}", args.command):
        raise RuntimeError("Command must be 2-32 lowercase letters, digits, underscores, or hyphens.")
    if not re.fullmatch(r"[A-Za-z0-9_ .-]{1,64}", args.author):
        raise RuntimeError("Author must be 1-64 letters, digits, spaces, underscores, dots, or hyphens.")
    props = properties()
    same_identity = props["packageName"] == args.package and props["pluginName"] == args.name and props["commandName"] == args.command
    if same_identity and props["author"] == args.author:
        print("Template already has this identity.")
        return
    moves = []
    for source_root in (ROOT / "src/main/java", ROOT / "src/test/java"):
        old = source_root / props["packageName"].replace(".", "/")
        target = source_root / args.package.replace(".", "/")
        if old != target and target.exists():
            raise RuntimeError(f"Target package already exists: {target}")
        moves.append((old, target))
    for source_root in (ROOT / "src/main/java", ROOT / "src/test/java"):
        for path in source_root.rglob("*.java"):
            path.write_text(path.read_text().replace(props["packageName"], args.package))
    for old, target in moves:
        if old != target:
            staged = old.parents[len(props["packageName"].split(".")) - 1] / (".rename-" + uuid.uuid4().hex)
            old.rename(staged)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(staged, target)
    replacements = {"group": args.package.rsplit(".", 1)[0], "packageName": args.package,
                    "pluginName": args.name, "commandName": args.command, "author": args.author,
                    "version": props["version"] if same_identity else "1.0.0-SNAPSHOT"}
    text = (ROOT / "gradle.properties").read_text()
    for key, value in replacements.items():
        text = re.sub(rf"^{key}=.*$", f"{key}={value}", text, flags=re.MULTILINE)
    (ROOT / "gradle.properties").write_text(text)
    (ROOT / "settings.gradle").write_text(f"rootProject.name = '{args.command}-plugin'\n")
    print(f"Configured {args.name} ({args.package}), /{args.command}. Run ./template validate --accept-eula.")


JAVA_KEYWORDS = set("abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null _".split())


def paper_release_versions():
    project = request_json("https://fill.papermc.io/v3/projects/paper")
    versions = [version for group in project["versions"].values() for version in group
                if re.fullmatch(r"\d+(?:\.\d+)+", version)]
    versions.sort(key=lambda version: tuple(map(int, version.split("."))), reverse=True)
    return versions


def latest_candidates():
    versions = paper_release_versions()
    selected = {}
    for version in versions:
        builds = request_json(f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds")
        for profile, channels in (("latest", {"STABLE", "RECOMMENDED", "BETA"}), ("stable", {"STABLE", "RECOMMENDED"})):
            candidates = [build for build in builds if build["channel"] in channels]
            if profile not in selected and candidates:
                selected[profile] = {"version": version, **max(candidates, key=lambda build: build["id"])}
        if len(selected) == 2:
            break
    return selected


def versions():
    candidates = latest_candidates()
    upstream_version = paper_release_versions()[0]
    upstream_paper = request_json(f"https://fill.papermc.io/v3/projects/paper/versions/{upstream_version}/builds/latest")
    upstream_minecraft = request_json("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")["latest"]
    current = properties()
    dependencies = {}
    for property_name, coordinate in {
        "junitVersion": "org/junit/jupiter/junit-jupiter",
        "jacocoVersion": "org/jacoco/org.jacoco.core",
        "mockBukkitVersion": f"org/mockbukkit/mockbukkit/mockbukkit-v{candidates['stable']['version']}",
    }.items():
        url = f"https://repo.maven.apache.org/maven2/{coordinate}/maven-metadata.xml"
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                available = [node.text for node in ET.parse(response).findall("versioning/versions/version")
                             if node.text and re.fullmatch(r"\d+(?:\.\d+)+", node.text)]
                latest = max(available, key=lambda value: tuple(map(int, value.split(".")))) if available else None
            dependencies[property_name] = {"pinned": current[property_name], "available": latest, "source": url}
        except OSError as exception:
            dependencies[property_name] = {"pinned": current[property_name], "error": str(exception), "source": url}
    print(json.dumps({"pinned": config()["servers"], "available": candidates,
                      "upstream": {"minecraft": upstream_minecraft, "paper": {"version": upstream_version, **upstream_paper}},
                      "latest_release_supported": candidates["latest"]["version"] == upstream_minecraft["release"],
                      "dependencies": dependencies,
                      "gradle": request_json("https://services.gradle.org/versions/current")}, indent=2))


def dev_state():
    path = STATE / "dev.json"
    if not path.exists():
        raise RuntimeError("No development server. Start one with ./template up --accept-eula.")
    return json.loads(path.read_text())


def up(args):
    if (STATE / "dev.json").exists():
        raise RuntimeError("A development server is already recorded. Run ./template down before starting another.")
    build()
    jar, _ = artifact()
    directory = STATE / "dev"
    directory.mkdir(parents=True, exist_ok=True)
    snapshot = directory / "plugin.jar"
    shutil.copy2(jar, snapshot)
    name = "paper-dev-" + hashlib.sha256(str(ROOT).encode()).hexdigest()[:12]
    profile = args.profile or config()["default_profile"]
    server_start(name, directory / "data", snapshot, profile, publish=f"127.0.0.1:{args.port}")
    write_json(STATE / "dev.json", {"container": name, "profile": profile, "port": args.port})
    try:
        wait_server(name, args.timeout)
        response = rcon(name, properties()["commandName"] + " status")
        if properties()["pluginName"] not in response:
            raise RuntimeError("Server started, but the plugin status command failed.")
    except Exception:
        print("Startup failed. Inspect ./template logs, then ./template down.", file=sys.stderr)
        raise
    print(f"{response}\nPaper {config()['servers'][profile]['version']} ({config()['servers'][profile]['channel']}) at localhost:{args.port}\n"
          "Use ./template rcon <command>, ./template logs, and ./template down.")


def down():
    state = dev_state()
    owned_container(state["container"])
    run(["docker", "stop", "--time", "60", state["container"]], capture=True, timeout=90)
    run(["docker", "rm", state["container"]], capture=True)
    (STATE / "dev.json").unlink()
    print("Server stopped. World and configuration remain in .template/dev/data.")


def parser():
    root = argparse.ArgumentParser(description="Build, personalize, and validate a Paper plugin with Docker.")
    commands = root.add_subparsers(dest="action", required=True)
    commands.add_parser("doctor", help="Check Docker and report prerequisites.")
    commands.add_parser("build", help="Build the jar and run all Java tests in Java 25 Docker.")
    gradle = commands.add_parser("gradle", help="Run Gradle tasks in the pinned Java 25 Docker image.")
    gradle.add_argument("tasks", nargs=argparse.REMAINDER, help="Tasks followed by Gradle options, e.g. wrapper --gradle-version 9.8.0.")
    commands.add_parser("test", help="Run the Java and tooling tests.")
    init = commands.add_parser("init", help="Personalize plugin metadata and Java packages in this checkout.")
    init.add_argument("--name", required=True)
    init.add_argument("--package", required=True)
    init.add_argument("--command", required=True)
    init.add_argument("--author", required=True)
    for action in ("validate", "up"):
        command = commands.add_parser(action, help="Validate real servers." if action == "validate" else "Build and start a local playable Paper server.")
        command.add_argument("--accept-eula", action="store_true", required=True, help="Accept https://aka.ms/MinecraftEULA for these local servers.")
        command.add_argument("--profile", choices=list(config()["servers"]), action="append" if action == "validate" else "store")
        command.add_argument("--timeout", type=int, default=300, help="Seconds allowed per server startup.")
        if action == "validate":
            command.add_argument("--skip-build", action="store_true", help="Use an existing jar; report records that the build was skipped.")
        else:
            command.add_argument("--port", type=int, default=25565)
    commands.add_parser("down", help="Stop the local server and preserve its data.")
    commands.add_parser("logs", help="Print local server logs.")
    console = commands.add_parser("rcon", help="Execute a local server command without exposing RCON.")
    console.add_argument("command", nargs="+")
    commands.add_parser("versions", help="Compare pins with current upstream releases; leave files unchanged.")
    return root


def main():
    args = parser().parse_args()
    if args.action == "doctor":
        doctor()
    elif args.action == "versions":
        versions()
    elif args.action in ("logs", "rcon"):
        name = dev_state()["container"]
        owned_container(name)
        if args.action == "logs":
            run(["docker", "logs", name])
        else:
            print(rcon(name, " ".join(args.command)))
    else:
        with project_lock():
            if args.action == "build":
                build()
            elif args.action == "gradle":
                build(args.tasks or ["tasks"])
            elif args.action == "test":
                build(["test"])
                run([sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-v"])
            elif args.action == "init":
                initialize(args)
            elif args.action == "validate":
                validate(args)
            elif args.action == "up":
                up(args)
            elif args.action == "down":
                down()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exception:
        print(f"ERROR: {exception}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)
