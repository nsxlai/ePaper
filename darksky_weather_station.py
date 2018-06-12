#!/usr/bin/env python
import json
import sys
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import commands
# import epd2in7
import time

modeTest = False     # for desktop testing (no ePaper display), set the mode to True; for RPI with ePaper testing, set the mode to False
if modeTest:
    EPD_WIDTH       = 176
    EPD_HEIGHT      = 264
    #     ------------------------
    #     |        HEIGHT        |
    #     |                      |
    #     |                      | Width
    #     |                      |
    #     |                      |
    #     ------------------------
else:
    print 'mode epd2in7'
    import RPi.GPIO as GPIO
    import epd2in7
    epd = epd2in7.EPD()
    epd.init()
    EPD_WIDTH       = epd2in7.EPD_WIDTH
    EPD_HEIGHT      = epd2in7.EPD_HEIGHT
    GPIO.setmode(GPIO.BCM)
    key1 = 5
    key2 = 6
    key3 = 13
    key4 = 19
  
    GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

'''Dark Sky API'''
api_key = '7b684b392b7e45f3878280a8dbb2d978'
# Location
home_city = 'Fremont'
location = { home_city     : {'latitude': 37.5483, 'longitude': -121.9886, 'tz': -7},
            # 'Milpitas'     : {'latitude': 37.4323, 'longitude': -121.8995, 'tz': -7},
            'New York'     : {'latitude': 42.3601, 'longitude': -71.0589, 'tz': -4},
            'Los Angeles'  : {'latitude': 34.0522, 'longitude': -118.243685, 'tz': -7},
            'San Francisco': {'latitude': 37.7740, 'longitude': -122.4313, 'tz': -7},
            'Hong Kong'    : {'latitude': 22.3964, 'longitude': 114.109497, 'tz': 8},
            'Paris'        : {'latitude': 48.8566, 'longitude': 2.3522, 'tz': 2},
            'Taipei'       : {'latitude': 25.1055, 'longitude': 121.5974, 'tz': 8},
            'Tokyo'        : {'latitude': 35.6528, 'longitude': 139.8395, 'tz': 9}
}

weather_icon = {'partly-cloudy-night': '4', 'partly-cloudy-day': 'H', 'cloudy': 'N',
                'rain': 'R', 'snow': 'X', 'clear-night': '2', 'clear-day': 'B',
                'windy': 'F', 'fog': 'L', 'celsius': '*', 'fehrenheit': '+', 'thermo': "'",
                'sunrise': 'J', 'sunset': 'A',}

def get_weather_report(city, latitude, longitude):
    '''Fetch the weather information from Darksky.net'''
    api_url = 'https://api.darksky.net/forecast/{}/{},{}'.format(api_key, latitude, longitude)
    req_data = requests.get(api_url)
    req_data = req_data.json()
    
    # Debug message
    print 'Summary: {}'.format(req_data['currently']['summary'])
    print 'Icon: {}'.format(req_data['currently']['icon'])
    print 'Location: {}'.format(city)
    print 'Latitude: {}'.format(req_data['latitude'])
    print 'Longitude: {}'.format(req_data['longitude'])
    print 'Temperature: {}'.format(req_data['currently']['temperature'])
    print 'Humidity: {}'.format(req_data['currently']['humidity'])
    print 'Pressure: {}'.format(req_data['currently']['pressure'])
    print 'Rain Chance: {}'.format(req_data['currently']['precipProbability'])
    print 'Wind Speed: {}'.format(req_data['currently']['windSpeed'])
    print 'Wind Bearing: {}'.format(req_data['currently']['windBearing'])
    return req_data

