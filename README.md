# Raspberry Pi ePaper Weather Station
Raspberry Pi ePaper Weather Station (05/2018)
--------------------------------------------------------------------------------------------------------------
HW Requirement:
1. Raspberry Pi 3+ (Any Pi will work but it is more convenient with built-in wireless to fetch information)
2. Waveshare/Seednew 2.7inch E-Ink display HAT (264x176) for Raspberry Pi, three-color (SKU: 13357)
(Amazon link: https://www.amazon.com/gp/product/B079M3G84Z/ref=oh_aui_detailpage_o01_s02?ie=UTF8&psc=1)
--------------------------------------------------------------------------------------------------------------
SW Requirement:
1. Developed using Raspbian Stretch
2. Install the python library and driver (see development resource #3 below)
--------------------------------------------------------------------------------------------------------------
Development Resource:
1. ePaper hat specification: https://www.waveshare.com/2.7inch-e-paper-hat-b.htm
2. ePaper WIKI: https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)
3. ePaper library and driver: http://www.seednew.com/wiki/Libraries_Installation_for_RPi (maybe obsolete)
                              https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi
4. Python image library (PILLOW) documentation: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
--------------------------------------------------------------------------------------------------------------
Tutorial Resource:
1. Jeedom weather station tutorial: https://diyprojects.io/weather-station-epaper-displaydashboard-jeedom-raspberry-pi-via-json-rpc-api/#.WwSXBKkh3Sw
===> jeedom_weather_station_demo.py: ePaper weather station tutorial code
===> Jeedom is a French weather API service. Not used in this project. the Python library setup guide is the first part of the tutorial is helpful
2. Adafruit ESP8266 WiFi Weather Station with Color TFT Display: https://learn.adafruit.com/wifi-weather-station-with-tft-display?view=all 
===> This tutorial is absolete; it uses WUnderground for weather API, which is no longer free
3. Adafruit Huzzah Weather Display: https://learn.adafruit.com/huzzah-weather-display?view=all#overview
===> This tutorial uses Darksky.net for weather API, which is the main source for this project
4. ePaper example codes: https://www.waveshare.com/w/upload/f/f5/2.7inch-e-paper-hat-code.7z
===> 1. demo_button.py: Example code for using the 4 buttons on the display
===> 2. epd2in7.py: python ibrary file
===> 3. main.py: Showing examples for drawing text and geometric shapes (requires the monocolor.bmp as input).


Project detail:
This project requires intermediate level of working on the Raspberry Pi. I am not including the Raspbian installation process since
there are plenty of online resources to follow. I use Raspbian Stretch since it is the latest image available at the moment.

Major components for this project:
1. Initial Setup for the Pi and prepare HW
2. Sign up for Darksky.net account
3. Modify the weather_station.py code (adding desired city to the group, display in Celsius or Fehrenheit, etc).
4. Finalize the Pi


1. Initial Setup for the Pi and prepare HW
------------------------------------------
Once the Raspberry Pi is booted up with the Stretch Raspbian:
1. Open a terminal window and enter "sudo raspi-config" to configure the Pi. Set localization (Change Internationalization: Locale (e.g., US = en.UTF-8, keyboard, and WIFI location)
2. Enable SSH and I2C bus
3. Reboot the Pi
4. Update the Pi: 
===> $ sudo apt-get update && sudo apt-get upgrade -y
5. 
