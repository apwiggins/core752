# CORE 7.5.2 / Vagrant VM - Multicast network testbed

## Multicast test environment
CORE 7.5.2 [1] is the last of the supported Tcl-based CORE versions.  It provides Quagga-based routing with protocols such as OSPF, RIP, BGP and OSPF-MDR.

Multicast isn't well supported out of the box in CORE, so this Vagrant setup adds support for PIM-DM using pimd-dense [2] and static multicast routing using smcroute [3].  A service wrapper script **pimdm.py** for PIM-DM and a service wrapper script **smcroute.py** for static multicast will be inserted at ~/.core/myservices.  This file location is the usual place for custom CORE services.

A couple of helper scripts **mcsend** and **mcrecv** are included to generate mutlicast traffic and receive multicast traffic using iperf [4].  These are typically run from the commandline inside a simulated data terminal instance.

## Example
Assuming a typical multicast scenario:  DT1 <--> Rtr1 <--> Rtr2 <--DT2

### Sender Example using multicast address 239.1.1.1:

	DT1$ mcsend 239.1.1.1 

Receiver Example using multicast address 239.1.1.1:

	DT2$ mcrecv 239.1.1.1

### Public service reminder
Everyone forgets at least once, but a multicast router requires 2 interfaces, so pimd-dense won't start if a router has only one interface.

# Installation
Vagrant is used to create the Virtualbox VM for CORE, install the custom multicast services in CORE and build CORE, ospf-mdr, pimd-dense, and smcroute from source.  The source tarballs will be downloaded during the installation.

## Assumptions:
 - you have some familiarity with VirtualBox and Vagrant.  
 - Virtualbox on Linux is installed (apt install virtualbox)
 - vagrant is installed (apt install vagrant)
 
 ## Install:
From a terminal:

     ./create_core_vm.sh

Installation takes about 5-10 minutes.  You will be prompted at one point to enter the vagrant password -- it's "vagrant".

 ## Post-install:
 The VirtualBox GUI will be available during the install process, but not usable until after the installation has been completed.  From the core752 directory on the HostMachine:

    vagrant halt  # stops the running core752 VM
    vagrant up    # starts the core752 VM (and GUI)
    vagrant ssh   # ssh into the running core752 VM
    
    ## if disaster has struck, then the next line cleans everything up
    vagrant destroy # you destroyed the core752 VM and need to re-run the install script

## Validate:
HostMachine> Stop the VM: 'vagrant halt'

HostMachine> Start the VM: 'vagrant up'

VM GUI > Confirm that CORE runs - from a command line run 'core-gui'

VM GUI > Confirm that CORE daemon runs - from a command line run 'sudo service core-daemon status'.  If not running, the 'sudo service core-daemon start'

## Multicast in CORE
The pimdm.py service in CORE automatically adds router interfaces to its configuration file pimdm.conf.
Right-clicking on a router icon and selecting the Services menu item brings up the set of available services including a Multicast section with both PIM-DM and SMCroute.

![alt text](https://github.com/apwiggins/core752/blob/main/Multicast_Services.png?raw=true)

![alt text](https://github.com/apwiggins/core752/blob/main/Multicast_in_CORE.png?raw=true)

 
References:
[1] https://github.com/coreemu/core

[2] https://github.com/troglobit/pimd-dense

[3] https://github.com/troglobit/smcroute

[4] https://iperf.fr/
