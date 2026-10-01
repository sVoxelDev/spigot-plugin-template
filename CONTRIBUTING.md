# Contributing

Use an isolated branch from `main`. Keep changes focused, use conventional commit messages, and describe the observable behavior in your PR. Follow [AGENTS.md](AGENTS.md) when using an agent.

## Build and validate

Python 3.11+ and Docker with Linux containers are required for the complete local workflow.

```bash
./template doctor
./template validate --accept-eula
python3 scripts/agent-test.py --accept-eula
```

The EULA flag accepts the Minecraft EULA for local test servers. `validate` builds and checks both Paper profiles; the agent test also proves personalization in a fresh copy. Inspect the JSON reports and logs. Include exact server builds/channels and the jar SHA-256 in your PR, or link the CI artifacts.

Use MockBukkit for focused player and command behavior tests. Use real server checks for classloading, packaging, configuration, and lifecycle behavior. Add appropriate integration checks for new gameplay. Write self-explanatory code with small methods and explicit types. Runtime APIs belong in `compileOnly`, and the server supplies Adventure.

## Updating versions

Run `./template versions` and verify the current official sources in [docs/modernization-research.md](docs/modernization-research.md). Update Gradle's wrapper and checksum together. Update Paper profile URLs, checksums, builds, and channels together. Keep the API and MockBukkit versions compatible and run both server profiles before claiming support.

## Releasing

Set `version` in `gradle.properties` to a release version such as `6.0.0`, submit a validated PR, and merge it after approval. A maintainer can then tag that commit as `v6.0.0` and push the tag. The release job checks the tag against the project version, waits for the build and server/agent validation jobs, and uploads the jars to a GitHub Release.

The release workflow uses GitHub's repository token and does not need a Node package manager. Gradle's Maven publication can also be published locally or to GitHub Packages using a host Java 25 installation:

```bash
./gradlew publishToMavenLocal
GITHUB_REPOSITORY=owner/repository GITHUB_ACTOR=your-user GITHUB_TOKEN=your-token ./gradlew publish
```

Supply real credentials through your environment or a secret manager. Keep tokens out of source and logs. The repository uses the GNU GPL license in [LICENSE](LICENSE).
