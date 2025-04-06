
import sys
import math
import queue
from host import Host
from packet import Packet

class MyHost(Host):

    def __init__(self, addr):
        Host.__init__(self, addr)  # initialize superclass

        self.numAckRecvdInCurrWin = {}     # key: 3-tuple (dst addr, src port, dst port)
                                           # value: number of acks received in current window

        self.numECNAckRecvdInCurrWin = {}  # key: 3-tuple (dst addr, src port, dst port)
                                           # value: number of acks received in current window with ECN flag set
        self.receivedPackets = set()
        self.enqueuedPackets = set()
        self.generatedAcks = set()


        """add your own class fields and initialization code here"""


    def sendPacket(self, currTimeslot, totalPktSent):
        """Send one packet out on the link"""

        """round robin flow scheduling"""
        if len(self.rrSched) > 0:
            dst = "0"
            sport = 0
            dport = 0

            i = 0
            schedFlow = 0
            while i < len(self.rrSched):
                i += 1
                dst, sport, dport = self.rrSched[self.rrPointer]
                if self.numPktSentInCurrWin[(dst,sport,dport)] < self.cwnd[(dst,sport,dport)]:
                    schedFlow = 1
                    if self.numPktSentInCurrWin[(dst,sport,dport)] == 0:
                        self.numAckRecvdInCurrWin[(dst,sport,dport)] = 0
                        self.numECNAckRecvdInCurrWin[(dst,sport,dport)] = 0
                    break
                else:
                    self.rrPointer = (self.rrPointer + 1) % len(self.rrSched)

            if schedFlow == 1:
                """send a packet from the scheduled flow"""
                seqNum = self.sFlows[(dst,sport,dport)][1]
                packet = Packet(self.addr, dst, sport, dport, seqNum, 0, 0, 0)
                self.link.send(packet, self.addr, currTimeslot)
                self.sFlows[(dst,sport,dport)][1] = seqNum + 1

                totalPktSent[0] += 1
                self.numPktSentInCurrWin[(dst,sport,dport)] += 1

                """delete scheduled flow if all packets from the flow have been sent out,
                   assuming no packet loss"""
                if self.sFlows[(dst,sport,dport)][0] == self.sFlows[(dst,sport,dport)][1]:
                    del self.sFlows[(dst,sport,dport)]
                    del self.cwnd[(dst,sport,dport)]
                    del self.alpha[(dst,sport,dport)]
                    del self.numPktSentInCurrWin[(dst,sport,dport)]
                    self.rrSched.remove((dst,sport,dport))
                    if self.rrPointer >= len(self.rrSched):
                        self.rrPointer = 0


    def handleRecvdPacket(self, packet, ackQueues):
        """Handle the packet received on the link
           and send an ack packet for the received packet
           by enqueuing the ack packet into the right ackQueue"""
        # Only handle data packets (ackFlag == 0); ACK packets are handled elsewhere
        #if packet.ecnFlag == 1:
            #print(f" packet from {packet.srcAddr} has ECN = {packet.ecnFlag} at receiver")
        # Create an ACK for the received data packet
        ack = Packet(
            srcAddr= packet.dstAddr,
            dstAddr= packet.srcAddr,
            srcPort= packet.dstPort,
            dstPort= packet.srcPort,
            seqNum=0,                   # Always 0 for ACK
            ackNum=packet.seqNum,       # Individual ACKing
            ackFlag=1,
            ecnFlag=1 if packet.ecnFlag == 1 else 0
        )
        

        # Enqueue ACK into the original sender's ACK queue for delivery
        ackQueues[packet.srcAddr].put(ack)
        if packet.ecnFlag == 1:
         print(f"[RECV] packet from {packet.srcAddr} to {self.addr}, seqNum: {packet.seqNum}, ECN: {packet.ecnFlag}")
        '''if ack.ecnFlag == 1:
         print(f"[ACK ] sending ACK to {packet.srcAddr}, ackNum: {packet.seqNum}, ECN: {ack.ecnFlag}")'''



        #pass


    def handleRecvdAcks(self, ackQueue):
        """Handle the received acks"""
        while not ackQueue.empty():
            ackPacket = ackQueue.get()
            assert(ackPacket.ackFlag == 1)
            # log recvd ACKs
            self.logPacket(ackPacket)
            dst = ackPacket.srcAddr
            sport = ackPacket.dstPort
            dport = ackPacket.srcPort
            if (dst,sport,dport) in self.rrSched: # the flow exists
                self.numPktSentInCurrWin[(dst,sport,dport)] -= 1
                assert(self.numPktSentInCurrWin[(dst,sport,dport)] >= 0)
                self.numAckRecvdInCurrWin[(dst,sport,dport)] += 1
                if (ackPacket.ecnFlag == 1):
                    self.numECNAckRecvdInCurrWin[(dst,sport,dport)] += 1
                if self.numAckRecvdInCurrWin[(dst,sport,dport)] == self.cwnd[(dst,sport,dport)]:
                    # received all the acks for curr window of sent data
                    # TODO: update the cwnd value below according to DCTCP algorithm
                    # In your TODO part
                    # All packets from the current window are now acknowledged
                    total_acks = self.numAckRecvdInCurrWin[(dst, sport, dport)]
                    ecn_marks = self.numECNAckRecvdInCurrWin[(dst, sport, dport)]
                    F = ecn_marks / total_acks                         # fraction of marked packets (ACKs) in this window
        # Update DCTCP alpha (running estimate of fraction marked)&#8203;:contentReference[oaicite:10]{index=10}
                    self.alpha[(dst, sport, dport)] = (1 - 0.75) * self.alpha[(dst, sport, dport)] + 0.75 * F
                    if ecn_marks > 0:
        # Congestion encountered: reduce cwnd based on alpha
                        new_cwnd = math.ceil(self.cwnd[(dst, sport, dport)] * (1 - self.alpha[(dst, sport, dport)] / 2))
                        self.cwnd[(dst, sport, dport)] = max(new_cwnd, 1)   # cwnd floor is 1 packet&#8203;:contentReference[oaicite:11]{index=11}
                    else:
        # No congestion signals: increase cwnd by 1 (additive increase)
                        self.cwnd[(dst, sport, dport)] += 1
        # Reset counters for the next window
                    self.numAckRecvdInCurrWin[(dst, sport, dport)] = 0
                    self.numECNAckRecvdInCurrWin[(dst, sport, dport)] = 0
                    #print(f"[ACK RECV] ACK from {flow.srcAddr}, ECN: {flow.ecnFlag}, alpha: {self.alpha}, cwnd: {self.cwnd}")
                    #print(f"[ACK RECV] ACK from {dst}, ECN: {ackPacket.ecnFlag}, alpha: {self.alpha[(dst, sport, dport)]}, cwnd: {self.cwnd[(dst, sport, dport)]}")


                    self.generatedAcks.clear()
                    self.enqueuedPackets.clear()
        




