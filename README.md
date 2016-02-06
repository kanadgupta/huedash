# HueDash

This Python enables you to use an Amazon Dash button to control Philips Hue lightbulbs in a variety of ways.

Documentation
-------------

###Requirements

- Python 2.6+

###Philips Hue Setup
This code uses [beautifulhue](https://github.com/allanbunch/beautifulhue), a Python library for the Philips Hue Lighting System API. 

###Scapy Installation

Click [here](http://www.secdev.org/projects/scapy/) to download a ZIP of the latest version of Scapy (used for packet sniffing). Navigate to the directory that you downloaded the ZIP to:

```bash
$ unzip scapy-2.*.zip
$ cd scapy-2.*
$ sudo python setup.py install
```
This part can be difficult to get working correctly, so you can read more about installation for your system [here.](http://www.secdev.org/projects/scapy/doc/installation.html)

###Amazon Dash Button Setup
This used Ted Benson's post on hacking an Amazon Dash button. You can read about how to set that up [here.](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.21lisrb4k)
