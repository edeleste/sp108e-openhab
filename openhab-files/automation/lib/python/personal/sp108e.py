### Based  on   https://gist.github.com/cgrin/a4c7a74faf2affe11b18d1e54e68f37a.js
### Some info in: https://github.com/hamishcoleman/led_sp108e/blob/master/notes.txt
### Please, save as: (.../openHAB-conf)/automation/lib/sp108e.py
import socket
import binascii
from time import sleep
from core.log import logging, LOG_PREFIX
log = logging.getLogger("{}.sp108e.py".format(LOG_PREFIX))

class SP108e:

    def __init__(self, host = "192.168.1.143", port = 8189):
        self.__CONTROLLER_IP   = host
        self.__CONTROLLER_PORT = port
        self.__SOCKET = None

    __mono_animations =  {
        "cd" : "meteor",
        "ce" : "breathing",
        "d1" : "wave",
        "d4" : "catch up",
        "d3" : "static",
        "cf" : "stack",
        "d2" : "flash",
        "d0" : "flow"
    }

    __chip_types = {
        "00":"SM16703"    ,
        "01":"TM1804"     ,
        "02":"UCS1903"    ,
        "03":"WS2811"     ,
        "04":"WS2801"     ,
        "05":"SK6812"     ,
        "06":"LPD6803"    ,
        "07":"LPD8806"    ,
        "08":"APA102"     ,
        "09":"APA105"     ,
        "0a":"DMX512"     ,
        "0b":"TM1914"     ,
        "0c":"TM1913"     ,
        "0d":"P9813"      ,
        "0e":"INK1003"    ,
        "0f":"P943S"      ,
        "10":"P9411"      ,
        "11":"P9413"      ,
        "12":"TX1812"     ,
        "13":"TX1813"     ,
        "14":"GS8206"     ,
        "15":"GS8208"     ,
        "16":"SK9822"     ,
        "17":"TM1814"     ,
        "18":"SK6812_RGBW",
        "19":"P9414"      ,
        "1a":"P9412"      
    }

    __color_orders = {
        "00":"RGB",
        "01":"RBG",
        "02":"GRB",
        "03":"GBR",
        "04":"BRG",
        "05":"BGR"
    }

    # return animations name if exist, else the number of the animation in decimal an hex
    __mono_animation_by_index = lambda self, x : SP108e.__mono_animations.get(x, str(int("0x"+x,16)) + " (x"+x.upper()+")")

    # return animations index by name 
    __mono_animation_by_name = lambda self, x : list(SP108e.__mono_animations.keys())[list(SP108e.__mono_animations.values()).index(x.lower())] 

    # convert decimal number to hex, filled with 0 
    __dec_to_even_hex = lambda self,decimal, output_bytes=1 : ("000000000000000000000000000000"+hex(decimal)[2:])[-(output_bytes*2):]    

    def __transmit_data(self,
        data,            # str,  the command and it's value(if it has a value)
        expect_response, # bool, set to true if you expect a response
        response_length  # str,  how long the response is
    ):
        for attemp in range(3) :
            try:
                if self.__SOCKET == None :
                    log.warning("Conecting to: " + self.__CONTROLLER_IP + ":" + str(self.__CONTROLLER_PORT))
                    self.__SOCKET = socket.create_connection((self.__CONTROLLER_IP, self.__CONTROLLER_PORT))

                self.__SOCKET.send(binascii.unhexlify(  data.replace(" ", "") ))

                if expect_response:
                    r = self.__SOCKET.recv(response_length)
                else:
                    r = None
                return r

            except socket.error as err:    
                log.error("Conection error to: " + self.__CONTROLLER_IP + ":" + str(self.__CONTROLLER_PORT) + " " + str(err))
                sleep(5)
                self.__SOCKET = None
        

    def __send_data(self, data, expect_response=False, response_length=0):
        response = self.__transmit_data(data, expect_response, response_length)
        return response

    def is_device_ready(self):
        return self.__transmit_data("38 000000 2f 83", True, 1)

    def get_name(self):
        result = self.__send_data("38 000000 77 83", True, 18);
        return result

    def get_device_raw_settings(self):
        result = self.__send_data("38 000000 10 83", True, 17);
        return binascii.hexlify(result).decode("ascii")

    def get_device_settings(self):   
        raw_settings = self.get_device_raw_settings()
        settings = {
            "turned_on": int(raw_settings[2:4], 16),
            "current_animation": self.__mono_animation_by_index(raw_settings[4:6]),
            "animation_speed": int(raw_settings[6:8], 16),
            "current_brightness": int(raw_settings[8:10], 16),
            "color_order": SP108e.__color_orders.get(raw_settings[10:12]),
            "leds_per_segment": int(raw_settings[12:16], 16),
            "segments": int(raw_settings[16:20], 16),
            "current_color": raw_settings[20:26].upper(),
            "chip_type": SP108e.__chip_types.get(raw_settings[26:28]),
            "recorded_patterns": int(raw_settings[28:30], 16),
            "white_channel_brightness": int(raw_settings[30:32], 16)
        }
        # log.error("STATUS: " + str(raw_settings))
        return settings

    def toggle_off_on(self):
        self.__send_data("38 000000 aa 83")

    def switch_on(self):
        sleep(2) # wait a little to get a valid status!
        if self.get_device_settings().get("turned_on") == 0: 
            self.toggle_off_on()
            for waiting in range(10): # wait until is notified that is on
                sleep(0.5)
                if self.get_device_settings().get("turned_on") == 1: break

    def switch_off(self):
        sleep(2) # wait a little to get a valid status!
        if self.get_device_settings().get("turned_on") == 1: 
            self.toggle_off_on()
            for waiting in range(10): # wait until is notified that is off
                sleep(0.5)
                if self.get_device_settings().get("turned_on") == 0: break

    def set_number_of_segments(self,segments=1):
        self.__send_data("38 " + self.dec_to_even_hex(segments, 2) + " 00 2e 83")

    def set_number_of_leds_per_segment(self,leds=50):
        self.__send_data("38 " + self.dec_to_even_hex(leds, 2) + " 00 2d 83")

    def change_color_hex(self,color):
        # color in hex format
        color = color.replace("#", "")
        self.__send_data("38 " + color + " 22 83")

    def change_color(self, R , G , B ):
        color = self.__dec_to_even_hex(R, 1) + self.__dec_to_even_hex(G, 1) + self.__dec_to_even_hex(B, 1)
        self.change_color_hex(color)

    def change_speed(self, speed):
        if not 0 <= speed <= 255:
            raise ValueError("speed must be between 0 and 255")
        self.__send_data("38 " + self.__dec_to_even_hex(speed) + " 0000 03 83")

    def change_brightness(self, brightness):
        if not 0 <= brightness <= 255:
            raise ValueError("brightness must be between 0 and 255")
        self.__send_data("38 " + self.__dec_to_even_hex(brightness) + " 0000 2a 83")

    def change_white_channel_brightness(self, brightness=255):
        if not 0 <= brightness <= 255:
            raise ValueError("brightness must be between 0 and 255")
        self.__send_data("38 " + self.__dec_to_even_hex(brightness) + " 0000 08 83")

    # set animation by name (you can add your favourites animations in the dictionary above...)
    def change_animation_by_name(self, name):
        self.__send_data("38 " + self.__mono_animation_by_name(name) + " 0000 2c 83")
        
    # 00  -> 179 (pattern animation) --- the app shows this value + 1    
    # 205 -> 212 (simple animations) -- in my case it's not working with these values
    def change_animation_by_index(self, index):
        # 0x00 -> 0xb2 (last animation 179) --- the app shows this value + 1
        self.__send_data("38 " + self.__dec_to_even_hex(index) + " 0000 2c 83") # specific animation

    # change custom animations (you can setup custom animations with the app "LED Shop")
    def change_custom_animation(self, index):
        self.__send_data("38 " + self.__dec_to_even_hex(index) + " 0000 02 83") # specific animation

    # in my case it's just another animation
    def enable_multicolor_animation(self):
        self.__send_data("38 000000 06 83") #auto mode
