from random import *
from collections import deque
import Packet


class Node:
    def __init__(self, identity_ip, buffer_size, gen_prob, total_nodes_in_system, randomization_ceiling, max_retrans_count_until_drop):
        self.identity_ip = identity_ip
        self.buffer_size = buffer_size
        self.buffer = deque([], buffer_size)  # initialize all the elements with -1
        self.gen_prob = gen_prob
        self.total_nodes_in_system = total_nodes_in_system
        self.max_retrans_count_until_drop = max_retrans_count_until_drop
        self.randomization_ceiling = randomization_ceiling
        self.back_off_time = 0
        self.num_of_collisions = 0
        self.lost_packet_count = 0  # due to buffer overflows
        self.num_of_gen_packets = 0
        self.num_of_retrans_packets = 0
        self.success_trans_packet_count = 0
        self.num_of_retrans_attempts = 0
        self.facedCollision = False
        self.num_of_delayed_slots = 0
        self.consecutive_collisions = 0

    def gen_packet_with_prob(self, generation_timeslot):
        allowable_upper_bound = (self.gen_prob * 100)
        rand_int = randint(1, 100)
        if rand_int <= allowable_upper_bound:
            # packet generated
            self.num_of_gen_packets += 1

            identity = 'Node '
            identity += str(randint(1, self.total_nodes_in_system))
            new_packet = Packet.Packet(self.identity_ip, identity, generation_timeslot)
            # insert in buffer if not full
            if len(self.buffer) == self.buffer.maxlen:
                # buffer size is full, so the packet is dropped, increase dropped packet count
                self.lost_packet_count += 1
            else:
                self.buffer.append(new_packet)

    def book_keeping_after_suc_trans(self, trans_timeslot):
        # packet transmitted
        print("successful transmission")
        self.success_trans_packet_count += 1
        # turn off faced collision flag
        if self.facedCollision:
            self.facedCollision = False
            self.num_of_retrans_packets += 1
        # remove from buffer
        transmitted_packet = self.buffer.popleft()
        # update packet retransmission attempts
        self.num_of_retrans_attempts += transmitted_packet.retrans_count
        # update delay variable
        self.num_of_delayed_slots += trans_timeslot - transmitted_packet.gen_time_slot
        # update consecutive collisions variable
        self.consecutive_collisions = 0

    def book_keeping_after_collision(self):
        # increase collision count
        self.num_of_collisions += 1
        # turn on faced collision flag
        self.facedCollision = True
        # change retransmission count for the collided packet
        self.buffer[0].retrans_count += 1
        # change backoff time
        exp = min(self.randomization_ceiling, self.num_of_collisions)
        result = (2 ** exp) - 1
        self.back_off_time = randint(0, result)
        # change consecutive collisions count
        if self.consecutive_collisions > 0:
            self.consecutive_collisions += 1
        if self.consecutive_collisions == self.max_retrans_count_until_drop:
            # packet is dropped due to consecutive collisions
            # remove from buffer
            self.buffer.popleft()
            # update consecutive collisions variable
            self.consecutive_collisions = 0
            # update lost packet count
            self.lost_packet_count += 1