def weather_summary(city, req_data):
    # Create a white mask
    image = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)
    #Create a Draw object than allows to add elements (line, text, circle...)
    draw = ImageDraw.Draw(image)
    
    # Top Left Quadrant
    # font1 = ImageFont.truetype('FreeMono.ttf', 16)
    font1 = ImageFont.truetype('FreeSansBold.ttf', 16)   # Weather information text
    font2 = ImageFont.truetype('meteocons.ttf', 60)      # Weather icon
    font3 = ImageFont.truetype('meteocons.ttf', 30)      # Fehrenheir sign
    font4 = ImageFont.truetype('FreeSansBold.ttf', 20)   # weather summary font
    font5 = ImageFont.truetype('FreeSansBold.ttf', 14)   # weather summary font
    
    #---------------------------------------------
    #Weather Icon
    draw.text((12, 0), weather_icon[req_data['currently']['icon']], font = font2, fill = 0)
    if len(req_data['currently']['summary']) <= 16:
        draw.text((80, 22), req_data['currently']['summary'], font = font4, fill = 0)
    else:
        draw.text((80, 22), req_data['currently']['summary'], font = font5, fill = 0)
    
    #---------------------------------------------
    # Weather Info
    x_start_pt = 50
    y_start_py = 65
    draw.text((x_start_pt, y_start_py), 'Location: {}'.format(city), font = font1, fill = 0)
    draw.text((x_start_pt, y_start_py + 18), 'Latitude: {}'.format(location[city]['latitude']), font = font1, fill = 0)
    draw.text((x_start_pt, y_start_py + 18*2), 'Longitude: {}'.format(location[city]['longitude']), font = font1, fill = 0)
    # draw.text((7, EPD_WIDTH/2 + 12), 'Temp: {}'.format(req_data['currently']['temperature']), font = font1, fill = 0)
    # draw.text((95, EPD_WIDTH/2 + 5), weather_icon['celsius'], font = font2, fill = 0)
    # draw.text((7, EPD_WIDTH/2 + 30), 'Humidity: {} %'.format(req_data['currently']['humidity']), font = font1, fill = 0)
    # draw.text((7, EPD_WIDTH/2 + 48), 'Pressure: {} Pcal'.format(req_data['currently']['pressure']), font = font1, fill = 0)
    draw.text((x_start_pt, y_start_py + 18*3), 'Temp: {}'.format(req_data['currently']['temperature']), font = font1, fill = 0)
    draw.text((x_start_pt + 90, y_start_py + 18*3-7), weather_icon['fehrenheit'], font = font3, fill = 0)
    hum = float(req_data['currently']['humidity']) * 100
    
    draw.text((x_start_pt, y_start_py + 18*4), 'Humidity: {} %'.format(hum), font = font1, fill = 0)
    draw.text((x_start_pt, y_start_py + 18*5), 'Pressure: {} HPcal'.format(req_data['currently']['pressure']), font = font1, fill = 0)
    
    #----------------------------------------------
    #Horizontal line
    draw.line((0,y_start_py - 5, EPD_HEIGHT, y_start_py - 5), fill = 0)
    #Vertical line
    # draw.line((EPD_HEIGHT/2, 0, EPD_HEIGHT/2, y_start_py - 5), fill = 0)
    
    
    #Save the picture on disk
    # image.save('demo_image_new.bmp',"bmp")
    rotated_image = image.rotate(90, expand = True)    # The expand flag will rotate the image size to the new format
    # rotated_image.save('rotated_demo_image_new.bmp', 'bmp')
    # epd.display_frame(epd.get_frame_buffer(Image.open('rotated_demo_image_new.bmp')))
    
    if modeTest == False:
      epd.display_frame(epd.get_frame_buffer(rotated_image))
    
    return

def time_display(update):
    # Create a white mask
    image = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)
    #Create a Draw object than allows to add elements (line, text, circle...)
    draw = ImageDraw.Draw(image)
    # Declare font type and size
    font1 = ImageFont.truetype('FreeSansBold.ttf', 48)
    
    output_date = commands.getoutput('date +%Y/%m/%d')
    output_time = commands.getoutput('date +%H:%M')
    minute = output_time.split(':')[1]
    draw.text((5, 30), output_date, font = font1, fill = 0)
    draw.text((70, 85), output_time, font = font1, fill = 0)
    
    rotated_image = image.rotate(90, expand = True)    # The expand flag will rotate the image size to the new format
    # rotated_image.save('rotated_demo_image_new.bmp', 'bmp')
    
    if update == True:   # Will update the display only if the update is set to True
        if modeTest == False:
          epd.display_frame(epd.get_frame_buffer(rotated_image))
    return minute

