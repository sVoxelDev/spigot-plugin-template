/*
 * This file is part of <REPLACE_WITH_PLUGIN>, licensed under the MIT License.
 * Copyright (c) <REPLACE_ME> <REPLACE_ME@REPLACE_ME>
 * Copyright (c) contributors
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy
 *  of this software and associated documentation files (the "Software"), to deal
 *  in the Software without restriction, including without limitation the rights
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *  copies of the Software, and to permit persons to whom the Software is
 *  furnished to do so, subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in all
 *  copies or substantial portions of the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *  SOFTWARE.
 */
package net.silthus.schat.cucumber.models;

import be.seeseemelk.mockbukkit.entity.PlayerMock;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;
import net.silthus.schat.cucumber.Context;
import org.bukkit.inventory.ItemStack;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.catchRuntimeException;

@Getter
@Setter
@Accessors(fluent = true)
public class Player {

    private final Context context;
    private final PlayerMock player;

    public Player(Context context, PlayerMock player) {
        this.context = context;
        this.player = player;}

    public void setPermission(String permission, boolean val) {
        player().addAttachment(context.plugin(), permission, val);
    }

    public void execute(String command) {
        player().performCommand(command);
    }

    public void join() {
        context.server().addPlayer(player());
    }

    public void assertReceivedMessage(String message) {
        assertThat(player().nextMessage())
            .withFailMessage("Player did not receive any messages")
            .isNotNull()
            .isEqualTo(message);
    }

    public void assertItem(ItemStack item, int amount) {
        assertThat(player().getInventory().contains(item, amount))
            .withFailMessage("Expecting inventory to contain %sx %s", amount, item.getType().getKey())
            .isTrue();
    }
}
