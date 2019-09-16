# Workspace Setup

You can use this template to develop your own Spigot plugins with [Gradle](https://gradle.org/). 

## Supported Versions

| Version | Support |
| ------- | :-----: |
| 1.8.8   | ✔️       |
| 1.12.2  | ✔️       |
| 1.13.2  | ✔️       |
| 1.14.4  | ✔️       |


## Setup Template

> **Note** This setup is actual only for IntelliJ 

- Creating a new project from VCS in IntelliJ and clone this repository.
- Import the project with gradle
- Go into the build.gradle file and set the mcVersion variable to one of the supported version. 
- Then execute the **setupServer** run configuration and the template will download the server jar file.

Then you can start coding :)


## Deploy Task

You can export your plugin to the plugins directory from your working directory with the Gradle **deploy task**. The task will **build and copy** your plugin **automatically**. 


## Debugging the Server

You can use and debug the installed test server by running the Server run configuration. Every time you start the server, the plugin will be deployed. You can disable it, when you edit the Server run configuration.


## Video Tutorial


[![German](http://img.youtube.com/vi/9p0yHAW6OFE/0.jpg)](http://www.youtube.com/watch?v=9p0yHAW6OFE "German")


## Important info

By using this template and starting the server, you agree to the Minecraft EULA automatically, because in this template is the eula file, because then you dont have to agree manually.
