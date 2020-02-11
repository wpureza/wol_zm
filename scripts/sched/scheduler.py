import os
import platform
from netmiko import ConnectHandler

def procDate(date):
    dia = date.split('/')[0]
    mes = date.split('/')[1]
    ano = date.split('/')[2]
    meslist = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    messtring = meslist[int(mes)-1]
    return messtring+"/"+dia+"/"+ano

def scheduler(hostname, host, port, username, password, data, horario):
    mikrotik = {'device_type': 'mikrotik_routeros',
                'host': host,
                'port': port,
                'username': username,
                'password': password}
    net_connect = ConnectHandler(**mikrotik)
    net_connect.send_command('/system script add name=wol source="/tool wol mac=FF:FF:FF:FF:FF"')
    out = net_connect.send_command('/system script print brief')

    for line in str(out).split('\n'):
        if line.__contains__('wol'):
            id_script  = line.split('wol')[0]
            id_script = id_script.replace(' ','')

    data_format = data
    data = procDate(data)
    horario = horario+":00"
    net_connect.send_command('/system scheduler add name=wol on-event=wol start-date='+data+' start-time='+horario)
    out = net_connect.send_command('/system scheduler print')

    for line in str(out).split('\n'):
        if line.__contains__('wol'):
            id_sched = line.split('wol')[0]
            id_sched = id_sched.replace(' ', '')

    net_connect.disconnect()

    if platform.system() == "Windows":
        path = "\\tmp\\sched\\"
    else:
        path = "/tmp/sched/"
    path = os.getcwd() + path
    schedfile = path + "sched"
    if os.path.isfile(schedfile):
        file = open(schedfile, 'a+')
    else:
        file = open(schedfile, 'w+')
    file.write(id_script + "::" + id_sched + "::"+hostname+"::"+host+"::"+ data_format + " " + horario + "::"+port+"\n")
    file.close()


def schedTableFiles():
    if platform.system() == "Windows":
        path = "\\tmp\\sched\\"
    else:
        path = "/tmp/sched/"
    path = os.getcwd() + path
    scheds = path + 'sched'
    if os.path.isfile(scheds):
        table = []
        file = open(scheds, 'r')
        for lines in file.readlines():
            if lines == '\n':
                continue
            id_script = lines.split('::')[0]
            id_sched = lines.split('::')[1]
            hostname = lines.split('::')[2]
            ip = lines.split('::')[3]
            data = lines.split('::')[4]
            port = lines.split('::')[5].replace('\n','')
            table.append(dict(id_script=id_script, id_sched=id_sched, ip=ip, hostname=hostname, data=data, port=port))
        return table
    return None


def cancelSched(host, port, username, password, id_script, id_sched, hostname, data):
    if platform.system() == "Windows":
        path = "\\tmp\\sched\\"
    else:
        path = "/tmp/sched/"
    path = os.getcwd() + path
    scheds = path + 'sched'
    sched_line = str(id_script)+"::"+str(id_sched)+"::"+hostname+"::"+host+"::"+data+"::"+port+"\n"
    print(sched_line)
    scheds2 = path + 'sched.aux'


    ####
    mikrotik = {'device_type': 'mikrotik_routeros',
                'host': host,
                'port': port,
                'username': username,
                'password': password}
    net_connect = ConnectHandler(**mikrotik)
    out = net_connect.send_command('/system script print')
    for line in str(out).split('\n'):
        if str(line).__contains__(str(id_script)) and str(line).__contains__('name="wol"'):
            net_connect.send_command('/system script remove '+str(id_script))

    out = net_connect.send_command('/system scheduler print')
    for line in str(out).split('\n'):
        if str(line).__contains__(str(id_sched)) and str(line).__contains__('wol'):
            net_connect.send_command('/system scheduler remove '+str(id_script))
    net_connect.disconnect()
    #######

    file2 = open(scheds2, 'x')
    if os.path.isfile(scheds):
        file = open(scheds, 'r+')
        for lines in file.readlines():
            if lines != sched_line:
                file2.write(lines)
            else:
                continue
        file.close()
        file2.close()
        os.remove(scheds)
        os.rename(scheds2, scheds)