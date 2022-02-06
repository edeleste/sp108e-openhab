### Rules file to control SP108e
### Requires 4 virtual items: a dimmer, a switch, a color item and scene
from core.rules import rule
from core.triggers import when
from core.actions import ScriptExecution
from core.log import logging, LOG_PREFIX
from personal.sp108e import SP108e
from core.jsr223.scope import HSBType
from time import sleep

log=logging.getLogger("{}.luz_led_jardin.py".format(LOG_PREFIX))
led=SP108e("192.168.1.143")

@rule("Luz Jardin Led Switch", description="on/off change", tags=["lights"])
@when("Item LuzJardin_Led_Switch changed")
def LuzJardin_Led_Switch(event):
    itemled = ir.getItem("LuzJardin_Led_Switch")
    if str(itemled.getState()) == "ON":
        log.warning("LuzJardin_Led_Switch --> ENCENDER " )
        led.switch_on()
    elif str(itemled.getState()) == "OFF":
        log.warning("LuzJardin_Led_Switch --> APAGAR " )
        led.switch_off()


@rule("Luz Jardin Led Mode", description="on/off animation", tags=["lights"])
@when("Item LuzJardin_Led_Mode changed")
def LuzJardin_Led_Mode(event):
    itemled = ir.getItem("LuzJardin_Led_Mode")
    
    if str(ir.getItem("LuzJardin_Led_Switch").getState()) == "OFF": 
        events.postUpdate("LuzJardin_Led_Switch", "ON")
    
    if str(itemled.getState()) == "ON":
        log.warning("LuzJardin_Led_Mode --> ENCENDER " )
        scene = int(float(str(ir.getItem("LuzJardin_Led_Scene").getState())))
        led.change_animation_by_index(scene)
    elif str(itemled.getState()) == "OFF":
        log.warning("LuzJardin_Led_Mode --> APAGAR " )
        led.change_animation_by_name("Static")


@rule("Luz Jardin Led Dimmer", description="dimmer change", tags=["lights"])
@when("Item LuzJardin_Led_Dimmer changed")
def LuzJardin_Led_Dimmer(event):
    brightness = str(ir.getItem("LuzJardin_Led_Dimmer").getState())
    log.warning("LuzJardin_Led_Dimmer --> brightness: " + brightness )
    led.change_brightness(int(float((brightness))))


# led color changes. switch off the animation, and also swith on/off the lights if neccesary
@rule("Luz Jardin Led Color", description="color change", tags=["lights"])
@when("Item LuzJardin_Led_Color changed")
def LuzJardin_Led_Color(event):
    events.postUpdate("LuzJardin_Led_Mode", "OFF")

    itemled = str(ir.getItem("LuzJardin_Led_Color").getState())
    hsb=HSBType(itemled)
    log.warning("LuzJardin_Led_Color --> CHANGED " + str(hsb))
    led.change_color(hsb.getRed().intValue(),hsb.getGreen().intValue(),hsb.getBlue().intValue())
 
    if hsb.getBrightness().intValue() == 0 and str(ir.getItem("LuzJardin_Led_Switch").getState()) == "ON":  
        events.postUpdate("LuzJardin_Led_Switch", "OFF")
    elif hsb.getBrightness().intValue() != 0 and str(ir.getItem("LuzJardin_Led_Switch").getState()) == "OFF": 
        events.postUpdate("LuzJardin_Led_Switch", "ON")


@rule("Luz Jardin Led Scene", description="scene change", tags=["lights"])
@when("Item LuzJardin_Led_Scene changed")
def LuzJardin_Led_Scene(event):
    scene = int(float(str(ir.getItem("LuzJardin_Led_Scene").getState())))
    log.warning("LuzJardin_Led_Scene --> CHANGED " + str(scene))
    led.change_animation_by_index(scene)


@rule("Luz Jardin Led Speed", description="speed change", tags=["lights"])
@when("Item LuzJardin_Led_Speed changed")
def LuzJardin_Led_Speed(event):
    speed = int(float(str(ir.getItem("LuzJardin_Led_Speed").getState())))
    log.warning("LuzJardin_Led_Speed --> CHANGED " + str(speed))
    led.change_speed(int(speed*2.55)) # value is between 0 - 255 (not 0-99)

