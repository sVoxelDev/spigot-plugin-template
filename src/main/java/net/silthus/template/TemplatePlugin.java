package net.silthus.template;

import co.aikar.commands.PaperCommandManager;
import kr.entree.spigradle.annotations.PluginMain;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;
import net.milkbowl.vault.chat.Chat;
import net.milkbowl.vault.economy.Economy;
import net.silthus.template.commands.TemplateCommands;
import net.silthus.template.integrations.vault.VaultProvider;
import org.bukkit.Bukkit;
import org.bukkit.configuration.InvalidConfigurationException;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.server.ServiceRegisterEvent;
import org.bukkit.plugin.PluginDescriptionFile;
import org.bukkit.plugin.RegisteredServiceProvider;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.plugin.java.JavaPluginLoader;

import java.io.File;
import java.io.IOException;
import java.util.Locale;
import java.util.Objects;

public class TemplatePlugin extends JavaPlugin implements Listener {

    @Getter
    @Accessors(fluent = true)
    private static TemplatePlugin instance;
    @Getter
    @Setter(AccessLevel.PACKAGE)
    private VaultProvider vault;
    private PaperCommandManager commandManager;

    public TemplatePlugin() {
        instance = this;
    }

    @SuppressWarnings("removal")
    public TemplatePlugin(
            JavaPluginLoader loader, PluginDescriptionFile description, File dataFolder, File file) {
        super(loader, description, dataFolder, file);
        instance = this;
    }

    @Override
    public void onEnable() {
        saveDefaultConfig();

        setupVaultIntegration();
        setupCommands();

        getServer().getPluginManager().registerEvents(this, this);
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        getLogger().info("Player joined.");
    }

    @EventHandler
    public void onServiceRegistration(ServiceRegisterEvent event) {
        if (event.getProvider().getService() == Economy.class) {
            setVault(new VaultProvider((Economy) event.getProvider().getProvider()));
            getLogger().info("Vault integration enabled.");
        }
    }

    private void setupVaultIntegration() {
        if (Bukkit.getPluginManager().isPluginEnabled("Vault")) {
            final RegisteredServiceProvider<Economy> serviceProvider = getServer().getServicesManager()
                .getRegistration(Economy.class);
            if (serviceProvider != null) {
                vault = new VaultProvider(Objects.requireNonNull(serviceProvider).getProvider());
                getLogger().info("Vault integration enabled.");
            }
        }
        if (vault == null) {
            vault = new VaultProvider();
            getLogger().warning("Vault integration is not yet available.");
        }
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
