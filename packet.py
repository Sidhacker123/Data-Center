# The code is subject to Purdue University copyright policies.
# Do not share, distribute, or post online.

class Packet:
    """Packet class"""

    def __init__(self, srcAddr, dstAddr, srcPort, dstPort, seqNum, ackNum, ackFlag, ecnFlag):
        """Initialize packet header fields"""
        self.srcAddr = srcAddr  # address of the source host
        self.dstAddr = dstAddr  # address of the destination host
        self.srcPort = srcPort  # source port value
        self.dstPort = dstPort  # destination port value
        self.seqNum = seqNum    # packet sequence number
        self.ackNum = ackNum    # acknowledgement number
        self.ackFlag = ackFlag  # set to 0 or 1 (1 = ACK packet)
        self.ecnFlag = ecnFlag  # set to 0 or 1

        """Simulator fileds. DO NOT TOUCH"""
        self.timeslotToDeq = None
        self.node = None
        self.entryTimeslot = None
        self.exitTimeslot = None
        self.route = []
        
