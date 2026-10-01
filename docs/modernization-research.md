# Modernization research

Verified on 2026-10-01 against official documentation, live release APIs, and published Maven metadata. Versions below describe this observation, not an evergreen promise. Recheck the linked endpoints before the next update.

## Current release baseline

| Component | Verified available version | Recommendation and source |
| --- | --- | --- |
| Minecraft Java Edition | 26.3, released 2026-09-15 | Mojang's manifest reports `latest.release=26.3` and `latest.snapshot=26.4-snapshot-2`. Use the release for the latest-version validation lane. [Official version manifest](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json). |
| Paper for latest Minecraft | 26.3 build 140, BETA, published 2026-09-29 | There are no STABLE or RECOMMENDED builds among the 55 published 26.3 builds. Label this lane beta. [Official builds API](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds). |
| Paper stable | 26.2 build 129, STABLE, published 2026-09-23 | Use this for the stable-server validation lane. [Official builds API](https://fill.papermc.io/v3/projects/paper/versions/26.2/builds). |
| Java | 25 for current Paper | Use a Java 25 toolchain and Java 25 server image. Paper's project setup shows Java 25. [Paper project setup](https://docs.papermc.io/paper/dev/project-setup/). |
| Gradle | 9.8.0, final release, built 2026-09-24 | Upgrade the checked-in wrapper and pin its distribution checksum. [Official current-version API](https://services.gradle.org/versions/current). |
| JUnit | 6.1.3 | Use the BOM, Jupiter, and Platform launcher. JUnit 6 still uses the `org.junit.jupiter` package and requires Java 17 or later. [Official user guide](https://docs.junit.org/6.1.3/overview.html), [published Maven metadata](https://repo.maven.apache.org/maven2/org/junit/jupiter/junit-jupiter/maven-metadata.xml). |
| MockBukkit for 26.2 | `org.mockbukkit.mockbukkit:mockbukkit-v26.2:4.116.1` | This is the published 26.2 artifact. There is no published 26.3 artifact in the group's Maven directory. [Published metadata](https://repo.maven.apache.org/maven2/org/mockbukkit/mockbukkit/mockbukkit-v26.2/maven-metadata.xml), [artifact directory](https://repo.maven.apache.org/maven2/org/mockbukkit/mockbukkit/). |
| JaCoCo | 0.8.15 | Upgrade from 0.8.7. The 0.8.16 trunk documentation describes a development build, not a published release. [Official release downloads](https://www.jacoco.org/jacoco/index.html), [published metadata](https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.core/maven-metadata.xml). |
| itzg Minecraft server image | 2026.9.2, published 2026-09-25 | Use the released `2026.9.2-java25` image, preferably with its manifest digest. [Official release](https://github.com/itzg/docker-minecraft-server/releases/tag/2026.9.2), [Java image tags](https://docker-minecraft-server.readthedocs.io/en/latest/versions/java/). |

Minecraft's latest release and Paper's latest stable release differ. A successful beta-server run proves compatibility with the latest Minecraft release, but does not change Paper's channel designation. Paper explicitly recommends stable builds for production. [Paper downloads service](https://docs.papermc.io/misc/downloads-service/).

## Paper build and plugin conventions

Paper changed its API coordinates starting with Minecraft 26.1. The old `1.19.3-R0.1-SNAPSHOT` convention becomes `<minecraft-version>.build.<build>-<status>`. Pin `io.papermc.paper:paper-api:26.3.build.140-beta` for the current latest build or `26.2.build.129-stable` for the stable build. Both artifacts exist in Paper's official repository. [Paper versioning announcement](https://papermc.io/news/26-1/), [26.3 publication](https://artifactory.papermc.io/artifactory/api/storage/releases/io/papermc/paper/paper-api/26.3.build.140-beta), [26.2 publication](https://artifactory.papermc.io/artifactory/api/storage/releases/io/papermc/paper/paper-api/26.2.build.129-stable).

Paper recommends Gradle and demonstrates Kotlin DSL with `compileOnly` for the Paper API. The server supplies its own API at runtime. A Java 25 toolchain replaces the old manually selected `javac` and Java 17 flags. Gradle supports running on Java 25 starting with 9.1.0, so 9.8.0 meets this requirement. [Paper project setup](https://docs.papermc.io/paper/dev/project-setup/), [Gradle Java compatibility](https://docs.gradle.org/current/userguide/compatibility.html).

Keep a normal `plugin.yml` in resources. Paper's setup guide still marks its newer Paper manifest as experimental and does not recommend it for this starting point. The `api-version` declares the minimum supported server API. Servers below that version refuse to load the plugin. Set it to 26.2 only if the example avoids 26.3-only methods and both real-server lanes pass. [Paper project setup](https://docs.papermc.io/paper/dev/project-setup/), [plugin.yml reference](https://docs.papermc.io/paper/dev/plugin-yml/).

Native Paper commands remove the need for ACF in a small example. `BasicCommand` can register through `JavaPlugin.registerCommand` during `onEnable`; full Brigadier command trees are available when a plugin needs richer parsing. Paper also supplies Adventure components for player messages. These are recommendations to reduce this template's dependencies, not a claim that ACF is unusable. [Basic command guide](https://docs.papermc.io/paper/dev/command-api/misc/basic-command/), [Paper component API](https://docs.papermc.io/paper/dev/component-api/introduction/).

The current template already compiles against Paper, even though its name advertises Spigot. A Paper-first rename makes its supported platform explicit. Remove the default Vault integration, ACF, and Lombok from the minimal greeting and management-command example. Add optional integrations only when a plugin needs them. This recommendation comes from the repository's existing dependency and example code, plus the user's request for a simpler Paper template.

If future plugins need to bundle dependencies, Shadow's maintained plugin ID is `com.gradleup.shadow`; the latest official release is 9.6.1. With no bundled dependencies, the normal Gradle JAR task is sufficient. [Shadow source and migration notice](https://github.com/GradleUp/shadow), [release 9.6.1](https://github.com/GradleUp/shadow/releases/tag/9.6.1).

## Testing limits and recommended proof

MockBukkit's 26.2 branch declares Java 25 and Paper `26.2.build.111-stable`. Its published POM omits the Paper API, so the template must add an explicit Paper API dependency to the test runtime. Its JUnit dependency is 6.1.3. [Maintainer build properties](https://github.com/MockBukkit/MockBukkit/blob/minecraft/v26.2/gradle.properties), [published POM](https://repo.maven.apache.org/maven2/org/mockbukkit/mockbukkit/mockbukkit-v26.2/4.116.1/mockbukkit-v26.2-4.116.1.pom).

Keep the MockBukkit runtime on its matching Paper version if the latest API breaks mock initialization. Compile the distributed plugin against the chosen current API separately. This is a compatibility recommendation, and actual test results must decide whether separation is necessary. MockBukkit tests cannot establish that a JAR loads under the real Paper classloader.

The validation contract should cover user-visible behavior:

- The packaged JAR contains the descriptor and defaults, excludes server API classes, and loads with the expected plugin identity.
- Fresh installation creates the default configuration and enables the plugin.
- Greeting, information, and status commands return expected output through the server command dispatcher.
- A permitted configuration reload changes behavior, and an invalid configuration reports failure without discarding the last valid settings.
- Permission-denied player behavior and join greetings pass focused mock tests or a real client test.
- Restart preserves the configuration and the plugin enables again.
- Shutdown disables the plugin cleanly, and captured logs contain no plugin exception.
- A newly customized template builds and runs through the same validation entry point.

These are project-specific acceptance criteria proposed from the user's request. They are not assertions that upstream documentation mandates this test suite. Save the server version, build/channel, image digest, JAR checksum, command responses, and logs so an agent can inspect the actual evidence.

## Docker and automation

itzg supports `TYPE=PAPER`, a fixed `VERSION`, and `PAPER_BUILD`. It can also use `PAPER_DOWNLOAD_URL`, which allows the template to select the exact Fill API artifact and verify its checksum. A host `/plugins` mount installs the built plugin; changing plugin JARs requires a server restart. [Official Paper image guide](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/server-types/paper/).

The image includes `mc-health`, backed by `mc-monitor status`. A healthy container proves server responsiveness, so follow it with plugin-specific commands. `docker exec <container> rcon-cli <command>` provides command output without an interactive terminal. Keep RCON inside the container and publish only the Minecraft port when human play is needed. [Official healthcheck guide](https://docker-minecraft-server.readthedocs.io/en/latest/misc/healthcheck/), [official command guide](https://docker-minecraft-server.readthedocs.io/en/latest/sending-commands/commands/).

The image's documented Paper channel names still include `default` and `experimental`, while the current upstream API returns `ALPHA`, `BETA`, and `STABLE`. An explicit artifact URL avoids assuming those labels map correctly. Confirm the selected JAR's build/channel in the validation report. [Image Paper guide](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/server-types/paper/), [current Paper builds](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds).

Paper requires automated API requests to send a non-generic `User-Agent` that identifies the software and includes a contact URL or email address. An update command should discover released versions, select the intended channel, record pinned artifacts, and validate before proposing a version change. It should not silently deploy whatever version upstream publishes next. [Official downloads API policy](https://docs.papermc.io/misc/downloads-service/).

Use a fresh isolated data directory per validation run and Minecraft version. This prevents one run from changing another run's configuration or upgrading an existing world. The template's start prompt and agent instructions should point at the same executable build, customize, start, command, stop, and validate tooling that CI uses.

## Verified checksums

| Artifact | SHA-256 | Source |
| --- | --- | --- |
| Gradle 9.8.0 binary distribution | `bafd5ce9cfaea0fbccfdc8439a1ac42fbd4cd9c89dc9a988228d8a2639a58e6c` | [Gradle current API](https://services.gradle.org/versions/current) |
| Gradle 9.8.0 wrapper JAR | `238e777fcddd7e34f9708186085def2abd6e08e658505b38718d79d74c21abd5` | [Gradle current API](https://services.gradle.org/versions/current) |
| Paper 26.3 build 140 server | `98aabc113a80b9b5e183475e839a17cf99c39c915a1f46b8f35a5e89fd5de0f1` | [Paper 26.3 builds](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds) |
| Paper 26.2 build 129 server | `b1d8f6bfa1b6101fa8e947b53041cb3bdf5540e7b83b6547ca19ba7edefeb083` | [Paper 26.2 builds](https://fill.papermc.io/v3/projects/paper/versions/26.2/builds) |
| itzg 2026.9.2-java25 image manifest | `de5d1b1a83eba576f6c8a688fac2a3523ce457724cdebc8ea48d7818b74cdf6e` | [Publisher's Docker Hub tag API](https://registry.hub.docker.com/v2/repositories/itzg/minecraft-server/tags/2026.9.2-java25) |

The image checksum identifies the multi-platform manifest. Docker selects the architecture-specific image from that manifest. The server and Gradle checksums identify downloadable files. Record both the intended pin and the artifact actually executed during validation.
