# The code is subject to Purdue University copyright policies.
# Do not share, distribute, or post online.

import sys
import queue
from link import Link

class Switch():
    """Switch class"""

    def __init__(self, addr):
        """Initialize parameters"""
        self.addr = addr  # address of switch
        self.links = {}   # links indexed by port, i.e., {port:link, ......, port:link}
        self.queues = {}  # output queues (of type queue.Queue) per port
                          # indexed by port, i.e., {port:queue, ......, port:queue}
                          # each output queue is a FIFO queue of infinite size


    def runSwitch(self, currTimeslot):
        """Main loop of switch"""
        for port in self.links.keys():  # in each timeslot, send a packet
                                        # at the head of each output port
                                        # queue out on the link
            try:
                packet = self.queues[port].get_nowait()
                self.links[port].send(packet, self.addr, currTimeslot)
            except queue.Empty:
                pass

        for port in self.links.keys():  # in each timeslot, receive a
                                        # packet (if any) on each input
                                        # port and handle it
            packet = self.links[port].recv(self.addr, currTimeslot)
            if packet:
                self.handleRecvdPacket(port, packet, currTimeslot)

