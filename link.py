
import sys
import queue

class Link:
    """Link class"""

    def __init__(self, e1, e2):
        """Create link queues and link delay"""
        self.e1 = e1  # addr of endpoint 1
        self.e2 = e2  # addr of endpoint 2
        self.q12 = queue.Queue()  # link queue of infinite size
        self.q21 = queue.Queue()  # link queue of infinite size
        self.delay = 3 # in unit of timeslots


    def send(self, packet, endpoint, currTimeslot):
        """Sends packet from the endpoint out on this link"""
        packet.timeslotToDeq = currTimeslot + self.delay
        if packet.node is None:
            packet.node = endpoint
            packet.entryTimeslot = str('-')
        packet.exitTimeslot = str(currTimeslot)
        packet.route.append((packet.node, packet.entryTimeslot, packet.exitTimeslot))
        if endpoint == self.e1:
            self.q12.put(packet)
        elif endpoint == self.e2:
            self.q21.put(packet)


    def recv(self, endpoint, currTimeslot):
        """Checks whether a packet is ready to be received by endpoint on this link.
           If packet is ready, returns the packet, else returns None"""
        if endpoint == self.e1:
            if not self.q21.empty():
                if currTimeslot >= self.q21.queue[0].timeslotToDeq:
                    packet = self.q21.get()
                    packet.node = endpoint
                    packet.entryTimeslot = str(currTimeslot)
                    return packet
                else:
                    return None
            else:
                return None
        elif endpoint == self.e2:
            if not self.q12.empty():
                if currTimeslot >= self.q12.queue[0].timeslotToDeq:
                    packet = self.q12.get()
                    packet.node = endpoint
                    packet.entryTimeslot = str(currTimeslot)
                    return packet
                else:
                    return None
            else:
                return None

