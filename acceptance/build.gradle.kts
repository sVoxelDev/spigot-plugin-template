plugins {
    id("plugin.api")
    id("se.thinkcode.cucumber-runner")
}

dependencies {
    testImplementation(project(":${providers.gradleProperty("plugin.prefix").get()}-bukkit"))
    testImplementation(testFixtures(project(":${providers.gradleProperty("plugin.prefix").get()}-bukkit")))

    testImplementation(libs.mockbukkit)

    testImplementation(libs.junit.platform.suite)

    testImplementation(libs.cucumber)
    testImplementation(libs.cucumber.junit)
    testImplementation(libs.cucumber.guice)

    testImplementation(libs.javax.inject)
    testImplementation(libs.guice)
    testImplementation(libs.configurate.core)
    testImplementation(libs.adventure.plain)
}

cucumber {
    main = "io.cucumber.core.cli.Main"
    featurePath = "$rootDir/acceptance/src/test/resources/features"
    glue = "classpath:${providers.gradleProperty("plugin.group").get()}.cucumber"
    plugin = arrayOf("pretty", "json:$rootDir/acceptance/build/reports/cucumber-report.json")
}
