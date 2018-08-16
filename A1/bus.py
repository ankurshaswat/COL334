                                                                                            
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController

class LinearTopo(Topo):
    "Linear topology of n hosts and n switches"
    def build(self, n=2):
        prevSwitch = None
        for h in range(n):
            # print(h)
            host = self.addHost('h%s' % (h+1))
            switch = self.addSwitch('s%s' % (h+1))
            self.addLink(host,switch)
            # print(switch,prevSwitch)
            if(h>0):
                self.addLink(prevSwitch,switch)
            prevSwitch = switch

class RingTopo(Topo):
    "Ring topology of n hosts and n switches"
    def build(self, n=2):
        prevSwitch = None
        firstSwitch = None
        for h in range(n):
            # print(h)
            host = self.addHost('h%s' % (h+1))
            switch = self.addSwitch('s%s' % (h+1))
            self.addLink(host,switch)
            # print(switch,prevSwitch)
            if(h>0):
                self.addLink(prevSwitch,switch)
            else:
                firstSwitch = switch
            prevSwitch = switch
        # print(firstSwitch,prevSwitch)
        self.addLink(prevSwitch,firstSwitch)

class MeshTopo(Topo):
    "Mesh Topology with n hosts"
    def build(self,n=2):
        switches = []
        for h in range(n):
            host = self.addHost('h%s' % (h+1))
            switch = self.addSwitch('s%s' % (h+1))
            self.addLink(host,switch)
            switches.append(switch)
        for i in range(len(switches)):
            for j in range(i+1,len(switches)):
                # if(switches[i] != s2):
                self.addLink(switches[i],switches[j])
                    # self.addLink(s2,s1)


class StarTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

def simpleTest():
    "Create and test a simple network"
    topo = LinearTopo(n=10)
    # topo = RingTopo(n=10)
    # topo = StarTopo(n=10)
    # topo = MeshTopo(n=3)
    net = Mininet(topo=topo,controller = OVSController)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
