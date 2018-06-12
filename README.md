# ePaper
ePaper Python Project (05/2018)

HW Requirement:
1. Raspberry Pi 3+ (Any Pi will work but it is more convenient with built-in wireless to fetch information)
2. Waveshare/Seednew 2.7inch E-Ink display HAT (264x176) for Raspberry Pi, three-color (SKU: 13357)
(Amazon link: https://www.amazon.com/gp/product/B079M3G84Z/ref=oh_aui_detailpage_o01_s02?ie=UTF8&psc=1)

SW Requirement:
1. Developed using Raspbian Stretch
2. Install the python library and driver (see development resource #3 below)

Development Resource:
1. ePaper hat specification: https://www.waveshare.com/2.7inch-e-paper-hat-b.htm
2. ePaper WIKI: https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)
3. ePaper library and driver: http://www.seednew.com/wiki/Libraries_Installation_for_RPi
4. ePaper example codes: https://www.waveshare.com/w/upload/f/f5/2.7inch-e-paper-hat-code.7z
5. ePaper weather station tutorial: https://diyprojects.io/weather-station-epaper-displaydashboard-jeedom-raspberry-pi-via-json-rpc-api/#.WwSXBKkh3Sw
6. Python image library (PILLOW) documentation: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html

Example code for the ePaper (from 2.7inch-e-paper-hat-code.7z)
1. demo_button.py: Example code for using the 4 buttons on the display
2. epd2in7.py: python ibrary file
3. main.py: Showing examples for drawing text and geometric shapes (requires the monocolor.bmp as input).

Example code for weather station tutorial: 
1. jeedom_weather_station_demo.py: ePaper weather station tutorial code (see development resource #4 above).

Project detail:
This project requires intermediate level of working on the Raspberry Pi. I am not including the Raspbian installation process since
there are plenty of online resources to follow. I use Raspbian Stretch since it is the latest image available at the moment.
