# Contributing Guidelines

First off, thank you for considering contributing to this project. It's people like you that make this such a great plugin.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

This is an open source project and we love to receive contributions from our community — you! There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into the plugin itself.

Please, don't use the issue tracker for [requesting new plugins](https://www.spigotmc.org/threads/open-small-to-medium-plugin-development-pay-what-you-want-8-years-experience-high-quality.435578/). Read the post on the Spigot board or send me a [email](mailto://me@silthus.net).

# Ground Rules

By contributing to this project you submit to following our [code of conduct](.github/CODE_OF_CONDUCT.md).
Please read this next section carefully and check if your contribution meets all requirements in this checklist. This will save you and us a lot of time.

## Issues: Feature Requests & Bug Reports

Please make sure you checked all of the following before submitting a new issue.

* Before submitting a new issue, search the existing (including closed) issues for any duplicates.
* If you found an existing issue - use the react feature to show you have the same problem or need the same feature. Don't post comments like +1.
* Use the Bug & Feature Issue templates and provide all the required information.
* Be as detailed as possible and include screenshots wherever possible. This will help reproducing your bug or understanding your feature request.
* Use the WorldGuard `/wg report -p` command to provide detailed debug information and post the pastebin link in the issue.

## Contributing Code

Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

* **Commit using the [conventional-commit](https://www.conventionalcommits.org/en/v1.0.0/) format!**
* Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
* Keep feature versions as small as possible, preferably one new feature per version.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds.

# Your First Contribution

Unsure where to begin contributing to this project? You can start by looking through these beginner and help-wanted issues:
Good first issues - issues which should only require a few lines of code, and a test or two.
Help wanted issues - issues which should be a bit more involved than beginner issues.

Working on your first Pull Request? You can learn how from this *free* series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first :smile_cat:

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

# Getting started

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs or added new features, update the documentation.
4. Ensure the test suite passes.
5. Test your changes on a server running the latest supported Minecraft version.
6. Issue that pull request!

> You can use the `Setup Server` gradle task to quickly get your test server setup. Then use the `deploy` task to compile and copy your plugin.jar to the server.

# Code review process

The core team will look at your change as soon as possible and review it. However since this a project that is done in free time, reviewing might sometimes take some time.

# Code, commit message and labeling conventions

We have very precise rules over how our git commit messages can be formatted. This leads to **more
readable messages** that are easy to follow when looking through the **project history**. 

It is important to note that we use the git commit messages to **generate** the [CHANGELOG](CHANGELOG.md) document. Improperly formatted commit messages may result in your
change not appearing in the CHANGELOG of the next release.

### <a name="commit-message-format"></a> Commit Message Format
Each commit message consists of a **header**, a **body** and a **footer**. The header has a special
format that includes a **type**, a **scope** and a **subject**:

```html
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

> Any line of the commit message cannot be longer 100 characters!<br/>
  This allows the message to be easier to read on GitHub as well as in various Git tools.

##### Type
Must be one of the following:

* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing
  semi-colons, etc)
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **perf**: A code change that improves performance
* **test**: Adding missing tests
* **chore**: Changes to the build process or auxiliary tools and libraries such as documentation
  generation

##### Scope
The scope could be anything that helps specifying the scope (or feature) that is changing.

Examples
- command
- event
- permission
- featureX

##### Subject
The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize first letter
* no dot (.) at the end

##### Body
Just as in the **subject**, use the imperative, present tense: "change" not "changed" nor "changes"
The body should include the motivation for the change and contrast this with previous behavior.

##### Footer
The footer should contain any information about **Breaking Changes** and is also the place to
reference GitHub issues that this commit **Closes**, **Fixes**, or **Relates to**.

> Breaking Changes are intended to be highlighted in the ChangeLog as changes that will require
  community users to modify their code after updating to a version that contains this commit.

##### Sample Commit messages:
```text
fix(command): allow execution of /help X from the console

when using the console /help x could not be executed

Fixes #11231
```
```text
feat(respawn): respawn player in bed after death

* add test of player respawning in bed
* add docs regarding how to set the bed respawn point
* add command to reset bed spawnpoint

Fixes #11161 Fixes #3857
```

```text
refactor(respawn): bed respawn event renamed

    BREAKING CHANGE: PlayerBedRespawn renamed to PlayerRespawnInBed

    Change your code from this:

    ```java
    @EventHandler
    public void onRepsawn(PlayerBedRespawn event) {
      ...
    }
    ```

    To this:

    ```java
    @EventHandler
    public void onRepsawn(PlayerRespawnInBed event) {
      ...
    }
    ```
```

<br/>
