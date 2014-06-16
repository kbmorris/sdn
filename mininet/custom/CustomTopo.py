'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.link import TCLink

class CustomTopo(Topo):
    "Simple Data Center Topology"
        
    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1={}, linkopts2={}, linkopts3={}, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        self.linkopts = ["", linkopts1, linkopts2, linkopts3]
        self.fanout = fanout
        self.createNode(0, 1)

    levels = ['c', 'a', 'e', 'h']
    linkopts = []
    nodeNumbers = [0,0,0,0]
    
    def createNode(self, level, number):
        """ Creates a node and then recursively
        calls to create the child nodes unless
        it is creating the host level nodes """
        # determine if we are creating hosts yet
        if level == len(self.levels) - 1:
            node = self.addHost(self.levels[level]+str(number))
        else:
            node = self.addSwitch(self.levels[level]+str(number))
            self.createChildren(level+1, node)
        return node

    def createChildren(self, level, parent):
        for item in range(self.fanout):
            number = self.nodeNumbers[level] = self.nodeNumbers[level] + 1
            child = self.createNode(level, number)
	    self.addLink( child, parent, bw=self.linkopts[level]['bw'], delay=self.linkopts[level]['delay'])
        return

def simpleTest():
    "Create and test a simple network"
    outputString = ''

    "Set up link parameters"
    print "a. Setting link parameters"
    "--- core to aggregation switches"
    linkopts1 = {'bw':50, 'delay':'5ms'}
    "--- aggregation to edge switches"
    linkopts2 = {'bw':30, 'delay':'10ms'}
    "--- edge switches to hosts"
    linkopts3 = {'bw':10, 'delay':'15ms'}

    "Creating network and run simple performance test"
    print "b. Creating Custom Topology"
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=3)

    print "c. Firing up Mininet"
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')
    h27 = net.get('h27')

    print "d. Starting Test"
    # Start pings
    outputString = h1.cmd('ping', '-c6', h27.IP())

    print "e. Stopping Mininet"
    net.stop()
    print outputString.strip()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()
        

        
                    
topos = { 'custom': ( lambda: CustomTopo() ) }
