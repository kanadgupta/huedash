# short test to get dash button working with the lights. basic light switch in this example
# https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.f9s8sg6eb

from scapy.all import *
from huecontroller import *
import datetime
import time
import csv
import os

def arp_display(pkt):

    if pkt[ARP].op == 1: #who-has (request)

      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe

        if pkt[ARP].hwsrc == 'a0:02:dc:d2:24:59': # ON
            print "On button pressed - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            logHandler("On button pressed")
            twoDashLightSwitch()

        elif pkt[ARP].hwsrc == 'f0:27:2d:ab:de:0e': # Gatorade
            print "Gatorade button pressed - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            logHandler("Gatorade button pressed")
            twoDashLightSwitch()

        elif pkt[ARP].hwsrc == '10:ae:60:c4:f6:bd': # Ice Breakers
            print "Ice Breakers button pressed - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            logHandler("Ice Breakers button pressed")
            strobeGroup()

    else:
      print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

def sniffer():
    print sniff(prn=arp_display, filter="arp", store=0)

def logHandler(inputString='default'):
    with open('log.csv', 'a') as csvlog:
        a = csv.writer(csvlog, delimiter=',')
        timeLog = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        logRow = [inputString, timeLog]
        a.writerow(logRow)


print "Beginning sniffing with PID " + str(os.getpid())
logHandler("Beginning sniffing with PID " + str(os.getpid()))
sniffer()
print "Fin"
logHandler("Sniff complete")
