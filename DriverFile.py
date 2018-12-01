import Node
# this is the main driver code for the project

# declare buttons here

# on click of 'Simulate' button


def simulate():
    # get values from UI

    simulation_time = 1000
    buffer_size = 100
    packet_gen_prob = 0.1
    num_of_nodes = 5
    randomization_ceiling = 10
    max_retrans_count_until_drop = 16
    # generate an array with node objects
    nodes_list = []
    identity = 'Node '
    for number in range(1, num_of_nodes):
        identity += str(number)
        nodes_list.append(Node.Node(identity, buffer_size, packet_gen_prob, num_of_nodes, randomization_ceiling, max_retrans_count_until_drop))

    # variables here
    channel_state = "idle"
    wasted_timeslots = 0
    utilized_timeslots = 0
    occupied_timeslot = 0
    for timeslot_instance in range(simulation_time):
        # processes that can happen concurrently in one time slot will be part of this loop

        # give a chance to every node to generate packets
        for node_instance in nodes_list:
            node_instance.gen_packet_with_prob(timeslot_instance)

        # decide channel state for this timeslot
        if channel_state == "transmission" and occupied_timeslot != 0:
            occupied_timeslot -= 1
            utilized_timeslots += 1
            channel_state = "transmission"
        else:
            nodes_list = get_nodes_wanting_to_transmit(nodes_list)
            if len(nodes_list) == 0:
                channel_state = "idle"
                wasted_timeslots += 1
            elif len(nodes_list) == 1:
                channel_state = "transmission"
                utilized_timeslots += 1
                transmiting_node = nodes_list.pop()
                transmiting_node.book_keeping_after_suc_trans(transmiting_node, timeslot_instance)
                occupied_timeslot = 9
            elif len(nodes_list) > 1:
                channel_state = "contention"
                wasted_timeslots += 1
                for node_instance in nodes_list:
                    node_instance.book_keeping_after_collision(node_instance)

    # results to be printed
    print("Timeslots: ")
    print(simulation_time)
    print("Number of frames generated by each station:")
    for node_instance in nodes_list:
        print("Number of frame generated by %s is %d" % (node_instance.identity_ip, node_instance.num_of_gen_packets))
    total_frames = get_total_num_of_frames_generated(nodes_list)
    print("Cumulative total of all the frames generated by stations: ")
    print(total_frames)
    for node_instance in nodes_list:
        print("Average Number of frame generated by %s is %d" % (node_instance.identity_ip, (node_instance.num_of_gen_packets / simulation_time)))
    print("Average number of frames generated by each station: ")
    print(total_frames / simulation_time)
    print("Total frames lost due to buffer overflows and maximum retransmission count reached: ")
    lost_frame_count = get_num_of_frames_lost(nodes_list)
    print(lost_frame_count)
    print("Total frames awaiting at the end of simulation time: ")
    awaiting_frame_count = get_num_of_awaiting_frames(nodes_list)
    print(awaiting_frame_count)
    print("Total successful frames at the end of simulation time: ")
    succ_frame_count = get_num_of_succ_trans(nodes_list)
    print(succ_frame_count)
    print("Throughput of the system")
    print(succ_frame_count/simulation_time)
    print("Channel utilization")
    print(utilized_timeslots/simulation_time)
    print("Channel waste")
    print(wasted_timeslots/simulation_time)
    print("Retransmission overhead")
    num_of_retrans = get_retrans_overhead(nodes_list)
    print(num_of_retrans/succ_frame_count)
    print("Delay")


def get_nodes_wanting_to_transmit(nodes_list):
    # count how many nodes have packets in their buffer
    transmitting_nodes = []
    for node_instance in nodes_list:
        if len(node_instance.buffer) > 0 and node_instance.back_off_time == 0:
            transmitting_nodes.append(node_instance)
    return transmitting_nodes


def get_num_of_awaiting_frames(nodes_list):
    count = 0
    for node_instance in nodes_list:
        count += len(node_instance.buffer)
    return count


def get_total_num_of_frames_generated(nodes_list):
    count = 0
    for node_instance in nodes_list:
        count += node_instance.num_of_gen_packets
    return count


def get_num_of_frames_lost(nodes_list):
    count = 0
    for node_instance in nodes_list:
        count += node_instance.lost_packet_count
    return count


def get_num_of_succ_trans(nodes_list):
    count = 0
    for node_instance in nodes_list:
        count += node_instance.success_trans_packet_count
    return count


def get_retrans_overhead(nodes_list):
    # addition of retransmission attempts
    count = 0
    for node_instance in nodes_list:
        count += node_instance.num_of_retrans_attempts
    return count


def get_avg_total_delay(nodes_list):
    # addition of number_of_delayed_slots / total_frames_generated across each station
    count = 0
    for node_instance in nodes_list:
        count += node_instance.num_of_delayed_slots
    return count
