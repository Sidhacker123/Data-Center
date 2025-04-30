import sys
import queue
import hashlib
from switch import Switch
from link import Link

class MySwitch(Switch):

    def __init__(self, addr, delta):
        Switch.__init__(self, addr)   # initialize superclass
        
        self.K = 5                    # threshold for ECN marking (in terms of number of packets)
        self.delta = delta            # delta for flowlet load balancing (in units of timeslots)

        self.packetCnt = [0] * 3      # count of packets transmitted on each of the three
                                      # upstream ports

        self.timeLastPktArrived = {}  # key: flowid
                                      # value: arrival time of the last seen packet from the flow

        self.flowOutPort = {}         # key: flowid
                                      # value: current upstream output port for the flow

        """add your own class fields and initialization code here"""


    def setECNFlag(self, packet, outPort):
        if self.queues[outPort].qsize() > self.K:
            packet.ecnFlag = 1


    def flowletLB(self, packet, arrivalTime):
        """return the output upstream port number
           to which the packet should be sent out on"""
        flowid = packet.srcAddr + packet.dstAddr + str(packet.srcPort) + str(packet.dstPort)
        # TODO: implement flowlet load balancing
        if flowid not in self.timeLastPktArrived:
        # First packet of a new flow -> start a new flowlet
        # Select the upstream port with the fewest packets sent (tie-break by smaller port number)
          offset = 3 if self.addr[0] in ['t', 'a'] else 0
          minCount = float('inf')
          selectedPort = None
          for i in range(3):
             portNum = offset + 1 + i
             if self.packetCnt[i] < minCount:
                 minCount = self.packetCnt[i]
                 selectedPort = portNum
             elif self.packetCnt[i] == minCount and portNum < selectedPort:
                 selectedPort = portNum
        # Assign this flowlet to the chosen port and update state
          self.flowOutPort[flowid] = selectedPort
          self.timeLastPktArrived[flowid] = arrivalTime
          self.packetCnt[selectedPort - offset - 1] += 1
          return selectedPort
    # Flow has been seen before; check inter-arrival time
        lastTime = self.timeLastPktArrived[flowid]
        interArrival = arrivalTime - lastTime
        if interArrival > self.delta:
        # Gap > delta => start a new flowlet on least-used port
         offset = 3 if self.addr[0] in ['t', 'a'] else 0
         minCount = float('inf')
         selectedPort = None
         for i in range(3):
            portNum = offset + 1 + i
            if self.packetCnt[i] < minCount:
                minCount = self.packetCnt[i]
                selectedPort = portNum
            elif self.packetCnt[i] == minCount and portNum < selectedPort:
                selectedPort = portNum
        # Update flowOutPort for the new flowlet
         self.flowOutPort[flowid] = selectedPort
        else:
        # Within delta => same flowlet, use previously assigned port
          selectedPort = self.flowOutPort[flowid]
    # Update last seen time and packet count for the selected port
        self.timeLastPktArrived[flowid] = arrivalTime
        offset = 3 if self.addr[0] in ['t', 'a'] else 0
        self.packetCnt[selectedPort - offset - 1] += 1
        return selectedPort


    def handleRecvdPacket(self, port, packet, arrivalTime):
        """Handle the packet received on the specified port.
           arrivalTime is the timeslot in which the packet was received"""
        if self.addr == "t1":
            if packet.dstAddr == "h1":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h2":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h3":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)

        elif self.addr == "t2":
            if packet.dstAddr == "h4":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h5":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h6":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t3":
            if packet.dstAddr == "h7":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h8":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h9":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t4":
            if packet.dstAddr == "h10":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h11":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h12":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t5":
            if packet.dstAddr == "h13":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h14":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h15":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t6":
            if packet.dstAddr == "h16":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h17":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h18":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t7":
            if packet.dstAddr == "h19":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h20":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h21":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t8":
            if packet.dstAddr == "h22":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h23":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h24":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t9":
            if packet.dstAddr == "h25":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h26":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h27":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t10":
            if packet.dstAddr == "h28":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h29":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h30":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t11":
            if packet.dstAddr == "h31":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h32":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h33":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t12":
            if packet.dstAddr == "h34":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h35":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h36":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t13":
            if packet.dstAddr == "h37":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h38":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h39":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t14":
            if packet.dstAddr == "h40":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h41":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h42":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t15":
            if packet.dstAddr == "h43":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h44":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h45":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t16":
            if packet.dstAddr == "h46":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h47":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h48":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t17":
            if packet.dstAddr == "h49":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h50":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h51":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "t18":
            if packet.dstAddr == "h52":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h53":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h54":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)

        elif self.addr == "a1" or self.addr == "a2" or self.addr == "a3":
            if packet.dstAddr == "h1" or packet.dstAddr == "h2" or packet.dstAddr == "h3":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h4" or packet.dstAddr == "h5" or packet.dstAddr == "h6":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h7" or packet.dstAddr == "h8" or packet.dstAddr == "h9":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "a4" or self.addr == "a5" or self.addr == "a6":
            if packet.dstAddr == "h10" or packet.dstAddr == "h11" or packet.dstAddr == "h12":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h13" or packet.dstAddr == "h14" or packet.dstAddr == "h15":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h16" or packet.dstAddr == "h17" or packet.dstAddr == "h18":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "a7" or self.addr == "a8" or self.addr == "a9":
            if packet.dstAddr == "h19" or packet.dstAddr == "h20" or packet.dstAddr == "h21":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h22" or packet.dstAddr == "h23" or packet.dstAddr == "h24":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h25" or packet.dstAddr == "h26" or packet.dstAddr == "h27":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "a10" or self.addr == "a11" or self.addr == "a12":
            if packet.dstAddr == "h28" or packet.dstAddr == "h29" or packet.dstAddr == "h30":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h31" or packet.dstAddr == "h32" or packet.dstAddr == "h33":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h34" or packet.dstAddr == "h35" or packet.dstAddr == "h36":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "a13" or self.addr == "a14" or self.addr == "a15":
            if packet.dstAddr == "h37" or packet.dstAddr == "h38" or packet.dstAddr == "h39":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h40" or packet.dstAddr == "h41" or packet.dstAddr == "h42":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h43" or packet.dstAddr == "h44" or packet.dstAddr == "h45":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)
                
        elif self.addr == "a16" or self.addr == "a17" or self.addr == "a18":
            if packet.dstAddr == "h46" or packet.dstAddr == "h47" or packet.dstAddr == "h48":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h49" or packet.dstAddr == "h50" or packet.dstAddr == "h51":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h52" or packet.dstAddr == "h53" or packet.dstAddr == "h54":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            else:
                outPort = self.flowletLB(packet, arrivalTime)
                self.setECNFlag(packet, outPort)
                self.queues[outPort].put(packet)

        elif self.addr[0] == 'c':
            if packet.dstAddr == "h1" or packet.dstAddr == "h2" or packet.dstAddr == "h3" or packet.dstAddr == "h4" or packet.dstAddr == "h5" or packet.dstAddr == "h6" or packet.dstAddr == "h7" or packet.dstAddr == "h8" or packet.dstAddr == "h9":
                self.setECNFlag(packet, 1)
                self.queues[1].put(packet)
            elif packet.dstAddr == "h10" or packet.dstAddr == "h11" or packet.dstAddr == "h12" or packet.dstAddr == "h13" or packet.dstAddr == "h14" or packet.dstAddr == "h15" or packet.dstAddr == "h16" or packet.dstAddr == "h17" or packet.dstAddr == "h18":
                self.setECNFlag(packet, 2)
                self.queues[2].put(packet)
            elif packet.dstAddr == "h19" or packet.dstAddr == "h20" or packet.dstAddr == "h21" or packet.dstAddr == "h22" or packet.dstAddr == "h23" or packet.dstAddr == "h24" or packet.dstAddr == "h25" or packet.dstAddr == "h26" or packet.dstAddr == "h27":
                self.setECNFlag(packet, 3)
                self.queues[3].put(packet)
            elif packet.dstAddr == "h28" or packet.dstAddr == "h29" or packet.dstAddr == "h30" or packet.dstAddr == "h31" or packet.dstAddr == "h32" or packet.dstAddr == "h33" or packet.dstAddr == "h34" or packet.dstAddr == "h35" or packet.dstAddr == "h36":
                self.setECNFlag(packet, 4)
                self.queues[4].put(packet)
            elif packet.dstAddr == "h37" or packet.dstAddr == "h38" or packet.dstAddr == "h39" or packet.dstAddr == "h40" or packet.dstAddr == "h41" or packet.dstAddr == "h42" or packet.dstAddr == "h43" or packet.dstAddr == "h44" or packet.dstAddr == "h45":
                self.setECNFlag(packet, 5)
                self.queues[5].put(packet)
            elif packet.dstAddr == "h46" or packet.dstAddr == "h47" or packet.dstAddr == "h48" or packet.dstAddr == "h49" or packet.dstAddr == "h50" or packet.dstAddr == "h51" or packet.dstAddr == "h52" or packet.dstAddr == "h53" or packet.dstAddr == "h54":
                self.setECNFlag(packet, 6)
                self.queues[6].put(packet)

