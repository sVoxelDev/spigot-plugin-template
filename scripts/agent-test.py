#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(directory, *args):
    subprocess.run([str(directory / "template"), *args], cwd=directory, check=True)


def main():
    parser = argparse.ArgumentParser(description="Exercise the documented new-plugin workflow in an isolated copy.")
    parser.add_argument("--accept-eula", action="store_true", required=True)
    args = parser.parse_args()
    destination = ROOT / "build/agent-validation"
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="paper-plugin-agent-") as temporary:
        project = Path(temporary) / "welcome"
        shutil.copytree(ROOT, project, ignore=shutil.ignore_patterns(".git", ".gradle", ".gradle-user-home", ".template", "build", "__pycache__"))
        run(project, "init", "--name", "WelcomePlugin", "--package", "io.github.alex.welcome", "--command", "welcome", "--author", "Alex")
        run(project, "init", "--name", "WelcomePlugin", "--package", "io.github.alex.welcome", "--command", "welcome", "--author", "Alex")
        result = subprocess.run([str(project / "template"), "init", "--name", "../Bad", "--package", "io.github.alex.welcome", "--command", "welcome", "--author", "Alex"], cwd=project)
        if result.returncode == 0:
            raise RuntimeError("Invalid plugin identity was accepted.")
        run(project, "validate", "--accept-eula")
        index = json.loads((project / "build/validation/latest.json").read_text())
        report = project / index["report"]
        summary = json.loads((report / "results.json").read_text())
        if summary["status"] != "passed":
            raise RuntimeError("Personalized plugin did not validate.")
        for profile in summary["servers"]:
            source = report / profile["profile"]
            target = destination / profile["profile"]
            target.mkdir(exist_ok=True)
            for path in source.glob("*.log"):
                shutil.copy2(path, target / path.name)
            shutil.copy2(source / "results.json", target / "results.json")
        shutil.copy2(report / "results.json", destination / "results.json")
        shutil.copy2(report / summary["jar"], destination / summary["jar"])
        print(f"PASS: the one-prompt setup workflow created and validated WelcomePlugin. Evidence: {destination}")


if __name__ == "__main__":
    main()
