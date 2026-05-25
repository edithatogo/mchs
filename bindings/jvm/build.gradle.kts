plugins {
    `java-library`
    `maven-publish`
    signing
}

group = "io.github.edithatogo"
version = "0.1.0"

val centralPortalDeployUrl = providers.gradleProperty("centralPortalDeployUrl")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_DEPLOY_URL"))
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_PORTAL_URL"))
val centralPortalUsername = providers.gradleProperty("centralPortalUsername")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_USERNAME"))
val centralPortalPassword = providers.gradleProperty("centralPortalPassword")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_PASSWORD"))
val signingKey = providers.gradleProperty("signingKey")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_SIGNING_KEY"))
val signingPassword = providers.gradleProperty("signingPassword")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_SIGNING_PASSWORD"))

java {
    withJavadocJar()
    withSourcesJar()
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}

publishing {
    publications {
        create<MavenPublication>("mavenJava") {
            from(components["java"])
            artifactId = "mchs"

            pom {
                name.set("MCHS JVM Binding")
                description.set("Minimal JVM binding scaffold for MCHS/NWAU contract interoperability.")
                url.set("https://github.com/edithatogo/mchs")
                licenses {
                    license {
                        name.set("Apache License 2.0")
                        url.set("https://www.apache.org/licenses/LICENSE-2.0.txt")
                    }
                }
                developers {
                    developer {
                        id.set("edithatogo")
                        name.set("Dylan Mordaunt")
                    }
                }
                scm {
                    connection.set("scm:git:https://github.com/edithatogo/mchs.git")
                    developerConnection.set("scm:git:https://github.com/edithatogo/mchs.git")
                    url.set("https://github.com/edithatogo/mchs")
                }
            }
        }
    }

    repositories {
        if (centralPortalDeployUrl.isPresent) {
            maven {
                name = "centralPortal"
                url = uri(centralPortalDeployUrl.get())
                credentials {
                    username = centralPortalUsername.orNull
                    password = centralPortalPassword.orNull
                }
            }
        }
    }
}

signing {
    setRequired {
        gradle.taskGraph.allTasks.any {
            it.project == project &&
                it.name.startsWith("publish") &&
                it.name.contains("CentralPortalRepository", ignoreCase = true)
        } &&
            !version.toString().endsWith("SNAPSHOT")
    }

    if (signingKey.isPresent) {
        useInMemoryPgpKeys(signingKey.get(), signingPassword.orNull)
    }

    sign(publishing.publications["mavenJava"])
}

gradle.taskGraph.whenReady {
    val centralPortalPublishRequested = allTasks.any {
        it.project == project &&
            it.name.startsWith("publish") &&
            it.name.contains("CentralPortalRepository", ignoreCase = true)
    }

    if (centralPortalPublishRequested) {
        require(centralPortalDeployUrl.isPresent) {
            "Central Portal publish tasks require -PcentralPortalDeployUrl, MAVEN_CENTRAL_DEPLOY_URL, or MAVEN_CENTRAL_PORTAL_URL. Use the deployment endpoint required by the selected Central Portal publishing workflow."
        }
        require(centralPortalUsername.isPresent && centralPortalPassword.isPresent) {
            "Central Portal publish tasks require -PcentralPortalUsername/-PcentralPortalPassword or MAVEN_CENTRAL_USERNAME/MAVEN_CENTRAL_PASSWORD."
        }
        require(signingKey.isPresent) {
            "Central Portal publish tasks require -PsigningKey or MAVEN_CENTRAL_SIGNING_KEY."
        }
    }
}
