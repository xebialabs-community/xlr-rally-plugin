# Preface #

This document describes the functionality provided by the xlr-rally-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-rally-plugin is a XL Release plugin that allows to integrate XL Release with Rally.

# Requirements #

* **Requirements**
	* **XL Release** 4.x
        * [Rally Rest Toolkit for Java](https://github.com/RallyTools/RallyRestToolkitForJava)

# Installation #

* Place the plugin JAR file into your `SERVER_HOME/plugins` directory.
* Place the Rally Rest Toolkit jarfile into your `SERVER_HOME/lib` directory.
* Restart the server  

# Types #

+ UpdateProperties

# Usage #

First, you need to add an entry in the [Configuration](https://docs.xebialabs.com/xl-release/how-to/create-custom-configuration-types-in-xl-release.html#configuration-page) section with information on how to connect to your Rally instance:

![Configuration](/rallyCI.png)

The next step is to add the required task [Types](#Types) to your release template, for example:

![Configuration](/updateStatusTask.png)

Note, properties are defined in the following format

`{ "property1Name" : "property1Value","property2Name" : "property2Value" }`

In the example above the Task TA3 has been updated with a new description and it's state has been progressed.

![Execution](/rallyResult.png)
