#!/usr/bin/python3

from config import ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT, ROUTER_IP
import xml.etree.ElementTree as ET
import paramiko
import sys
import re
import json
import xmltodict

# Configurações do SSH
router_ip = ROUTER_IP
router_port = ROUTER_PORT
ssh_username = ROUTER_USERNAME
ssh_password = ROUTER_PASSWORD

interfaces = ["Gi0/3/9.5000", "Gi0/3/9.5002"]

# Dicionário para armazenar os dados das interfaces
interface_data = {}

for interface in interfaces:
    # Comando que você deseja executar
    command = f"display access-user interface {interface} brief | no-more"

    # Executar o comando via SSH e obter a saída
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, port=router_port, username=ssh_username, password=ssh_password)

        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        output = stdout.read().decode()

        ssh_client.close()

    except paramiko.AuthenticationException:
        print("Erro de autenticação. Verifique o usuário e senha SSH.")
        sys.exit(1)

    except paramiko.SSHException as e:
        print(f"Erro SSH: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Erro ao executar comando via SSH: {e}")
        sys.exit(1)

    # Encontrar as linhas com os dados relevantes usando expressões regulares
    pattern = r"\d+\s+\S+\s+GE\S+\s+\S+\s+\S+\s+\S+\s+\S+"
    data_lines = re.findall(pattern, output)

    # Adicionar os dados ao dicionário da interface correspondente
    interface_data[interface] = []

    for line in data_lines:
        data = line.split()
        if len(data) == 7:
            # Remover os caracteres '/-' do campo Vlan
            vlan = data[6].replace('/-', '')
            interface_data[interface].append({
                'UserID': data[0],
                'Username': data[1],
                'Interface': data[2],
                'IPAddress': data[3],
                'IPv6Address': data[4],
                'MAC': data[5],
                'Vlan': vlan
            })

# Criar a estrutura XML e JSON final com os dados acumulados
root = ET.Element('Devices')
final_json_data = []

for interface, devices in interface_data.items():
    for device in devices:
        device_elem = ET.SubElement(root, 'Device')
        ET.SubElement(device_elem, 'UserID').text = device['UserID']
        ET.SubElement(device_elem, 'Username').text = device['Username']
        ET.SubElement(device_elem, 'Interface').text = device['Interface']
        ET.SubElement(device_elem, 'IPAddress').text = device['IPAddress']
        ET.SubElement(device_elem, 'IPv6Address').text = device['IPv6Address']
        ET.SubElement(device_elem, 'MAC').text = device['MAC']
        ET.SubElement(device_elem, 'Vlan').text = device['Vlan']

        final_json_data.append(device)

# Salvar a árvore XML em um arquivo
xml_file = '/usr/local/share/pyhuawei/devices.xml'
tree = ET.ElementTree(root)
tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# Salvar o JSON final em um arquivo
json_file = '/usr/local/share/pyhuawei/devices.json'
with open(json_file, 'w') as json_out:
    json.dump(final_json_data, json_out, indent=4)

print(f"Arquivo JSON gerado: {json_file}")
print(f"Arquivo XML gerado: {xml_file}")


