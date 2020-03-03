from netmiko import ConnectHandler
import re

mikrotik = {'device_type': 'mikrotik_routeros',
            'host': '',
            'port': '8297',
            'username': '',
            'password': ''}


mac_table = []
net_connect = ConnectHandler(**mikrotik)
output = net_connect.send_command('/interface bridge host print')
output_arp = net_connect.send_command('/ip arp print')
######################################################################################################
###################                     HOSTNAME                  ####################################
######################################################################################################
hostname = net_connect.send_command('/system identity print')
hostname = hostname.split('name:')[1]
if hostname.__contains__('\n'):
    hostname = hostname.split('\n')[0]
print(hostname)
######################################################################################################
for line in output.split('\n'):
    try:
        mac_address = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', line, re.I).group()
    except:
        continue
    if line.split(mac_address)[0].__contains__('DL'):
        continue
    mac_table.append(mac_address)




print(mac_table)
# /tool wol mac=D0:94:66:AA:33:D3

net_connect.disconnect()
