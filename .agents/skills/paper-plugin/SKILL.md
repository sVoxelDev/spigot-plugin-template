---
name: paper-plugin
description: Create, personalize, validate, or update a Paper plugin from this template, or prepare its installation on a user's Paper server.
---

# Build a Paper plugin

Work from the repository root. Read `AGENTS.md` and `./template --help`. When the user specifies a plugin, use its requested behavior as the contract. Resolve routine implementation choices locally; ask only for missing requirements that affect observable behavior or a real server destination.

For a fresh template, personalize it with `./template init --name WelcomePlugin --package io.github.alex.welcome --command welcome --author Alex`, using the user's identity. It updates Java packages, descriptor metadata, command permissions, and artifact identity together. Preserve any existing implementation when adapting an already personalized project.

Implement the smallest working plugin and test its behavior through MockBukkit's dispatcher, events, and player messages. Inspect `src/main` and `src/test` to find the existing example. Adapt the tests and validation contract when replacing the greeting example with another plugin. Treat the example as starter code to change, not a requirement that every plugin has greetings.

Run `./template doctor`, then `./template validate --accept-eula` if the user authorized accepting the Minecraft EULA. The flag records that acceptance for the local servers; ask once if that authorization is absent. Read the reported `build/validation/<run>/results.json`, each profile's `results.json`, and captured logs. A pass requires the packaged plugin to load, command behavior to match, configuration changes to survive restart, and clean shutdowns on every advertised profile. Report player mock tests separately from real server behavior.

For a playable local server, run `./template up --accept-eula`; use `./template rcon <command>` to inspect it and `./template down` to stop it. The local server uses online authentication and binds to localhost. Its world and configuration survive `down`. Rebuild and restart to load a changed jar.

When installing on an existing host or provisioning a remote server, read [../../../docs/deployment.md](../../../docs/deployment.md). Prepare a validated jar and a concrete installation command for the destination. Confirm actual deployment authorization, retain a backup of the replaced jar and config, and inspect real server logs and commands after restart. Never copy development worlds or validation state to a production server.

For dependency or Minecraft updates, run `./template versions` and consult [../../../docs/modernization-research.md](../../../docs/modernization-research.md). Check official current releases and compatibility, update the pins, and run the full matrix. The `latest` lane may be beta; `stable` must select a stable build. Change the minimum API only when all advertised servers support it. Package API classes as `compileOnly`, not inside the jar.

Deliver the jar path, SHA-256, exact server builds/channels, validation report path, and any untested behavior. If a PR is requested, create it with the evidence and await the user's merge approval.
