'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
policies = csv.DictReader(open(policyFile, "rb"))



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        log.debug("Firewall sees connection %s", dpidToStr(event.dpid))
        
        for policy in policies:
            log.debug("Installing rule # %s", policy['id'])
            flowRule = of.ofp_flow_mod()
            #flowRule.actions.append(of.ofp_action_drop())
            flowRule.priority = 65535
            flowRule.match.dl_src = EthAddr(policy['mac_0'])
            flowRule.match.dl_dst = EthAddr(policy['mac_1'])
            event.connection.send(flowRule)
            flowRule.match.dl_dst = EthAddr(policy['mac_0'])
            flowRule.match.dl_src = EthAddr(policy['mac_1'])
            event.connection.send(flowRule)
        
            
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
