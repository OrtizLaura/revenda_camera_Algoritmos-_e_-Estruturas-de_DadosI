import requests
import matplotlib.pyplot as plt
import numpy as np
import pwinput

url = "http://localhost:3000/cameras"
url_login = "http://localhost:3000/login"

usuario_id = ""
token = ""

def login():
    titulo("Login do Usuário")

    email = input("E-mail...: ")
    senha = pwinput.pwinput(prompt='Senha....: ')

    response = requests.post(url_login, json={
        "email": email,
        "senha": senha
    })

    if response.status_code == 200:
        resposta = response.json()
        global usuario_id
        global token
        usuario_id = resposta['id']
        token = resposta['token']
        print(f"Ok! Bem-vindo {resposta['nome']}")
    else:
        print("Erro... Não foi possível realizar login no sistema")


def inclusao():
    titulo("Inclusão de Câmeras", "=")

    if token == "":
        print("Erro... Você precisa fazer login para incluir câmeras")
        return

    modelo = input("Modelo......: ")
    marca = input("Marca.......: ")
    ano = int(input("Ano.........: "))
    preco = float(input("Preço R$....: "))
    classificacao = input("Classificacao.........: ")

    response = requests.post(url,
                             headers={"Authorization": f"Bearer {token}"},
                             json={
                                 "modelo": modelo,
                                 "marca": marca,
                                 "ano": ano,
                                 "preco": preco,
                                 "classificacao": classificacao,
                                 "usuarioId": usuario_id
                             })

    if response.status_code == 201:
        camera = response.json()
        print(f"Ok! Câmera cadastrada com código: {camera['id']}")
    else:
        print("Erro... Não foi possível incluir a câmera")


def listagem():
    titulo("Listagem das Câmeras Cadastradas")

    response = requests.get(url)

    if response.status_code != 200:
        print("Erro... Não foi possível acessar a API")
        return

    cameras = response.json()

    print("Cód. Modelo.............: Marca.........: Ano:......... Preço R$:")
    print("--------------------------------------------------------")

    for camera in cameras:
        print(
            f"{camera['id']:4d} {camera['modelo']:20s} {camera['marca']:15s} {camera['ano']:4d} {float(camera['preco']):9.2f}")


def alteracao():
    listagem()

    if token == "":
        print("Erro... Você precisa fazer login para alterar câmeras")
        return

    id = int(input("\nQual o código da câmera a alterar? "))

    response = requests.get(url)
    cameras = response.json()

    camera = [x for x in cameras if x['id'] == id]

    if len(camera) == 0:
        print("Erro... Informe um código existente")
        return

    print(f"\nModelo..: {camera[0]['modelo']}")
    print(f"Marca...: {camera[0]['marca']}")
    print(f"Ano.....: {camera[0]['ano']}")
    print(f"Preço R$: {float(camera[0]['preco']):9.2f}")

    novoPreco = float(input("Novo Preço R$: "))

    response = requests.put(url+"/"+str(id),
                              headers={"Authorization": f"Bearer {token}"},
                              json={"preco": novoPreco, "modelo": camera[0]['modelo'], "marca": camera[0]['marca'], "ano": camera[0]['ano'], "classificacao": camera[0]['classificacao'], "usuarioId": usuario_id})

    if response.status_code == 200:
        camera = response.json()
        print("Ok! Câmera alterada com sucesso!")
    else:
        print("Erro... Não foi possível alterar o preço da câmera")


def exclusao():
    if token == "":
        print("Erro... Você precisa fazer login para excluir câmeras")
        return

    listagem()

    id = int(input("\nQual código da câmera você deseja excluir (0: sair)? "))

    if id == 0:
        return

    response = requests.get(url)
    cameras = response.json()

    camera = [x for x in cameras if x['id'] == id]

    if len(camera) == 0:
        print("Erro... Informe um código existente")
        return

    print(f"\nModelo..: {camera[0]['modelo']}")
    print(f"Marca...: {camera[0]['marca']}")
    print(f"Ano.....: {camera[0]['ano']}")
    print(f"Preço R$: {float(camera[0]['preco']):9.2f}")

    confirma = input("Confirma a exclusão (S/N)? ").upper()

    if confirma == "S":
        response = requests.delete(url+"/"+str(id), 
                                   headers={"Authorization": f"Bearer {token}"})

        if response.status_code == 200:
            camera = response.json()
            print("Ok! Câmera excluída com sucesso!")
        else:
            print("Erro... Não foi possível excluir esta câmera")


def grafico():
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro... Não foi possível acessar a API")
        return

    cameras = response.json()
    labels = list(set([x['marca'] for x in cameras]))
    sizes = [0] * len(labels)

    for camera in cameras:
        index = labels.index(camera['marca'])
        sizes[index] += 1

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_title('Nº câmeras por Marca')
    plt.gcf().canvas.manager.set_window_title("Gráfico por Marcas")
    ax.pie(sizes, labels=labels)
    plt.show()


def grafico2():
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro... Não foi possível acessar a API")
        return

    cameras = response.json()
    soma_valores = {}

    for item in cameras:
        marca = item['marca']
        valor = float(item['preco'])
        if marca in soma_valores:
            soma_valores[marca] += valor
        else:
            soma_valores[marca] = valor

    
    marcas = list(soma_valores.keys())
    valores = list(soma_valores.values())

    
    plt.figure(figsize=(9, 5))
    plt.bar(marcas, valores, color=["blue", "orange"])
    plt.title("Soma dos Valores das Câmeras por Marca")
    plt.xlabel("Marca")
    plt.ylabel("Soma dos preços")
    plt.show()

def titulo(texto, traco="-"):
    print()
    print(texto)
    print(traco*40)


while True:
    titulo("Cadastro de câmeras")
    print("1. Login do Usuário")
    print("2. Inclusão de câmeras")
    print("3. Listagem de câmeras")
    print("4. Alteração de Preço")
    print("5. Exclusão de câmera")
    print("6. Gráfico de Marcas (Pizza)")
    print("7. Gráfico de Marcas (Colunas Empilhadas)")
    print("8. Finalizar")
    opcao = int(input("Opção: "))
    if opcao == 1:
        login()
    elif opcao == 2:
        inclusao()
    elif opcao == 3:
        listagem()
    elif opcao == 4:
        alteracao()
    elif opcao == 5:
        exclusao()
    elif opcao == 6:
        grafico()
    elif opcao == 7:
        grafico2()
    else:
        break
