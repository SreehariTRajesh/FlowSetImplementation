from bloom_filter.bloom import generate_hash, generate_hash_fromXOR, compute_flowXOR
# Define Macros for the hash functions

OLD_FLOW = 0
NEW_FLOW = 1

class CountingTableEntry:

    def __init__(self, flowXOR: int, flowCount: int, pktCount: int):
        self.flowXOR: int = flowXOR
        self.flowCount: int = flowCount
        self.pktCount: int = pktCount
    
class CountingTable:

    def __init__(self, table_size: int, num_hashes: int):
        self.ctable: list[CountingTableEntry] = []
        for i in range(table_size):
            self.ctable.append(CountingTableEntry(0, 0, 0))
        self.table_size: int = table_size 
        self.num_hashes: int = num_hashes
        
    def insert_flow(self, flow: tuple[int, int, int, int, int], flow_type: int):

        if flow_type == OLD_FLOW:
            for i in range(0, self.num_hashes):
                id = generate_hash(i, flow) % self.table_size
                self.ctable[id].pktCount += 1  
        
        elif flow_type == NEW_FLOW:
            for i in range(0, self.num_hashes):
                id = generate_hash(i, flow) % self.table_size
                self.ctable[id].pktCount += 1
                self.ctable[id].flowCount += 1
                self.ctable[id].flowXOR ^= compute_flowXOR(flow)

    def single_decode(self):
        flowset: set[CountingTableEntry] = {}
        for entry in self.ctable:
            if entry.flowCount == 1:
                flowset.add(entry.flowXOR)
                count: int = entry.flowCount
                for j in range(1, self.num_hashes):
                    l: int = generate_hash_fromXOR(j, entry.flowXOR) % self.table_size
                    self.ctable[l].flowXOR = self.ctable[l].flowXOR ^ entry.flowXOR
                    self.ctable[l].flowCount -= 1
                    self.ctable[l].pktCount -= count
        return flowset
    
    def construct_linear_equations(self, flowset: set[CountingTableEntry]):
        t: int = 0
        numFlows: int = len(flowset)
        M = [ [0] * numFlows ] * self.table_size
        b = [0] * self.table_size

        for flow in flowset:
            for j in range(0, self.num_hashes):
                l = generate_hash_fromXOR(hashID=j, flowXOR=flow)
                M[l][t] =1
            t += 1

        for j in range(0, len(self.ctable)):
            b[j] = self.ctable[j].pktCount

    def counter_decode(self):

        return 0







        