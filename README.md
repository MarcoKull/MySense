# MySense
This program is a measurement system for IoT devices based on the LoPy4 Microcontroller written in Micropython. It was created during a internship at the GreenTechLab at Fontys Venlo, inspired by and making use of the original MySense software developed by Teus Hagen.

## Supported Devices
- BME680 Temperature/Humidity/Airquality Sensor
- HCSR04 Distance Sensor
- K33ELG CO² Sensor
- MB7040 Distance Sensor
- MB7092 Distance Sensor
- NEO6m GPS
- PMSx003 Particulate Matter Sensor
- DS3231 RTCC (for external sleep)

## Requirements
This software is intended to run on the LoPy4. However it was designed with portability in mind, so other platforms running python/micropthon could be supported as well.
To easily work with the LoPy4 it is recommended that you use either [Atom](https://atom.io/) or [Visual Studio Code](https://code.visualstudio.com/) in conjunction with the [PyMakr Plugin](https://pycom.io/solutions/software/pymakr/).

## Usage
Just download or clone this repository and and open its directory with your editor. You should be able to upload the program to your device. Now you can make changes to the main config file ```mysense/config/core.conf``` to configure the main functionality and which modules should be loaded. Afterwards you can adjust the other config files of the modules you chose.

## Description
The program flow is kept very simple, have a look at the [activity diagram](doc/activity-diagram.png). For an overview of the classes you can find the class diagram [here](doc/class-diagram.png)
### Modules
The system makes use of five different module types that are described in this section. If you want to create a new module you have to make sure that you create a new directory for it containing a file ```modules.py``` containing a class that matches exactly the directories name.
#### Input Modules
Input modules are used to get data that should be sent. Look at the [DateTime input module](mysense/modules/input/DateTime) for reference.
#### Ouput Modules
Output modules are used to sent the data gathered from the input modules. Look at the [Print output module](mysense/modules/output/Print) for reference.
#### Platform Modules
Platform modules are used to encapsulate platform specific code and behaviour. Look at the [Generic platform module](mysense/modules/platform/Generic) for reference.
#### Status Modules
Status modules are used to indicate the device status and/or display measurements, typically a display would be implemented using this kind of module. Look at the [Print status module](mysense/modules/status/Print) for reference.
#### Sleep Modules
Sleep modules are used to implement the sleeping behaviour. Look at the [Soft sleep module](mysense/modules/sleep/Soft) for reference.
