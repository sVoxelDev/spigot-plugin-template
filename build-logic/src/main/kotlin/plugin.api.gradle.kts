import com.adarshr.gradle.testlogger.theme.ThemeType
import net.kyori.indra.repository.sonatypeSnapshots
import org.gradle.accessors.dm.LibrariesForLibs

plugins {
    id("plugin.publishing")
    id("net.kyori.indra")
    id("net.kyori.indra.crossdoc")
    id("net.kyori.indra.checkstyle")
    id("net.kyori.indra.license-header")
    id("com.adarshr.test-logger")
    id("io.freefair.lombok")
    java
    `java-library`
    `java-test-fixtures`
    jacoco
}

indra {
    javaVersions {
        target(17)
    }
    checkstyle("9.3")
}

checkstyle {
    // set false to fail on checkstyle errors
    isIgnoreFailures = true
}

testlogger {
    theme = ThemeType.MOCHA_PARALLEL
    showPassed = true
}

configurations {
    testCompileClasspath {
        exclude(group = "junit")
    }
}

repositories {
    mavenCentral()
    sonatypeSnapshots()
    maven("https://repo.velocitypowered.com/snapshots/") {
        content {
            includeGroup("com.velocitypowered")
        }
    }
    maven("https://papermc.io/repo/repository/maven-public/") {
        content {
            includeGroup("io.papermc.paper")
        }
    }
    maven("https://hub.spigotmc.org/nexus/content/repositories/snapshots/") {
        content {
            includeGroup("org.bukkit")
            includeGroup("org.spigotmc")
        }
    }
    maven("https://repo.dmulloy2.net/repository/public/") {
        content {
            includeGroup("com.comphenix.protocol")
        }
    }
    maven("https://repo.extendedclip.com/content/repositories/placeholderapi/") {
        content {
            includeGroup("me.clip")
        }
    }
}

dependencies {
    val libs = (project as ExtensionAware).extensions.getByName("libs") as LibrariesForLibs
    api(libs.checkerframework)

     checkstyle(libs.checkstyle.plugin.stylecheck)

    testImplementation(libs.bundles.testing.api)
    testFixturesImplementation(libs.bundles.testing.api)
    testRuntimeOnly(libs.bundles.testing.runtime)
}

indraCrossdoc {
    baseUrl().set(providers.gradleProperty("javadocPublishRoot").get())
    nameBasedDocumentationUrlProvider {
        projectNamePrefix.set(providers.gradleProperty("plugin.prefix").get() + "-")
    }
}

tasks {
    withType<JavaCompile> {
        dependsOn(updateLicenses)
        options.compilerArgs.add("-parameters")
    }

    processResources {
        project.setProperty("version", version)
        filesMatching("*.properties") {
            expand(project.properties)
        }
        filesMatching("plugin.yml") {
            expand("version" to version)
        }
        filesMatching("velocity-plugin.json") {
            expand("version" to version)
        }
    }

    javadoc {
        val opt = options as StandardJavadocDocletOptions
        opt.addStringOption("Xdoclint:none", "-quiet")
        opt.tags("sinceMinecraft:a:Since Minecraft:")

        opt.encoding("UTF-8")
        opt.charSet("UTF-8")
        doFirst {
            opt.links(
                "https://docs.oracle.com/en/java/javase/17/docs/api/",
            )
        }
    }

    jacocoTestReport {
        dependsOn(test)
    }
}

if (project.hasProperty("local_script")) {
    apply(file("${project.property("local_script")}/build.local.gradle"))
}
