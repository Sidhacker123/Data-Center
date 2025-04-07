
import sys
import queue
import hashlib
from switch import Switch
from link import Link

class MySwitch(Switch):

    def __init__(self, addr, delta):
        Switch.__init__(self, addr)  # initialize superclass

        self.K = 5  # threshold for ECN marking (in terms of number of packets)
        self.enqueuedPackets = set()
        """add your own class fields and initialization code here"""
        self.receivedPackets = set()


    def ecmp(self, packet):
        flowid = packet.srcAddr + packet.dstAddr + str(packet.srcPort) + str(packet.dstPort)
        outPort = int(hashlib.sha256(flowid.encode('utf-8')).hexdigest(), 16) % 3 + 4
        return outPort


    def handleRecvdPacket(self, port, packet, arrivalTime):
        """Handle the packet received on the specified port.
           arrivalTime is the timeslot in which the packet was received"""
       
    # Choose next-hop port (ECMP hashing)
    # DCTCP ECN marking: mark packet if queue length beyond threshold K
    
       #print(f"Packet from {packet.srcAddr} to {packet.dstAddr} placed in queue {outPort} with ECN {packet.ecnFlag}")

# Always enqueue the packet
        #self.queues[out_port].put(packet)

        if self.addr == "t1":
            if packet.dstAddr == "h1":
                outPort = 1
            elif packet.dstAddr == "h2":
                outPort = 2
            elif packet.dstAddr == "h3":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

        elif self.addr == "t2":
            if packet.dstAddr == "h4":
                outPort = 1
            elif packet.dstAddr == "h5":
                outPort = 2
            elif packet.dstAddr == "h6":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
                
        elif self.addr == "t3":
            if packet.dstAddr == "h7":
                outPort = 1
            elif packet.dstAddr == "h8":
                outPort = 2
            elif packet.dstAddr == "h9":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

        elif self.addr == "t4":
            if packet.dstAddr == "h10":
                outPort = 1
            elif packet.dstAddr == "h11":
                outPort = 2
            elif packet.dstAddr == "h12":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

        elif self.addr == "t5":
            if packet.dstAddr == "h13":
                outPort = 1
            elif packet.dstAddr == "h14":
                outPort = 2
            elif packet.dstAddr == "h15":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
            self.queues[outPort].put(packet)
            
                
        elif self.addr == "t6":
            if packet.dstAddr == "h16":
                outPort = 1
            elif packet.dstAddr == "h17":
                outPort = 2
            elif packet.dstAddr == "h18":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1   # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")                   
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            
                
        elif self.addr == "t7":
            if packet.dstAddr == "h19":
                outPort = 1
            elif packet.dstAddr == "h20":
                outPort = 2
            elif packet.dstAddr == "h21":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
                
        elif self.addr == "t8":
            if packet.dstAddr == "h22":
                outPort = 1
            elif packet.dstAddr == "h23":
                outPort = 2
            elif packet.dstAddr == "h24":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

        elif self.addr == "t9":
            if packet.dstAddr == "h25":
                outPort = 1
            elif packet.dstAddr == "h26":
                outPort = 2
            elif packet.dstAddr == "h27":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

        elif self.addr == "t10":
            if packet.dstAddr == "h28":
                outPort = 1
            elif packet.dstAddr == "h29":
                outPort = 2
            elif packet.dstAddr == "h30":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

                
        elif self.addr == "t11":
            if packet.dstAddr == "h31":
                outPort = 1
            elif packet.dstAddr == "h32":
                outPort = 2
            elif packet.dstAddr == "h33":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
                
        elif self.addr == "t12":
            if packet.dstAddr == "h34":
                outPort = 1
            elif packet.dstAddr == "h35":
                outPort = 2
            elif packet.dstAddr == "h36":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
                
        elif self.addr == "t13":
            if packet.dstAddr == "h37":
                outPort = 1
            elif packet.dstAddr == "h38":
                outPort = 2
            elif packet.dstAddr == "h39":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
                
        elif self.addr == "t14":
            if packet.dstAddr == "h40":
                outPort = 1
            elif packet.dstAddr == "h41":
                outPort = 2
            elif packet.dstAddr == "h42":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
                
        elif self.addr == "t15":
            if packet.dstAddr == "h43":
                outPort = 1
            elif packet.dstAddr == "h44":
                outPort = 2
            elif packet.dstAddr == "h45":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
            #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")

        elif self.addr == "t16":
            if packet.dstAddr == "h46":
                outPort = 1
            elif packet.dstAddr == "h47":
                outPort = 2
            elif packet.dstAddr == "h48":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            #self.queues[outPort].put(packet)
                
        elif self.addr == "t17":
            if packet.dstAddr == "h49":
                outPort = 1
            elif packet.dstAddr == "h50":
                outPort = 2
            elif packet.dstAddr == "h51":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            #self.queues[outPort].put(packet)
                
        elif self.addr == "t18":
            if packet.dstAddr == "h52":
                outPort = 1
            elif packet.dstAddr == "h53":
                outPort = 2
            elif packet.dstAddr == "h54":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
              #print(f"[ECN MARK] Congestion at {self.addr} port {outPort} ECN {packet.ecnFlag}")
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)

        elif self.addr == "a1" or self.addr == "a2" or self.addr == "a3":
            if packet.dstAddr == "h1" or packet.dstAddr == "h2" or packet.dstAddr == "h3":
                outPort = 1
            elif packet.dstAddr == "h4" or packet.dstAddr == "h5" or packet.dstAddr == "h6":
                outPort = 2
            elif packet.dstAddr == "h7" or packet.dstAddr == "h8" or packet.dstAddr == "h9":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
                
        elif self.addr == "a4" or self.addr == "a5" or self.addr == "a6":
            if packet.dstAddr == "h10" or packet.dstAddr == "h11" or packet.dstAddr == "h12":
                outPort = 1
            elif packet.dstAddr == "h13" or packet.dstAddr == "h14" or packet.dstAddr == "h15":
                outPort = 2
            elif packet.dstAddr == "h16" or packet.dstAddr == "h17" or packet.dstAddr == "h18":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
                
        elif self.addr == "a7" or self.addr == "a8" or self.addr == "a9":
            if packet.dstAddr == "h19" or packet.dstAddr == "h20" or packet.dstAddr == "h21":
                outPort = 1
            elif packet.dstAddr == "h22" or packet.dstAddr == "h23" or packet.dstAddr == "h24":
                outPort = 2
            elif packet.dstAddr == "h25" or packet.dstAddr == "h26" or packet.dstAddr == "h27":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
                
        elif self.addr == "a10" or self.addr == "a11" or self.addr == "a12":
            if packet.dstAddr == "h28" or packet.dstAddr == "h29" or packet.dstAddr == "h30":
                outPort = 1
            elif packet.dstAddr == "h31" or packet.dstAddr == "h32" or packet.dstAddr == "h33":
                outPort = 2
            elif packet.dstAddr == "h34" or packet.dstAddr == "h35" or packet.dstAddr == "h36":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
                
        elif self.addr == "a13" or self.addr == "a14" or self.addr == "a15":
            if packet.dstAddr == "h37" or packet.dstAddr == "h38" or packet.dstAddr == "h39":
                outPort = 1
            elif packet.dstAddr == "h40" or packet.dstAddr == "h41" or packet.dstAddr == "h42":
                outPort = 2
            elif packet.dstAddr == "h43" or packet.dstAddr == "h44" or packet.dstAddr == "h45":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
                
        elif self.addr == "a16" or self.addr == "a17" or self.addr == "a18":
            if packet.dstAddr == "h46" or packet.dstAddr == "h47" or packet.dstAddr == "h48":
                outPort = 1
            elif packet.dstAddr == "h49" or packet.dstAddr == "h50" or packet.dstAddr == "h51":
                outPort = 2
            elif packet.dstAddr == "h52" or packet.dstAddr == "h53" or packet.dstAddr == "h54":
                outPort = 3
            else:
                outPort = self.ecmp(packet)
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)

        elif self.addr[0] == 'c':
            if packet.dstAddr == "h1" or packet.dstAddr == "h2" or packet.dstAddr == "h3" or packet.dstAddr == "h4" or packet.dstAddr == "h5" or packet.dstAddr == "h6" or packet.dstAddr == "h7" or packet.dstAddr == "h8" or packet.dstAddr == "h9":
                outPort = 1
            elif packet.dstAddr == "h10" or packet.dstAddr == "h11" or packet.dstAddr == "h12" or packet.dstAddr == "h13" or packet.dstAddr == "h14" or packet.dstAddr == "h15" or packet.dstAddr == "h16" or packet.dstAddr == "h17" or packet.dstAddr == "h18":
                outPort = 2
            elif packet.dstAddr == "h19" or packet.dstAddr == "h20" or packet.dstAddr == "h21" or packet.dstAddr == "h22" or packet.dstAddr == "h23" or packet.dstAddr == "h24" or packet.dstAddr == "h25" or packet.dstAddr == "h26" or packet.dstAddr == "h27":
                outPort = 3
            elif packet.dstAddr == "h28" or packet.dstAddr == "h29" or packet.dstAddr == "h30" or packet.dstAddr == "h31" or packet.dstAddr == "h32" or packet.dstAddr == "h33" or packet.dstAddr == "h34" or packet.dstAddr == "h35" or packet.dstAddr == "h36":
                outPort = 4
            elif packet.dstAddr == "h37" or packet.dstAddr == "h38" or packet.dstAddr == "h39" or packet.dstAddr == "h40" or packet.dstAddr == "h41" or packet.dstAddr == "h42" or packet.dstAddr == "h43" or packet.dstAddr == "h44" or packet.dstAddr == "h45":
                outPort = 5
            elif packet.dstAddr == "h46" or packet.dstAddr == "h47" or packet.dstAddr == "h48" or packet.dstAddr == "h49" or packet.dstAddr == "h50" or packet.dstAddr == "h51" or packet.dstAddr == "h52" or packet.dstAddr == "h53" or packet.dstAddr == "h54":
                outPort = 6
            if self.queues[outPort].qsize() > self.K:  
              packet.ecnFlag = 1                    # Mark ECN if queue occupancy > K
             # Enqueue the packet (no drop on congestion)
            self.queues[outPort].put(packet)
