package net.silthus.template;

import net.kyori.adventure.text.Component;
import org.bukkit.configuration.ConfigurationSection;

public record PluginSettings(boolean greetingEnabled, String greetingMessage) {

    public PluginSettings {
        if (greetingMessage == null || greetingMessage.isBlank()) {
            throw new IllegalArgumentException("greeting.message must be a nonempty string");
        }
    }

    public static PluginSettings from(ConfigurationSection config) {
        if (!config.isBoolean("greeting.enabled")) {
            throw new IllegalArgumentException("greeting.enabled must be true or false");
        }
        if (!config.isString("greeting.message")) {
            throw new IllegalArgumentException("greeting.message must be a nonempty string");
        }
        return new PluginSettings(config.getBoolean("greeting.enabled"), config.getString("greeting.message"));
    }

    public Component greeting(String playerName) {
        return Component.text(greetingMessage.replace("{player}", playerName));
    }
}
