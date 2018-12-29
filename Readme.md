# Workspace Setup

You can use this template to develop your own Spigot plugins with [Gradle](https://gradle.org/). 



## Supported Versions

| Version | Support |
| ------- | ------- |
| 1.8.8   | ✔️       |
| 1.12.2  | ✔️       |
| 1.13.2  | ✔️       |



## Setup Template

> **Note** This setup is actual only for IntelliJ 

1. Creating a new project from VCS in IntelliJ and clone this repository.
2. Go into the build.gradle file and set the mcVersion variable to one of the supported version. 
3. Then execute the **setupSpigot** task with gradle and the template will download the server jar file.
4. Add a Jar Application run configuration in IntelliJ and set a few things:
   1. The name of the configuration, for example Server.
   2. Path to the downloaded server.jar file in the working directory.
   3. Set the Working directory to the working directory, where the server.jar file is stored.
   4. Choose your JRE, I recommend Java 8.

Then you can start coding :)



## Deploy Task

You can export your plugin to the plugins directory from your working directory with the Gradle **deploy task**. The task will **build and copy** your plugin **automatically**. 

## Important info

By using this template and starting the server, you agree to the Minecraft EULA automatically, because in this template is the eula file, because then you dont have to agree manually.