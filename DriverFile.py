# this is the outline

/*        """ for (int i = 0; i < timeSlots; i++) {

			// generate packets
			for (int j = 0; j < node.length; j++) {
				node[j].generatePacket();//generate packet with probability of 0.1
				//decrease backoff time if it is not 0
			}

			// check how many nodes have packet to be transmitted

				//if only one node has packet && its backoff time is 0 && channel is idle (state:transmission)
			    	//channel state = transmission
			        //for that node, decrease the buffer size by 1, call a method (node.removePacket&DecreaseBuffersize)
			        //transcount = 10 (because channel is occupied for 10 time slots)
			        //change the channel state to idle when transcount is 0
			        //update other statistics variables here

				//else if channel is idle && more than one nodes have packets (state:contention)
			        //channel state = contention
			        //for every node, update collision and backoff variables, call a method (node.updateBackoffVariables)

			    //else if there are no packets to be sent in  any of the nodes && transcount is 0
			        //channel state = idle

			//transcount--
		}


	 * This method takes array of nodes as input, checks if any nodes have pending
	 * packets, returns an arraylist of nodes which have pending packets.
	 *
	 * @param array of nodes
	 * @param max
	 * @return arraylist of nodes

	"""

