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

import io.cucumber.java.ParameterType;
import javax.inject.Inject;
import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;

public class ItemSteps {
    private final Context context;

    @Inject
    public ItemSteps(Context context) {
        this.context = context;
    }

    @ParameterType("[a-zA-Z_:]+")
    public Material material(String name) {
        return Material.matchMaterial(name);
    }

    @ParameterType("[a-zA-Z_:]+")
    public ItemStack item(String item) {
        return new ItemStack(material(item));
    }
}
