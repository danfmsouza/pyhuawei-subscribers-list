#!/usr/bin/python3
from flask import Flask, request, redirect, render_template, session, jsonify
from flask_httpauth import HTTPBasicAuth
from config import USERNAME, PASSWORD, SECRET_KEY
from vlancounter import VLANCounter
from vlancounter_interface import VLANCounterInterface
from device_manager import DeviceManager
from auth_manager import AuthManager

import xml.etree.ElementTree as ET
import subprocess, json, logging


app = Flask(__name__)
app.secret_key = SECRET_KEY 
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Use uma verificação de token mais robusta na prática
    # Neste exemplo, usaremos um token fixo 'your_token'
    expected_token = app.secret_key
    return expected_token == password

vlancounter: VLANCounterInterface = VLANCounter()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        auth_manager = AuthManager(username, password)
        if auth_manager.authenticate():
            session['logged_in'] = True
            subprocess.run(['python3', '/usr/local/share/pyhuawei/pyhuaweivlan.py'], capture_output=True, text=True)
            return redirect('/')
        else:
            return 'Credenciais inválidas'
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    # INICIAL
    return render_template('index.html')

@app.route('/subs')
def subs():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('subs.html', devices=DeviceManager.get_devices())

@app.route('/vlans')
def vlans():
    if not session.get('logged_in'):
        return redirect('/login')
    vlancounter.reset_counts()  # Zera os contadores antes de iniciar uma nova iteração
    vlancounter.count_vlans()  # Conta as VLANs
    return render_template('vlans.html', devices=DeviceManager.get_devices(), vlan_count=vlancounter.get_counts())

@app.route('/getVlans')
#@auth.login_required
def get_vlans():
    vlancounter.reset_counts()  # Zera os contadores antes de iniciar uma nova iteração
    vlancounter.count_vlans()  # Conta as VLANs

    vlan_counts = vlancounter.get_counts() 

    # Converte o dicionário de contagens em uma lista de objetos LLD
    lld_data = [{"VLAN": vlan, "COUNT": data['count'], "INTERFACE": data['interface']} for vlan, data in vlan_counts.items()]

    return jsonify({"data": lld_data})  # Retorna o formato LLD do Zabbix

@app.route('/refresh')
def refresh():
    if not session.get('logged_in'):
        return redirect('/login')
    back = request.referrer
    subprocess.run(['python3', '/usr/local/share/pyhuawei/pyhuaweivlan.py'], capture_output=True, text=True)
    return redirect(back)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
