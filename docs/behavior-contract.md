# Template behavior contract

This contract defines observable checks for an independent agent. Use the public CLI and generated artifacts. Read the setup skill and user documentation; keep implementation files out of the validation process.

## Setup

Use an isolated copy of the template with Python 3.11+ and Docker. The validator is authorized to accept the Minecraft EULA for temporary local servers and to change files in its own copy. It must leave the main checkout and existing servers alone.

## Required workflows

1. `./template --help` identifies build, personalization, validation, and server lifecycle commands. `./template doctor` reports a working Docker daemon.
2. `./template init --name WelcomePlugin --package io.github.alex.welcome --command welcome --author Alex` creates a buildable identity. Repeating it preserves the result. Invalid names/packages leave the project intact and produce a nonzero exit.
3. `./template validate --accept-eula` builds the customized jar, runs focused tests, boots every advertised Paper profile, and emits a report and real logs. Each profile tests commands, valid and invalid reloads, persistence across restart, invalid startup, and clean shutdown. Reported server channels match the pins.
4. `./template up --accept-eula --profile stable --port 25568` starts a local server and reports the actual plugin identity. `./template rcon welcome status` returns a real configuration state. Change the generated config, reload, and confirm that the state changes. Stop and start the server; the state survives. `./template down` preserves data.
5. Validation failures return nonzero and record a failed report with useful logs. A server being healthy is insufficient to pass a missing or disabled plugin. Reject an incorrect Paper checksum before booting it.
6. The installable jar contains the personalized plugin descriptor and defaults, and excludes Paper/Bukkit and test classes. The report's jar checksum matches the jar it executed.
7. Player greetings, permission behavior, literal message text, and playtime conversion have focused mock tests. These are not claimed as real client connections. Real player login and gameplay are outside this template's current Docker contract.

## Evidence

Return one report with pass/fail/blocked for every clause, commands exercised, paths to generated reports, and any remaining limitations. Probe a different plugin identity, invalid input, a changed configuration, and a persisted restart. Capture failures as well as successful output. Stop every container created by the validation run.
