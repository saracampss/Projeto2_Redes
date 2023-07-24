import pdb
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel

class TopoProjeto2( Topo ):
    hostList = []
    switchList = []

    # Por padrao utiliza 2 hosts e 1 switch
    def __init__( self, x = 2, y = 1, hostList = hostList, switchList = switchList, **opts ):
        Topo.__init__( self, **opts )

        # criando switches da rede
        for s in range(y):
            switch = self.addSwitch('s%s' % (s+1))
            switchList.append(switch)

        # conecta os switches - starbus toplogy
        for i in range(1, len(switchList)):
            self.addLink(switchList[i], switchList[0])

        # criando hosts da rede
        lastSwitch = 1  # define qual sera o switch a se conectar com o host
        for h in range(x):
            if h < 9:
                host = self.addHost('h0%s' % (h+1), ip = '192.168.1.%s/24' % (h+1), mac = '00:00:00:00:00:0%s' % (h+1))
            else:
                host = self.addHost('h%s' % (h+1), ip = '192.168.1.%s/24' % (h+1), mac = '00:00:00:00:00:%s' % (h+1))
            hostList.append(host)
            if (y > 1):
                self.addLink(host, switchList[lastSwitch])
            else:   # caso em que so ha um switch
                self.addLink(host, switchList[0])
            # configura IP do host
            lastSwitch += 1
            if lastSwitch >= (y): # se tiver chegado ao ultimo switch adicionado, retorna p/ o comeco 
                lastSwitch = 1
        
    def getHostList(self):
        print(self.hostList)
        return self.hostList
    
    def getSwitchList(self):
        print(self.switchList)
        return self.switchList

    # Testa a rede
def Test():
    # Escolher 10 hosts e 4 switches p/ o teste
    x = int(input("Quantidade de hosts:"))
    y = int(input("Quantidade de switches:"))
    topo = TopoProjeto2(x,y)
    net = Mininet(topo, controller=RemoteController)
    net.start()

    dumpNodeConnections(net.hosts)

    print("rodando CLI")
    CLI(net)
    net.stop()

if __name__=='__main__':
    setLogLevel('info')
    Test()