import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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
            "commandName=template\nauthor=Silthus\nversion=6.0.0-SNAPSHOT\n")
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