def weather_hourly_forecast(city, req_data):
    '''Parse the weather data into hourly report'''
    font1 = ImageFont.truetype('FreeSansBold.ttf', 14)   # Weather information text
    font2 = ImageFont.truetype('meteocons.ttf', 30)      # Weather icon
    font3 = ImageFont.truetype('FreeSansBold.ttf', 20)
    # Create a white mask
    image = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)
    #Create a Draw object than allows to add elements (line, text, circle...)
    draw = ImageDraw.Draw(image)
    draw.text((6, 17), '{}'.format(city), font = font3, fill = 0)
    date_stamp, time_stamp = local_time(city, req_data['currently']['time'])   # Local time input is in Epoch time format, and returns as HH:MM format
    # time_stamp = commands.getoutput("echo {} | perl -pe 's/(\d+)/localtime($1)/e'".format(lt))  #
    draw.text((180, 5), date_stamp.split()[0], font = font1, fill = 0)
    draw.text((180, 20), date_stamp[4:], font = font1, fill = 0)
    draw.text((180, 37), time_stamp, font = font3, fill = 0)
    #Horizontal line
    draw.line((0, 60, EPD_HEIGHT, 60), fill = 0)
    #Vertical line
    draw.line((170, 0, 170, 60), fill = 0)
    
    hour = []
    for i in range(6):
        hour.append(req_data['hourly']['data'][i])
    
    x_start_pt = 10
    y_start_pt = 75
    sp_mul = 42    # space multiplier
    for i in hour:
        print 'summary = {}'.format(i['summary'])
        print 'icon = {}'.format(i['icon'])
        print 'temperature = {}'.format(i['temperature'])
        draw.text((x_start_pt + hour.index(i) * sp_mul, y_start_pt), weather_icon[i['icon']], font = font2, fill = 0)
        # draw.text((x_start_pt + hour.index(i) * sp_mul, y_start_pt + 30), i['summary'], font = font1, fill = 0)
        draw.text((x_start_pt + hour.index(i) * sp_mul, y_start_pt + 45), str(i['temperature']), font = font1, fill = 0)
        draw.text((x_start_pt + hour.index(i) * sp_mul, y_start_pt + 60), '+{} hr'.format(hour.index(i)), font = font1, fill = 0)
        
    rotated_image = image.rotate(90, expand = True)    # The expand flag will rotate the image size to the new format
    # rotated_image.save('rotated_demo_image_new.bmp', 'bmp')
    # epd.display_frame(epd.get_frame_buffer(Image.open('rotated_demo_image_new.bmp')))
    
    if modeTest == False:
      epd.display_frame(epd.get_frame_buffer(rotated_image))
    return

