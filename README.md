# sp108e-openhab
Phyton libary to control SP108E WIFI led controller and some stuff to integrate with OPENHAB. The SP108E is a Wi-Fi controller box to control addressable LED strips.

![image](https://user-images.githubusercontent.com/34882353/152693123-7adcb8e7-7586-4c1e-a20d-66ab14f78a05.png)

There's an app called "LED shop" to control the LED strips for android and IOS. I wanted to integrate this led strips with my OpenHab installation at home, so based in some information and examples I found, I made this library that has the most useful funtions.

The SP108E must be configured in STA mode in the same WIFI network you'll use and you have your OpenHab installation.

Before integrating this with OpenHab I recommend you to test the Phyton Script standalone (test.py).

To use inside OpenHab, you have to configure Python Rules in OpenHab (sorry for that, but it's not well documented!! https://community.openhab.org/t/starting-with-python-in-oh3/113995), and then copy the content of folder "openhab-files" at your openhab configuration folder (in my case in /srv/openhab-conf)

Finally, I have included a rules file for openhab,... just to give an example. If you want to use this example you must configure some virtual items:
![image](https://user-images.githubusercontent.com/34882353/152693084-e2e1ae29-d22b-49cc-8ae0-697c690172c8.png)

![image](https://user-images.githubusercontent.com/34882353/152693211-5dadac7a-72b6-425b-823e-d9ddc3753f9c.png)

