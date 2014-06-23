'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
        

    def port_forward(self, event, ports):
        for in_port in ports:
            for out_port in ports:
                if in_port<>out_port:
                    log.debug("Sending from port %s to port %s.", in_port, out_port)
                    flowRule = of.ofp_flow_mod()
                    flowRule.match.in_port = in_port
                    flowRule.actions.append(of.ofp_action_output(port=out_port))
                    event.connection.send(flowRule)
        

        
    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):
        
        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this 
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)
        """ Add your logic here """
        borderSwitches = ['00-00-00-00-00-01', '00-00-00-00-00-04']
        if dpid in borderSwitches:
            portPairs = [[2, 4], [1, 3]]
            for ports in portPairs:
                self.port_forward(event, ports)
        else:
            ports = [1, 2]
            self.port_forward(event, ports)

                
                
def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
