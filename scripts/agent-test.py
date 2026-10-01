#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(directory, *args, capture=False):
    return subprocess.run([str(directory / "template"), *args], cwd=directory,
                          check=True, text=True, capture_output=capture)


def copy_evidence(project, destination):
    index = project / "build/validation/latest.json"
    if not index.exists():
        return
    report = project / json.loads(index.read_text())["report"]
    summary = json.loads((report / "results.json").read_text())
    for source in report.glob("*/results.json"):
        target = destination / source.parent.name
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target / source.name)
        for log in source.parent.glob("*.log"):
            shutil.copy2(log, target / log.name)
    shutil.copy2(report / "results.json", destination / "results.json")
    if "jar" in summary:
        shutil.copy2(report / summary["jar"], destination / summary["jar"])


def exercise_local_server(project):
    port = "25569"
    evidence = {}
    try:
        evidence["first_start"] = run(project, "up", "--accept-eula", "--profile", "stable", "--port", port, capture=True).stdout
        state = json.loads((project / ".template/dev.json").read_text())
        container = state["container"]
        bindings = json.loads(subprocess.run(["docker", "inspect", "--format", "{{json .NetworkSettings.Ports}}", container],
                                            text=True, capture_output=True, check=True).stdout)
        if bindings["25565/tcp"] != [{"HostIp": "127.0.0.1", "HostPort": port}] or bindings.get("25575/tcp"):
            raise RuntimeError("Development server must bind to localhost and keep RCON private.")
        evidence["port_bindings"] = bindings
        config = project / ".template/dev/data/plugins/WelcomePlugin/config.yml"
        config.write_text("greeting:\n  enabled: false\n  message: 'Quiet, {player}.'\n")
        response = run(project, "rcon", "welcome", "reload", capture=True).stdout
        if "Configuration reloaded." not in response:
            raise RuntimeError("Development server did not reload changed settings.")
        evidence["changed_status"] = run(project, "rcon", "welcome", "status", capture=True).stdout
        if "Greeting: disabled." not in evidence["changed_status"]:
            raise RuntimeError("Development server status did not reflect the changed configuration.")
        config_hash = hashlib.file_digest(config.open("rb"), "sha256").hexdigest()
        reports = {path: hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
                   for path in (project / "build/validation").rglob("*") if path.suffix in (".json", ".log")}
        run(project, "down")
        if (project / ".template/dev.json").exists() or not (project / ".template/dev/data/world/level.dat").is_file():
            raise RuntimeError("Down must remove dev state while preserving world data.")
        evidence["restart"] = run(project, "up", "--accept-eula", "--profile", "stable", "--port", port, capture=True).stdout
        evidence["persisted_status"] = run(project, "rcon", "welcome", "status", capture=True).stdout
        if "Greeting: disabled." not in evidence["persisted_status"] or hashlib.file_digest(config.open("rb"), "sha256").hexdigest() != config_hash:
            raise RuntimeError("Development restart did not preserve the configuration.")
        for path, expected in reports.items():
            if not path.exists() or hashlib.file_digest(path.open("rb"), "sha256").hexdigest() != expected:
                raise RuntimeError("Starting a development server removed or changed validation evidence.")
        evidence["preserved_reports"] = len(reports)
    finally:
        if (project / ".template/dev.json").exists():
            run(project, "down")
    remaining = subprocess.run(["docker", "ps", "-aq", "--filter", f"label=paper-template.checkout={project}"], text=True, capture_output=True, check=True).stdout.strip()
    if remaining:
        raise RuntimeError("Workflow left a template container behind.")
    return evidence


def main():
    parser = argparse.ArgumentParser(description="Exercise the documented new-plugin and local-server workflow in an isolated copy.")
    parser.add_argument("--accept-eula", action="store_true", required=True)
    parser.parse_args()
    destination = ROOT / "build/agent-validation"
    destination.mkdir(parents=True, exist_ok=True)
    workflow = {"status": "running"}
    with tempfile.TemporaryDirectory(prefix="paper-plugin-agent-") as temporary:
        project = Path(temporary) / "welcome"
        shutil.copytree(ROOT, project, ignore=shutil.ignore_patterns(".git", ".gradle", ".gradle-user-home", ".template", "build", "__pycache__"))
        try:
            help_text = run(project, "--help", capture=True).stdout
            if any(command not in help_text for command in ("doctor", "init", "validate", "up", "rcon", "down")):
                raise RuntimeError("Public help is missing a workflow command.")
            workflow["doctor"] = json.loads(run(project, "doctor", capture=True).stdout)
            for _ in range(2):
                run(project, "init", "--name", "WelcomePlugin", "--package", "io.github.alex.welcome", "--command", "welcome", "--author", "Alex")
            invalid = subprocess.run([str(project / "template"), "init", "--name", "../Bad", "--package", "io.github.alex.welcome", "--command", "welcome", "--author", "Alex"], cwd=project)
            if invalid.returncode == 0:
                raise RuntimeError("Invalid plugin identity was accepted.")
            run(project, "validate", "--accept-eula")
            workflow["local_server"] = exercise_local_server(project)
            workflow["status"] = "passed"
            print(f"PASS: personalized WelcomePlugin and local server workflow. Evidence: {destination}")
        except Exception as exception:
            workflow["status"] = "failed"
            workflow["error"] = str(exception)
            raise
        finally:
            copy_evidence(project, destination)
            (destination / "workflow.json").write_text(json.dumps(workflow, indent=2) + "\n")


if __name__ == "__main__":
    main()
