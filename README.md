# 2n-hass
Home Assistant integration for 2n/Helios devices
**Heavily WIP**

# Supported features
Currently the following features are supported:
- Control switches through home assistant
- Sensors for attached inputs (such as tamper switches or door open sensors)
- Restart the device
The following features are planned:
- Events/sensors based on logs (such as MotionDetected)
- Camera integration

# Supported devices
Devices have been tested with Firmware version 2.39, and as of now this is the only supported firmware level.
Older firmware versions *should* work, but no guarantees.
Supported devices:
- All 2n IP intercoms (IP Verso, LTE Verso, IP Style, etc.)
- 2n Access Unit 1.0/2.0/M

*Note: Some older intercoms and firmware versions need a license for API functionality. Newer firmware versions (if available) lift this restriction, so check for updates before you purchase!*

# Installation
## HACS
1. Add https://github.com/SVD-NL/helios2n-hass as a custom repository
2. Download 2n/Helios through the regular explore & download prompt
3. Restart Homeassistant

## Manual
1. Copy custom_components/helios2n and its contents to the custom_components folder in your homeassistant configuration folder.
2. Restart HA.

# Configuration
## On device
1. Log in to the web interface of your intercom.
2. Go to system>maintenance and make sure your intercom is updated to the latest version. Creating a config backup is recommended.
3. Go to services>HTTP API and enable the following services with connection type insecure(TCP) and authentication Basic: *Can't find this menu item? Your device may not be supported*
	- System
	- Switch
	- I/O
4. Go to one of the "account" tabs at the top of the page
5. Create a username/password combo
6. Select the following permissions:
	- System - Monitoring
	- System - Control (if you need the restart function)
	- Switches - Control
	- Inputs and Outputs - Monitoring
	- Inputs and Outputs - Control (If you need to control the outputs directly)
	- **More permissions may be needed in the future**

## In Home Assistant
Go to Settings>Devices & Services>Add Integration. Search for 2n/Helios, and select it.
Enter the IP address or hostname of your device, and the API credentials you just made, for example:

host: "192.168.1.25"
username: "homeassistant"
password: "S3cUReP@sS"

*Note: username (and password, obviously) are case sensitive*

Your intercom should be automatically added as a device, with entities for every **enabled** switch.
Monostable switches are added as a button entity
Bistable switches are added as a lock entity
After changing the switch mode or enabling/disabling a switch on the intercom, restart home assistant to update the entities.
**Caution** changing the switch mode will create a new entity and disable the previous one. Reverting will re-enable the previous entity and disable the second entity.
All other configuration changes do not change the entity in home assistant.

Outputs will be added as a switch entity.
Inputs will be added as a default sensor entity. You can use "show as" in the entity settings to change the entity type to the specific type of sensor (Tamper, door open, etc.)
Inputs and outputs are disabled by default.

## A note about switches and outputs
Be careful when controlling the same output through a switch and directly at the same time.
These can and will conflict with each other, and their statuses may desynchronise.
In those cases the state of the switch entity will be the accurate state of the output.
But again, this is highly discouraged.

# Bug reports and feature requests
When filing a bug report or requesting a feature, please open an issue and use the provided templates.
