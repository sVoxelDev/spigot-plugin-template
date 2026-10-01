# Start with one prompt

Open a clone of this template in your coding agent. It reads `AGENTS.md`; the repository skill lives in `.agents/skills/paper-plugin/SKILL.md`. Python 3.11+ and a running Docker daemon are required. Linux, macOS, and Windows through WSL2 are supported. Reserve about 4 GB of available RAM and 3 GB of disk for the first run.

## Build your plugin

```text
Use the paper-plugin skill in .agents/skills/paper-plugin/SKILL.md to turn this template into WelcomePlugin, package io.github.alex.welcome, command /welcome, author Alex. Greet joining players with "Hello, {player}!". Let administrators turn the greeting off and reload the configuration, and let players view their playtime. I accept the Minecraft EULA for the local test servers. Work autonomously: personalize the template, implement the behavior, update the focused tests, build it, and validate it on every pinned Paper profile using Docker. Fix failures until it passes. Return the installable jar, checksum, exact versions, and validation evidence. Keep deployment separate until I provide a destination and authorize it.
```

Replace the identity and plugin behavior with your own. The prompt is an example request, so the generated implementation can differ from the default greeting plugin.

## Update an existing plugin

```text
Use the paper-plugin skill to update this plugin to current Paper standards. Research official releases, compare them with ./template versions, update compatible pins and the agent instructions, and preserve the plugin's behavior. I accept the Minecraft EULA for local tests. Run the focused tests and the full Docker validation matrix, fix all failures, and create a PR with the jar checksum and captured evidence. Distinguish beta Paper from stable Paper. Await my approval before merging or deploying.
```

## Install on your server

```text
Use the paper-plugin skill and docs/deployment.md to build and validate this plugin. My server is [host or local path], runs Paper [version/build] with Java [version], and its plugin directory is [path]. I accept the Minecraft EULA for local validation. Prepare the jar and an installation plan with the existing jar/config backup, restart command, and post-install checks. Deploy only after I approve that concrete plan.
```

If you already authorize deployment, say so and provide the actual host, path, access method, and restart command. An agent cannot infer your remote server's credentials or invent a destination.
