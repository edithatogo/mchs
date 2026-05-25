plugins {
    `java-library`
    `maven-publish`
    signing
}

import org.gradle.api.credentials.PasswordCredentials

group = "io.github.edithatogo"
version = "0.1.0"

val centralPortalUsername = providers.gradleProperty("centralPortalUsername")
val centralPortalPassword = providers.gradleProperty("centralPortalPassword")

java {
    withJavadocJar()
    withSourcesJar()
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}

publishing {
    repositories {
        maven {
            name = "centralPortal"
            url = uri("https://central.sonatype.com/api/v1/publisher")
            credentials(PasswordCredentials::class) {
                username = centralPortalUsername.orNull
                password = centralPortalPassword.orNull
            }
        }
    }

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
        maven {
            name = "centralPortal"
            url = uri(
                providers.environmentVariable("MAVEN_CENTRAL_PORTAL_URL")
                    .orElse("https://central.sonatype.com/api/v1/publisher")
                    .get()
            )
            credentials {
                username = providers.environmentVariable("MAVEN_CENTRAL_USERNAME").orNull
                password = providers.environmentVariable("MAVEN_CENTRAL_PASSWORD").orNull
            }
        }
    }
}

signing {
    val signingKey = providers.environmentVariable("MAVEN_CENTRAL_SIGNING_KEY")
    val signingPassword = providers.environmentVariable("MAVEN_CENTRAL_SIGNING_PASSWORD")

    setRequired {
        gradle.taskGraph.allTasks.any { it.name.startsWith("publish") } &&
            !version.toString().endsWith("SNAPSHOT")
    }

    if (signingKey.isPresent) {
        useInMemoryPgpKeys(signingKey.get(), signingPassword.orNull)
    }

    sign(publishing.publications["mavenJava"])
}

gradle.taskGraph.whenReady {
    if (hasTask("publish") ||
        hasTask("publishAllPublicationsToCentralPortalRepository") ||
        hasTask("publishMavenJavaPublicationToCentralPortalRepository")
    ) {
        require(centralPortalUsername.isPresent && centralPortalPassword.isPresent) {
            "Central Portal publish tasks require -PcentralPortalUsername and -PcentralPortalPassword. The publish path fails closed when either credential is missing."
        }
    }
}