def weather_6day_forecast(city, req_data):
    '''Parse the weather data into daily report'''
    font1 = ImageFont.truetype('FreeSansBold.ttf', 14)   # Weather information text
    font2 = ImageFont.truetype('meteocons.ttf', 30)      # Weather icon
    font3 = ImageFont.truetype('FreeSansBold.ttf', 20)
    # Create a white mask
    image = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)
    #Create a Draw object than allows to add elements (line, text, circle...)
    draw = ImageDraw.Draw(image)
    draw.text((6, 17), '{}'.format(city), font = font3, fill = 0)
    date_stamp, time_stamp = local_time(city, req_data['currently']['time'])   # Local time input is in Epoch time format, and returns as HH:MM format
    # time_stamp = commands.getoutput("echo {} | perl -pe 's/(\d+)/localtime($1)/e'".format(local_time))
    draw.text((180, 5), date_stamp.split()[0], font = font1, fill = 0)
    draw.text((180, 20), date_stamp[4:], font = font1, fill = 0)
    draw.text((180, 37), time_stamp, font = font3, fill = 0)
    #Horizontal line
    draw.line((0, 60, EPD_HEIGHT, 60), fill = 0)
    #Vertical line
    draw.line((170, 0, 170, 60), fill = 0)
    
    day = []
    for i in range(6):
        day.append(req_data['daily']['data'][i])
    
    x_start_pt = 10
    y_start_pt = 75
    sp_mul = 42    # space multiplier
    for i in day:
        print 'summary = {}'.format(i['summary'])
        print 'icon = {}'.format(i['icon'])
        print 'temperatureHigh = {}'.format(i['temperatureHigh'])
        print 'temperatureLow = {}'.format(i['temperatureLow'])
        draw.text((x_start_pt + day.index(i) * sp_mul, y_start_pt), weather_icon[i['icon']], font = font2, fill = 0)
        # draw.text((x_start_pt + hour.index(i) * sp_mul, y_start_pt + 30), i['summary'], font = font1, fill = 0)
        draw.text((x_start_pt + day.index(i) * sp_mul, y_start_pt + 45), str(i['temperatureHigh']), font = font1, fill = 0)
        draw.text((x_start_pt + day.index(i) * sp_mul, y_start_pt + 60), str(i['temperatureLow']), font = font1, fill = 0)
        draw.text((x_start_pt + day.index(i) * sp_mul, y_start_pt + 75), '+{}day'.format(day.index(i)), font = font1, fill = 0)
        
    rotated_image = image.rotate(90, expand = True)    # The expand flag will rotate the image size to the new format
    # rotated_image.save('rotated_demo_image_new.bmp', 'bmp')
    # epd.display_frame(epd.get_frame_buffer(Image.open('rotated_demo_image_new.bmp')))
    
    if modeTest == False:
      epd.display_frame(epd.get_frame_buffer(rotated_image))
    return

def local_time(city, time_str):
    '''To calculate the city local time by using the 'tz' in the location dictionary.
       The 'tz' variable is in hours in respect to the UTC
       When doing the API call, the time in ['currently']['time'] is in the time zone of the device
       time_str = Epoch time format
    '''
    
    utc_time = int(time_str) + -(location[home_city]['tz'] * 3600)  # time string is in Epoch time format (in seconds)
    local_time = utc_time + (location[city]['tz'] * 3600)
    time_stamp = commands.getoutput("echo {} | perl -pe 's/(\d+)/localtime($1)/e'".format(local_time))

    time_array = time_stamp.split()      # change from 'Tue Jun 12 10:11:34 2018' to ['Tue', 'Jun', '12', '10:11:34', '2018']
    date_stamp = '{} {} {} {}'.format(time_array[0], time_array[1], time_array[2], time_array[4])
    time_stamp = time_array[3][:-3]    # Excluding the seconds (HH:MM:SS to HH:MM)
    print 'date_stamp = {}'.format(date_stamp)
    print 'time_stamp = {}'.format(time_stamp)
    return date_stamp, time_stamp

