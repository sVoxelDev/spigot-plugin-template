plugins {
    id("plugin.publishing")
    alias(libs.plugins.indra.publishing.sonatype)
}

group = providers.gradleProperty("plugin.group").get()
description = providers.gradleProperty("plugin.description").get()

indraSonatype {
    useAlternateSonatypeOSSHost("s01")
}
