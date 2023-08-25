# Lovelace example for discoverable-tph-280

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Prerequisites](#prerequisites)
  - [Install the module if you haven't already](#install-the-module-if-you-havent-already)
  - [Run the module](#run-the-module)
  - [Create input_select](#create-input_select)
  - [Create the JavaScript resource](#create-the-javascript-resource)
  - [Create API token](#create-api-token)
  - [Enable UI changes](#enable-ui-changes)
  - [Create card](#create-card)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Prerequisites

### Install the module if you haven't already

sudo python3.11 pip install discoverable-tph-280

alternatively run the following to install the tph_280 service

make install

### Run the module

python3.11 -m discoverable-tph-280

### Create input_select

- Edit your Home Asistant configuration.yaml file one of the following methods (or another of your choice):
    - Addon - File Helper
    - Addon - Visual Studio Code
    - If you're using docker to run home assistant:
      - sudo docker exec -it `sudo docker ps|grep 'homeassistant:'|cut -d' ' -f1  -` bash
      - vi
- open the configuration.yaml file in the /config folder
- add the following to the configuration.yaml in the /config folder:

        input_select:
          temperature_units:
            name: Change Temperature Units
            options:
              - °C
              - °F
              - °K
            initial: °C
          humidity_units:
            name: Change Humidity Units
            options: ["%"]
            initial: "%"
          pressure_units:
            name: Change Pressure Units
            options:
              - hPa
              - kPa
              - Pa
              - bar
              - cbar
              - mbar
              - inHg
              - mmHg
              - PSI
            initial: hPa

- If there is no input_select: in the existing system configuration.yaml, just add the new data to the bottom
- If there is an existing input_select: add the configuration.yaml from the examples folder to the system's configuration.yaml after the last part of the existing input_select: statement, but delete the input_select: statement from the data you just added. There should only be a single input_select: statement in the resulting system configuration.yaml

### Create the JavaScript resource
- Create a folder in the www folder and call it unit-guage
- In the unit-guage folder, create a file and call it unit-guage.js
- Paste the contents of the file unit-guage.js from the cloned repository and paste in the unit-guage.js file you just created.
- Add a resource by doing the following:
 - click Settings in the side navigation bar
 - click Dashboards
 - click the 3 dots in the upper-right
 - click Resources
 - click the blue ADD RESOURCE button, in the URL
 - type /local/unit-guage/unit-guage.js
 - make sure JavaScript Module is checked
 - click CREATE.

### Create API token
- Click your userid in the bottom left corner
- Scroll to the bottom to the Long-Lived Tokens sections
- Click CREATE TOKEN
- Enter a name for the token
- Click OK
- Click the boxes to the right of the token to copy the token
- Click save the token temporarily in a text editor somewhere
- Use this token as (API Token) below

### Enable UI changes
- Enable your changes by clicking Developer Tools->YAML->Check Configuration. If you get Configuration will not prevent Home Assistant from starting! everything's OK. If you get an error or it seems to take a long time, fix it before you continue. Notifications or logs (use the editor like above) may help.
- Click RESTART, then Quick Restart
- Click Settings->Entities. The three input_select entities should be there.

### Create card
- Click Overview
- Select the View in which to place the card
- Click the 3 dots in the upper left
- Click Edit Dashboard
- Click the blue button in the bottom right to ADD CARD
- Scroll to the bottom and select Need to add a custom card or just want to manually right the YAML?
- Replace type: '' with the following:
 - type: custom:unit-gauge
 - label: Office
 - temperature_label: Temp.
 - temperature_entity: sensor.my_thermometer
 - temperature_units: input_select.temperature_units
 - pressure_label: Pres.
 - pressure_entity: sensor.my_barometer
 - pressure_units: input_select.pressure_units
 - humidity_label: Hum.
 - humidity_entity: sensor.my_hygrometer
 - humidity_units: input_select.humidity_units
 - api_token: >-
 -   (API-Token)
- Click Save
