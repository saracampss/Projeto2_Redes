from pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.revent import *


regras = []

# Cria regras p/ bloquear MAC addresses da conexão entre 10 hosts de forma sequente (contato de 1 e 2 bloqueados, contato de 2 e 3 bloqueados, etc)
for x in range(1, 9):
    regras.append(['00:00:00:00:00:0%s' % x, '00:00:00:00:00:0%s' % (x+1)])
regras.append(['00:00:00:00:00:09','00:00:00:00:00:10'])

class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)

    def _handle_ConnectionUp(self, event):
        for regra in regras:
            # bloqueia a conexão entre dispositivos com os endereços mac presentes nas regras
            block = of.ofp_match()
            block.dl_src = EthAddr(regra[0])
            block.dl_dst = EthAddr(regra[1])
            flow_mod = of.ofp_flow_mod()
            flow_mod.match = block
            event.connection.send(flow_mod)


def launch():
    core.registerNew(Firewall)