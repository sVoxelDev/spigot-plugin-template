# Permissions

sChat bundles its permissions into `schat.player` (*default: `true`*) and `schat.admin` (*default: `OP`*) permissions.  

## Player Permissions

Every player has the following permissions by default.

!!! info
    You need to negate the `schat.player` permission if you only want to give players access to a portion of the player [commands][commands] and features.

| Permission | Description | Since |
| ---------- | ----------- | -----: |
| `schat.player` | This permission grouping contains all of the `schat.player.*` permissions. It is applied to all players by default. | [:octicons-milestone-24: 1.0.0][1.0.0] |
| `schat.player.channel.join` | Allows the player to join channels. This can be further restricted with individual channel permissions. | [:octicons-milestone-24: 1.0.0][1.0.0] |
| `schat.player.channel.leave` | Allows the player to leave channels. | [:octicons-milestone-24: 1.0.0][1.0.0] |
| `schat.player.channel.quickmessage` | Enables the player to send quick messages (`/ch <channel> <message>`) to channels he is allowed to write in. | [:octicons-milestone-24: 1.0.0][1.0.0] |
| `schat.player.directmessage` | Allows the player to send direct messages (`/dm <player> <message>`) to other players. | [:octicons-milestone-24: 1.0.0][1.0.0] |

## Admin Permissions

These are the additional permissions for admins.

| Permission | Description | Since |
| ---------- | ----------- | -----: |
| `schat.admin` | This permission groups all admin permissions nested under the `schat.admin.*` permissions. OPs get this by default. | [:octicons-milestone-24: 1.0.0][1.0.0] |
| `schat.admin.reload` | Allows performing the `/schat reload` command to reload the plugin. | [:octicons-milestone-24: 1.0.0][1.0.0] |

[commands]: /commands
[next]: https://github.com/sVoxelDev/sChat/releases/latest
[1.0.1]: https://github.com/sVoxelDev/sChat/releases/tag/v1.0.1
[1.0.0]: https://github.com/sVoxelDev/sChat/releases/tag/v1.0.0
[1.0.0]: https://github.com/sVoxelDev/sChat/releases/tag/1.0.0
