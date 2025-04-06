# The code is subject to Purdue University copyright policies.
# Do not share, distribute, or post online.

import sys
import queue
from packet import Packet

class Host:
    """Host class"""

    def __init__(self, addr):
        """Inititalize parameters"""
        self.addr = addr
        self.link = None
        self.sFlows = {}    # a dictionary storing state for active flows sourced at this host
                            # key: 3-tuple (dst addr, src port, dst port)
                            # value: [flow size (in number of packets), number of packets sent]

        self.rFlows = {}    # a dictionary storing state for active flows destined to this host
                            # key: 3-tuple (src addr, src port, dst port)
                            # value: [id, flow size (in number of packets), list of packet seq num received, flow start time, time last pkt sent, num of reordering]

        self.rrSched = []   # stores the list of active flows sourced at this host
                            # for round-robin scheduling

        self.rrPointer = 0  # points to the flow to be scheduled according to round-robin

        self.cwnd = {}      # a dictionary storing the congestion window for active flows
                            # key: 3-tuple (dst addr, src port, dst port)
                            # value: congestion window

        self.alpha = {}     # a dictionary storing the alpha value for active flows
                            # key: 3-tuple (dst addr, src port, dst port)
                            # value: alpha

        self.numPktSentInCurrWin = {}   # key: 3-tuple (dst addr, src port, dst port)
                                        # value: number of packets sent in current window

        self.packetLogFile = None
        self.cwndLogFile = None


    def logPacket(self, packet):
        self.packetLogFile.write("src: " + packet.srcAddr + ", dst: " + packet.dstAddr)
        self.packetLogFile.write(", sport: " + str(packet.srcPort) + ", dport: " + str(packet.dstPort))
        self.packetLogFile.write(", seqNum: " + str(packet.seqNum) + ", ackNum: " + str(packet.ackNum))
        self.packetLogFile.write(", ackFlag: " + str(packet.ackFlag) + ", ecnFlag: " + str(packet.ecnFlag))
        self.packetLogFile.write(", route: ")
        self.packetLogFile.write('->'.join('(%s,%s,%s)' % x for x in packet.route))
        self.packetLogFile.write("\n\n")
        self.packetLogFile.flush()


    def runHost(self, currTimeslot, flowLogFile, ackQueues, totalPktSent, totalPktRecvd):
        """Main loop of host"""
        for dst, sport, dport in self.cwnd: # log the cwnd value for each active flow in each timeslot
            self.cwndLogFile.write("time: " + str(currTimeslot) + ", ")
            self.cwndLogFile.write("flow (5-tuple): " + "(" + self.addr + "," + dst + "," + str(sport) + "," + str(dport) + ",dctcp" + "), ")
            self.cwndLogFile.write("cwnd: " + str(self.cwnd[(dst,sport,dport)]))
            self.cwndLogFile.write("\n")

        self.sendPacket(currTimeslot, totalPktSent)  # in each timeslot, send a
                                                     # packet (if any) out on the link

        self.handleRecvdAcks(ackQueues[self.addr])  # handle received ACKs

        if self.link:  # in each timeslot, receive a
                       # packet (if any) from the link
                       # and handle it
            packet = self.link.recv(self.addr, currTimeslot)
            if packet:
                if packet.dstAddr != self.addr:
                    sys.stdout.write("Routing Error: Packet with dst " + packet.dstAddr + " was received at " + self.addr + "\n")
                    return
                packet.route.append((packet.node, packet.entryTimeslot, '-'))
                self.logPacket(packet)

                # reordering count
                for i in range(0, packet.seqNum):
                    if i not in self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][2]:
                        self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][5] += 1
                        break

                if packet.seqNum == self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][1] - 1: #last packet
                    timeLastPktSent = int(packet.route[0][2])
                    self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][4] = timeLastPktSent

                if packet.ackFlag == 0 and packet.seqNum not in self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][2]:
                    self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][2].append(packet.seqNum)
                    # log finished flow
                    Id = self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][0]
                    flowsize = self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][1]
                    starttime = self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][3]
                    timeLastPktSent = self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][4]
                    reordering = self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][5]
                    if len(self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][2]) == flowsize:
                        if max(self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][2]) == flowsize - 1:
                            if min(self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)][2]) == 0:
                                flowLogFile.write(str(Id) + ", ")
                                flowLogFile.write("src: " + packet.srcAddr + ", dst: " + packet.dstAddr)
                                flowLogFile.write(", sport: " + str(packet.srcPort) + ", dport: " + str(packet.dstPort))
                                flowLogFile.write(", flowsize: " + str(flowsize))
                                flowLogFile.write(", starttime: " + str(starttime))
                                flowLogFile.write(", finishtime: " + str(currTimeslot))
                                fct = currTimeslot - starttime
                                flowLogFile.write(", fct: " + str(fct))
                                recvTput = (flowsize * 1500 * 8)/(fct * 120.0)
                                flowLogFile.write(", recvtput: " + str(round(recvTput,2)) + " Gbps")
                                assert(timeLastPktSent >= starttime)
                                timeToSendFlow = timeLastPktSent - starttime + 1
                                sendTput = (flowsize * 1500 * 8)/(timeToSendFlow * 120.0)
                                flowLogFile.write(", sendtput: " + str(round(sendTput,2)) + " Gbps")
                                flowLogFile.write(", reordering: " + str(reordering))
                                flowLogFile.write("\n\n")
                                flowLogFile.flush()
                                # delete finished flow
                                del self.rFlows[(packet.srcAddr,packet.srcPort,packet.dstPort)]

                totalPktRecvd[0] += 1
                self.handleRecvdPacket(packet, ackQueues)



