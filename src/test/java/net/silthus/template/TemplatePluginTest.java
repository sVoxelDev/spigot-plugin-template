package net.silthus.template;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import net.kyori.adventure.text.serializer.plain.PlainTextComponentSerializer;
import org.bukkit.Statistic;
import org.bukkit.event.player.PlayerJoinEvent;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockbukkit.mockbukkit.MockBukkit;
import org.mockbukkit.mockbukkit.ServerMock;
import org.mockbukkit.mockbukkit.entity.PlayerMock;

class TemplatePluginTest {

    private ServerMock server;
    private TemplatePlugin plugin;
    private String command;

    @BeforeEach
    void startPlugin() {
        server = MockBukkit.mock();
        plugin = MockBukkit.load(TemplatePlugin.class);
        command = plugin.commandName();
    }

    @AfterEach
    void stopPlugin() {
        MockBukkit.unmock();
    }

    @Test
    void freshInstallCreatesDefaultsAndGreetsPlayers() {
        assertTrue(plugin.isEnabled());
        assertTrue(Files.isRegularFile(plugin.getDataFolder().toPath().resolve("config.yml")));
        var player = server.addPlayer("Alex");
        assertEquals("Welcome, Alex!", player.nextMessage());
    }

    @Test
    void infoConvertsTicksToWholeMinutes() {
        var player = joinedPlayer();
        player.setStatistic(Statistic.PLAY_ONE_MINUTE, 3599);
        assertTrue(server.dispatchCommand(player, command + " info"));
        assertEquals("Your name is: Alex. Playtime: 2 minutes.", player.nextMessage());
    }

    @Test
    void consoleInfoExplainsThatAPlayerIsRequired() {
        assertTrue(server.dispatchCommand(server.getConsoleSender(), command + " info"));
        assertEquals("Only players can use this command.", server.getConsoleSender().nextMessage());
    }

    @Test
    void administratorCanReloadACustomGreeting() throws IOException {
        var player = joinedPlayer();
        player.addAttachment(plugin, command + ".admin.reload", true);
        configure("greeting:\n  enabled: true\n  message: 'Hello, {player}. Enjoy the server!'\n");
        server.dispatchCommand(player, command + " reload");
        assertEquals("Configuration reloaded.", player.nextMessage());
        server.getPluginManager().callEvent(new PlayerJoinEvent(player, net.kyori.adventure.text.Component.empty()));
        assertEquals("Hello, Alex. Enjoy the server!", player.nextMessage());
    }

    @Test
    void regularPlayerCannotReloadConfiguration() throws IOException {
        var player = joinedPlayer();
        configure("greeting:\n  enabled: false\n  message: 'Changed'\n");
        server.dispatchCommand(player, command + " reload");
        assertEquals("You do not have permission to use this command.", player.nextMessage());
        assertTrue(plugin.settings().greetingEnabled());
    }

    @Test
    void disabledGreetingSendsNoMessage() throws IOException {
        configure("greeting:\n  enabled: false\n  message: 'Changed'\n");
        server.dispatchCommand(server.getConsoleSender(), command + " reload");
        var player = server.addPlayer("Alex");
        assertNull(player.nextMessage());
        assertFalse(plugin.settings().greetingEnabled());
    }

    @Test
    void malformedReloadPreservesLastWorkingSettings() throws IOException {
        configure("greeting: [broken\n");
        server.dispatchCommand(server.getConsoleSender(), command + " reload");
        assertTrue(server.getConsoleSender().nextMessage().startsWith("Configuration was not reloaded:"));
        var player = server.addPlayer("Alex");
        assertEquals("Welcome, Alex!", player.nextMessage());
    }

    @Test
    void incorrectSettingTypePreservesLastWorkingSettings() throws IOException {
        configure("greeting:\n  enabled: 'false'\n  message: 'Changed'\n");
        server.dispatchCommand(server.getConsoleSender(), command + " reload");
        assertTrue(server.getConsoleSender().nextMessage().contains("greeting.enabled must be true or false"));
        assertTrue(plugin.settings().greetingEnabled());
    }

    @Test
    void playerNamesAndConfigurationAreLiteralText() throws IOException {
        configure("greeting:\n  enabled: true\n  message: '<red>Welcome, {player}!</red>'\n");
        server.dispatchCommand(server.getConsoleSender(), command + " reload");
        var player = server.addPlayer("Alex");
        assertEquals("<red>Welcome, Alex!</red>", player.nextMessage());
        assertEquals("<red>Welcome, Alex!</red>", PlainTextComponentSerializer.plainText().serialize(plugin.settings().greeting("Alex")));
    }

    @Test
    void statusRequiresPermissionAndReportsCurrentConfiguration() {
        var player = joinedPlayer();
        server.dispatchCommand(player, command + " status");
        assertEquals("You do not have permission to use this command.", player.nextMessage());
        player.addAttachment(plugin, command + ".admin.status", true);
        server.dispatchCommand(player, command + " status");
        assertEquals(plugin.getPluginMeta().getName() + " v" + plugin.getPluginMeta().getVersion() + ". Greeting: enabled.", player.nextMessage());
    }

    @Test
    void completionShowsOnlyCommandsThePlayerCanUse() {
        var player = joinedPlayer();
        var registered = plugin.getCommand(command);
        assertNotNull(registered);
        assertEquals(List.of("info"), registered.tabComplete(player, command, new String[]{""}));
        player.addAttachment(plugin, command + ".admin.reload", true);
        assertEquals(List.of("info", "reload"), registered.tabComplete(player, command, new String[]{""}));
        assertEquals(List.of(), registered.tabComplete(player, command, new String[]{"info", ""}));
    }

    @Test
    void unknownOrExtraArgumentsShowUsage() {
        var player = joinedPlayer();
        server.dispatchCommand(player, command + " unknown");
        assertEquals("Usage: /" + command + " [info|status|reload]", player.nextMessage());
        server.dispatchCommand(player, command + " info unexpected");
        assertEquals("Usage: /" + command + " [info|status|reload]", player.nextMessage());
    }

    private PlayerMock joinedPlayer() {
        var player = server.addPlayer("Alex");
        player.nextMessage();
        return player;
    }

    private void configure(String yaml) throws IOException {
        Files.writeString(plugin.getDataFolder().toPath().resolve("config.yml"), yaml);
    }
}
