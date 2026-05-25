plugins {
    `java-library`
    `maven-publish`
    signing
}

import org.gradle.api.artifacts.repositories.PasswordCredentials

group = "io.github.edithatogo"
version = "0.1.0"

val centralPortalRepositoryUrl = providers.environmentVariable("MAVEN_CENTRAL_PORTAL_URL")
    .orElse("https://ossrh-staging-api.central.sonatype.com/service/local/staging/deploy/maven2/")
val centralPortalUsername = providers.environmentVariable("MAVEN_CENTRAL_USERNAME")
val centralPortalPassword = providers.environmentVariable("MAVEN_CENTRAL_PASSWORD")
val signingKey = providers.environmentVariable("MAVEN_CENTRAL_SIGNING_KEY")
val signingPassword = providers.environmentVariable("MAVEN_CENTRAL_SIGNING_PASSWORD")

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
        maven {
            name = "centralPortal"
            url = uri(centralPortalRepositoryUrl.get())
            credentials(PasswordCredentials::class) {
                username = centralPortalUsername.orNull
                password = centralPortalPassword.orNull
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
        require(centralPortalUsername.isPresent && centralPortalPassword.isPresent) {
            "Central Portal publish tasks require MAVEN_CENTRAL_USERNAME and MAVEN_CENTRAL_PASSWORD. The publish path fails closed when either credential is missing."
        }
        require(signingKey.isPresent) {
            "Central Portal publish tasks require MAVEN_CENTRAL_SIGNING_KEY. The publish path fails closed when signing material is missing."
        }
    }
}
