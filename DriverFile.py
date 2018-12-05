import Node
from tkinter import *

# all the functions go here


# function to be called on click of 'Simulate Button'
def simulate():

    # get values from UI
    print("let the execution begin")
    global simulation_time
    simulation_time = int(number_of_time_slots.get())
    buffer_size = int(size_of_buffer.get())
    packet_gen_prob = float(probability_of_generating_packet.get())
    num_of_nodes = int(number_of_nodes.get())
    randomization_ceiling = int(maximum_randomisation_ceiling.get())
    max_retrans_count_until_drop = int(maximum_retransmission_count.get())

    # generate an array with node objects
    nodes_list = []
    for number in range(0, num_of_nodes):
        identity = 'Node '
        identity += str(number+1)
        nodes_list.append(Node.Node(identity, buffer_size, packet_gen_prob, num_of_nodes, randomization_ceiling,
                                    max_retrans_count_until_drop))
    # variables here
    channel_state = "idle"
    wasted_timeslots = 0
    utilized_timeslots = 0
    occupied_timeslot = 0
    for timeslot_instance in range(0, simulation_time):
        # processes that can happen concurrently in one time slot will be part of this loop

        # give a chance to every node to generate packets
        for node_instance in nodes_list:
            node_instance.gen_packet_with_prob(timeslot_instance)

        # reduce backoff time of each node
        for node_instance in nodes_list:
            if node_instance.back_off_time > 0:
                node_instance.back_off_time -= 1

        # decide channel state for this timeslot
        if channel_state == "transmission" and occupied_timeslot != 0:
            occupied_timeslot -= 1
            utilized_timeslots += 1
            channel_state = "transmission"
        else:
            transmitting_nodes_list = get_nodes_wanting_to_transmit(nodes_list)
            if len(transmitting_nodes_list) == 0:
                channel_state = "idle"
                wasted_timeslots += 1
            elif len(transmitting_nodes_list) == 1:
                channel_state = "transmission"
                utilized_timeslots += 1
                transmiting_node = transmitting_nodes_list.pop()
                transmiting_node.book_keeping_after_suc_trans(timeslot_instance)
                occupied_timeslot = 9
            elif len(transmitting_nodes_list) > 1:
                channel_state = "contention"
                wasted_timeslots += 1
                for node_instance in transmitting_nodes_list:
                    node_instance.book_keeping_after_collision()

    # results to be printed
    print("Number of frames generated by each station:")
    for node_instance in nodes_list:
        print("Number of frame generated by %s is %d" % (node_instance.identity_ip, node_instance.num_of_gen_packets))

    global total_frames
    total_frames = get_total_num_of_frames_generated(nodes_list)

    for node_instance in nodes_list:
        if simulation_time != 0:
            station_average = (node_instance.num_of_gen_packets / simulation_time)
        else:
            station_average = 0
        print("Average Number of frame generated by %s is %f" % (node_instance.identity_ip, station_average))

    global average_frames
    if simulation_time != 0:
        average_frames = (total_frames/simulation_time)
    else:
        average_frames = 0

    global lost_frame_count
    lost_frame_count = get_num_of_frames_lost(nodes_list)

    global awaiting_frame_count
    awaiting_frame_count = get_num_of_awaiting_frames(nodes_list)

    global succ_frame_count
    succ_frame_count = get_num_of_succ_trans(nodes_list)

    global total_num_of_collisions
    total_num_of_collisions = get_num_of_coll_trans(nodes_list)

    print("Throughput of the system")
    global throughput
    if simulation_time != 0:
        throughput = (succ_frame_count / simulation_time)
    else:
        throughput = 0

    print("Channel utilization")
    global channel_util
    if simulation_time != 0:
        channel_util = (utilized_timeslots / simulation_time)
    else:
        channel_util = 0

    print("Channel waste")
    global channel_waste
    if simulation_time != 0:
        channel_waste = (wasted_timeslots / simulation_time)
    else:
        channel_waste = 0

    print("Retransmission overhead")
    global retrans_overhead
    num_of_retrans = get_retrans_overhead(nodes_list)
    if succ_frame_count != 0:
        retrans_overhead = (num_of_retrans/succ_frame_count)
    else:
        retrans_overhead = 0

    print("Average Delay")
    global avg_delay
    num_of_delayed_slots = get_avg_total_delay(nodes_list)
    if succ_frame_count != 0:
        avg_delay = num_of_delayed_slots / succ_frame_count
    else:
        avg_delay = 0

    display_output()


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


def get_num_of_coll_trans(nodes_list):
    count = 0
    for node_instance in nodes_list:
        count += node_instance.num_of_collisions
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


