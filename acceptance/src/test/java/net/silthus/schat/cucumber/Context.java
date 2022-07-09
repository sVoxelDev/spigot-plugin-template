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

import be.seeseemelk.mockbukkit.MockBukkit;
import io.cucumber.guice.ScenarioScoped;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.github.silthus.template.CustomServerMock;
import io.github.silthus.template.TemplateBukkitPlugin;
import java.util.HashMap;
import java.util.Map;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;
import net.silthus.schat.cucumber.models.Player;
import org.bukkit.inventory.ItemStack;

@Getter
@Setter
@Accessors(fluent = true)
@ScenarioScoped
public class Context {

    private final CustomServerMock server = new CustomServerMock();
    private final PlayerSteps playerSteps;
    private final ItemSteps itemSteps;

    private final Map<String, Player> users = new HashMap<>();

    private TemplateBukkitPlugin plugin;

    public Context() {
        this.playerSteps = new PlayerSteps(this);
        this.itemSteps = new ItemSteps(this);
    }

    @Before(order = 10)
    public void setup() {
        MockBukkit.mock(server);
    }

    @Before(order = 20)
    public void loadPlugin() {
        plugin = MockBukkit.load(TemplateBukkitPlugin.class);
    }

    @After
    public void tearDown() {
        MockBukkit.unmock();
    }
}
