__author__ = "Dan C Williams"
__version__ = "0.2"
__date__ = "Jul-24-2016"
__email__ = "dan.c.williams@gmail.com"
__status__ = "Development"\

import netaddr
import collections



def main():

    raw_lines = [line.rstrip('\n') for line in open('TEST_PL_DATA.txt')]
    blackList = ['!']
    splitList = []
    plList = []
    plDict = collections.defaultdict(list)
    plDictFinal = {}
    deleteList = []
    temporaryList = []
    plDescription = []
    plDefaultRoute = []
    plDescDict = collections.defaultdict(list)
    plDefaultDict = collections.defaultdict(list)
    
    
    for i, line in enumerate(raw_lines):  # Remove Garbage.  Clean data set
        for j in blackList:
            if j in line:
                temporaryList.append(line)
    
    for del_lines in temporaryList: # CLEARS OUT DESCRIPTIONS & DEFAULT ROUTES
        raw_lines.remove(del_lines)
    
    for i, line in enumerate(raw_lines):
        temporaryList = line.split() #SPLITTING LINES INTO LIST
        splitList.append(temporaryList)  #ADDING LIST TO LIST OF LIST
        temporaryList = [] #Reset TEMP List
    
    for i, line in enumerate(splitList): #Grab PL name and description and place them
        if line[3] == 'description':    #in a list of lists for further processing
            temporaryList.append(line[2]) 
            temporaryList.append(' '.join(line[4::]))
            plDescription.append(temporaryList)
            deleteList.append(line)
        if line [6] == '0.0.0.0/0':
            temporaryList.append(line[2]) 
            temporaryList.append(line[6])
            plDefaultRoute.append(temporaryList)
            deleteList.append(line)
        temporaryList = []
    
    for del_lines in deleteList: # CLEARS OUT DESCRIPTIONS & DEFAULT ROUTES
        splitList.remove(del_lines)
    
    for i, line in enumerate(splitList): #Grab PL name and network and place them
        temporaryList.append(line[2]) #in a list of lists for further processing
        temporaryList.append(line[6])
        plList.append(temporaryList)
        temporaryList = []
    
    for key, value in plDescription:  #create plDescDict using the key and description string
        tempString = value
        plDescDict[key] = tempString
    
    for key, value in plList:  #create plDefaultDict using the key and network
        plDefaultDict[key].append(netaddr.IPNetwork(value))
        
    for key, value in plList:  #create plDict using the key and network
        plDict[key].append(netaddr.IPNetwork(value))
    
    for key, value in plDict.items():
        value = netaddr.cidr_merge(value)
        value.sort()
        plDictFinal[key] = value
    
    target = open('test_output.txt', 'w')
    
    d = collections.OrderedDict(sorted(plDictFinal.items()))
    
    for key, value in d.items():
        seq_num = 5
        if key in plDescDict:
            target.write("ip prefix-list " + str(key) + " description " + str(plDescDict[key]) + "\n")
        for i, ip_address in enumerate(value):
            if str(ip_address.netmask) == '255.255.255.255':
                target.write("ip prefix-list " + str(key) + " seq " + str(seq_num) + " permit " + str(ip_address) + ("\n"))
            else:
                target.write("ip prefix-list " + str(key) + " seq " + str(seq_num) + " permit " + str(ip_address) + " le 32\n")
            seq_num += 5
        if key in plDefaultDict:
            target.write("ip prefix-list " + str(key) + " seq 500000 deny 0.0.0.0/0 le 32\n")
        target.write("!\n")
    
    target.close()
    
    print('COMPLETE')

if __name__ == "__main__":
    main()
