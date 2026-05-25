plugins {
    `java-library`
    `maven-publish`
    signing
}

import org.gradle.api.credentials.PasswordCredentials

group = "io.github.edithatogo"
version = "0.1.0"

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
            credentials(PasswordCredentials::class)
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
}

signing {
    setRequired {
        gradle.taskGraph.hasTask("publish")
    }
    sign(publishing.publications["mavenJava"])
}
