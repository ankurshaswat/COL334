from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.node import RemoteController, OVSSwitch

# BANDWIDTH = 10
# DELAY = '5ms'
# LOSS = 2
# MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 100
# DELAY = '5ms'
# LOSS = 2
# MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 10
# DELAY = '8ms'
# LOSS = 2
# MAX_QUEUE_SIZE = 1000

# BANDWIDTH = 10
# DELAY = '5ms'
# LOSS = 5
# MAX_QUEUE_SIZE = 1000

BANDWIDTH = 10
DELAY = '5ms'
LOSS = 2
MAX_QUEUE_SIZE = 700

class StarTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host,switch,bw=BANDWIDTH, delay=DELAY, loss=LOSS, max_queue_size=MAX_QUEUE_SIZE)

def simpleTest():
    "Create and test a simple network"
    topo = StarTopo(n=10)
    net = Mininet(topo=topo,controller = RemoteController, host=CPULimitedHost, link=TCLink )
    net.start()

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    
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
