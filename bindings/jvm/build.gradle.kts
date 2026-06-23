plugins {
    kotlin("jvm") version "2.2.21"
    `maven-publish`
    signing
}

group = "io.github.edithatogo"
version = "0.1.0"

kotlin { jvmToolchain(11) }

java {
    withSourcesJar()
    withJavadocJar()
}

dependencies {
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}

val centralPortalNamespaceVerified = providers
    .gradleProperty("mavenCentralNamespaceVerified")
    .map(String::toBoolean)
    .orElse(false)
val centralPortalUsername = providers
    .gradleProperty("mavenCentralUsername")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_USERNAME"))
val centralPortalPassword = providers
    .gradleProperty("mavenCentralPassword")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_PASSWORD"))
val signingKey = providers
    .gradleProperty("mavenCentralSigningKey")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_SIGNING_KEY"))
val signingPassword = providers
    .gradleProperty("mavenCentralSigningPassword")
    .orElse(providers.environmentVariable("MAVEN_CENTRAL_SIGNING_PASSWORD"))
val releaseMode = providers
    .gradleProperty("mavenCentralRelease")
    .map(String::toBoolean)
    .orElse(false)

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
            artifactId = "mchs-jvm-bindings"
            pom {
                name.set("MCHS JVM Bindings")
                description.set("JVM binding contract metadata and transport adapters for MCHS NWAU shared-core interoperability.")
                url.set("https://github.com/edithatogo/mchs")
                licenses { license { name.set("Apache-2.0"); url.set("https://www.apache.org/licenses/LICENSE-2.0") } }
                developers {
                    developer {
                        id.set("edithatogo")
                        name.set("edithatogo")
                        email.set("d.a.mordaunt@gmail.com")
                        organization.set("MCHS")
                        organizationUrl.set("https://github.com/edithatogo")
                    }
                }
                scm {
                    url.set("https://github.com/edithatogo/mchs")
                    connection.set("scm:git:https://github.com/edithatogo/mchs.git")
                    developerConnection.set("scm:git:ssh://git@github.com/edithatogo/mchs.git")
                }
            }
        }
    }
}

signing {
    isRequired = releaseMode.get()
    if (signingKey.isPresent && signingPassword.isPresent) {
        useInMemoryPgpKeys(signingKey.get(), signingPassword.get())
    }
    sign(publishing.publications["maven"])
}

tasks.register("validateCentralPortalReadiness") {
    group = "verification"
    description = "Checks Maven Central Portal readiness without uploading or requiring credentials."

    dependsOn(
        "checkPomFileForMavenPublication",
        "generateMetadataFileForMavenPublication",
        "generatePomFileForMavenPublication",
        "jar",
        "javadocJar",
        "sourcesJar",
    )

    doLast {
        val blockers = mutableListOf<String>()
        if (!centralPortalNamespaceVerified.get()) {
            blockers += "Central Portal namespace io.github.edithatogo has not been marked verified."
        }
        if (!centralPortalUsername.isPresent || !centralPortalPassword.isPresent) {
            blockers += "Central Portal publisher credentials are not present."
        }
        if (!signingKey.isPresent || !signingPassword.isPresent) {
            blockers += "In-memory PGP signing key/password are not present."
        }

        val reportFile = layout.buildDirectory.file("reports/central-portal-readiness.txt").get().asFile
        reportFile.parentFile.mkdirs()
        reportFile.writeText(
            buildString {
                appendLine("coordinate=io.github.edithatogo:mchs-jvm-bindings:0.1.0")
                appendLine("pomMetadata=passed")
                appendLine("sourcesJar=present")
                appendLine("javadocJar=present")
                appendLine("publicationUpload=not-attempted")
                appendLine("namespaceVerified=${centralPortalNamespaceVerified.get()}")
                appendLine("publisherCredentialsPresent=${centralPortalUsername.isPresent && centralPortalPassword.isPresent}")
                appendLine("signingCredentialsPresent=${signingKey.isPresent && signingPassword.isPresent}")
                appendLine("externalBlockers=${if (blockers.isEmpty()) "none" else blockers.joinToString(" | ")}")
            },
        )

        logger.lifecycle("Maven Central readiness report written to ${reportFile.relativeTo(projectDir)}")

        if (releaseMode.get() && blockers.isNotEmpty()) {
            throw GradleException("Maven Central release mode requested but external gates are missing: ${blockers.joinToString("; ")}")
        }
    }
}
