package net.silthus.template;

import co.aikar.commands.PaperCommandManager;
import kr.entree.spigradle.annotations.PluginMain;
import lombok.Getter;
import lombok.experimental.Accessors;
import net.silthus.template.commands.TemplateCommands;
import org.bukkit.configuration.InvalidConfigurationException;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.PluginDescriptionFile;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.plugin.java.JavaPluginLoader;

import java.io.File;
import java.io.IOException;
import java.util.Locale;

@PluginMain
public class TemplatePlugin extends JavaPlugin implements Listener {

    @Getter
    @Accessors(fluent = true)
    private static TemplatePlugin instance;
    private PaperCommandManager commandManager;

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

        setupCommands();

        getServer().getPluginManager().registerEvents(this, this);
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        getLogger().info("Player joined.");
    }

    private void setupCommands() {
        commandManager = new PaperCommandManager(this);
        commandManager.enableUnstableAPI("help");

        loadCommandLocales(commandManager);

        commandManager.registerCommand(new TemplateCommands());
    }

    // see https://github.com/aikar/commands/wiki/Locales
    private void loadCommandLocales(PaperCommandManager commandManager) {
        try {
            saveResource("lang_en.yaml", true);
            commandManager.getLocales().setDefaultLocale(Locale.ENGLISH);
            commandManager.getLocales().loadYamlLanguageFile("lang_en.yaml", Locale.ENGLISH);
            // this will detect the client locale and use it where possible
            commandManager.usePerIssuerLocale(true);
        } catch (IOException | InvalidConfigurationException e) {
            getLogger().severe("Failed to load language config 'lang_en.yaml': " + e.getMessage());
            e.printStackTrace();
        }
    }
}
