# netconnect
[![Build Status](https://travis-ci.org/bobthebutcher/netconnect.svg?branch=master)](https://travis-ci.org/bobthebutcher/netconnect)
[![Coverage Status](https://coveralls.io/repos/github/bobthebutcher/netconnect/badge.svg?branch=master)](https://coveralls.io/github/bobthebutcher/netconnect?branch=master) 
Connect to devices via telnet and ssh 
Currently under development not ready for production 

### Overview
netconnect utilizes pexpect to control telnet or ssh sessions. 
netconnect has been designed with a focus on network device automation. 
It is usefull for controlling terminal sessions where an API is not available 
or not yet enabled.

netconnect has a concept of drivers which are used to seperate out the differing terminal intricacies.
There is currently drivers for the following device models: 
 - cisco
 - juniper
 - arista
 - unix (bash)

A driver can be written for any terminal type that accepts telnet or SSH control.


### Install
``` python
pip install https://github.com/bobthebutcher/netconnect/archive/master.zip
```

### Usage
```python
from netconnect.cisco.cisco_driver import CiscoDriver
dev = CiscoDriver(device='test-dev', username='test-user', password='password')
dev.login(enable_password='enable-pass')
commands = ['show version', 'show run']
results = dev.send_commands(commands)
```

### Enable debugging
```python
from netconnect import helpers
helpers.DEBUG = True
```