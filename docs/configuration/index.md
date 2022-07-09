# Configuration

The configuration documentation of sChat is split into two parts. One for [common settings][reference], like logging,
private chats and so on. The second part goes into detail how you can configure and setup [channels][channels].

!!! warning "New Config Options"
    New config options are not automatically added to the `config.yml`.  
    The default option will be used if nothing is configured.  
    Take a look at the [configuration reference][reference] to see what options where added when.

## Complete Config

--8<-- "docs/partials/_config.md"

## Configuration Reference Legend

You will notice several different icons and symbols across the [config reference][reference]. These are explained here.

| Symbol | Meaning |
| ------ | ------- |
| :octicons-milestone-24: 1.0.0 | The config option had its first stable release in the given version. |
| :octicons-milestone-24: next | The option is currently under development and available in the latest snapshot. |
| :octicons-pin-24: | Marks an option as the default option. |
| :octicons-sync-24: | The config option is reloadable, requiring no full server restart. *All [channel settings][channels] are reloadable.* |
| :octicons-beaker-24: | The feature is still experimental and may behave unexpected or suddenly change. |

[reference]: reference.md

[channels]: channels.md