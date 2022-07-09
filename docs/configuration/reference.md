# Configuration Reference

These are all of the available config options for sChat. The following type of settings exist:

| Type | Values |
| ---- | ------ |
| `boolean` | `true` or `false` |
| `string` | A sequence of characters. |
| `number` | A valid number with or without floating points. |
| `minimessage` | A `string` parsed using the [MiniMessage Format][minimessage] format. |
| `color` | A valid Minecraft or hex color. See [here for details][color]. |
| `decoration` | A named text decoration. See [this reference][decoration]. |

!!! question "Looking for the channel settings?"
    Head over to the seperate [channel configuration][channels] section.

--8<-- "docs/partials/_config.md"

## `debug`

[:octicons-milestone-24: 1.0.0][1.0.0] · `boolean` · :octicons-pin-24: `false`

Set to `true` and restart your server to produce an enormous amount of debug logs.

```yaml
debug: true
```

## `messenger`

[:octicons-milestone-24: 1.0.0][1.0.0] · `string` · :octicons-pin-24: `pluginmessage`

The messenger controls how [`global`][channels] messages are forwarded to the other servers in the network.

| Type | Description | Since |
| ---- | ----------- | ----- |
| :octicons-pin-24: `pluginmessage` | Messages are sent thru the [Plugin Messaging Channel][pluginmessage] to the proxy. The proxy then forwards them to all other servers in the network. **sChat must be installed on the proxy** for this to work. | [:octicons-milestone-24: 1.0.0][1.0.0] |

```yaml
messenger: "pluginmessage"
```

!!! error "Invalid Messenger"
    An invalid messenger type will prevent your server from starting.

## `view`

The following settings control how the view is rendered to players.  
All config options reside under the `view` section.

```yaml
view:
  ...
```

### `system_message_format`

[:octicons-milestone-24: 1.0.0][1.0.0] · [`minimessage`][minimessage] · :octicons-sync-24:

Controls how system messages (messages not sent by players) are rendered.  

!!! note
    There is normally no need to modify this setting.

```yaml
view:
  system_message_format: "<dark_aqua><text>"
```

[![System Message Format](images/system_message_format.png)](https://webui.adventure.kyori.net/?mode=chat_closed&input=%3Cdark_aqua%3EPlayer%20joined%20the%20game.&bg=grass&st=%7B%22channel_name%22%3A%22Global%22%2C%22text%22%3A%22Hi%22%2C%22channel_key%22%3A%22global%22%2C%22source_name%22%3A%22Silthus%22%2C%22source_display_name%22%3A%22Silthus%22%7D)

### `private_chat_format`

The following section controls how private chats are formatted.  
All config options go under `view.private_chat_format` section.

!!! warning
    The private chat formatting is **not reloadable**.  
    You must restart your server for the changes to take effect.  
    The formatting configs of channels is reloadable.

```yaml
view:
  private_chat_format:
    ... # <-- all options go here
```

--8<-- "docs/configuration/_tab_format_config.md"

[![Private Chat Message Format](images/private_chat-message_format.png)](https://webui.adventure.kyori.net/?mode=chat_closed&input=%3Cdark_aqua%3E%3C%3Cyellow%3E%3Csource_display_name%3E%3Cdark_aqua%3E%3E%20%3Cgray%3E%3Ctext%3E&bg=grass&st=%7B%22channel_name%22%3A%22Global%22%2C%22text%22%3A%22Hi%22%2C%22channel_key%22%3A%22global%22%2C%22source_name%22%3A%22Silthus%22%2C%22source_display_name%22%3A%22Silthus%22%7D)

[channels]: channels.md
[minimessage]: minimessage.md
[next]: https://github.com/sVoxelDev/sChat/releases/latest
[1.0.1]: https://github.com/sVoxelDev/sChat/releases/tag/v1.0.1
[1.0.0]: https://github.com/sVoxelDev/sChat/releases/tag/v1.0.0
[1.0.0]: https://github.com/sVoxelDev/sChat/releases/tag/1.0.0
[pluginmessage]: https://www.spigotmc.org/wiki/bukkit-bungee-plugin-messaging-channel/
[color]: minimessage.md#color
[decoration]: minimessage.md#decoration