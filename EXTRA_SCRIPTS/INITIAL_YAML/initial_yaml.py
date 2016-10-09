__author__ = "Dan C Williams"
__version__ = "0.01"
__date__ = "Oct-9-2016"
__email__ = "dan.c.williams@gmail.com"
__status__ = "Development"

import netaddr
import collections
import re
import yaml

class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def main():

    raw_lines = [line.rstrip('\n') for line in open('CLEAR_TEST_PL_DATA.txt') if line[:-1]]
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
    yaml_dict = {}

    for i, line in enumerate(raw_lines):  # Identify garbage in data set
        for j in black_list:
            if j in line:
                temporary_list.append(line)

    for del_lines in temporary_list: # CLEARS OUT GARBAGE
        raw_lines.remove(del_lines)

    for i, line in enumerate(raw_lines):
        temporary_list = line.split() #SPLITTING LINES INTO LIST
        split_list.append(temporary_list)  #ADDING LIST TO LIST OF LIST
        temporary_list = [] #Reset TEMP List

    for i, line in enumerate(split_list): #Grab PL name and description and place them in pl_descripiton_list
        pl_names_dict[line[2]] = ''
        if line[3] == 'description':    # in a list of lists for further processing
            temporary_list.append(line[2]) 
            temporary_list.append(' '.join(line[4::]))
            pl_description_list.append(temporary_list)
            delete_list.append(line)
        if line [6] == '0.0.0.0/0': # Finds and removes default routes
            temporary_list.append(line[2]) 
            temporary_list.append(line[6])
            pl_default_route.append(temporary_list)
            delete_list.append(line)
        temporary_list = []

    for del_lines in delete_list: # CLEARS OUT DESCRIPTIONS & DEFAULT ROUTES
        split_list.remove(del_lines)

    for i, line in enumerate(split_list): # Grab PL name and network and place them
        temporary_list.append(line[2])    # in a list of lists for further processing
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

    d = collections.OrderedDict(sorted(pl_names_dict.items()))
    
    yaml_dict['allowed'] = {}
    yaml_dict['remediation'] = {}

    for key, blank in d.items():
        if "ALLOWED" in key:
           m = re.findall('\d:\d{4}', key)
           if m:
                vrf = m
           yaml_dict['allowed'][vrf[0]] = {}
           if key in pl_desc_dict:
                yaml_dict['allowed'][vrf[0]]['description'] = pl_desc_dict[key]
           yaml_dict['allowed'][vrf[0]]['prefix'] = {}
           if key in pl_dict_final:
                temp_list = []
                for i, ip_address in enumerate(pl_dict_final[key]):
                    temp_list.append(str(ip_address))
                yaml_dict['allowed'][vrf[0]]['prefix'] = temp_list
        if "REMEDIATION" in key:
           m = re.findall('\d:\d{4}', key)
           if m:
                vrf = m
           yaml_dict['remediation'][vrf[0]] = {}
           if key in pl_desc_dict:
                yaml_dict['remediation'][vrf[0]]['description'] = pl_desc_dict[key]
           yaml_dict['remediation'][vrf[0]]['prefix'] = {}
           if key in pl_dict_final:
                temp_list = []
                for i, ip_address in enumerate(pl_dict_final[key]):
                    temp_list.append(str(ip_address))
                yaml_dict['remediation'][vrf[0]]['prefix'] = temp_list
 
    with open('initial_load.yaml', 'w') as outfile:
        stream = yaml.dump(yaml_dict, Dumper=MyDumper, default_flow_style=False)
        outfile.write('---\n')
        outfile.write(stream)

    outfile.close()

    print('COMPLETE')

if __name__ == "__main__":
    main()
