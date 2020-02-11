from sched import scheduler
from flask import Flask, flash, redirect, render_template, request, session, abort, make_response, send_file, Response
from flask_bootstrap import Bootstrap
import os
import scripts.devices.devices as dev
import scripts.tables.tables as tabs
import re
from datetime import date, datetime
import time
import scripts.sched.scheduler as sched

app = Flask(__name__)
app.secret_key = "key"
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        return render_template('dashboard.html')

@app.route('/dashboard/<string:content>',  methods=['GET', 'POST'])
def dashboardContent(content):
    if not session.get('logged_in'):
        return redirect('login')
    else:
        if content == 'logout':
            return redirect('/logout')
        elif content == 'dev':
            if request.method == 'POST' and request.form['addhost'] != '':
                print(request.form['addhost'])

                rta_table = None
                return render_template('/dashboard/dev.html', addhost=request.form['addhost'])
            if request.method == 'GET':
                rta_table = None
                return render_template('/dashboard/dev.html', table=rta_table)
        elif content == 'zbx-server':
            if request.method == 'POST':
                zbxhost = request.form['zbxhost']
                user = request.form['username']
                pwd = request.form['password']
                if (str(zbxhost).__contains__("http://")) or (str(zbxhost).__contains__("https://")):
                    if user != "" and pwd != "":
                        zapi = zbx.login(zbxhost, user, pwd)
                        if zapi == None:
                            flash(u'Erro na Conexão', 'error')
                        else:
                            print("OK")
                            cache.zapi = zapi
                            return render_template('/dashboard/zbx-server.html', zapi=zapi)
                    else:
                        flash(u'Login incorreto', 'error')
                        return render_template('/dashboard/zbx-server.html')
                else:
                    flash(u'Host incorreto', 'error')
                    return render_template('/dashboard/zbx-server.html')
                return render_template('/dashboard/zbx-server.html')
            if request.method == 'GET':
                return render_template('/dashboard/zbx-server.html')
        return render_template('/dashboard/%s.html' % content)


@app.route('/dev/<string:content>',  methods=['GET', 'POST'])
def device(content):
    if content == 'conf' and request.method == 'POST':
        host = request.form['device']
        port = request.form['port']
        user = request.form['username']
        password = request.form['password']
        desc = request.form['desc']
        hostname, result = dev.tryConn(host, port, user, password)
        if result == True:
            if dev.checkDevExist(hostname, host):
                flash(u'Host já existe!', 'error')
                return render_template('/dev/%s.html' % content)
            dev.addDevice(hostname, host, port, desc)
            flash(u'' + hostname + '  adicionado com sucesso!')
            tabs.getARP(hostname, host, port, user, password)
            tabs.getMAC(hostname, host, port, user, password)
        else:
            flash(u'Erro na Conexão', 'error')
        return render_template('/dev/%s.html' % content)
    ################
    elif content == 'mgmt':
        devs = dev.devTableFiles()
        return render_template('/dev/mgmt.html', devs=devs)
    return render_template('/dev/%s.html' % content)

@app.route('/table/<string:content>',  methods=['GET', 'POST'])
def tables(content):
    devs = dev.devTableFiles()
    try:
        if request.args['action'] == 'view' and request.method == 'POST':
            if request.args['type'] == 'arp':
                arp = tabs.viewARP(request.args['host'], request.args['ip'])
                return render_template('/table/%s.html' % content, devs=devs, arp=arp)
            elif request.args['type'] == 'mac':
                mac = tabs.viewMAC(request.args['host'], request.args['ip'])
                return render_template('/table/%s.html' % content, devs=devs, mac=mac)
        elif request.args['action'] == 'get' and request.method == 'POST':
            hostname = request.args['host']
            ip = request.args['ip']
            port = request.args['port']
            get=[hostname, ip, port]
            return render_template('/table/%s.html' % content, devs=devs, action=get)

        elif request.args['action'] == 'login' and request.method == 'POST':
            user = request.form['username']
            password = request.form['password']
            hostname = request.args['host']
            ip = request.args['ip']
            port = request.args['port']
            try:
                if request.args['type'] == 'arp'and request.method == 'POST':
                    tabs.getARP(hostname, ip, port, user, password)
                    arp = tabs.viewARP(request.args['host'], request.args['ip'])
                    return render_template('/table/arp.html', devs=devs, arp=arp)
                elif request.args['type'] == 'mac'and request.method == 'POST':
                    tabs.getMAC(hostname, ip, port, user, password)
                    mac = tabs.viewMAC(request.args['host'], request.args['ip'])
                    return render_template('/table/mac.html', devs=devs, mac=mac)
            except:
                flash(u'Falha na requisição', 'error')
                return render_template('/table/arp.html', devs=devs)

    except:
        return render_template('/table/%s.html' % content, devs=devs)

