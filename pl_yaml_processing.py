import yaml
import netaddr
import os.path
import time

class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def main():

    remediation_vrfs = ['1:1200', '1:1500', '1:1600', '1:2100', '1:2600']
    output_dict = {}
    output_yaml = {}
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_yaml['allowed'] = {}
    output_yaml['remediation'] = {}
    backup_path = 'ORIGINAL_BACKUPS/'
    change_path = 'CHG_SCRIPTS/'
    original_path = 'ORIGINAL/'

    original_file = os.path.join(original_path, 'original.yaml')

    with open(original_file, 'r') as stream:
        try:
            original_yaml = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open("pl_changes.yaml", 'r') as stream:
        try:
            change_yaml = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    temp_list = change_yaml['change_number']
    change_number = temp_list[0]

    output_file = os.path.join(change_path, change_number + '.yaml')

    backup_file = os.path.join(backup_path, 'original_pre_' + change_number + '_' + timestr + '.yaml')

    with open(backup_file, 'w') as outfile:
        stream = yaml.dump(original_yaml, Dumper=MyDumper, default_flow_style=False)
        outfile.write(stream)

    for top_level_key, blank in change_yaml.items():
        if top_level_key == 'add':
            allowed_vrf_list = []
            for vrf, blank in change_yaml[top_level_key].items():
                allowed_vrf_list.append(vrf)
                #print(allowed_vrf_list)
                output_dict['allowed'] = allowed_vrf_list
                #temp_ip_list = []
                temp_ip_set = netaddr.IPSet()
                temp_list = change_yaml[top_level_key][vrf]
                #print(temp_list)
                for i, ip_address in enumerate(temp_list):
                    temp_ip_set.add(ip_address)
                for i, ip_address in enumerate(original_yaml['allowed'][vrf]['prefix']):
                    temp_ip_set.add(ip_address)
                temp_list = []
                for i, ip_address in enumerate(temp_ip_set.iter_cidrs()):
                    temp_list.append(str(ip_address))
                original_yaml['allowed'][vrf]['prefix'] = temp_list
                if vrf in remediation_vrfs:
                    remediation_required = True
                    for i, rem_vrf in enumerate(remediation_vrfs):
                        temp_ip_set = netaddr.IPSet()
                        if vrf != rem_vrf:
                            temp_list = change_yaml[top_level_key][vrf]
                            for i, ip_address in enumerate(temp_list):
                                temp_ip_set.add(ip_address)
                            for i, ip_address in enumerate(original_yaml['remediation'][rem_vrf]['prefix']):
                                temp_ip_set.add(ip_address)
                            temp_list = []
                            for i, ip_address in enumerate(temp_ip_set.iter_cidrs()):
                                temp_list.append(str(ip_address))
                            original_yaml['remediation'][rem_vrf]['prefix'] = temp_list

        if top_level_key == 'remove':
            for vrf, blank in change_yaml[top_level_key].items():
                temp_ip_set = netaddr.IPSet()
                temp_list = change_yaml[top_level_key][vrf]
                #print(temp_list)
                for i, ip_address in enumerate(original_yaml['allowed'][vrf]['prefix']):
                    temp_ip_set.add(ip_address)
                for i, ip_address in enumerate(temp_list):
                    temp_ip_set.remove(ip_address)
                temp_list = []
                for i, ip_address in enumerate(temp_ip_set.iter_cidrs()):
                    temp_list.append(str(ip_address))
                original_yaml['allowed'][vrf]['prefix'] = temp_list
                if vrf in remediation_vrfs:
                    remediation_required = True
                    for i, rem_vrf in enumerate(remediation_vrfs):
                        temp_ip_set = netaddr.IPSet()
                        if vrf != rem_vrf:
                            temp_list = change_yaml[top_level_key][vrf]
                            for i, ip_address in enumerate(original_yaml['remediation'][rem_vrf]['prefix']):
                                temp_ip_set.add(ip_address)
                            for i, ip_address in enumerate(temp_list):
                                temp_ip_set.remove(ip_address)
                            temp_list = []
                            for i, ip_address in enumerate(temp_ip_set.iter_cidrs()):
                                temp_list.append(str(ip_address))
                            original_yaml['remediation'][rem_vrf]['prefix'] = temp_list

 
    for i, final_vrf in enumerate(allowed_vrf_list):
        output_yaml['allowed'][final_vrf] = original_yaml['allowed'][final_vrf]
    if remediation_required == True:
        for i, final_vrf in enumerate(remediation_vrfs):
            output_yaml['remediation'][final_vrf] = original_yaml['remediation'][final_vrf]
    
    with open(original_file, 'w') as outfile:
        stream = yaml.dump(original_yaml, Dumper=MyDumper, default_flow_style=False)
        outfile.write('---\n')
        outfile.write(stream)

    with open(output_file, 'w') as outfile:
        stream = yaml.dump(output_yaml, Dumper=MyDumper, default_flow_style=False)
        outfile.write('---\n')
        outfile.write('change_number:\n')
        outfile.write('  - ' + change_number + '\n')
        outfile.write(stream)

    outfile.close()
    
    print('COMPLETE')
    
if __name__ == "__main__":
    main()
