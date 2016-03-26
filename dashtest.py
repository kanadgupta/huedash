# short test to get dash button working with the lights. basic light switch in this example
# https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.f9s8sg6eb

from scapy.all import *
from beautifulhue.api import Bridge
import datetime
import time
import csv
import os

username = 'beautifulhuetest'
bridge = Bridge(device={'ip':'10.1.10.18'}, user={'name':username})

def arp_display(pkt):

    if pkt[ARP].op == 1: #who-has (request)

      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe

        if pkt[ARP].hwsrc == 'f0:27:2d:ed:68:24': # Gatorade
          print "Gatorade button pressed - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
          logHandler("Gatorade button pressed")
          oneDashLightSwitch()

    else:
      print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

def groupDashLightSwitch(num=0):
    resource = {'which':num}
    data = bridge.group.get(resource)
    isOn = data['resource']['action']['on']
    action = {
                 'which':num,
                 'data':{
                     'action':{
                         'on':not isOn
                     }
                 }
             }
    switchedTo = "off" if isOn else "on"
    bridge.group.update(action)
    print "Lights turned " + switchedTo + " - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    logHandler("Group " + str(num) + " turned " + switchedTo)

def oneDashLightSwitch(num=2):
    resource = {'which':num}
    data = bridge.light.get(resource)
    isOn = data['resource']['state']['on']
    state = {
                 'which':num,
                 'data':{
                     'state':{
                         'on':not isOn
                     }
                 }
             }
    switchedTo = "off" if isOn else "on"
    bridge.light.update(state)
    print "One light turned " + switchedTo + " - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    logHandler("Light " + str(num) + " turned " + switchedTo)

def twoDashLightSwitch(num1=1, num2=2):
    resource1 = {'which':num1}
    data1 = bridge.light.get(resource1)
    isOn1 = data1['resource']['state']['on']
    resource2 = {'which':num2}
    data2 = bridge.light.get(resource2)
    isOn2 = data2['resource']['state']['on']

    if (isOn1 or isOn2) == True:
        setLightsTo = False
    else:
        setLightsTo = True
    state1 = {
                 'which':num1,
                 'data':{
                     'state':{
                         'on': setLightsTo
                     }
                 }
             }
    state2 = {
                 'which':num2,
                 'data':{
                     'state':{
                         'on': setLightsTo
                     }
                 }
             }
    switchedTo = "on" if setLightsTo else "off"
    bridge.light.update(state1)
    bridge.light.update(state2)
    print "Two lights turned " + switchedTo + " - Timestamp: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    logHandler("Light " + str(num1) + " and " + str(num2) + " turned " + switchedTo)

def recursiveSniffer():
    print sniff(prn=arp_display, filter="arp", store=0)
    print "Starting again: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    logHandler("Recursive sniff")
    recursiveSniffer()

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
