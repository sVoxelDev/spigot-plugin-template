package net.silthus.template.commands;

import be.seeseemelk.mockbukkit.entity.PlayerMock;
import net.silthus.template.Constants;
import net.silthus.template.TestBase;
import org.bukkit.Statistic;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class TemplateCommandsTests extends TestBase {

    private PlayerMock player;

    @Override
    @BeforeEach
    public void setUp() {
        super.setUp();

        player = server.addPlayer();
        player.addAttachment(plugin, Constants.INFO_CMD_PERMISSION, true);
    }

    @Test
    void info_forSelf_printsOwnPlayerName() {
        player.performCommand("stemplate info");

        int minutesPlayed = player.getStatistic(Statistic.PLAY_ONE_MINUTE);
        assertThat(player.nextMessage()).contains("Your name is: Player0. Playtime: " + minutesPlayed);
    }
}
