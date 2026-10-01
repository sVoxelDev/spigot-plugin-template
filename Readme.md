# Paper plugin template

Create a Java 25 Paper plugin, test its behavior, and prove that its jar loads on real servers. The starter includes a configurable join greeting, player playtime, administrator commands, and repeatable Docker validation.

## Start with your coding agent

Open this repository in your agent and paste the [new-plugin prompt](docs/start-prompts.md). The agent uses [AGENTS.md](AGENTS.md) and the [paper-plugin skill](.agents/skills/paper-plugin/SKILL.md) to personalize, implement, test, and validate your plugin.

For the existing example, one command builds it and checks both supported servers:

```bash
./template validate --accept-eula
```

The flag accepts the [Minecraft EULA](https://aka.ms/MinecraftEULA) for local servers. Install Python 3.11+ and start Docker first. Java and Gradle run in Docker, so you do not need a host JDK. Use Linux, macOS, or Windows through WSL2 with Linux containers. Allow about 4 GB of RAM and 3 GB of disk for the first run.

## Current baseline

Verified on October 1, 2026. [Research and official sources](docs/modernization-research.md) explain the choices.

| Component | Version |
| --- | --- |
| Java | 25 |
| Gradle wrapper | 9.8.0 with SHA-256 verification |
| Paper API and minimum server API | 26.2 build 129 stable |
| Default server, latest Minecraft | Paper 26.3 build 140 beta |
| Stable server | Paper 26.2 build 129 stable |
| JUnit / MockBukkit / JaCoCo | 6.1.3 / 26.2 version 4.116.1 / 0.8.15 |

Paper has not published a stable 26.3 build yet. The `latest` profile exercises it explicitly; use `--profile stable` for a stable server. The stable API baseline keeps the example compatible with both servers. This template targets Paper, without a Spigot or Folia compatibility claim.

## Personalize it

Click GitHub's **Use this template** or clone the repository, then run:

```bash
./template init --name WelcomePlugin --package io.github.alex.welcome --command welcome --author Alex
./template validate --accept-eula
```

`init` changes package paths, plugin identity, commands, permissions, and jar naming together. Add your plugin behavior in `src/main/java` and focused behavior tests in `src/test/java`. The entry class is named `TemplatePlugin`; its package and descriptor identify your plugin. Change the class name and descriptor together if you prefer another entry class.

Use `./template --help` for commands and `./template doctor` to check Docker. `./template build` creates the installable jar in `build/libs/`; `./template test` runs Java and tooling tests. A host Java 25 installation can also run `./gradlew build` directly.

## Run and play locally

```bash
./template up --accept-eula
./template rcon template status
./template down
```

Join `localhost:25565` with a matching Minecraft client and an authenticated account. Use your personalized command in place of `template`. `up` builds and tests before starting; `down` preserves the world and plugin config. The server binds to localhost, and RCON stays inside Docker. Use `--port 25566` for another port and `--profile stable` for Paper 26.2.

The default plugin sends `Welcome, {player}!` on join. `/template info` displays the player's name and whole minutes played. `/template status` and `/template reload` require their `template.admin.*` permissions, which default to operators. Edit `plugins/TemplatePlugin/config.yml` inside the local server data directory to change or disable greetings. Invalid reloads retain the last valid settings; invalid startup disables the plugin with an explanation.

## What validation proves

`validate` runs the Java build, MockBukkit player tests, and Python tooling tests. It inspects the jar and boots isolated Docker servers for both pinned Paper profiles. On each server it verifies actual plugin identity, commands, valid and invalid reloads, configuration persistence across restart, rejection of invalid startup settings, and clean shutdown. It checks captured logs and verifies the downloaded Paper jar's checksum before execution.

Reports, command responses, jar checksums, and logs live in `build/validation/<run>/`; `build/validation/latest.json` points to the most recent run. Every run gets a fresh world. Validation returns nonzero on failures and removes its containers. `--skip-build` is for CI jobs using an already tested jar and is recorded in the report.

Player greetings, permissions, and playtime use MockBukkit. Docker checks use real Paper and RCON; they do not log in a real player. Add an appropriate client or server integration test for gameplay beyond this example. [The behavior contract](docs/behavior-contract.md) defines independent agent checks.

`python3 scripts/agent-test.py --accept-eula` exercises the documented setup flow in an isolated copy. It personalizes a `WelcomePlugin`, checks invalid input, runs the full server matrix, and tests local server commands, port isolation, persisted settings, report retention, and cleanup. Evidence stays in `build/agent-validation/`. CI runs both the original and personalized template workflows.

## Install and maintain

Follow [deployment instructions](docs/deployment.md) to copy the validated jar to an existing Paper server or provision a Docker host. Use a full server restart to load a new jar. `reload` only changes this plugin's settings.

Run `./template versions` to compare pins with current official releases without changing them. It reports Mojang's newest release and Paper's newest build separately from the newest accepted beta/stable lanes, so an alpha-only release remains visible. Dependency PRs run the same validation as feature PRs. Update coupled Paper URL, checksum, version, and build fields in `template.json` together. Keep the minimum API compatible with every advertised server profile.

GitHub Actions builds and tests pushes and PRs, validates both Paper profiles, and uploads reports and jars. Publishing a `v*` tag runs the same gates and creates a GitHub Release with the installable jar and source/documentation jars. Set `version` in `gradle.properties` to match the release tag before pushing it. Maven publishing remains available through `./gradlew publishToMavenLocal` or `publish` with GitHub Packages credentials.

## Migrating from the Spigot template

This is a new major template baseline. It replaces Java 17, Minecraft 1.19.3, Spigradle, ACF, Lombok, and the sample Vault integration. Commands now use the native server dispatcher and Adventure; the old `/stemplate` command becomes `/template`. Add economy or command frameworks when your plugin needs them. The normal jar contains only plugin code and resources; server APIs and test libraries stay out of it.

The project name is `paper-plugin-template`. The existing GitHub repository URL remains usable. The historical changelog stays in [CHANGELOG.md](CHANGELOG.md); current contribution and release guidance is in [CONTRIBUTING.md](CONTRIBUTING.md).