def sun_dial(city, req_data):
    '''Display the sunrise and sunset time for today'''
    font1 = ImageFont.truetype('FreeSansBold.ttf', 14)   # Weather information text
    font2 = ImageFont.truetype('meteocons.ttf', 45)      # Weather icon
    font3 = ImageFont.truetype('FreeSansBold.ttf', 20)
    # Create a white mask
    image = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)
    #Create a Draw object than allows to add elements (line, text, circle...)
    draw = ImageDraw.Draw(image)
    draw.text((6, 17), '{}'.format(city), font = font3, fill = 0)
    date_stamp, time_stamp = local_time(city, req_data['currently']['time'])   # Local time input is in Epoch time format, and returns as HH:MM format
    # time_stamp = commands.getoutput("echo {} | perl -pe 's/(\d+)/localtime($1)/e'".format(local_time))
    draw.text((180, 5), date_stamp.split()[0], font = font1, fill = 0)
    draw.text((180, 20), date_stamp[4:], font = font1, fill = 0)
    draw.text((180, 37), time_stamp, font = font3, fill = 0)
    #Horizontal line
    draw.line((0, 60, EPD_HEIGHT, 60), fill = 0)
    #Vertical line
    draw.line((170, 0, 170, 60), fill = 0)
    
    # sunrise_time = req_data['daily']['data'][0]['sunriseTime']
    # sunset_time  = req_data['daily']['data'][0]['sunsetTime']
    # print 'sunrise_time = {}'.format(sunrise_time)
    # print 'sunrise_time = {}'.format(sunrise_time)
    date_stamp, sunrise_time_stamp = local_time(city, req_data['daily']['data'][0]['sunriseTime'])
    date_stamp, sunset_time_stamp  = local_time(city, req_data['daily']['data'][0]['sunsetTime'])
    # print 'Sunrise Time = {}'.format(sunrise_time_stamp)
    # print 'Sunset  Time = {}'.format(sunset_time_stamp)
    
    draw.text((10, 75), weather_icon['sunrise'], font = font2, fill = 0)
    draw.text((65, 90), 'Sun rises at {}'.format(sunrise_time_stamp), font = font3, fill = 0)
    draw.text((10, 125), weather_icon['sunset'],  font = font2, fill = 0)
    draw.text((65, 140), 'Sun sets  at {}'.format(sunset_time_stamp), font = font3, fill = 0)
    
    rotated_image = image.rotate(90, expand = True)    # The expand flag will rotate the image size to the new format
    # rotated_image.save('rotated_demo_image_new.bmp', 'bmp')
    # epd.display_frame(epd.get_frame_buffer(Image.open('rotated_demo_image_new.bmp')))
    
    if modeTest == False:
      epd.display_frame(epd.get_frame_buffer(rotated_image))
    return

if __name__ == '__main__':
    # for city in location:
    #     # print 'City: {}'.format(city)
    #     req_data = get_weather_report(city, location[city]['latitude'], location[city]['longitude'])
    #     print '-' * 20
    
    city = home_city
    req_data = get_weather_report(city, location[city]['latitude'], location[city]['longitude'])
    weather_summary(city, req_data)
    # image_epaper_display()
    
    counter = 0
    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)
        
        city_list = []
        for i in location:
            city_list.append(i)

        if key1state == False:
            print '-' * 20
            counter += 1
            if counter >= len(city_list):
                counter = 0
            city = city_list[counter]
            req_data = get_weather_report(city, location[city]['latitude'], location[city]['longitude'])
            weather_summary(city, req_data)
            print 'counter = {}'.format(counter)    
            time.sleep(0.2)
            
        if key2state == False:
            print '-' * 20
            weather_hourly_forecast(city, req_data)
            time.sleep(0.2)
            
        if key3state == False:
            print '-' * 20
            weather_6day_forecast(city, req_data)
            time.sleep(0.2)
            
        if key4state == False:
            print '-' * 20
            sun_dial(city, req_data)
            time.sleep(0.2)
            # print 'Display time'
            # time_display(True)
            # keep_time = True
            # update = True
            # while keep_time == True:
            #     minute_01 = time_display(update)
            #     print 'Current minute_01: {}'.format(minute_01)
            #     if key1state == False:   # since the logic is button depress = False
            #         keep_time == False                                                 # Use "and" logic instead of "or"
            #         print 'keep_time = {}'.format(keep_time)
            #     time.sleep(1)
            #     minute_02 = time_display(False)
            #     print 'Current minute_02: {}'.format(minute_02)
            #     if minute_01 == minute_02:
            #         update = False
            #     else:
            #         update = True
            #     print 'keep_time = {}'.format(keep_time)
            #     print 'update = {}'.format(update)
                    
            