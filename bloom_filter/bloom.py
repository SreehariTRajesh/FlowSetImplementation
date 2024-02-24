import hashlib

def compute_flowXOR(flow: tuple[int, int, int, int, int]):
    source_ip, source_port, dest_ip, dest_port, protocol = flow
    return source_ip ^ source_port ^ dest_ip ^ dest_port ^ protocol


def generate_hash(hashID: int, flow: tuple[int, int, int, int ,int]):
    flowXOR: int = compute_flowXOR(flow)
    return int(hashlib.sha256(str(flowXOR ^ hashID).encode()).hexdigest(), 16) 

def generate_hash_fromXOR(hashID: int, flowXOR: int):
    return int(hashlib.sha256(str(flowXOR ^ hashID).encode()).hexdigest(), 16)


class BloomFilter:

    def __init__(self, filter_size: int, hash_count: int):
        self.bloom_filter = [0] * filter_size
        self.filter_size = filter_size
        self.hash_count = hash_count
        self.element_count = 0
    
    def insert(self, flow: tuple[int, int, int, int, int]):
        for i in range(0, self.hash_count):
            id = generate_hash(i, flow) % self.filter_size
            self.bloom_filter[id] = 1
        self.element_count += 1

    def check(self, flow: tuple[int, int, int, int, int]):
        for i in range(0, self.hash_count):
            id = generate_hash(i, flow) % self.filter_size
            if self.bloom_filter[id] == 0:
                return False
        return True

    def compute_false_positive_rate(self):
        return (1 - ( 1 - 1 / self.filter_size ) ** (self.hash_count * self.element_count)) ** self.hash_count
