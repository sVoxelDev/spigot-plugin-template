[![Build Status](https://github.com/Silthus/spigot-plugin-template/workflows/Build/badge.svg)](../../actions?query=workflow%3ABuild)
[![codecov](https://codecov.io/gh/Silthus/spigot-plugin-template/branch/master/graph/badge.svg)](https://codecov.io/gh/Silthus/spigot-plugin-template)
[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/Silthus/spigot-plugin-template?include_prereleases&label=release)](../../releases)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

# Workspace Setup

> This project is part of a pay what you want open source initiative.
>
> [Find out more on the Spigot forums!](https://www.spigotmc.org/threads/open-small-to-medium-plugin-development-pay-what-you-want-8-years-experience-high-quality.435578/)

You can use this template to develop your own Spigot plugins with [Gradle](https://gradle.org/).

## Supported Versions

| Version | Support |
| ------- | :-----: |
| 1.15.2  |   ✔️    |

## Setup Template

> **Note** This setup is actual only for IntelliJ

- Create a new Github project using this template.
- Clone this repository and open it in IntelliJ.
- Import the project with gradle.
- Go into the gradle.properties file and update the variables.
- Delete the [Changelog]. It will be generated on your first release.
- Update this `README` with your links and project information.
- Then execute the **setupServer** run configuration and the template will download the server jar file.

Please read the [Contributing Guidelines](CONTRIBUTING.md) before submitting any pull requests or opening issues.

## Deploy Task

You can export your plugin to the plugins directory from your working directory with the Gradle **deploy task**. The task will **build and copy** your plugin **automatically**.

## Debugging the Server

You can use and debug the installed test server by running the Server run configuration. Every time you start the server, the plugin will be deployed. You can disable it, when you edit the Server run configuration.

## Important info

By using this template and starting the server, you agree to the Minecraft EULA automatically, because in this template is the eula file, because then you dont have to agree manually.
