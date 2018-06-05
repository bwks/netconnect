# netconnect
[![Build Status](https://travis-ci.org/bobthebutcher/netconnect.svg?branch=master)](https://travis-ci.org/bobthebutcher/netconnect)
[![Coverage Status](https://coveralls.io/repos/github/bobthebutcher/netconnect/badge.svg?branch=master)](https://coveralls.io/github/bobthebutcher/netconnect?branch=master) 

### Overview
Connect to devices via ssh or telnet and run automated work flows.  
netconnect utilizes pexpect to control telnet or ssh sessions.  
netconnect has been designed with a focus on network device automation.  
It is usefull for controlling terminal sessions where an API is not available or not yet enabled.  

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
# Cisco device
from netconnect.cisco import CiscoDriver
dev = CiscoDriver(device='test-csr-01', username='test-user', password='password', enable_password='enable-pass')
dev.login()
commands = ['show version', 'show run']
results = dev.send_commands(commands)

# Juniper Device
from netconnect.juniper import JuniperDriver
dev = JuniperDriver(device='test-vmx-01', username='test-user', password='password')
dev.login()
dev.enable_api()

# Arista Device
from netconnect.arista import AristaDriver
dev = AristaDriver(device='test-eos-01', username='test-user', password='password')
dev.login()
dev.enable_api()
```

### Enable debugging
```python
from netconnect import helpers
helpers.DEBUG = True
```


### Context Manager
The context manager will take care of logging in and also closing the connection
automatically if there is a failure.
```python
# Cisco device
from netconnect.cisco import CiscoDriver
with CiscoDriver(device='test-csr-01', username='test-user', password='password', enable_password='enable-pass') as dev:
    commands = ['show version', 'show run']
    results = dev.send_commands(commands)
```