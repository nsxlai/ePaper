# ePaper
Weather Station with ePaper Display Project (05/2018)
![text](https://github.com/nsxlai/ePaper/blob/master/IMG_20180611_230516.jpg)

HW Requirement:
---------------
1. Raspberry Pi 3+ (Any Pi will work but it is more convenient with built-in wireless to fetch information)
2. Waveshare/Seednew 2.7inch E-Ink display HAT (264x176) for Raspberry Pi, three-color (SKU: 13357)
(Amazon link: https://www.amazon.com/gp/product/B079M3G84Z/ref=oh_aui_detailpage_o01_s02?ie=UTF8&psc=1)

SW Requirement:
---------------
1. Developed using Raspbian Stretch
2. Install the python library and driver (see development resource #3 below)

Development Resource:
---------------------
1. ePaper hat specification: https://www.waveshare.com/2.7inch-e-paper-hat-b.htm
2. ePaper WIKI: https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)
3. ePaper library and driver: http://www.seednew.com/wiki/Libraries_Installation_for_RPi (Maybe obsolete)
                              https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi
4. Python image library (PILLOW) documentation: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html

Example code for the ePaper HAT: https://www.waveshare.com/w/upload/f/f5/2.7inch-e-paper-hat-code.7z
--------------------------------
1. demo_button.py: Example code for using the 4 buttons on the display
2. epd2in7.py: python ibrary file
3. main.py: Showing examples for drawing text and geometric shapes (requires the monocolor.bmp as input).

Tutorial Resource:
------------------
1. Jeedom weather station tutorial: https://diyprojects.io/weather-station-epaper-displaydashboard-jeedom-raspberry-pi-via-json-rpc-api/#.WwSXBKkh3Sw
==> This tutorial uses the exact HW configuration (Raspberry Pi 3 and e-Paper HAT) but uses Jeedom weather API. This service doesn't seem to be working for US based users. Also the development is done in French for the most of the part.
==> jeedom_weather_station_demo.py: ePaper weather station tutorial code.

2. Adafruit ESP8266 WiFi Weather Station with Color TFT Display: https://learn.adafruit.com/wifi-weather-station-with-tft-display?view=all
==> This tutorial uses WUnderground for weather API, which is no longer free.

3. Adafruit Huzzah Weather Display: https://learn.adafruit.com/huzzah-weather-display?view=all
==> This tutorial uses Darksky.net for weather API. This service is free for the first 1000 API per day, which is ideal for this project. The main part of this project is using this API.

Project detail:
---------------
This project requires intermediate level of working on the Raspberry Pi. I am not including the Raspbian installation process since
there are plenty of online resources to follow. I use Raspbian Stretch since it is the latest image available at the moment.

   Project Phase:
   1. Initial setup for the Pi and prepare HW
   2. Sign up for the Darksky.net account
   3. Modify the weather_station.py code (add more destination cities, displaying temperature units in Celius or Fehrenheit).
   4. Finalize the Pi for running headless mode (no display and USB keyboard/mouse).


Phase 1:
--------
At the time of writting this README, Stretch is the latest version of Rasbian. I use the full version for development purpose but the lite version may be better for the final headless running mode.

Connect display and USB keyboard/mouse for configuration purpose. Once the Raspberry Pi is booted up with the Stretch Raspbian:
1. Update the Pi: ===> $ sudo apt-get update && sudo apt-get upgrade -y
2. Enter raspi-config utility.
3. Change the password.
4. Set localization (Change Internationalization: Locale (e.g., US = en.UTF-8, keyboard, and WIFI location).
5. Enable SSH.
6. Enable I2C.
7. Reboot the Pi.
8. Adjust date/time: timezone (tzselect), date (sudo date +%Y%m%d -s ‘20120418'), and time (sudo date +%T -s '11:14:00')

Note: At the time of documenting this README, I am using the Rasbian Stretch image release in June. The new feature released in this version of the Stretch image is that it includes first time setup process during the first boot. The password, WIFI, country, and time zone setting will be prompt for change. At the end, the first time setup dialogue will have the option to perform apt-get update && apt-get upgrade before rebooting. After the reboot, just enable the I2C, SPI, and SSH via raspi-config utilty.

## Phase 2:
1. Install the following library for the project:
=> sudo apt-get install python-dev python-pil python-imaging
=> sudo apt-get install python-smbus python-serial
=> pip install spidev
=> wget https://www.waveshare.com/w/upload/f/f5/2.7inch-e-paper-hat-code.7z
=> sudo apt-get install p7zip-full
=> 7za e 2.7inch-e-paper-hat-code.7z

## Phase 3: Install Docker
2. Update Packages:

Update Raspberry Pi packages using the following command –
sudo apt-get update && sudo apt-get upgrade
3. Install Docker:

Install Docker using following command –
curl -sSL https://get.docker.com | sh
4. Add permission to Pi User to run Docker Commands:

Add “pi” user to “docker” group using the following command –
sudo usermod -aG docker pi
You must Log off from Raspberry Pi and Login again, for this to take effect.
5. Verify Installation:

Check Docker installation using the “docker –version” command. If you see the correct version, you are good to go.
pi@RaPi1:~ $ docker --version
Docker version 17.05.0-ce, build 89658be
pi@RaPi1:~ $
6. Run Hello-World Program:

Run the ARM-based “hello-word” Docker container using “docker run armhf/hello-world” command. All the Docker Images under the namespace armhf are created by Docker team.
You can NOT run the default “hello-world” container (using “docker run hello-world”command) on Raspberry Pi as it is created for X86 Architecture and won’t work on ARM architecture based Raspberry Pi.
On successful execution, you should see following output on your Raspberry Pi –
pi@RaPi1:~ $ docker run armhf/hello-world


## Phase 4:
1. Reduce the memory split between the GPU and the rest of the system down to 16mb.

## What's next?
There are several ideas to imporve this weather station:
1. Use the utility developed for the e-paper display to shorten the refresh time. The utility was done in C so it should be better handle the display changes. The current Python method refreash rate is about 1 to 2 seconds (slow!) after the button press is registered.
2. Dockerize the project
3. Substitute the Raspberry Pi 3+ with Raspberry Pi Zero W. The Pi Zero W should be better suited for this applicate since the weather station project is not CPU intensive.
