from beautifulhue.api import Bridge
import datetime
import time
import csv

username = 'beautifulhuetest'
bridge = Bridge(device={'ip':'10.1.10.18'}, user={'name':username})

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

def strobe(num=2):
    resource = {'which':num}
    data = bridge.light.get(resource)
    isOn = data['resource']['state']['on']
    defaultState = data['resource']['state']
    noEffect = {
                 'which':num,
                 'data':{
                     'state':defaultState
                 }
            }
    bridge.light.update(noEffect)
    dimState = {
                 'which':num,
                 'data':{
                     'state':{
                         'on':False,
                     }
                 }
             }

    briState = {
                 'which':num,
                 'data':{
                     'state':{
                         # 'bri':defaultBrightness,
                         'on':True,
                         'sat':random.randint(0,254)
                     }
                 }
             }

    blueState = {
                 'which':num,
                 'data':{
                     'state':{
                         'on':True,
                         'bri': 254,
                         'hue': 46578,
                         'sat': 254,
                         'colormode': "hs"
                     }
                 }
             }

    pinkState = {
                 'which':num,
                 'data':{
                     'state':{
                         'on':True,
                         'bri': 254,
                         'hue': 55132,
                         'sat': 254,
                         'colormode': "hs"
                     }
                 }
             }

    colorStates = [pinkState, blueState]
    briFlag = True
    timeout = time.time() + 10   # 5 seconds from now
    colorIndex = 0

    while time.time() < timeout:
        # state = dimState if briFlag else briState
        bridge.light.update(colorStates[colorIndex])
        # briFlag = not briFlag
        time.sleep(.125)
        bridge.light.update(dimState)
        time.sleep(.125)
        colorIndex = (colorIndex + 1) % len(colorStates)
    print "Back to normal - " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    bridge.light.update(noEffect)
    print "It should have done it!!!!"

def strobeGroup(num=2):
    resource = {'which':num}
    data = bridge.group.get(resource)
    isOn = data['resource']['action']['on']
    defaultState = data['resource']['action']
    noEffect = {
                 'which':num,
                 'data':{
                     'action':defaultState
                 }
            }
    bridge.group.update(noEffect)
    dimState = {
                 'which':num,
                 'data':{
                     'action':{
                         'on':False,
                     }
                 }
             }

    briState = {
                 'which':num,
                 'data':{
                     'action':{
                         # 'bri':defaultBrightness,
                         'on':True,
                         'sat': 254
                     }
                 }
             }

    blueState = {
                 'which':num,
                 'data':{
                     'action':{
                         'on':True,
                         'bri': 254,
                         'hue': 46578,
                         'sat': 254,
                         'colormode': "hs"
                     }
                 }
             }

    pinkState = {
                 'which':num,
                 'data':{
                     'action':{
                         'on':True,
                         'bri': 254,
                         'hue': 55132,
                         'sat': 254,
                         'colormode': "hs"
                     }
                 }
             }

    colorStates = [pinkState, blueState]
    colorIndex = 0

    timeout = time.time() + 10   # 5 seconds from now
    while time.time() < timeout:
        # state = dimState if briFlag else briState
        bridge.group.update(colorStates[colorIndex])
        # briFlag = not briFlag
        time.sleep(.125)
        bridge.group.update(dimState)
        time.sleep(.125)
        colorIndex = (colorIndex + 1) % 2
    print "Back to normal - " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    bridge.group.update(noEffect)
    print "It should have done it!!!!"


def logHandler(inputString='default'):
    with open('log.csv', 'a') as csvlog:
        a = csv.writer(csvlog, delimiter=',')
        timeLog = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        logRow = [inputString, timeLog]
        a.writerow(logRow)
