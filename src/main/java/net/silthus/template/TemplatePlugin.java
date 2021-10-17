package net.silthus.template;

import kr.entree.spigradle.annotations.PluginMain;
import lombok.Getter;
import lombok.experimental.Accessors;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.PluginDescriptionFile;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.plugin.java.JavaPluginLoader;

import java.io.File;

@PluginMain
public class TemplatePlugin extends JavaPlugin implements Listener {

    @Getter
    @Accessors(fluent = true)
    private static TemplatePlugin instance;

    public TemplatePlugin() {
        instance = this;
    }

    public TemplatePlugin(
            JavaPluginLoader loader, PluginDescriptionFile description, File dataFolder, File file) {
        super(loader, description, dataFolder, file);
        instance = this;
    }

    @Override
    public void onEnable() {

        saveDefaultConfig();

        getServer().getPluginManager().registerEvents(this, this);
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        getLogger().info("Player joined.");
    }
}
