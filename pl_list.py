__author__ = "Dan C Williams"
__version__ = "0.2"
__date__ = "Jul-24-2016"
__email__ = "dan.c.williams@gmail.com"
__status__ = "Development"\

import netaddr
import collections

raw_lines = [line.rstrip('\n') for line in open('TEST_PL_DATA.txt')]
blackList = ['0.0.0.0/0', 'description', '!']
split_list = []
ip_list =[]
pl_list = []
pl_dict = collections.defaultdict(list)
pl_dict_final = {}
del_list = []
temp_list = []
split_list = []

def main():

    temp_list = []
    
    for i, line in enumerate(raw_lines):  # IDs DESCRIPTIONS & DEFAULT ROUTES
        for j in blackList:
            if j in line:
                temp_list.append(line)

    for del_lines in temp_list: # CLEARS OUT DESCRIPTIONS & DEFAULT ROUTES
        raw_lines.remove(del_lines)

    for i, line in enumerate(raw_lines):
        temp_list = line.split() #SPLITTING LINES INTO LIST
        split_list.append(temp_list)  #ADDING LIST TO LIST OF LIST
        temp_list = [] #Reset TEMP List

    for i, line in enumerate(split_list): #Grab PL name and network and place them
        temp_list.append(line[2]) #in a list of lists for further processing
        temp_list.append(line[6])
        pl_list.append(temp_list)
        temp_list = []

    for key, value in pl_list:  #create pl_dict using the key and network
        pl_dict[key].append(netaddr.IPNetwork(value))

    for key, value in pl_dict.items():
        value = netaddr.cidr_merge(value)
        value.sort()
        pl_dict_final[key] = value

    target = open('test_output.txt', 'w')

    d = collections.OrderedDict(sorted(pl_dict_final.items()))

    for key, value in d.items():
        seq_num = 5
        target.write("ip prefix-list " + str(key) + " description Permit Networks Assigned to the Aviation BU\n")
        for i, ip_address in enumerate(value):
            if str(ip_address.netmask) == '255.255.255.255':
                target.write("ip prefix-list " + str(key) + " seq " + str(seq_num) + " permit " + str(ip_address) + ("\n"))
            else:
                target.write("ip prefix-list " + str(key) + " seq " + str(seq_num) + " permit " + str(ip_address) + " le 32\n")
            seq_num += 5
        target.write("ip prefix-list " + str(key) + " seq 500000 deny 0.0.0.0/0 le 32\n")
        target.write("!\n")

    target.close()

    print('COMPLETE')

if __name__ == "__main__":
    main()
