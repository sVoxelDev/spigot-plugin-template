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
package net.silthus.schat.cucumber;

import be.seeseemelk.mockbukkit.entity.PlayerMock;
import io.cucumber.java.ParameterType;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import javax.inject.Inject;
import net.silthus.schat.cucumber.models.Player;
import org.bukkit.inventory.ItemStack;

public class PlayerSteps {
    private final Context context;

    @Inject
    public PlayerSteps(Context context) {
        this.context = context;
    }

    public Player me() {
        return player("I");
    }

    @ParameterType("I|[a-zA-Z0-9]+")
    public Player player(String player) {
        return context.users().computeIfAbsent(player, this::createPlayer);
    }

    private Player createPlayer(String name) {
        return new Player(context, new PlayerMock(context.server(), name));
    }

    @Given("{player} have/has the {string} permission")
    public void setPermission(Player player, String permission) {
        player.setPermission(permission, true);
    }

    @Given("I am {player}")
    public void iAmPlayer(Player player) {
        context.users().put("I", player);
    }

    @Given("{player} join(s)/joined the server")
    public void joinsTheServer(Player player) {
        player.join();
    }

    @When("{player} execute(s) {string}")
    public void executeCommand(Player player, String command) {
        player.execute(command);
    }

    @Then("{player} receive(s) (the )message: {string}")
    public void playerReceivesMessage(Player player, String message) {
        player.assertReceivedMessage(message);
    }

    @Then("{player} get(s) {int} {item}")
    public void playerGetsItem(Player player, int amount, ItemStack item) {
        player.assertItem(item, amount);
    }
}
