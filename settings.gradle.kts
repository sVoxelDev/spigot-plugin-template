enableFeaturePreview("VERSION_CATALOGS")

pluginManagement {
    includeBuild("build-logic")
}

rootProject.name = providers.gradleProperty("plugin.name").get()

pluginTemplateProject("acceptance")
pluginTemplateProject("bukkit")
pluginTemplateProject("core")
pluginTemplateProject("platform")

fun pluginTemplateProject(path: String, name: String = "${providers.gradleProperty("plugin.prefix").get()}-$path"): ProjectDescriptor {
    include(path)
    val project = project(":$path")
    project.name = name
    return project
}