import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")


# Criar o banco de dados
db = client["Agenda"]
colecao = db["contatos"]

def validar_numero(numero):
    numero_str = str(numero)
    if len(numero_str) != 11 or not numero_str.isdigit():
        return False
    return True

def read():
    input_escolha = input("Você deseja visualizar todos os contatos ou apenas um específico? \n T - Todos, \n E - Específico \n ")
    try:
        if input_escolha.lower() == "t":
            resultado = colecao.find()
            print("Contatos:")
            for contato in resultado:
                print(f"Nome: {contato['nome']}, Número: {contato['numero']}")
        elif input_escolha.lower() == "e":
            nome_procurado = input("De quem você deseja saber o número? ")
            filtro = {"nome": nome_procurado}
            resultado = colecao.find_one(filtro)
            if resultado:
                print(f"Nome: {resultado['nome']}, Número: {resultado['numero']}")
            else:
                print("Contato não encontrado.")
        else:
            print("Opção inválida.")
    except ValueError:
        print("Por favor, digite um número inteiro válido.")

def insert():
    nome = input("Nome do contato: ")
    while True:
        numero = int(input("Digite o número (Somente números | Ex: 81999999999): "))
        if validar_numero(numero):
            break
        else:
                print("Número de telefone inválido. Por favor, insira um número válido.")
    documento = {"nome":nome,
                "numero":numero}
    colecao.insert_one(documento)
    print("Número adicionado com sucesso!")

def update():
    resultado = colecao.find()
    print("Contatos:")
    for contato in resultado:
        print(f"Nome: {contato['nome']}, Número: {contato['numero']}")
    nome = input("Nome do contato que você deseja alterar o número: ")
    while True:
        novo_numero = input("Digite o novo número: ")
        if validar_numero(novo_numero):
            break
        else:
                print("Número de telefone inválido. Por favor, insira um número válido.")
    atualizacoes = {"$set":{"numero": novo_numero}}
    filtro = {"nome": nome}
    colecao.update_one(filtro,atualizacoes)
    print("Contato alterado com sucesso!")


def delete():
    nome = input("Nome do contato que você deseja apagar: ")
    filtro = {"nome": nome}
    colecao.delete_one(filtro)
    print("Contato excluído com sucesso!")


def opcao_invalida():
    print("Opção inválida. Por favor, escolha uma opção válida.")


def menu(opcao):
    opcoes = {
        1: read,
        2: insert,
        3: update,
        4: delete
    }


    funcao = opcoes.get(opcao, opcao_invalida)
    funcao()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Escolha uma opção:")
    print("1. Mostrar contato")
    print("2. Inserir contato")
    print("3. Alterar contato")
    print("4. Apagar contato")
    print("0. Sair")
    try:
        escolha = int(input("Digite o número da opção desejada: "))
        if escolha == 0:
            print("Saindo do programa...")
            break
        menu(escolha)
        input("Pressione Enter para voltar ao menu...")
    except ValueError:
        print("Por favor, digite um número inteiro válido.")
