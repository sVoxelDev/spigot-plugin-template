import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar
import kr.entree.spigradle.kotlin.papermc
import kr.entree.spigradle.kotlin.spigotmc

plugins {
    id("plugin.api")
    id("plugin.shadow")
    id("kr.entree.spigradle")
}

description = providers.gradleProperty("plugin.description").get()

spigot {
//    depends = listOf("ProtocolLib")
//    softDepends = listOf("PlaceholderAPI", "WorldGuard")
    permissions {
        create("template.player") {
            description = "General permission for all players."
            defaults = "true"
            children = mapOf(
                "template.player.diamonds" to true
            )
        }
    }
}

dependencies {
    compileOnly(libs.spigot)

    implementation(libs.cloud.commands.paper)
    implementation(libs.adventure.platform.bukkit)
    implementation(libs.bstats.bukkit)

    testImplementation(libs.mockbukkit)

    testFixturesImplementation(libs.mockbukkit)
}

tasks.withType<ShadowJar> {
    dependencies {
        include(dependency("org.bstats:bstats-bukkit:"))
    }

    val lib = "net.silthus.schat.lib"
    relocate("org.bstats", "$lib.bstats")
}