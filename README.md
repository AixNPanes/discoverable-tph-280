# discoverable-tph-280

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Prerequisites](#prerequisites)
  - [Install the module if you haven't already](#install-the-module-if-you-havent-already)
- [MQTT broker configuration](#mqtt-broker-configuration)
- [Module configuration](#module-configuration)
  - [Specify location of the configuration file](#specify-location-of-the-configuration-file)
  - [Configuration parameters](#configuration-parameters)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Prerequisites

### Install the module if you haven't already

See README_ui.md for module installation

## MQTT broker configuration

This code has only been tested with an external MQTT broker. I used Eclipse Mosquitto from https://mosquitto.org/. I had trouble using the internal MQTT broker, probably because of port forwarding issues due to running under docker.

Make sure the MQTT integration is installed on the Home Assistant server.
- Click Settings
- Click Devices and Services
- Click Integrations
You should find MQTT listed, if not perform the following to install:
- Click the blue button in the lower right hand corner labeled ADD INTEGRATION
- Enter MQTT in the search
- Click MQTT in the list of integrations (it's probably the only one)
- You'll get a list of MQTT integrations, click the one that says only MQTT
If the MQTT integration is installed, do the following:
- Click the MQTT icon
- Click Configure
- Click RE-CONFIGURE MQTT
Once you have ensured that the MQTT integration is installed, continue with the following to verify the correct parameters.
- Enter the Broker (the name or address of you MQTT broker)
- Enter the port for your MQTT broker, 1883 is the default, but use whatever is neede by the MQTT broker
- Enter the username, I believe homeassistant is the default
- Enter the password
- For MQTT protocol, use 5, 3.1 has been deprecated but will probably work.
- Click Next in the bottom right
- For Enable discovery, click the Enable button, if necessary, to enable
- For Discovery prefix, enter homeassistant, I believe this is the default
- Enable Birth messages, click the Enable button, if necessary, to enable
- For Birth message topic, enter homeassistant/status
- For birth message payload, enter online
- Click Submit

## Module configuration

### Specify location of the configuration file

The location of the configuration file is specified in the "config" environment variable. This form is primarily used for starting the module as a service, in which case it is specified as followed in the modules service file:

Environment="config=/etc/discoverable-tph-280/discoverable-tph-280.config"

This is the default if you use "make install" to install the service.

If the config environment variable is not found, then the filesystem is searched in the following order:

1. .config.yaml in the current directory
2. config.yaml in the module directory

### Configuration parameters

The contents of the .config.yaml file is as follows:

mqtt_broker:
  host: hastings.attlocal.net
  username: homeassistant
  password: wu2veeJoi5ox5ooP8wai9ich0oothaepaeg5keteu4mahwui9iexai7uNufae1sa
  discovery_prefix: homeassistant
  state_prefix: hmd
gpio:
  port: 1
  address: 0x76

Where the parameters have the following meaning:

- host: the Broker specified in the MQTT broker configuration on the Home Assistant server
- username: the username specified in the MQTT broker configuration on the Home Assistant server
- password: the password specified in the MQTT broker configuration on the Home Assistant server
- discovery_prefix: the Discovery Prefix specified in the MQTT broker configuration on the Home Assistant Server
- state_prefix: the state_prefix that the Home Assistant server will use to send state information to the module, this can be of your choosing as this configuration parameter is sent to the Home Assistant server during handshake so that the Home Assistant server knows which prefix to use and therefore there is no place to configure it on the Home Assistant Server
- port: the i2c port number used to communicate with the BME280 chip, normally 1
- address: the device address on the i2c bus used to communicate with the BME280 chip, normally 0x76
