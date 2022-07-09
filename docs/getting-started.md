# Installation

**sChat** requires at least **Java 17** and [ProtocolLib][ProtocolLib] (*on the bukkit platform*).  
After these prerequisites are met [download sChat][download] and drop it into the `plugins/` folder. Restart the server and you are done.

!!! hint "Multi-Server Networks"
    If you have a multi server setup using **Bungeecord** or **Velocity**, then download the plugin for the proxy and restart the proxy as well.

## Initial Configuration

sChat comes with two preconfigured channels: `global` and `team`. The latter can only be accessed by players that have the `schat.channel.team.join` permission.
It is [`protected`][config-protected]. Both channels are [`global`][config-global] and forward messages to all servers.

Here is a quick overview of the channel configuration. Each setting is explained in great detail in the [channel configuration][configuration-channel] section.

```yaml title="Global Channel Config"
channels:
  global:
    name: "<#189AB4>Global" # colors the name with the given hex formatted color
    settings:
      protected: false # the channel can be joined without a permission
      auto_join: true # the channel is added automatically to players
      global: true # messages are forwarded to all servers on the network
      forced: true # the channel cannot be left
  team:
    name: "Team"
    settings:
      protected: true # the channel can only be joined with the 'schat.channel.team.join' permission
      auto_join: true
      global: true
      forced: false # players can leave the channel if they wish
```

You can reload the channel configuration on-the-fly with the `/schat reload` command.

??? faq "Do I need to set all options of a channel for it to be valid?"
    No.
    The only thing you need to configure for a valid channel is the name.
    ```yaml
    channels:
      minimal:
        name: Minimal
    ```

??? faq "What do I need to configure on the proxy?"
    The proxy does not require any configuration and only serves as a message relay between servers.  
    *This might change in the future. But for know you don't need to touch the proxy config.*

## Full config.yml

--8<-- "docs/partials/_config.md"

## Next Steps

Now that you are setup, you have one of many options:

- take a look at the [commands][commands] and [permissions][permissions]
- deep dive into the [configuration][configuration]
- or get started with the [developer API][api]

[api]: ../developer/
[commands]: commands/
[permissions]: permissions/
[configuration]: ../configuration/
[configuration-channel]: ../configuration/channels
[config-global]: ../configuration/channel#global
[config-protected]: ../configuration/channel#protected
[download]: https://github.com/sVoxelDev/sChat/releases/latest
[ProtocolLib]: https://www.spigotmc.org/resources/protocollib.1997/
