package net.silthus.template;

import be.seeseemelk.mockbukkit.MockBukkit;
import be.seeseemelk.mockbukkit.ServerMock;
import org.bukkit.event.player.PlayerJoinEvent;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TemplatePluginTests {

  private ServerMock server;

  @BeforeEach
  public void setUp() {
    server = MockBukkit.mock();
    MockBukkit.load(TemplatePlugin.class);
  }

  @Test
  public void shouldFirePlayerJoinEvent() {

    server.addPlayer();

    server.getPluginManager().assertEventFired(PlayerJoinEvent.class);
  }

  @AfterEach
  public void tearDown() {
    MockBukkit.unmock();
  }
}
