
class Packet:
    def __init__(self, src_ip, dest_ip, gen_time_slot):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.retrans_count = 0
        self.gen_time_slot = gen_time_slot


