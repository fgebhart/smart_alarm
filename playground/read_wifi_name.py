import os

wifi_name = os.popen("iw dev wlan0 link | grep SSID | awk '{print $2}'").read()

print(wifi_name)
