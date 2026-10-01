package net.silthus.template.commands;

import java.io.IOException;
import java.util.List;
import java.util.Locale;
import net.kyori.adventure.text.Component;
import net.silthus.template.TemplatePlugin;
import org.bukkit.Statistic;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.configuration.InvalidConfigurationException;
import org.bukkit.entity.Player;

public final class TemplateCommand implements CommandExecutor, TabCompleter {

    private final TemplatePlugin plugin;
    private final String commandName;

    public TemplateCommand(TemplatePlugin plugin, String commandName) {
        this.plugin = plugin;
        this.commandName = commandName;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        String action = args.length == 0 ? "help" : args[0].toLowerCase(Locale.ROOT);
        if (args.length > 1) {
            help(sender);
            return true;
        }
        switch (action) {
            case "info" -> info(sender);
            case "status" -> {
                if (allowed(sender, "status")) {
                    sender.sendMessage(Component.text(plugin.getPluginMeta().getName() + " v"
                        + plugin.getPluginMeta().getVersion() + ". Greeting: "
                        + (plugin.settings().greetingEnabled() ? "enabled" : "disabled") + "."));
                }
            }
            case "reload" -> {
                if (allowed(sender, "reload")) {
                    reload(sender);
                }
            }
            default -> help(sender);
        }
        return true;
    }

    private void help(CommandSender sender) {
        sender.sendMessage(Component.text("Usage: /" + commandName + " [info|status|reload]"));
    }

    private void info(CommandSender sender) {
        if (sender instanceof Player player) {
            long minutes = player.getStatistic(Statistic.PLAY_ONE_MINUTE) / 1200L;
            sender.sendMessage(Component.text("Your name is: " + player.getName() + ". Playtime: " + minutes + " minutes."));
        } else {
            sender.sendMessage(Component.text("Only players can use this command."));
        }
    }

    private boolean allowed(CommandSender sender, String action) {
        if (sender.hasPermission(commandName + ".admin." + action)) {
            return true;
        }
        sender.sendMessage(Component.text("You do not have permission to use this command."));
        return false;
    }

    private void reload(CommandSender sender) {
        try {
            plugin.reloadSettings();
            sender.sendMessage(Component.text("Configuration reloaded."));
        } catch (IOException | InvalidConfigurationException | IllegalArgumentException exception) {
            sender.sendMessage(Component.text("Configuration was not reloaded: " + exception.getMessage()));
        }
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (args.length != 1) {
            return List.of();
        }
        return List.of("info", "status", "reload").stream()
            .filter(action -> action.equals("info") || sender.hasPermission(commandName + ".admin." + action))
            .filter(action -> action.startsWith(args[0].toLowerCase(Locale.ROOT)))
            .toList();
    }
}
