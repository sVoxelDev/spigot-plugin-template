package net.silthus.template;

import java.io.File;
import java.io.IOException;
import java.util.Objects;
import net.silthus.template.commands.TemplateCommand;
import org.bukkit.configuration.InvalidConfigurationException;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.PluginDescriptionFile;
import org.bukkit.plugin.java.JavaPlugin;

public class TemplatePlugin extends JavaPlugin implements Listener {

    private PluginSettings settings;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        try {
            reloadSettings();
        } catch (IOException | InvalidConfigurationException | IllegalArgumentException exception) {
            getLogger().severe("Invalid configuration: " + exception.getMessage());
            getServer().getPluginManager().disablePlugin(this);
            return;
        }
        String commandName = commandName();
        var command = Objects.requireNonNull(getCommand(commandName));
        var executor = new TemplateCommand(this, commandName);
        command.setExecutor(executor);
        command.setTabCompleter(executor);
        getServer().getPluginManager().registerEvents(this, this);
    }

    public String commandName() {
        return ((PluginDescriptionFile) getPluginMeta()).getCommands().keySet().iterator().next();
    }

    public PluginSettings settings() {
        return settings;
    }

    public void reloadSettings() throws IOException, InvalidConfigurationException {
        var configuration = new YamlConfiguration();
        configuration.load(new File(getDataFolder(), "config.yml"));
        settings = PluginSettings.from(configuration);
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        if (settings.greetingEnabled()) {
            event.getPlayer().sendMessage(settings.greeting(event.getPlayer().getName()));
        }
    }
}
