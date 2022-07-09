plugins {
    id("net.kyori.indra.publishing")
}

if (System.getenv("CI").toBoolean()) {
    val signingKey = System.getenv("SIGNING_KEY")
    val signingPassword = System.getenv("SIGNING_PASSWORD")
    if (signingKey != null && signingPassword != null) {
        signing.useInMemoryPgpKeys(signingKey, signingPassword)
    }
}

indra {
    github(providers.gradleProperty("plugin.github.user").get(), providers.gradleProperty("plugin.github.repo").get()) {
        ci(true)
    }

    mitLicense()

    configurePublications {
        pom {
            developers {
                developer {
                    id.set(providers.gradleProperty("plugin.developer.id").get())
                    name.set(providers.gradleProperty("plugin.developer.name").get())
                    timezone.set(providers.gradleProperty("plugin.developer.timezone").get())
                }
            }
        }
    }
}