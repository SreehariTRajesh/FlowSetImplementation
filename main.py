from bloom_filter.bloom import BloomFilter
from bloom_filter.counting_table import CountingTable, CountingTableEntry
from network_flow.packet_generator import PacketGenerator
from time import sleep
from random import randint
import TableIt

FILTER_SIZE = 16
COUNTING_TABLE_SIZE = 12
FILTER_HASH_COUNT = 2
TABLE_HASH_COUNT = 1
OLD_FLOW = 0
NEW_FLOW = 1

def print_bloom_filter(bloom_filter: list[int]):
    TableIt.printTable([
        bloom_filter
    ])

def print_counting_table(counting_table: list[CountingTableEntry]):
    flowXOR = ['FlowXOR'] + [x.flowXOR for x in counting_table]
    flowCount = ['FlowCount'] + [x.flowCount for x in counting_table]
    packetCount = ['PacketCount'] + [x.pktCount for x in counting_table]
    TableIt.printTable([
        flowXOR,
        flowCount,
        packetCount
    ])

def main():
    bloomFilter = BloomFilter(filter_size=FILTER_SIZE, hash_count= FILTER_HASH_COUNT)
    countingTable = CountingTable(table_size=COUNTING_TABLE_SIZE, num_hashes=TABLE_HASH_COUNT)
    packetGenerator = PacketGenerator(filePath='static_files/FlowData.csv')

    while True:    
        packetFlow = packetGenerator.generate_packet()

        bloomFilter.insert(packetFlow)
    
        if bloomFilter.check(packetFlow) == False:
            countingTable.insert_flow(packetFlow, flow_type=OLD_FLOW)
        else:
            countingTable.insert_flow(packetFlow, flow_type=NEW_FLOW)
    
        print_bloom_filter(bloom_filter=bloomFilter.bloom_filter)
        print_counting_table(counting_table=countingTable.ctable)

        timeInterval: int = randint(1,4)
        sleep(timeInterval)

if __name__ == '__main__':
    main()