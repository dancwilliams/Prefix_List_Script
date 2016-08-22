__author__ = "Dan C Williams"
__version__ = "0.42"
__date__ = "Jul-27-2016"
__email__ = "dan.c.williams@gmail.com"
__status__ = "Development"

import netaddr
import collections



def main():

    raw_lines = [line.rstrip('\n') for line in open('TEST_PL_DATA.txt') if line[:-1]]
    black_list = ['!']
    split_list = []
    pl_list = []
    pl_names_dict = {}
    pl_dict = collections.defaultdict(list)
    pl_dict_final = {}
    delete_list = []
    temporary_list = []
    pl_description_list = []
    pl_default_route = []
    pl_desc_dict = collections.defaultdict(list)
    pl_default_dict = collections.defaultdict(list)
    
    
    for i, line in enumerate(raw_lines):  # Remove Garbage.  Clean data set
        for j in black_list:
            if j in line:
                temporary_list.append(line)
    
    for del_lines in temporary_list: # CLEARS OUT DESCRIPTIONS & DEFAULT ROUTES
        raw_lines.remove(del_lines)
    
    for i, line in enumerate(raw_lines):
        temporary_list = line.split() #SPLITTING LINES INTO LIST
        split_list.append(temporary_list)  #ADDING LIST TO LIST OF LIST
        temporary_list = [] #Reset TEMP List
    
    for i, line in enumerate(split_list): #Grab PL name and description and place them
        pl_names_dict[line[2]] = ''
        if line[3] == 'description':    #in a list of lists for further processing
            temporary_list.append(line[2]) 
            temporary_list.append(' '.join(line[4::]))
            pl_description_list.append(temporary_list)
            delete_list.append(line)
        if line [6] == '0.0.0.0/0':
            temporary_list.append(line[2]) 
            temporary_list.append(line[6])
            pl_default_route.append(temporary_list)
            delete_list.append(line)
        temporary_list = []
    
    for del_lines in delete_list: # CLEARS OUT DESCRIPTIONS & DEFAULT ROUTES
        split_list.remove(del_lines)
    
    for i, line in enumerate(split_list): #Grab PL name and network and place them
        temporary_list.append(line[2]) #in a list of lists for further processing
        temporary_list.append(line[6])
        pl_list.append(temporary_list)
        temporary_list = []
    
    for key, value in pl_description_list:  #create pl_desc_dict using the key and description string
        tempString = value
        pl_desc_dict[key] = tempString
    
    for key, value in pl_default_route:  #create pl_default_dict using the key and network
        pl_default_dict[key].append(netaddr.IPNetwork(value))
        
    for key, value in pl_list:  #create pl_dict using the key and network
        pl_dict[key].append(netaddr.IPNetwork(value))
    
    for key, value in pl_dict.items():
        value = netaddr.cidr_merge(value)
        value.sort()
        pl_dict_final[key] = value
    
    target = open('test_output.txt', 'w')
    
    d = collections.OrderedDict(sorted(pl_names_dict.items()))
    
    for key, blank in d.items():
        seq_num = 5
        if key in pl_desc_dict:
            target.write("ip prefix-list " + str(key) + " description " + str(pl_desc_dict[key]) + "\n")
        if key in pl_dict_final:
            for i, ip_address in enumerate(pl_dict_final[key]):
                if str(ip_address.netmask) == '255.255.255.255':
                    target.write("ip prefix-list " + str(key) + " seq " + str(seq_num) + " permit " + str(ip_address) + ("\n"))
                else:
                    target.write("ip prefix-list " + str(key) + " seq " + str(seq_num) + " permit " + str(ip_address) + " le 32\n")
                seq_num += 5
        if key in pl_default_dict:
            target.write("ip prefix-list " + str(key) + " seq 500000 deny 0.0.0.0/0 le 32\n")
        target.write("!\n")
    
    target.close()
    
    print('COMPLETE')

if __name__ == "__main__":
    main()