def formulate_window():
    global window
    window = Tk()
    window.title("Transmission Simulation")
    window.geometry('1200x600')
    filename = PhotoImage(file="networking.png")
    background_label = Label(window, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Insert the labels in the window
    text = Label(window, text="Input Value", font=('Helvetica', 20, 'bold'))
    text.grid(column=0, row=0, columnspan=2)

    text = Label(window, text="\t", font=('Helvetica', 20, 'bold'))
    text.grid(column=2, row=0,)

    text = Label(window, text="Values to Compute", font=('Helvetica', 20, 'bold'))
    text.grid(column=3, row=0, columnspan=2)

    # To display Number of Node label,spin box
    lbl = Label(window, text="Enter the Number of Nodes (0-100)", font=('Helvetica', 10, 'bold'))
    lbl.grid(column=0, row=1)
    global number_of_nodes
    number_of_nodes = Spinbox(window, from_=0, to=100, width=20)
    number_of_nodes.grid(column=1, row=1)

    # To display Number of Time Slot label,spin box
    lbl = Label(window, text="Enter the Number of Time Slots (0-100)", font=('Helvetica', 10, 'bold'))
    lbl.grid(column=0, row=2)
    global number_of_time_slots
    number_of_time_slots = Spinbox(window, from_=0, to=100, width=20)
    number_of_time_slots.grid(column=1, row=2)

    # # To display Buffer Size label,spin box
    lbl = Label(window, text="Enter the Buffer Size (0-100)", font=('Helvetica', 10, 'bold'))
    lbl.grid(column=0, row=3)
    global size_of_buffer
    size_of_buffer = Spinbox(window, from_=0, to=100, width=20)
    size_of_buffer.grid(column=1, row=3)
    #
    # # To display Probability of Generating packet label,spin box, double data type was used for decimal
    lbl = Label(window, text="Enter the Probability of Generating Packet (0.1-1)", font=('Helvetica', 10, 'bold'))
    lbl.grid(column=0, row=4)
    global probability_of_generating_packet
    probability_of_generating_packet = Spinbox(window, from_=0, to=1, increment=0.1, width=20)
    probability_of_generating_packet.grid(column=1, row=4)
    #
    # # To display Re-transmission count
    lbl = Label(window, text="Enter the re-transmission count (0-100)", font=('Helvetica', 10, 'bold'))
    lbl.grid(column=0, row=5)
    global maximum_retransmission_count
    maximum_retransmission_count = Spinbox(window, from_=0, to=100, width=20)
    maximum_retransmission_count.grid(column=1, row=5)
    #
    # # To display Maximum randomisation ceiling
    lbl = Label(window, text="Enter Maximum randomisation ceiling (0-100)", font=('Helvetica', 10, 'bold'))
    lbl.grid(column=0, row=6)
    global maximum_randomisation_ceiling
    maximum_randomisation_ceiling = Spinbox(window, from_=0, to=100, width=20)
    maximum_randomisation_ceiling.grid(column=1, row=6)
    #
    #
    # # To display a button
    global button
    button = Button(window, text='Simulate', command=simulate, height=3, width=17, font=('Helvetica', 10, 'bold'))
    button.grid(column=0, row=7, columnspan=2)
    button.configure(background='Steelblue1')
    # OutputDisplay

    window.mainloop()


def display_output():
    lb2 = Label(window, text="Simulation period: " + str(simulation_time), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=1)
    lb2 = Label(window, text="Cumulative total of all the frames generated: " + str(total_frames),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=2)
    lb2 = Label(window, text="Average number of frames generated by each station: " + str(average_frames),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=3)
    lb2 = Label(window, text="Total frames lost due to buffer overflows and maximum retransmission count reached:  "
                             + str(lost_frame_count), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=4)
    lb2 = Label(window, text="Total frames awaiting at the end of simulation time: " + str(awaiting_frame_count),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=5)
    lb2 = Label(window, text="Total successful frames at the end of simulation time: " + str(succ_frame_count),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=6)

    lb2 = Label(window, text="Total collisions at the end of simulation time: " + str(total_num_of_collisions),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=7)

    lb2 = Label(window, text="Throughput of the system: " + str(throughput), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=8)
    lb2 = Label(window,
                text="Channel utilization: " + str(channel_util),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=9)
    lb2 = Label(window,
                text="Channel waste " + str(channel_waste),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=10)
    lb2 = Label(window,
                text="Retransmission overhead " + str(retrans_overhead),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=11)
    lb2 = Label(window,
                text="Average Delay" + str(avg_delay),
                font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=12)


# this is the main driver code for the project

# declare buttons here

# on click of 'Simulate' button

# formulate window

formulate_window()
