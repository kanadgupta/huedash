# short test to get dash button working with the lights. basic light switch in this example
# https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.f9s8sg6eb

from scapy.all import *
from beautifulhue.api import Bridge
import datetime
import time


username = 'beautifulhuetest'
bridge = Bridge(device={'ip':'10.1.10.18'}, user={'name':username})

def arp_display(pkt):
    
    if pkt[ARP].op == 1: #who-has (request)

      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe

        if pkt[ARP].hwsrc == 'f0:27:2d:ed:68:24': # Gatorade
          print "Gatorade button pressed - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
          dashLightSwitch()

    else:
      print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

def dashLightSwitch():
    resource = {'which':0}
    data = bridge.group.get(resource)
    isOn = data['resource']['action']['on']
    action = {
                 'which':1,
                 'data':{
                     'action':{
                         'on':not isOn
                     }
                 }
             }
    switchedTo = "off" if isOn else "on"
    bridge.group.update(action)
    print "Lights turned " + switchedTo + " - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

print "Beginning sniffing"
print sniff(prn=arp_display, filter="arp", store=0)
print "Fin"