@app.route('/wol/<string:content>', methods=['GET', 'POST'])
def wol(content):
    devs = dev.devTableFiles()
    if  content == 'agendar':
        try:
            if request.args['action'] == 'sched' and request.method == 'POST':
                data = request.form['end']
                horario = request.form['time']
                try:
                    re.search(r'(\d+/\d+/\d+)', data, re.I).group()
                    time.strptime(horario, '%H:%M')
                    today = date.today()
                    if today.strftime("%d/%m/%Y") > data:
                        flash('Erro na Data')
                        return render_template('/wol/%s.html' % content, devs=devs)
                    else:
                        now = datetime.now()
                        if today.strftime("%d/%m/%Y") == data and now.strftime("%H:%M") >= horario:
                            flash('Erro no Horário')
                            return render_template('/wol/%s.html' % content, devs=devs)
                except:
                    flash('Erro no Requisição')
                    return render_template('/wol/%s.html' % content, devs=devs)
                device = request.form.get('device')
                hostname = str(device).split("::")[0]
                ip = str(device).split("::")[1]
                port = str(device).split("::")[2]
                return render_template('/wol/%s.html' % content, devs=devs, action=[hostname, ip, port, data, horario])
            elif request.args['action'] == 'login' and request.method == 'POST':
                hostname = request.args['hostname']
                ip = request.args['ip']
                port = request.args['port']
                user = request.form['username']
                password = request.form['password']
                data = request.args['data']
                horario = str(request.args['time'])
                try:
                    sched.scheduler(hostname, ip, port, user, password, data, horario)
                except:
                    flash('Falha na Autenticação')
                return render_template('/wol/%s.html' % content, devs=devs)
        except:
            return render_template('/wol/%s.html' % content, devs=devs)
    elif content == 'agendados':
        schedulers = sched.schedTableFiles()
        if schedulers != None:
            return render_template('/wol/%s.html' % content, sched=schedulers)
    return render_template('/wol/%s.html' % content, devs=devs)


@app.route('/sched/<string:content>', methods=['POST'])
def schedFunctions(content):
    schedulers = sched.schedTableFiles()
    if content == 'cancel':
        if request.args['action'] == 'sched_cancel':
            hostname = request.args['host']
            ip = request.args['ip']
            id_script = request.args['id_script']
            id_sched = request.args['id_sched']
            data = request.args['data']
            port = request.args['port']
            cancel = [hostname, ip, id_script, id_sched, data, port]
            return render_template('/wol/agendados.html', sched=schedulers, action=cancel)
        elif request.args['action'] == 'login':
            hostname = request.args['host']
            ip = request.args['ip']
            port = request.args['port']
            id_script = request.args['id_script']
            id_sched = request.args['id_sched']
            data = request.args['data']
            user = request.form['username']
            password = request.form['password']
            sched.cancelSched(ip, port, user, password, id_script, id_sched,hostname,data)
            return render_template('/wol/agendados.html', sched=schedulers)

    return render_template('/wol/agendados.html', sched=schedulers)




@app.route('/dev/del/<string:id>',  methods=['POST'])
def delDevice(id):
    dev.delTableindex(id)
    devs = dev.devTableFiles()
    return render_template('/dev/mgmt.html', devs=devs)

@app.route('/login',  methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return redirect('dashboard')
        else:
            flash(u'Login incorreto', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


if __name__ == "__main__":
    app.run(host='0.0.0.0')

