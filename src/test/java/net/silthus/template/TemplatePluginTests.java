package net.silthus.template;

import org.bukkit.event.player.PlayerJoinEvent;
import org.junit.jupiter.api.Test;

public class TemplatePluginTests extends TestBase {

    @Test
    public void shouldFirePlayerJoinEvent() {
        server.addPlayer();

        server.getPluginManager().assertEventFired(PlayerJoinEvent.class);
    }
}
