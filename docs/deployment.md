# Install a plugin on Paper

Build and validate with `./template validate --accept-eula`. The jar to install is `build/libs/<pluginName>-<version>.jar`, without `-sources` or `-javadoc`. Check `gradle.properties` for its identity and the validation report for its checksum.

## Existing server

Use Java 25 and a supported Paper release. The template declares API 26.2 and validates both stable 26.2 and latest 26.3. Paper 26.3 is currently beta. Choose the stable profile for production unless you deliberately use the beta release.

1. Back up the existing plugin jar and its `plugins/<pluginName>/` configuration directory.
2. Stop the server using its normal service or container command.
3. Copy the validated jar to `plugins/`, removing the previous jar for the same plugin from that directory. Keep the backup outside `plugins/`.
4. Start the server. Inspect `logs/latest.log` for the plugin's enable message and any exceptions.
5. Run `version <pluginName>` and `<commandName> status` from the console. Check that configuration matches your expectations and test the plugin's player behavior.

Use a full restart for jar changes. The example's `<commandName> reload` only reloads its configuration. If startup fails, stop the server, restore the previous jar/config, and restart.

The default command is `/template`. Players can use `/template info`. Administrators with `template.admin.status` and `template.admin.reload` can inspect and reload settings. Personalization replaces the command and its permission prefix.

## Local server for development

```bash
./template up --accept-eula --profile stable
./template rcon template status
./template logs
./template down
```

The server binds to `127.0.0.1:25565` and uses online authentication. Set `--port 25566` if another local server uses that port. Its data stays in `.template/dev/data`; `down` only removes the container. Changing jars requires `down` followed by `up`.

## A new Docker host

Use the validated jar with the official [itzg Paper image](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/server-types/paper/). Choose the exact supported version/build from `template.json`, expose only the Minecraft port, and keep RCON private. Store the world and plugin configuration on a persistent volume with regular backups.

This example uses the stable profile and starts a publicly reachable server. Run it only on a host you intend to operate as a Minecraft server. Place your jar in `./plugins/` first and choose a private RCON password in `.env`, outside Git.

```yaml
services:
  paper:
    image: itzg/minecraft-server:2026.9.2-java25@sha256:de5d1b1a83eba576f6c8a688fac2a3523ce457724cdebc8ea48d7818b74cdf6e
    ports:
      - '25565:25565'
    environment:
      EULA: '${EULA:?Set EULA=TRUE after accepting the Minecraft EULA}'
      TYPE: PAPER
      VERSION: '26.2'
      PAPER_DOWNLOAD_URL: 'https://fill-data.papermc.io/v1/objects/b1d8f6bfa1b6101fa8e947b53041cb3bdf5540e7b83b6547ca19ba7edefeb083/paper-26.2-129.jar'
      MEMORY: 4G
      ONLINE_MODE: 'TRUE'
      RCON_PASSWORD: '${RCON_PASSWORD:?Set a private password}'
    volumes:
      - './data:/data'
      - './plugins:/plugins:ro'
    restart: unless-stopped
```

Save as `compose.yaml`, configure `.env`, and run `docker compose up -d`. Verify with `docker compose logs paper` and `docker compose exec paper rcon-cli '<commandName> status'`. Keep your host's firewall and authentication configured for your intended players. The local template workflow does not deploy to this host automatically.
