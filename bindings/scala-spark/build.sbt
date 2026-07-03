ThisBuild / organization := "example.invalid"
ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.12"

lazy val root = (project in file("."))
  .settings(
    name := "mchs-scala-spark-binding",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "3.5.1" % Provided
    ),
    description := "Synthetic Scala/Spark transport adapter for lakehouse costing-study workflows"
  )
