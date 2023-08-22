import xml.etree.ElementTree as ET
import os

def main():
    if not os.path.exists("vlans.xml"):
        create_xml_file()

    while True:
        print("\nEscolha uma operação:")
        print("1. Criar VLAN")
        print("2. Listar VLANs")
        print("3. Atualizar VLAN")
        print("4. Deletar VLAN")
        print("5. Sair")

        choice = input("Digite o número da operação desejada: ")

        if choice == "1":
            create_vlan()
        elif choice == "2":
            list_vlans()
        elif choice == "3":
            update_vlan()
        elif choice == "4":
            delete_vlan()
        elif choice == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")

def create_vlan():
    vlan_id = int(input("Digite o ID da VLAN: "))
    name = input("Digite o nome da VLAN: ")

    vlans_list = load_vlans()
    vlan_id_set = {int(vlan.find("ID").text) for vlan in vlans_list}

    if vlan_id in vlan_id_set:
        print("Esse ID já está em uso. Digite um ID diferente.")
        return

    vlan = ET.Element("Vlan")
    name_element = ET.SubElement(vlan, "Name")
    id_element = ET.SubElement(vlan, "ID")

    name_element.text = name
    id_element.text = str(vlan_id)

    tree = ET.parse("vlans.xml")
    root = tree.getroot()
    root.append(vlan)
    tree.write("vlans.xml", encoding="utf-8", xml_declaration=True)

    print("VLAN adicionada com sucesso!")

def list_vlans():
    vlans_list = load_vlans()

    if not vlans_list:
        print("Nenhuma VLAN encontrada.")
    else:
        for vlan in vlans_list:
            print(f"ID: {vlan.find('ID').text}, Nome: {vlan.find('Name').text}")

def update_vlan():
    vlan_id = int(input("Digite o ID da VLAN que deseja atualizar: "))
    name = input("Digite o novo nome da VLAN: ")

    vlans_list = load_vlans()
    vlan_found = False

    for vlan in vlans_list:
        if int(vlan.find("ID").text) == vlan_id:
            vlan.find("Name").text = name
            save_vlans(vlans_list)
            print("VLAN atualizada com sucesso!")
            vlan_found = True
            break

    if not vlan_found:
        print("VLAN não encontrada.")

def delete_vlan():
    vlan_id = int(input("Digite o ID da VLAN que deseja excluir: "))

    vlans_list = load_vlans()
    vlan_found = False

    for vlan in vlans_list:
        if int(vlan.find("ID").text) == vlan_id:
            vlans_list.remove(vlan)
            save_vlans(vlans_list)
            print("VLAN excluída com sucesso!")
            vlan_found = True
            break

    if not vlan_found:
        print("VLAN não encontrada.")

def create_xml_file():
    vlans = ET.Element("Vlans")
    tree = ET.ElementTree(vlans)
    tree.write("vlans.xml", encoding="utf-8", xml_declaration=True)

def load_vlans():
    try:
        with open("vlans.xml", "r") as file:
            return ET.fromstring(file.read())
    except FileNotFoundError:
        return []

def save_vlans(vlans_list):
    tree = ET.ElementTree(vlans_list)
    tree.write("vlans.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
