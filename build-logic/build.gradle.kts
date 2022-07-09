plugins {
    `kotlin-dsl`
    kotlin("jvm") version "1.5.31"
}

repositories {
    gradlePluginPortal()
}

dependencies {
    implementation(libs.gradle.plugin.indra)
    implementation(libs.gradle.plugin.indra.publishing)
    implementation(libs.gradle.plugin.indra.crossdoc)
    implementation(libs.gradle.plugin.testlog)
    implementation(libs.gradle.plugin.lombok)
    implementation(libs.gradle.plugin.shadow)
    implementation(libs.gradle.plugin.cucumber)
    implementation(libs.gradle.plugin.spigradle)

    implementation(files(libs.javaClass.protectionDomain.codeSource.location))
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
    kotlinOptions {
        jvmTarget = "17"
    }
}
