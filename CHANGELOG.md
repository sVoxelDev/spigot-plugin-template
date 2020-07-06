## [2.0.1](https://github.com/Silthus/spigot-plugin-template/compare/v2.0.0...v2.0.1) (2020-07-06)


### Bug Fixes

* **debug:** exclude all content inside debug/ ([751d2b7](https://github.com/Silthus/spigot-plugin-template/commit/751d2b7057a57330851968cb9c9bafad82f09d56))

# [2.0.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.7.1...v2.0.0) (2020-07-06)


### Features

* update spigradle to 2.0.0 ([df1f431](https://github.com/Silthus/spigot-plugin-template/commit/df1f431c6cb68bab085a182970c33cd0e96cddca)), closes [#19](https://github.com/Silthus/spigot-plugin-template/issues/19)


### BREAKING CHANGES

* The `@Plugin` annotation on the plugin main class for spigradle was renamed to `@PluginMain`

## [1.7.1](https://github.com/Silthus/spigot-plugin-template/compare/v1.7.0...v1.7.1) (2020-07-03)


### Bug Fixes

* target Minecraft 1.16.1 in gradle.properties ([8beb34a](https://github.com/Silthus/spigot-plugin-template/commit/8beb34a733787bd4c7cdb814a60234be2b3e981e))

# [1.7.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.6.0...v1.7.0) (2020-07-02)


### Features

* use new spigradle debug task for running the server ([d7a3f25](https://github.com/Silthus/spigot-plugin-template/commit/d7a3f25a694ab92e03ebc7bf9058264b5324acf1))

# [1.6.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.5.2...v1.6.0) (2020-06-25)


### Features

* **build:** split build and test into separate jobs ([38f74d4](https://github.com/Silthus/spigot-plugin-template/commit/38f74d48d258521f9414d1f050cacb7201cf6bfd))

## [1.5.2](https://github.com/Silthus/spigot-plugin-template/compare/v1.5.1...v1.5.2) (2020-06-25)


### Bug Fixes

* **build:** only run once on PR from same repo ([4df7f57](https://github.com/Silthus/spigot-plugin-template/commit/4df7f5701a2c47c46bf5394f544ca5fdf4d8bec4))

## [1.5.1](https://github.com/Silthus/spigot-plugin-template/compare/v1.5.0...v1.5.1) (2020-06-10)


### Bug Fixes

* **docs:** remove invalid whitespaces from gradle.properties ([d3fd4b5](https://github.com/Silthus/spigot-plugin-template/commit/d3fd4b53f1d7c1bd4f331f92b1651f89682b3122))

# [1.5.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.4.0...v1.5.0) (2020-06-10)


### Features

* auto update dependencies with dependabot ([e28ccf4](https://github.com/Silthus/spigot-plugin-template/commit/e28ccf4cbb64ee9975b23c974b50ad1f0a4315f9))

# [1.4.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.7...v1.4.0) (2020-06-08)


### Features

* **docs:** add spiget shields to spigot resource ([0907394](https://github.com/Silthus/spigot-plugin-template/commit/090739466d919f7b6f3fe24c3a2fade87129732d))

## [1.3.7](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.6...v1.3.7) (2020-05-25)


### Bug Fixes

* **build:** copy plugin to server based on rootProject.rootDir ([1315050](https://github.com/Silthus/spigot-plugin-template/commit/1315050ac27aa8740672a773ad6fc9fa14ee180e))
* **git:** ignore automatic generated plugin.yml ([4cccd5b](https://github.com/Silthus/spigot-plugin-template/commit/4cccd5b1197311dd456bb742c2ec5cb06dcadb8f))
* **plugin:** set correct spigradle plugin name ([a7d5af5](https://github.com/Silthus/spigot-plugin-template/commit/a7d5af590f8b8b06bf5350bff8e25059cdc4f7d6))

## [1.3.6](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.5...v1.3.6) (2020-05-24)


### Bug Fixes

* **release:** override GitHub API url with GH_URL ([43669f7](https://github.com/Silthus/spigot-plugin-template/commit/43669f730eee93f4c62a9bae1d0666a9513a8046))

## [1.3.5](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.4...v1.3.5) (2020-05-23)


### Bug Fixes

* **build:** hash yarn.lock for cache ([307b744](https://github.com/Silthus/spigot-plugin-template/commit/307b744c7a15fe940d1d8e967e44c93a3063cc67))


### Reverts

* publish shadowJar artifact  ([6e869fc](https://github.com/Silthus/spigot-plugin-template/commit/6e869fcc11de056faad831f215c80538c112435b))

## [1.3.4](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.3...v1.3.4) (2020-05-23)


### Bug Fixes

* **test:** copy plugin.yml to test resources ([54893f2](https://github.com/Silthus/spigot-plugin-template/commit/54893f201d37958e2fc1b07dfb403014d09ff1c0))

## [1.3.3](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.2...v1.3.3) (2020-05-23)


### Bug Fixes

* **plugin:** use pluginName property in plugin.yml ([094c57b](https://github.com/Silthus/spigot-plugin-template/commit/094c57b3730178470b60b7038950be8e1ced6c51))
* **publish:** publish shadow jar artifact ([64968ce](https://github.com/Silthus/spigot-plugin-template/commit/64968cefa69d10fea0f3a26b2d3da7abc1e627d5))

## [1.3.2](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.1...v1.3.2) (2020-05-23)


### Bug Fixes

* **build:** cache node correctly ([20bb9e3](https://github.com/Silthus/spigot-plugin-template/commit/20bb9e349a16efb5712c037b1786358447bfdda1))

## [1.3.1](https://github.com/Silthus/spigot-plugin-template/compare/v1.3.0...v1.3.1) (2020-05-22)


### Bug Fixes

* **release:** update semantic-release/GitHub ([aefa8c1](https://github.com/Silthus/spigot-plugin-template/commit/aefa8c1c9e250dc4df9e1707c096bf7e91b8b79d))

# [1.3.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.2.0...v1.3.0) (2020-05-20)


### Bug Fixes

* **publish:** revert publishing to project namespace ([4f2aa72](https://github.com/Silthus/spigot-plugin-template/commit/4f2aa72fd4aeb065fce5db6b8a137d9aa2e2c148))
* **tests:** output jacoco html report for intellij coverage ([7f94567](https://github.com/Silthus/spigot-plugin-template/commit/7f945670a9d63265be695d9adb21dbf0f24ead2b))


### Features

* **publish:** publish github package to user namespace ([ac38c81](https://github.com/Silthus/spigot-plugin-template/commit/ac38c811219942159901e5a177f71c9bb2e1d22e))

# [1.2.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.1.1...v1.2.0) (2020-05-12)


### Bug Fixes

* **build:** include dependencies in the shadow jar ([803099b](https://github.com/Silthus/spigot-plugin-template/commit/803099bdf08c8a9a465d9d1323e3e65e1d498b7a))


### Features

* **build:** replace artifactory with github packages ([f83a08a](https://github.com/Silthus/spigot-plugin-template/commit/f83a08a3507345e234105cb46a1bcf0b9950816a))
* **build:** target JDK 1.8 ([0cc380c](https://github.com/Silthus/spigot-plugin-template/commit/0cc380cc335780ebba57f46ad035badff6cfe299))

## [1.1.1](https://github.com/Silthus/spigot-plugin-template/compare/v1.1.0...v1.1.1) (2020-05-10)


### Bug Fixes

* **build:** cache yarn.lock instead of package-lock ([c067aab](https://github.com/Silthus/spigot-plugin-template/commit/c067aab502cb076253232e20533449336e54fa15))
* **lint:** remove spotless linting ([cb2f8d1](https://github.com/Silthus/spigot-plugin-template/commit/cb2f8d1e70081e414e6fbe76479d7a2387108070))

# [1.1.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.0.1...v1.1.0) (2020-05-09)


### Bug Fixes

* **build:** use ubuntu-18.04 as build host ([38669f1](https://github.com/Silthus/spigot-plugin-template/commit/38669f1523270edfc35e57f3d0278a2cb976a00c))
* **release:** add github credentials ([c6387b5](https://github.com/Silthus/spigot-plugin-template/commit/c6387b57e79260a55423c5a824353200c5ad1bbd))


### Features

* **publish:** publish artifact to github packages ([29afd59](https://github.com/Silthus/spigot-plugin-template/commit/29afd59e039142340e6ae52aa0dfd4d8891c78fc))

# [1.1.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.0.1...v1.1.0) (2020-05-09)


### Bug Fixes

* **build:** use ubuntu-18.04 as build host ([38669f1](https://github.com/Silthus/spigot-plugin-template/commit/38669f1523270edfc35e57f3d0278a2cb976a00c))
* **release:** add github credentials ([c6387b5](https://github.com/Silthus/spigot-plugin-template/commit/c6387b57e79260a55423c5a824353200c5ad1bbd))


### Features

* **publish:** publish artifact to github packages ([29afd59](https://github.com/Silthus/spigot-plugin-template/commit/29afd59e039142340e6ae52aa0dfd4d8891c78fc))

# [1.1.0](https://github.com/Silthus/spigot-plugin-template/compare/v1.0.1...v1.1.0) (2020-05-09)


### Bug Fixes

* **build:** use ubuntu-18.04 as build host ([38669f1](https://github.com/Silthus/spigot-plugin-template/commit/38669f1523270edfc35e57f3d0278a2cb976a00c))
* **release:** add github credentials ([c6387b5](https://github.com/Silthus/spigot-plugin-template/commit/c6387b57e79260a55423c5a824353200c5ad1bbd))


### Features

* **publish:** publish artifact to github packages ([29afd59](https://github.com/Silthus/spigot-plugin-template/commit/29afd59e039142340e6ae52aa0dfd4d8891c78fc))

## [1.1.1](https://github.com/Silthus/spigot-plugin-template/compare/v1.1.0...v1.1.1) (2020-05-08)


### Bug Fixes

* **release:** add github credentials ([c6387b5](https://github.com/Silthus/spigot-plugin-template/commit/c6387b57e79260a55423c5a824353200c5ad1bbd))

# [1.1.0](https://github.com/mcSilthus/spigot-plugin-template/compare/v1.0.1...v1.1.0) (2020-05-08)


### Bug Fixes

* **build:** use ubuntu-18.04 as build host ([38669f1](https://github.com/mcSilthus/spigot-plugin-template/commit/38669f1523270edfc35e57f3d0278a2cb976a00c))


### Features

* **publish:** publish artifact to github packages ([29afd59](https://github.com/mcSilthus/spigot-plugin-template/commit/29afd59e039142340e6ae52aa0dfd4d8891c78fc))

## [1.0.1](https://github.com/mcSilthus/spigot-plugin-template/compare/v1.0.0...v1.0.1) (2020-05-05)


### Bug Fixes

* **release:** run gradle-release before github ([a3ef1fa](https://github.com/mcSilthus/spigot-plugin-template/commit/a3ef1fa22441879e8de6d27a8af0cd5f2ad581f9))

# 1.0.0 (2020-05-05)


### Bug Fixes

* **gradle:** publish build artifacts to maven ([a997f81](https://github.com/mcSilthus/spigot-plugin-template/commit/a997f8196d7e58f2dbeea46a94f0584ef1be6593))
* **release:** use node 12 for semantic-release ([88166a9](https://github.com/mcSilthus/spigot-plugin-template/commit/88166a91ec37f5fa86324137a45e07126a3072e0))
* **test:** directly reference plugin.yml in test ([97f7fc4](https://github.com/mcSilthus/spigot-plugin-template/commit/97f7fc4956138cf83625026c7134d9fb1eaf3794))
* plugin startup ([134f07f](https://github.com/mcSilthus/spigot-plugin-template/commit/134f07f22badfddfe8e924627a75ec68d3814978))


### Features

* **build:** add semantic versioning ([cdedcfd](https://github.com/mcSilthus/spigot-plugin-template/commit/cdedcfd8315309c030668421a4730a23f5282bec))
