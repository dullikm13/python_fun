# import module
import os
import time
import re
 
# Scan available Wifi networks - current approach stops and starts the wlansvc service to initiate a fresh scan. 
# Probably a less intrusive way to do this is, as the core functionality here is to provide protection against flaky connections :)
os.system('cmd /c "net stop wlansvc"')
os.system('cmd /c "net start wlansvc"')

# Initialize some variables here
running = True
current_network = ""
next_network = ""
consecutive_loss = 0
networks = os.popen('cmd /c "netsh wlan show networks"')

# Print a list of SSIDs for the user to pick from if they don't know the names off-hand
for network in networks:
    if("SSID" in network):
        print(network)

 
# Input Wifi names
# This program assumes you already have a working profile so there is no password prompt or anything like that
network1 = input('Name of network 1: ')
network2 = input('Name of network 2: ')

# If we're going to be switching from a bad network from a good one, we should identify which of the two provided we're currently using.
wlan_interface = os.popen('cmd /c "netsh wlan show interfaces"')
for line in wlan_interface:
    if(("SSID" in line) and ("BSSID" not in line)):
        current_network = line.replace("SSID","")
        current_network = line.replace(":","")
        current_network = line.replace(" ","")
        if(current_network == network1):
            current_network = network1
            next_network = network2

        if(current_network == network2):
            current_network = network2
            next_network = network1

# The main loop of the script
# Pings in sets of 20 and then checks the percent loss reported. If we see more than 10% loss for 3 consecutive polls, we switch the network we're on.
while(running):
    ping_results = os.popen('cmd /c "ping -n 20 8.8.8.8"')
    for result in ping_results:
        if("%" in result):
            pattern = re.compile(r'\d%')
            pattern_match = pattern.search(result).group()
            percent_loss = pattern_match.replace("%","")
            if(percent_loss > 10):
                consecutive_loss += 1
            else:
                consecutive_loss = 0

    if(consecutive_loss > 2):
        os.system(f'''cmd /c "netsh wlan connect name={next_network}"''')
        old_network = current_network
        current_network = next_network 
        next_network = old_network

 
