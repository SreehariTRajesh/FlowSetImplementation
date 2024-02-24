import random
import os
import csv

FLOW_DATA_FILE = 'FlowData.csv'

def convert_ip_to_int(ip: str) -> int:
    num_list = [int(x) for x in ip.split(".")]
    j: int = 1
    converted_ip: int = 0
    for num in reversed(num_list):
        converted_ip += num * j
        j *= 256
    return converted_ip

class PacketGenerator:

    def __init__(self, filePath):
        packetFile = open(file=filePath)
        self.packetIDs: list[tuple[int, int, int, int, int]] = []
        for line in csv.reader(packetFile):
            src_ip = convert_ip_to_int(line[0])
            src_port = int(line[1])
            dest_ip = convert_ip_to_int(line[2])
            dest_port = int(line[3])
            protocol = int(line[4])
            self.packetIDs.append((src_ip, src_port, dest_ip, dest_port, protocol))
        self.packetArrayLen = len(self.packetIDs)
        self.prevPacket = (-1, -1, -1, -1, -1)

    def generate_packet(self):
        ret: tuple[int, int, int, int, int]
        while True:
            ret = random.choice(self.packetIDs)
            if ret != self.prevPacket:
                self.prevPacket = ret
                return ret
        return (-1, -1, -1, -1, -1)
    
            
