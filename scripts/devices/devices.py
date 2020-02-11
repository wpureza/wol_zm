import os
import platform
import socket
from netmiko import ConnectHandler

def checkPort(address, port):
    # Create a TCP socket
    s = socket.socket()
    print("Attempting to connect to %s on port %s" % (address, port))
    try:
        s.connect((address, port))
        print("Connected to %s on port %s" % (address, port))
        return True
    except:
        print("Connection to %s on port %s failed:" % (address, port))
        return False
    finally:
        s.close()

def tryConn(host, port, username, password):

    mikrotik = {'device_type': 'mikrotik_routeros',
                'host': host,
                'port': port,
                'username': username,
                'password': password}

    try:
        net_connect = ConnectHandler(**mikrotik)
        hostname = net_connect.send_command('/system identity print')
        hostname = hostname.split('name: ')[1]
        if hostname.__contains__('\n'):
            hostname = hostname.split('\n')[0]
        net_connect.disconnect()
        return hostname, True
    except:
        return False

def addDevice(hostname, ip, port, desc):
    if platform.system() == "Windows":
        path = "\\tmp\\"
    else:
        path = "/tmp/"
    path = os.getcwd()+path
    devices = path + 'devs'
    if os.path.isfile(devices):
        file = open(devices, 'r')
        id = 1
        for line in file.readlines():
            id += 1
        file = open(devices, 'a+')
        file.write(str(id)+"::"+hostname+"::"+ip+"::"+port+"::"+desc+"\n")
        file.close()
    else:
        file = open(devices, 'x')
        file.close()
        addDevice(hostname, ip, port, desc)

def devTableFiles():
    if platform.system() == "Windows":
        path = "\\tmp\\"
    else:
        path = "/tmp/"
    path = os.getcwd() + path
    devices = path + 'devs'
    if os.path.isfile(devices):
        table = []
        file = open(devices, 'r')
        for lines in file.readlines():
            if lines == '\n':
                continue
            id = lines.split('::')[0]
            hostname = lines.split('::')[1]
            ip = lines.split('::')[2]
            port = lines.split('::')[3]
            desc = lines.split('::')[4]
            table.append(dict(id=id, hostname=hostname, ip=ip, port=port, desc=desc))
        return table
    else:
        file = open(devices, 'w+')
        file.close()
    # for i in range(0, len(lines)):
    return None

def delTableindex(index):
    if platform.system() == "Windows":
        path = "\\tmp\\"
        path_arp = "\\tmp\\arp\\"
        path_mac = "\\tmp\\mac\\"
    else:
        path = "/tmp/"
        path_arp = "/tmp/arp/"
        path_mac = "/tmp/mac/"
    path = os.getcwd() + path
    path_arp = os.getcwd() + path_arp
    path_mac = os.getcwd() + path_mac
    devices = path + 'devs'
    devices2 = path + 'devs.aux'
    file2 = open(devices2, 'x')
    if os.path.isfile(devices):
        file = open(devices, 'r+')
        count = 0
        newindex = 1
        for lines in file.readlines():
                count += 1
                if (count != int(index)):
                    reindex = lines.split('::')[0]
                    line2 = lines.replace(reindex+"::", str(newindex)+"::")
                    file2.write(line2)
                    newindex += 1
                else:
                    hostname = lines.split("::")[1]
                    ip = lines.split("::")[2]
                    if os.path.isfile(path_arp+hostname+"_"+ip):
                        os.remove(path_arp+hostname+"_"+ip)
                    if os.path.isfile(path_mac + hostname + "_" + ip):
                        os.remove(path_mac + hostname + "_" + ip)
        file.close()
        file2.close()
        os.remove(devices)
        os.rename(devices2, devices)


    else:
        file = open(devices, 'w+')
        file.close()
    return None

def checkDevExist(hostname, ip):
    if platform.system() == "Windows":
        path = "\\tmp\\"
    else:
        path = "/tmp/"
    path = os.getcwd() + path
    devices = path + 'devs'
    if os.path.isfile(devices):
        file = open(devices, 'r+')
        for lines in file.readlines():
            line_host = lines.split('::')[1]
            line_addr = lines.split('::')[2]
            if line_host == hostname and line_addr == ip:
                file.close()
                return True
        file.close()
        return False
    else:
        file = open(devices, 'w+')
        file.close()
        return False