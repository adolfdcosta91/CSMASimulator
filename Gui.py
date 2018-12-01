from tkinter import*
window = Tk()

# Store the user data and to print


def print_values():
    lb2 = Label(window, text="Number of Nodes: " + number_of_nodes.get(), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=1)
    lb2 = Label(window, text="Number of Time Slots: " + number_of_time_slots.get(), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=2)
    lb2 = Label(window, text="Buffer Size: " + buffer_size.get(), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=3)
    lb2 = Label(window, text="Probability of Packet Generation: " + probability_of_generating_packet.get(), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=4)
    lb2 = Label(window, text="Re-transmission count: " + maximum_retransmission_count.get(), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=5)
    lb2 = Label(window, text="Maximum randomisation ceiling: " + maximum_randomisation_ceiling.get(), font=('Helvetica', 10, 'bold'))
    lb2.grid(column=3, row=6)

    print(number_of_nodes.get())
    print(number_of_time_slots.get())
    print(buffer_size.get())
    print(probability_of_generating_packet.get())
    print(maximum_retransmission_count.get())
    print(maximum_randomisation_ceiling.get())


window.title("Transmission Simulation Input")
window.geometry('900x600')
filename = PhotoImage(file="E:networking.png")
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
number_of_nodes = Spinbox(window, from_=0, to=100, width=20,)
number_of_nodes.grid(column=1, row=1)

# To display Number of Time Slot label,spin box
lbl = Label(window, text="Enter the Number of Time Slots (0-100)", font=('Helvetica', 10, 'bold'))
lbl.grid(column=0, row=2)
number_of_time_slots = Spinbox(window, from_=0, to=100, width=20)
number_of_time_slots.grid(column=1, row=2)

# To display Buffer Size label,spin box
lbl = Label(window, text="Enter the Buffer Size (0-100)", font=('Helvetica', 10, 'bold'))
lbl.grid(column=0, row=3)
buffer_size = Spinbox(window, from_=0, to=100, width=20)
buffer_size.grid(column=1, row=3)

# To display Probability of Generating packet label,spin box, double data type was used for decimal
lbl = Label(window, text="Enter the Probability of Generating Packet (0.1-1)", font=('Helvetica', 10, 'bold'))
lbl.grid(column=0, row=4)
probability_of_generating_packet = Spinbox(window, from_=0, to=1, increment=0.1, width=20)
probability_of_generating_packet.grid(column=1, row=4)

# To display Re-transmission count
lbl = Label(window, text="Enter the re-transmission count (0-100)", font=('Helvetica', 10, 'bold'))
lbl.grid(column=0, row=5)
maximum_retransmission_count = Spinbox(window, from_=0, to=100, width=20)
maximum_retransmission_count.grid(column=1, row=5)

# To display Maximum randomisation ceiling
lbl = Label(window, text="Enter Maximum randomisation ceiling (0-100)", font=('Helvetica', 10, 'bold'))
lbl.grid(column=0, row=6)
maximum_randomisation_ceiling = Spinbox(window, from_=0, to=100, width=20)
maximum_randomisation_ceiling.grid(column=1, row=6)


# To display a button
button = Button(window, text='Simulate', command=print_values, height=3, width=17, font=('Helvetica', 10, 'bold'))
button.grid(column=0, row=7, columnspan=2)
button.configure(background='Steelblue1')
# OutputDisplay

window.mainloop()
