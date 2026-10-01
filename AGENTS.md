# Working on the Paper plugin template

Use `./template --help` for the supported build and server commands. The local workflow requires Python 3.11+ and Docker with Linux containers; Java runs inside Docker. Keep changes in an isolated checkout when another agent is working on the template.

For a new plugin, server installation, or a dependency update, read [.agents/skills/paper-plugin/SKILL.md](.agents/skills/paper-plugin/SKILL.md). It describes the setup workflow and routes to deployment instructions. [docs/start-prompts.md](docs/start-prompts.md) contains copyable user prompts.

Keep the plugin small. Use Paper APIs and Adventure components supplied by the server. Introduce an integration or bundled dependency when the requested plugin needs it. Configure server dependencies as `compileOnly`; use a maintained shading plugin and relocation for libraries that must ship in the plugin jar. The main `JavaPlugin` class stays extendable because MockBukkit subclasses it.

Use explicit types, small methods, and names that explain the code. Write focused tests through the server dispatcher and observable player messages. Keep Bukkit operations on the server thread. Treat configuration reloads as atomic: validate new settings before replacing the running settings.

After code changes, run `./template validate --accept-eula` when authorized to accept the Minecraft EULA. It runs the build, mock tests, tooling tests, and both pinned Paper server profiles. Read the generated `results.json` and server logs before claiming success. A health check alone does not prove that a plugin loads or works. Player interaction tests use MockBukkit; real-server checks exercise console commands and the plugin lifecycle. For new player gameplay, add a relevant real-client or server-side integration check and report its limits.

For upstream updates, run `./template versions` and read [docs/modernization-research.md](docs/modernization-research.md). Verify current official releases, preserve the distinction between beta and stable, and update coupled server URL/checksum/build fields together. The API baseline and `api-version` must support every advertised server profile. Run the full validation matrix before publishing a version update.

PRs need a concrete change description, the exact server versions tested, a jar checksum, and the path or CI link to validation artifacts. Keep generated worlds and caches out of Git. Obtain the user's final approval before merging or deploying to their existing server.
