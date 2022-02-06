from time import sleep
from sp108e import SP108e


l=SP108e("192.168.1.143")

print("Switch on")
l.switch_on()
sleep(2)

print("Animación 2")
l.change_animation_by_index(2)
sleep(2)

print("Animación Static")
l.change_animation_by_name("Static")
sleep(2)

print("Color RED")
l.change_color(255,0,0)
sleep(2)

print("Brightness 3")
l.change_brightness(3)
sleep(2)

print("Custom animation 1")
l.change_custom_animation(1)
sleep(2)

print("Change speed 1")
l.change_speed(40)
sleep(5)

print("Change multicolo animation")
l.enable_multicolor_animation()
sleep(2)

print(l.get_device_settings())
sleep(2)
l.switch_off()

