plugins {
    `java-library`
    `maven-publish`
    signing
}

import org.gradle.api.artifacts.repositories.PasswordCredentials

group = "io.github.edithatogo"
version = "0.1.0"

val centralPortalDeployUrlExplicit = providers.gradleProperty("centralPortalDeployUrl")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_DEPLOY_URL"))
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_PORTAL_URL"))
val centralPortalDeployUrl = centralPortalDeployUrlExplicit
    .orElse("https://central.sonatype.com/api/v1/publisher")
val centralPortalUsername = providers.gradleProperty("centralPortalUsername")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_USERNAME"))
val centralPortalPassword = providers.gradleProperty("centralPortalPassword")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_PASSWORD"))
val mavenSigningKey = providers.gradleProperty("mavenSigningKey")
    .orElse(providers.gradleProperty("signingKey"))
    .orElse(providers.environmentVariable("MAVEN_SIGNING_KEY"))
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_SIGNING_KEY"))
val mavenSigningPassword = providers.gradleProperty("mavenSigningPassword")
    .orElse(providers.gradleProperty("signingPassword"))
    .orElse(providers.environmentVariable("MAVEN_SIGNING_PASSWORD"))
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
        maven {
            name = "centralPortal"
            url = uri(centralPortalDeployUrl.get())
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
            !gradle.startParameter.isDryRun &&
            !version.toString().endsWith("SNAPSHOT")
    }

    if (mavenSigningKey.isPresent) {
        useInMemoryPgpKeys(mavenSigningKey.get(), mavenSigningPassword.orNull)
    }

    sign(publishing.publications["mavenJava"])
}

gradle.taskGraph.whenReady {
    val centralPortalPublishRequested = allTasks.any {
        it.project == project &&
            it.name.startsWith("publish") &&
            it.name.contains("CentralPortalRepository", ignoreCase = true)
    }

    if (centralPortalPublishRequested && !gradle.startParameter.isDryRun) {
        require(centralPortalDeployUrlExplicit.isPresent) {
            "Central Portal publish tasks require -PcentralPortalDeployUrl, MAVEN_CENTRAL_DEPLOY_URL, or MAVEN_CENTRAL_PORTAL_URL. Use the deployment endpoint required by the selected Central Portal publishing workflow."
        }
        require(centralPortalUsername.isPresent && centralPortalPassword.isPresent) {
            "Central Portal publish tasks require -PcentralPortalUsername/-PcentralPortalPassword or MAVEN_CENTRAL_USERNAME/MAVEN_CENTRAL_PASSWORD."
        }
        require(mavenSigningKey.isPresent && mavenSigningPassword.isPresent) {
            "Central Portal publish tasks require -PmavenSigningKey/-PmavenSigningPassword or MAVEN_SIGNING_KEY/MAVEN_SIGNING_PASSWORD."
        }
    }
}
