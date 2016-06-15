### This code is an EXAMPLE of how to exploit a .csv file from python. It is an annexe to the paper "Collective Anomaly Detection based on Long Short-Term Memory Recurrent Neural Network".
# The selected features are not the ones used in the main experiment.
# The used data are from a .csv file, transformed from the KDD 1999 tcpdump data (cf KDD1999_preprocess.py).

# Code by Loic BONTEMPS, INSA de Lyon.


import csv
import matplotlib.pyplot as plt
import math
import numpy


def csv_dict_reader(file_obj):

    # Initializing the value of selected features for each time step
    tcp_min = []
    udp_min = []
    len = []
    total_min = []
    
    nb_tcp = 0
    nb_udp = 0
    nb_total = 0
    nb_packets = 0   
    tcp_compt = 0
    udp_compt = 0
    
    time_index = 840
    tab_index = 0

    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        
        # Feature extraction
        a = int(line["frame.number"])
        
        b = (line["frame.time"])     
        hours = int(b[13:15])
        minutes = int(b[16:18])
        index_minutes = (60 * hours) + minutes 

        protocol = line["ip.proto"]
        d = int(line["frame.len"])

        # If we are still in the same time step.
        if index_minutes == time_index:            
            nb_total += 1
            if protocol == "6":
                nb_tcp += 1
                tcp_compt += 1
            if protocol == "17":
                nb_udp += 1
                udp_compt += 1
            nb_packets += d

        # If we reached a new time step.
        if index_minutes != time_index:
            time_index += 1
            tab_index += 1

            tcp_min[tab_index:(tab_index+1)] = [nb_tcp]
            udp_min[tab_index:(tab_index+1)] = [nb_udp]
            len[tab_index:(tab_index+1)] = [nb_packets]
            total_min[tab_index:(tab_index+1)] = [nb_total]

            nb_total = 1
            if protocol == "6":
                nb_tcp = 1
                tcp_compt += 1
            if protocol == "17":
                nb_udp = 1
                udp_compt += 1
            nb_packets = d
 
    tcp_average = tcp_compt/300  
    udp_average = udp_compt/300  

#print(numpy.tanh(udp_min))

    plt.plot(total_min)
    plt.show()
    plt.plot(tcp_min)
    plt.show()    
    plt.plot(udp_min)
    plt.show()

##################################

if __name__ == "__main__":
    with open("Friday1.csv") as f_obj:
        csv_dict_reader(f_obj)
