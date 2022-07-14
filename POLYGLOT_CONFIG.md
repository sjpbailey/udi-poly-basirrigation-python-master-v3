# Universal Devices BAS Irrigation Network

## BASpi-SYS6U6R DIY BacNet Control Device by Contemporary Controls

### The purpose of this Nodeserver is for custom control of BASpi modules on a network

* The purpose of this Nodeserver is for Irrigation and home automation using BASpi modules on an IP network.
* Python 3.7.7

* Supported Nodes
  * Inputs
  * Outputs
  * Multiple Instances
  
#### Configuration

##### Defaults

* Default Short Poll:  Every 2 minutes
* Default Long Poll: Every 4 minutes (heartbeat)

###### User Provided

* Enter the nuber of controllers you desire 0-6 Key = nodes Value = 1-6
* Enter your IP address for up to six (6) BASpi-SYS6U6R controller,
* Config: key = irrip_* (* = 0-5) Value = Enter Your BASpi IP Address, Example: key irrip_0  value 192.168.1.50
* Save and restart the NodeServer
