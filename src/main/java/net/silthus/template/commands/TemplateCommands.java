package net.silthus.template.commands;

import co.aikar.commands.BaseCommand;
import co.aikar.commands.CommandHelp;
import co.aikar.commands.MessageType;
import co.aikar.commands.annotation.*;
import co.aikar.locales.MessageKey;
import org.bukkit.Statistic;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import static net.silthus.template.Constants.ACF_BASE_KEY;
import static net.silthus.template.Constants.INFO_CMD_PERMISSION;

@CommandAlias("stemplate")
public class TemplateCommands extends BaseCommand {

    // see https://github.com/aikar/commands/wiki/Locales
    static MessageKey key(String key) {
        return MessageKey.of(ACF_BASE_KEY + "." + key);
    }

    // see https://github.com/aikar/commands/wiki/Command-Help
    @HelpCommand
    @Subcommand("help")
    public void showHelp(CommandSender sender, CommandHelp help) {
        help.showHelp();
    }

    @Subcommand("info|i")
    @CommandAlias("info")
    @Description("{@@commands.descriptions.info}")
    @CommandCompletion("@players")
    @CommandPermission(INFO_CMD_PERMISSION)
    public void info(@Flags("self") Player player) {
        success("info",
                "{player}", player.getName(),
                "{play_time}", player.getStatistic(Statistic.PLAY_ONE_MINUTE) + " Minutes"
        );
    }

    private void success(String key, String... replacements) {
        getCurrentCommandIssuer().sendMessage(MessageType.INFO, key(key), replacements);
    }

    private void error(String key, String... replacements) {
        getCurrentCommandIssuer().sendMessage(MessageType.ERROR, key(key), replacements);
    }
}
