# The code is subject to Purdue University copyright policies.
# Do not share, distribute, or post online.

import sys
import os
sys.path.append(os.getcwd())
import glob
from collections import defaultdict
import json
import queue
from myHost import MyHost
from link import Link
from mySwitch import MySwitch

class Network:
    """Network class maintains all hosts, switches, and links"""

    def __init__(self, netJsonFilepath, delta):
        """Create a new network from the parameters in the file at netJsonFilepath"""

        # parse configuration details
        netJsonFile = open(netJsonFilepath, 'r')
        netJson = json.load(netJsonFile)

        # parse and create switches, hosts, and links
        self.switches = self.parseswitches(netJson["switches"], delta)
        self.hosts = self.parseHosts(netJson["hosts"])
        self.links = self.parseLinks(netJson["links"])

        netJsonFile.close()


    def parseswitches(self, switchParams, delta):
        """Parse switches from switchParams dict"""
        switches = {}
        for addr in switchParams:
            switches[addr] = MySwitch(addr, delta)
        return switches


    def parseHosts(self, hostParams):
        """Parse hosts from hostParams dict"""
        hosts = {}
        for addr in hostParams:
            hosts[addr] = MyHost(addr)
        return hosts


    def parseLinks(self, linkParams):
        """Parse links from linkParams dict"""
        links = {}
        for addr1, addr2, p1, p2 in linkParams:
            link = Link(addr1, addr2)
            links[(addr1,addr2)] = (p1, p2, link)
        return links


    def addLinks(self):
        """Add links to hosts and switches"""
        for addr1, addr2 in self.links:
            p1, p2, link = self.links[(addr1, addr2)]
            if addr1 in self.hosts:
                self.hosts[addr1].link = link
                self.hosts[addr1].packetLogFile = open("logs/"+addr1+"-recvd-packets.txt", "a")
                self.hosts[addr1].cwndLogFile = open("logs/"+addr1+"-cwnd.txt", "a")
            if addr2 in self.hosts:
                self.hosts[addr2].link = link
                self.hosts[addr2].packetLogFile = open("logs/"+addr2+"-recvd-packets.txt", "a")
                self.hosts[addr1].cwndLogFile = open("logs/"+addr2+"-cwnd.txt", "a")
            if addr1 in self.switches:
                self.switches[addr1].links[p1] = link
                self.switches[addr1].queues[p1] = queue.Queue()
            if addr2 in self.switches:
                self.switches[addr2].links[p2] = link
                self.switches[addr2].queues[p2] = queue.Queue()


    def run(self, flowtrace, endTimeslot, flowLogFile):
        """Run the network"""
        self.addLinks()

        ackQueues = {}
        for h in self.hosts:
            ackQueues[h] = queue.Queue()

        currTimeslot = 0

        totalPktSent = [0]
        totalPktRecvd = [0]

        f = open(flowtrace, "r")
        line = f.readline()
        line = f.readline()
        tokens = line.split(',')
        if len(tokens) != 7:
            sys.stdout.write("Wrong flowtrace file format.\n")
            return
        Id = int(tokens[0])
        src = tokens[1]
        dst = tokens[2]
        sport = int(tokens[3])
        dport = int(tokens[4])
        flowsize = int(tokens[5])
        startTimeslot = int(tokens[6].strip())

        eof = False

        while currTimeslot < endTimeslot:
            if currTimeslot % 100 == 0:
                sys.stdout.write("current timeslot: " + str(currTimeslot) + " total packets sent: " + str(totalPktSent[0]) + " total packets received: " + str(totalPktRecvd[0]) + "\n")

            while not eof and currTimeslot == startTimeslot:
                self.hosts[src].sFlows[(dst,sport,dport)] = [flowsize, 0]
                self.hosts[dst].rFlows[(src,sport,dport)] = [Id, flowsize, [], startTimeslot, 0, 0]
                self.hosts[src].rrSched.append((dst,sport,dport))
                self.hosts[src].cwnd[(dst,sport,dport)] = 1
                self.hosts[src].alpha[(dst,sport,dport)] = 0
                self.hosts[src].numPktSentInCurrWin[(dst,sport,dport)] = 0
                line = f.readline()
                if not line:
                    eof = True
                    break
                tokens = line.split(',')
                if len(tokens) != 7:
                    sys.stdout.write("Wrong flowtrace file format.\n")
                    return
                Id = int(tokens[0])
                src = tokens[1]
                dst = tokens[2]
                sport = int(tokens[3])
                dport = int(tokens[4])
                flowsize = int(tokens[5])
                startTimeslot = int(tokens[6].strip())

            for h in self.hosts:
                self.hosts[h].runHost(currTimeslot, flowLogFile, ackQueues, totalPktSent, totalPktRecvd)
            for s in self.switches:
                self.switches[s].runSwitch(currTimeslot)

            currTimeslot += 1

            # break if finished reading entire flowtrace file and all flows have finished
            count = 0
            for h in self.hosts:
                if len(self.hosts[h].rFlows) == 0:
                    count += 1
            if eof and count == len(self.hosts):
                sys.stdout.write("current timeslot: " + str(currTimeslot) + " total packets sent: " + str(totalPktSent[0]) + " total packets received: " + str(totalPktRecvd[0]) + "\n")
                sys.stdout.write("Ending simulation as all flows have finished.\n")
                break

        if currTimeslot >= endTimeslot:
            sys.stdout.write("current timeslot: " + str(currTimeslot) + " total packets sent: " + str(totalPktSent[0]) + " total packets received: " + str(totalPktRecvd[0]) + "\n")
            sys.stdout.write("Ending simulation as end timeslot reached.\n")

        for h in self.hosts:
            self.hosts[h].packetLogFile.close()
            self.hosts[h].cwndLogFile.close()

        f.close()
        return


def main():
    """Main function parses command line arguments and runs the network"""
    if len(sys.argv) < 5:
        sys.stdout.write("Usage: python3 network.py [networkSimulationFile.json] [flowtrace.dat] [endtimeslot] [delta]\n")
        return
    netCfgFilepath = sys.argv[1]
    flowtrace = sys.argv[2]
    endTimeslot = int(sys.argv[3])
    delta = int(sys.argv[4])
    net = Network(netCfgFilepath, delta)
    files = glob.glob('logs/*')
    for f in files:
        os.remove(f)
    flowLogFile = open("logs/recvd-flows.txt", "a")
    net.run(flowtrace, endTimeslot, flowLogFile)
    flowLogFile.close()
    return


if __name__ == "__main__":
    main()

