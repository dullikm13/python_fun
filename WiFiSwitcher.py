# import module
import os
import time
import re
 
# scan available Wifi networks
os.system('cmd /c "net stop wlansvc"')
os.system('cmd /c "net start wlansvc"')

running = True
current_network = ""
networks = os.popen('cmd /c "netsh wlan show networks"')

for network in networks:
    if("SSID" in network):
        print(network)

 
# input Wifi name
#name_of_router = input('Enter Name/SSID of the Wifi Network you wish to connect to: ')
network1 = input('Name of network 1: ')
network2 = input('Name of network 2: ')

wlan_interface = os.popen('cmd /c "netsh wlan show interfaces"')
for line in wlan_interface:
    if(("SSID" in line) and ("BSSID" not in line)):
        current_network = line.replace("SSID","")
        current_network = line.replace(":","")
        current_network = line.replace(" ","")
        print("current_network=" + current_network)

 
while(running):
    ping_results = os.popen('cmd /c "ping -n 20 8.8.8.8"')
    for result in ping_results:
        if("%" in result):
            pattern = re.compile(r'\d%')
            pattern_match = pattern.search(result).group()
            percent_loss = pattern_match.replace("%","")
            print(percent_loss)






# connect to the given wifi network
#os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
 
