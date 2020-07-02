[![Build Status](https://github.com/Silthus/spigot-plugin-template/workflows/Build/badge.svg)](../../actions?query=workflow%3ABuild)
[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/Silthus/spigot-plugin-template?include_prereleases&label=release)](../../releases)
![Spiget tested server versions](https://img.shields.io/spiget/tested-versions/79903)
[![Spiget Downloads](https://img.shields.io/spiget/downloads/79903)](https://www.spigotmc.org/resources/splugintemplate.79903/)
[![Spiget Rating](https://img.shields.io/spiget/rating/79903)](https://www.spigotmc.org/resources/splugintemplate.79903/)
[![codecov](https://codecov.io/gh/Silthus/spigot-plugin-template/branch/master/graph/badge.svg)](https://codecov.io/gh/Silthus/spigot-plugin-template)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

# Workspace Setup

> This project is part of a pay what you want open source initiative.
>
> [Find out more on the Spigot forums!](https://www.spigotmc.org/threads/open-small-to-medium-plugin-development-pay-what-you-want-8-years-experience-high-quality.435578/)

You can use this template to develop your own Spigot plugins with [Gradle](https://gradle.org/).

## Features

The template or better boilerplate comes with a lot of features that are useful if you want to develop high quality plugins. However you don't need to use all of them, you can simply remove the features you don't need.

- Ready to use [**Gradle**](https://gradle.org/) project with lots of utility tasks
- Automatic **generation of `plugin.yaml`** based of project properties with [SpiGradle](https://github.com/EntryPointKR/Spigradle/)
- Integrated [**Spigot test server**](https://github.com/EntryPointKR/Spigradle/) with a one click build, copy plugin and start debugging in IntelliJ task 
- [**Gradle shadow plugin**](https://imperceptiblethoughts.com/shadow/) to easily ship your needed dependencies with your plugin
- **[JUnit 5](https://junit.org/junit5/docs/current/user-guide/)** test setup including [MockBukkit](https://github.com/seeseemelk/MockBukkit) and [AssertJ](https://joel-costigliola.github.io/assertj/)
- **[Jacoco](https://github.com/jacoco/jacoco) code coverage** report including an upload task to [codecov](https://codecov.io/) 
- Fully integrated [**semantic-release**](https://semantic-release.gitbook.io/semantic-release/) release pipeline 
- Automatic [**changelog generation**](https://github.com/semantic-release/changelog) based on [conventional commit messages](https://www.conventionalcommits.org/)
- [**Github Actions**](https://github.com/features/actions) workflow for build and release
- Publishing of **maven artifacts** to [GitHub Packages](https://github.com/features/packages)
  > no more need for self hosted nexus or artifactory server
- GitHub [**issue templates**](https://help.github.com/en/github/building-a-strong-community/configuring-issue-templates-for-your-repository) for bug and feature requests
- Contributing and Code of Conduct **guidelines**
- Nice [**badges**](https://shields.io) to show of your project

## Setup Template

> **Note** This setup is actual only for IntelliJ

- Create a new Github project using this template.
- Clone the new repository and open it in IntelliJ.
- Import the project with gradle.
- Go into the gradle.properties file and update the variables.
- Delete the [Changelog]. It will be generated on your first release.
- Update this `README` with your links and project information.
- Then execute the **setupServer** run configuration and the template will download the server jar file.

Please read the [Contributing Guidelines](CONTRIBUTING.md) before submitting any pull requests or opening issues.

## Github Package Authentication

You need to configure [authentication for Github Packages](https://help.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-gradle-for-use-with-github-packages#authenticating-to-github-packages) if you want to use the maven package in other projects.

1. [Create a Github Personal Access Token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
2. Create or update the `gradle.properties` inside `C:\Users\%username%\.gradle` with the following and replace `YOUR_GITHUB_USERNAME` with your Github username and `YOUR_PERSONAL_ACCESS_TOKEN` with the access token from step 1.

```properties
gpr.user=YOUR_GITHUB_USERNAME
gpr.key=YOUR_PERSONAL_ACCESS_TOKEN
```

## Deploy Task

You can export your plugin to the plugins directory from your working directory with the Gradle **prepareSpigotPlugins** task. The task will **build and copy** your plugin **automatically** into the `plugins/` directory.

## Debugging the Server

You can run or debug the `Server` application from within IntelliJ to automatically download the Minecraft server, built it, copy your and dependent plugins into it and start it in debugging mode.

This is due to the awesome power of Spigradle's spigot tasks. Find out more on the [Spigradle Github page](https://github.com/spigradle/spigradle).

## References

* [Spigradle](https://github.com/spigradle/spigradle/): *provides awesome gradle tasks that make your live a lot easier*
* [semantic-release](https://semantic-release.gitbook.io/semantic-release/): *in my opinion every project should use this!*
* [conventional commit messages](https://www.conventionalcommits.org/): *do commit message the right way*
