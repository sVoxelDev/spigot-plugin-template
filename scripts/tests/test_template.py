import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess
import zipfile

MODULE = Path(__file__).resolve().parents[1] / "template.py"
spec = importlib.util.spec_from_file_location("paper_template", MODULE)
template = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template)


class TemplateToolTest(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.root_patch = patch.object(template, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.directory.cleanup)
        (self.root / "gradle.properties").write_text(
            "group=net.silthus\npackageName=net.silthus.template\npluginName=TemplatePlugin\n"
            "commandName=template\nauthor=Silthus\nversion=6.0.0-SNAPSHOT\napiVersion=26.2\n")
        (self.root / "settings.gradle").write_text("rootProject.name = 'paper-plugin-template'\n")
        for source_set in ("main", "test"):
            source = self.root / f"src/{source_set}/java/net/silthus/template/TemplatePlugin.java"
            source.parent.mkdir(parents=True)
            source.write_text("package net.silthus.template;\nclass TemplatePlugin {}\n")
        self.args = argparse.Namespace(name="WelcomePlugin", package="io.github.alex.welcome",
                                       command="welcome", author="Alex")

    def test_personalized_source_and_metadata_have_matching_identity(self):
        template.initialize(self.args)
        props = template.properties()
        self.assertEqual("WelcomePlugin", props["pluginName"])
        self.assertEqual("io.github.alex", props["group"])
        self.assertEqual("welcome", props["commandName"])
        for source_set in ("main", "test"):
            source = self.root / f"src/{source_set}/java/io/github/alex/welcome/TemplatePlugin.java"
            self.assertIn("package io.github.alex.welcome;", source.read_text())
            self.assertFalse((self.root / f"src/{source_set}/java/net/silthus/template").exists())
        before = (self.root / "gradle.properties").read_text()
        template.initialize(self.args)
        self.assertEqual(before, (self.root / "gradle.properties").read_text())

    def test_package_can_be_nested_under_the_old_package(self):
        self.args.package = "net.silthus.template.welcome"
        template.initialize(self.args)
        self.assertTrue((self.root / "src/main/java/net/silthus/template/welcome/TemplatePlugin.java").is_file())

    def test_corrected_author_is_applied_without_resetting_an_existing_version(self):
        template.initialize(self.args)
        props = self.root / "gradle.properties"
        props.write_text(props.read_text().replace("version=1.0.0-SNAPSHOT", "version=2.0.0"))
        self.args.author = "Alex Builder"
        template.initialize(self.args)
        self.assertEqual("Alex Builder", template.properties()["author"])
        self.assertEqual("2.0.0", template.properties()["version"])

    def test_invalid_identity_leaves_files_unchanged(self):
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        for field, value in (("name", "../Bad"), ("package", "io.github.class.welcome"),
                             ("command", "bad\ncommand"), ("author", "Author'${injection}")):
            with self.subTest(field=field):
                original = getattr(self.args, field)
                setattr(self.args, field, value)
                with self.assertRaises(RuntimeError):
                    template.initialize(self.args)
                setattr(self.args, field, original)
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_upstream_discovery_distinguishes_beta_and_stable(self):
        responses = {
            "https://fill.papermc.io/v3/projects/paper": {"versions": {"26.3": ["26.3", "26.3-rc1"], "26.2": ["26.2"]}},
            "https://fill.papermc.io/v3/projects/paper/versions/26.3/builds": [{"id": 140, "channel": "BETA"}, {"id": 141, "channel": "ALPHA"}],
            "https://fill.papermc.io/v3/projects/paper/versions/26.2/builds": [{"id": 129, "channel": "STABLE"}],
        }
        with patch.object(template, "request_json", side_effect=lambda url: responses[url]):
            candidates = template.latest_candidates()
        self.assertEqual(("26.3", 140, "BETA"), tuple(candidates["latest"][key] for key in ("version", "id", "channel")))
        self.assertEqual(("26.2", 129, "STABLE"), tuple(candidates["stable"][key] for key in ("version", "id", "channel")))

    def test_validation_rejects_exception_logs(self):
        log = "[Server/INFO]: Done!\n[Server/ERROR]: Could not load plugin\njava.lang.NoClassDefFoundError: example\nCaused by: java.lang.ClassNotFoundException: example"
        self.assertEqual(2, len(template.log_errors(log)))
        self.assertEqual([], template.log_errors("[Server/INFO]: Enabled plugin"))

    def test_expected_invalid_config_cannot_hide_other_errors(self):
        log = "[Server/ERROR]: Invalid configuration: greeting.message must be a nonempty string\n[Server/ERROR]: Other plugin failed"
        self.assertEqual(["[Server/ERROR]: Other plugin failed"], template.log_errors(log, expected_invalid=True))

    def test_paper_checksum_failure_leaves_no_executable_jar(self):
        import io
        with patch.object(template, "STATE", self.root / ".template"), \
             patch.object(template, "config", return_value={"servers": {"stable": {"version": "26.2", "build": 129,
                          "channel": "STABLE", "sha256": "0" * 64, "url": "https://example.test/paper.jar"}}}), \
             patch.object(template.urllib.request, "urlopen", return_value=io.BytesIO(b"wrong jar")):
            with self.assertRaisesRegex(RuntimeError, "checksum"):
                template.paper_jar("stable")
        self.assertEqual([], list((self.root / ".template/downloads").iterdir()))

    def test_renamed_entrypoint_matches_source_descriptor_and_packaged_class(self):
        source = self.root / "src/main/resources/plugin.yml"
        source.parent.mkdir(parents=True)
        source.write_text("main: '${packageName}.GreetingPlugin'\n")
        jar = self.root / "build/libs/TemplatePlugin-6.0.0-SNAPSHOT.jar"
        jar.parent.mkdir(parents=True)
        descriptor = "name: TemplatePlugin\nversion: 6.0.0-SNAPSHOT\nmain: net.silthus.template.GreetingPlugin\napi-version: '26.2'\n"
        for packaged_main, class_present, expected_error in (
                ("GreetingPlugin", True, None),
                ("TemplatePlugin", True, "wrong main"),
                ("GreetingPlugin", False, "entrypoint class is missing")):
            with self.subTest(main=packaged_main, class_present=class_present):
                with zipfile.ZipFile(jar, "w") as archive:
                    archive.writestr("plugin.yml", descriptor.replace(".GreetingPlugin", "." + packaged_main))
                    archive.writestr("config.yml", "greeting:\n  enabled: true\n")
                    if class_present:
                        archive.writestr("net/silthus/template/GreetingPlugin.class", b"class")
                if expected_error:
                    with self.assertRaisesRegex(RuntimeError, expected_error):
                        template.artifact()
                else:
                    self.assertEqual((jar, True), template.artifact())

    def test_start_does_not_remove_a_preexisting_container(self):
        with patch.object(template, "run", return_value=subprocess.CompletedProcess([], 0, "[]", "")) as commands:
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                template.server_start("existing", self.root / "data", self.root / "plugin.jar", "stable")
        self.assertFalse(any(call.args[0][:2] == ["docker", "rm"] for call in commands.call_args_list))

    def test_invalid_startup_cannot_pass_when_disable_only_happens_at_shutdown(self):
        state = {}
        pin = {"version": "26.2", "build": 129, "channel": "STABLE"}
        details = {"State": {"ExitCode": 0}, "Image": "example"}

        def start(name, data, jar, profile, **kwargs):
            path = data / "plugins/TemplatePlugin/config.yml"
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("greeting:\n  enabled: true\n  message: Welcome\n")
            state.update(config=path, greeting="enabled: true" in path.read_text(),
                         invalid="message: ''" in path.read_text(), stopped=False)

        def console(name, command):
            if command == "plugins":
                return "Plugins (1): TemplatePlugin"
            if command.startswith("version "):
                return "6.0.0-SNAPSHOT"
            if command.endswith(" status"):
                return "TemplatePlugin v6.0.0-SNAPSHOT. Greeting: " + ("enabled." if state["greeting"] else "disabled.")
            if command.endswith(" info"):
                return "Only players can use this command."
            if command.endswith(" reload"):
                text = state["config"].read_text()
                if "[broken" in text:
                    return "Configuration was not reloaded: malformed YAML"
                if "enabled: 'false'" in text:
                    return "Configuration was not reloaded: greeting.enabled must be true or false"
                state["greeting"] = "enabled: true" in text
                return "Configuration reloaded."
            return "Usage: /template"

        def docker(command, **kwargs):
            output = ""
            if command[:2] == ["docker", "logs"]:
                output = "Loading Paper 26.2-129-main\nEnabling TemplatePlugin v6.0.0-SNAPSHOT\n"
                if state["invalid"]:
                    output += "[Server/ERROR]: Invalid configuration: greeting.message must be a nonempty string\n"
                if state["stopped"]:
                    output += "Disabling TemplatePlugin v6.0.0-SNAPSHOT\n"
            elif command[:2] == ["docker", "stop"]:
                state["stopped"] = True
            return subprocess.CompletedProcess(command, 0, output, "openjdk 25" if command[:2] == ["docker", "exec"] else "")

        directory = self.root / "reports"
        with patch.object(template, "config", return_value={"servers": {"stable": pin}}), \
             patch.object(template, "server_start", side_effect=start), patch.object(template, "wait_server"), \
             patch.object(template, "owned_container", return_value=details), \
             patch.object(template, "container_details", return_value=details), \
             patch.object(template, "rcon", side_effect=console), patch.object(template, "run", side_effect=docker):
            with self.assertRaisesRegex(RuntimeError, "before shutdown"):
                template.validate_server("stable", directory, self.root / "plugin.jar", True, 1)
        report = json.loads((directory / "stable/results.json").read_text())
        self.assertEqual("failed", report["status"])
        self.assertFalse(any(check.get("check") == "invalid configuration disables the plugin" for check in report["checks"]))

    def test_failures_before_server_start_still_produce_a_report(self):
        args = argparse.Namespace(skip_build=True, profile=["stable"], timeout=10)
        with patch.object(template, "config", return_value={"server_image": "example", "servers": {"stable": {}}}), \
             patch.object(template, "docker_ready"), patch.object(template, "run"), \
             patch.object(template, "artifact", side_effect=RuntimeError("Packaged descriptor has the wrong main.")):
            with self.assertRaises(RuntimeError):
                template.validate(args)
        index = json.loads((self.root / "build/validation/latest.json").read_text())
        result = json.loads((self.root / index["report"] / "results.json").read_text())
        self.assertEqual("failed", index["status"])
        self.assertEqual("failed", result["status"])
        self.assertIn("wrong main", result["error"])

    def test_unavailable_docker_is_recorded_as_a_failed_validation(self):
        args = argparse.Namespace(skip_build=True, profile=["stable"], timeout=10)
        with patch.object(template, "config", return_value={"server_image": "example", "servers": {"stable": {}}}), \
             patch.object(template, "docker_ready", side_effect=RuntimeError("Docker daemon is unavailable")):
            with self.assertRaises(RuntimeError):
                template.validate(args)
        index = json.loads((self.root / "build/validation/latest.json").read_text())
        result = json.loads((self.root / index["report"] / "results.json").read_text())
        self.assertEqual("failed", result["status"])
        self.assertEqual("Docker daemon is unavailable", result["error"])


if __name__ == "__main__":
    unittest.main()
