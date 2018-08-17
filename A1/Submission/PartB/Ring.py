from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.node import RemoteController, OVSSwitch

BANDWIDTH = 10
DELAY = '5ms'
LOSS = 2
MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 100
# DELAY = '5ms'
# LOSS = 2
# MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 10
# DELAY = '15ms'
# LOSS = 2
# MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 10
# DELAY = '5ms'
# LOSS = 5
# MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 10
# DELAY = '5ms'
# LOSS = 2
# MAX_QUEUE_SIZE = 700

class RingTopo(Topo):
    "Ring topology of n hosts and n switches"
    def build(self, n=2):
        prevSwitch = None
        firstSwitch = None
        for h in range(n):
            host = self.addHost('h%s' % (h+1))
            switch = self.addSwitch('s%s' % (h+1))
            self.addLink(host,switch,bw=BANDWIDTH, delay=DELAY, loss=LOSS, max_queue_size=MAX_QUEUE_SIZE)
            if(h>0):
                self.addLink(prevSwitch,switch,bw=BANDWIDTH, delay=DELAY, loss=LOSS, max_queue_size=MAX_QUEUE_SIZE)
            else:
                firstSwitch = switch
            prevSwitch = switch
        self.addLink(prevSwitch,firstSwitch,bw=BANDWIDTH, delay=DELAY, loss=LOSS, max_queue_size=MAX_QUEUE_SIZE)
    

def simpleTest():
    "Create and test a simple network"
    topo = RingTopo(n=10)
    net = Mininet(topo=topo,controller = RemoteController, host=CPULimitedHost, link=TCLink )
    net.start()

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    
    switches = net.switches

    for i in range(len(switches)):
        switches[i].cmd('ovs-vsctl set bridge s%s stp-enable=true' % (i+1))

    net.waitConnected()
    print("Testing network connectivity")

    net.pingAll()
   
    hosts = net.hosts

    print("Pinging h6 from h1")
    print(hosts[0].cmd('ping -c1 %s' % hosts[5].IP()))  
    
    print("Running iperf between h1 and h6")  
    print(net.iperf([hosts[0],hosts[5]]))

    print("Running iperf between h1 and h10")  
    print(net.iperf([hosts[0],hosts[9]]))

    print("Running ifconfig on h1")
    print(hosts[0].cmd('ifconfig'))   

    print("Running route on h1")
    print(hosts[0].cmd('route'))

    print("Running traceroute from h1 to h10")
    print(hosts[0].cmd('traceroute %s' % hosts[9].IP()))    

    # print("Running nslookup from h1")
    # print(hosts[0].cmd('nslookup www.google.com'))

    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
