from pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.revent import *
import pox.lib.packet as pkt


regras = []
log = core.getLogger()

# Cria regras p/ bloquear MAC addresses da conexao entre 10 hosts de forma sequente (contato de 1 e 2 bloqueados, contato de 2 e 3 bloqueados, etc)
for x in range(1, 9):
    regras.append(['00:00:00:00:00:0%s' % x, '00:00:00:00:00:0%s' % (x+1)])
regras.append(['00:00:00:00:00:09','00:00:00:00:00:10'])

class Firewall(EventMixin):
    packetSrc = None
    packetDst = None

    def __init__(self):
        self.listenTo(core.openflow)


    def _handle_ConnectionUp(self, event):
        for regra in regras:
            # bloqueia a conexao entre dispositivos com os endereços mac presentes nas regras
            block = of.ofp_match()
            block.dl_src = EthAddr(regra[0])
            block.dl_dst = EthAddr(regra[1])
            flow_mod = of.ofp_flow_mod()
            flow_mod.match = block
            event.connection.send(flow_mod)

    def _handle_packet_in(self, event):
        self.packetSrc = event.parsed.src
        self.packetDst = event.parsed.dst
        for switch in core.openflow.connections:
            switch.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

    def _handle_flow_stats(self, event):
            limitFlow = ["00:00:00:00:00:03"]
            port = 80

            bytes = 0
            for b in event.stats:
                if b.match.tp_dst == port or b.match.tp_src == port:
                    bytes += b.byte_count
            if (bytes > 590 and str(self.packetDst) in limitFlow):
                # bloqueia endereco mac de quem enviou pacote acima do limite
                if (self.packetSrc != None and self.packetDst != None):
                    mac_1 = EthAddr(self.packetSrc)
                    mac_2 = EthAddr(self.packetDst)
                block = of.ofp_match()
                block.dl_src = EthAddr(mac_1)
                block.dl_dst = EthAddr(mac_2)
                flow_mod = of.ofp_flow_mod()
                flow_mod.match = block
                event.connection.send(flow_mod)


    def _start_stats_request(self):
        core.openflow.addListenerByName("FlowStatsReceived", self._handle_flow_stats) # escuta por estatisticas do fluxo
        core.openflow.addListenerByName("PacketIn", self._handle_packet_in)
        # requerimentos de flow stats de cada switch


def launch():
    firewall = Firewall()
    core.registerNew(Firewall)
    firewall._start_stats_request()