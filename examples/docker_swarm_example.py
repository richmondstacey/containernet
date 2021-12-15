#!/usr/bin/python
"""Run the topology over Docker Swarm."""

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d5 = net.addDockerSwarm('d5', ip='10.0.0.251', dimage="ubuntu:trusty", numRep=2)
#d5 = net.addDocker('d5', ip='10.0.0.251', dimage="ubuntu:trusty")
d6 = net.addDocker('d6', ip='10.0.0.252', dimage="ubuntu:trusty")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(d5, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, d6)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d5, d6])
info('*** Run http server on Swarm\n')
d5.cmd('sudo python3 -m http.server 80 &')
d6.cmd('apt install wget')
info('*** Wget server\n')
info(d6.cmd('wget -O - 10.0.0.251'))
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
