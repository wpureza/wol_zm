from netmiko import ConnectHandler
import re
import platform
import os


def getARP(hostname, host, port, username, password):
    mikrotik = {'device_type': 'mikrotik_routeros',
                'host': host,
                'port': port,
                'username': username,
                'password': password}

    net_connect = ConnectHandler(**mikrotik)
    output_arp = net_connect.send_command('/ip arp print')
    arp = ''
    for line in output_arp.split('\n'):
        try:
            re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', line, re.I).group()
            arp += line+"\n"
        except:
            continue
    if platform.system() == "Windows":
        path = "\\tmp\\arp\\"
    else:
        path = "/tmp/arp/"
    path = os.getcwd() + path
    arpfile = path + hostname+"_"+host
    file = open(arpfile, 'w+')
    file.write(arp)
    file.close()
    net_connect.disconnect()


def viewARP(hostname, ip):
    if platform.system() == "Windows":
        path = "\\tmp\\arp\\"
    else:
        path = "/tmp/arp/"
    path = os.getcwd() + path
    arpfile = path + hostname + "_" + ip
    file = open(arpfile, 'r')
    text = []
    for line in file:
        text.append(line)
    return text

def viewMAC(hostname, ip):
    if platform.system() == "Windows":
        path = "\\tmp\\mac\\"
    else:
        path = "/tmp/mac/"
    path = os.getcwd() + path
    macfile = path + hostname + "_" + ip
    file = open(macfile, 'r')
    text = []
    for line in file:
        text.append(line)
    return text


def getMAC(hostname, host, port, username, password):
    mikrotik = {'device_type': 'mikrotik_routeros',
                'host': host,
                'port': port,
                'username': username,
                'password': password}

    net_connect = ConnectHandler(**mikrotik)
    output_mac = net_connect.send_command('/interface bridge host print')
    mac_table = []
    for line in output_mac.split('\n'):
        try:
            mac_address = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', line, re.I).group()
        except:
            continue
        if line.split(mac_address)[0].__contains__('DL'):
            continue
        mac_table.append(mac_address)
    if platform.system() == "Windows":
        path = "\\tmp\\mac\\"
    else:
        path = "/tmp/mac/"
    path = os.getcwd() + path
    macfile = path + hostname+"_"+host
    file = open(macfile, 'w+')
    for mac in mac_table:
        file.write(mac+"\n")
    file.close()
    net_connect.disconnect()