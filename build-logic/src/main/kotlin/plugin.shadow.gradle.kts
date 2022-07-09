import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar
import gradle.kotlin.dsl.accessors._9bc3b6a3f384e4e728217dbc108ce9f4.build
import gradle.kotlin.dsl.accessors._9bc3b6a3f384e4e728217dbc108ce9f4.publish

plugins {
    id("com.github.johnrengelman.shadow")
}

tasks.withType<ShadowJar> {
    archiveClassifier.set("")
    dependencies {
        include(project(":${providers.gradleProperty("plugin.prefix").get()}-core"))
        include(project(":${providers.gradleProperty("plugin.prefix").get()}-platform"))
        include(dependency("cloud.commandframework::"))
        include(dependency("io.leangen.geantyref::"))
        include(dependency("org.spongepowered::"))
        include(dependency("org.bstats::"))
    }

    val lib = providers.gradleProperty("plugin.group").get() + ".lib"

    relocate("cloud.commandframework", "$lib.commands")
    relocate("org.spongepowered.configurate", "$lib.configurate")
    relocate("io.leangen.geantyref", "$lib.typetoken")
    relocate("org.bstats", "$lib.bstats")
}

tasks.build {
    dependsOn(tasks.withType<ShadowJar>())
}

tasks.publish {
    dependsOn(tasks.withType<ShadowJar>())
}