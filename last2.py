from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import locale

produto = input("Produto: ")


# ------------------------------------------------------------- SUBMARINO
url_submarino = "https://www.submarino.com.br/busca/" + produto 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

pagina_submarino = requests.get(url_submarino, headers=headers)
html_submarino = BeautifulSoup(pagina_submarino.content, "html.parser")

div_produtos_submarino = html_submarino.find("div", class_="grid__StyledGrid-sc-1man2hx-0 iFeuoP src__GridItem-sc-cyp7mw-0 dpeJTS")
produtos_submarino = div_produtos_submarino.find_all("h3", class_="product-name__Name-sc-1shovj0-0 htEpFr")
descontos_submarino = div_produtos_submarino.find_all("span", class_="src__Text-sc-154pg0p-0 price__Price-sc-h6xgft-0 JbUli")
preco_submarino = div_produtos_submarino.find_all("span", class_="src__Text-sc-154pg0p-0 price__PromotionalPrice-sc-h6xgft-1 ctBJlj price-info__ListPriceWithMargin-sc-1xm1xzb-2 liXDNM")
produtos_com_desconto = []

for i in range(len(produtos_submarino)):
    titulo = produtos_submarino[i].get_text().strip()
    preco = preco_submarino[i].get_text().strip()
    desconto = descontos_submarino[i].get_text().strip() if i < len(descontos_submarino) else "Sem desconto"
    produtos_com_desconto.append({"titulo": titulo, "desconto": desconto, "preco": preco})


# ------------------------------------------------------------- MAGAZINE LUIZA
url_magazine = "https://www.magazineluiza.com.br/busca/" + produto

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

pagina_magazine = requests.get(url_magazine, headers=headers)
html_magazine = BeautifulSoup(pagina_magazine.content, "html.parser")
div_produtos_magazine = html_magazine.find("div", class_="sc-fqkvVR sPxxI sc-APcvf feaSJL")
produtos_magazine = div_produtos_magazine.find_all("h2", class_="sc-ZEldx llMBjh")
desconto_magazine = div_produtos_magazine.find_all("p", class_="sc-kpDqfm efxPhd sc-fUBkdm hrUkqj")
preco_magazine = div_produtos_magazine.find_all("p", class_="sc-kpDqfm eCPtRw sc-hBtRBD fPPQXa")


produtos = []
descontos_m = []
precos_m = []



for h2 in  produtos_magazine:
        produtos.append({"titulo": h2.get_text().strip()})

for p in desconto_magazine:
        descontos_m.append({"desconto": p.get_text().strip()})

for p in preco_magazine:
        precos_m.append({"preco": p.get_text().strip()})

produtos_com_desconto2 = []

for i in range(len(produtos)):
        titulo = produtos[i]["titulo"]
        if i < len(descontos_m):
            desconto = descontos_m[i]["desconto"]
        else:
            desconto = "Sem desconto"
        preco = precos_m[i]["preco"]
        produtos_com_desconto2.append({"titulo": titulo, "desconto": desconto, "preco": preco})

def titulo(msg, traco="-"):
    print()
    print(msg)
    print(traco*50)

produtos_com_desconto_total = produtos_com_desconto + produtos_com_desconto2

def lista_submarino():
     titulo("Produtos na Submarino")
     table_data = []
     headers = ["Nome do produto", "Valor sem Desconto", "Valor com Desconto"]

     for produto in produtos_com_desconto:
        tituloo = produto['titulo']
        desconto = produto['desconto']
        preco = produto['preco']
        table_data.append([tituloo, desconto, preco])

     print(tabulate(table_data, headers, tablefmt="grid"))

def lista_magazine():
    titulo(f"Produtos em Magazine Luiza")

    table_data = []
    headers = ["Nome do produto", "Valor sem Desconto", "Valor com Desconto"]

    for produto in produtos_com_desconto2:
        tituloo = produto['titulo']
        desconto = produto['desconto']
        preco = produto['preco']
        table_data.append([tituloo, desconto, preco])

    print(tabulate(table_data, headers, tablefmt="grid"))
   
def lista_todos():
    todos = set()
    
    for produtos in produtos_com_desconto:
        todos.add(produtos['titulo'])
    
    for produtos in produtos_com_desconto2:
        todos.add(produtos['titulo'])
    
    lista = list(todos)
    lista2 = sorted(lista)
    
    titulo(f"Todos os produtos desejados")
    
    for produtos in lista2:
        print(produtos)

def onlymagazine():
    set_submarino = set()     
    set_magazine = set()

    for produtos in produtos_com_desconto:
        set_magazine.add(produtos['titulo'])

    for produtos in produtos_com_desconto2:
        set_submarino.add(produtos['titulo'])

    em_magazine = set_magazine.difference(set_submarino)

    titulo("Produtos apenas de Magazine Luiza")

    if len(em_magazine) == 0:
        print("Obs.: * Não há produtos em Magaine Luiza")
    else:
        for produtos in em_magazine:
            print(produtos)


def onlysubmarino():
    set_submarino = set()     
    set_magalu = set()

    for produtos in produtos_com_desconto2:
        set_magalu.add(produtos['titulo'])

    for produtos in produtos_com_desconto:
        set_submarino.add(produtos['titulo'])

    em_submarino = set_submarino.difference(set_magalu)

    titulo("Produtos apenas de Submarino")

    if len(em_submarino) == 0:
        print("Obs.: * Não há produtos em Submarino")
    else:
        for produtos in em_submarino:
            print(produtos)

def total():
    total_preco = 0

    for produto in produtos_com_desconto_total:
        preco = produto['preco']
        preco_numerico = round(float(preco.replace("R$", "").replace(".", "").replace(",", ".")), 2)

        total_preco += preco_numerico

    titulo("Totalização de preços Submarino e Magazine Luiza")
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    preco_formatado = locale.currency(total_preco, grouping=True, symbol="R$")
    print("Total de Preços:", preco_formatado)


def agrupar_sem_desconto():
    dicionario = {}
    for produto in produtos_com_desconto_total:
        if produto["desconto"] == "Sem desconto":
            chave = dicionario.get(produto["desconto"], None)
            if chave == None:
                dicionario[produto["desconto"]] = produto["titulo"]
            else:
                dicionario[produto["desconto"]] = chave + ", " + produto["titulo"]

    ordenados = sorted(dicionario.items(), key=lambda c : c[0])
    
    for (desconto, titulo) in ordenados:
        print(f"{desconto}: {titulo}")

def pesq_preco():
    valor_maximo = float(input("Valor máximo: "))
    produtos = []

    for produto in produtos_com_desconto_total:
        preco = float(produto["preco"].replace("R$", "").replace(".", "").replace(",", "."))

        if preco <= valor_maximo:
            produtos.append(produto)

    if len(produtos) == 0:
        print("Nenhum produto encontrado dentro do valor máximo.")
    else:
        print(f"Produtos com valor até R${valor_maximo:.2f}:")
        for produto in produtos:
            print(f" {produto['titulo']}")
            print(f" Preço com desconto: {produto['preco']}")
            print()

def comum():
    set_submarino = set()     
    set_magazine = set()

    for produtos in produtos_com_desconto:
        set_submarino.add(produtos['titulo'])

    for produtos in produtos_com_desconto2:
        set_magazine.add(produtos['titulo'])

    comuns = set_submarino.intersection(set_magazine)

    titulo("Produtos disponiveis em ambos os sites")

    if len(comuns) == 0:
        print("Obs.: * Não há produtos comuns aos dois sites")
    else:
        for produtos in comuns:
            print(produtos)


while True:
    titulo("Produtos")    
    print("1. Produtos Submarino")
    print("2. Produtos Magazine Luiza")
    print("3. Todos os produtos")
    print("4. Apenas em Submarino")
    print("5. Apenas em Magazine Luiza")
    print("6. Comuns nos dois sites")
    print("7. Total de preços nos dois sites")    
    print("8. Pesquisa produtos por valor")    
    opcao = int(input("Opção: "))
    if opcao == 1:
        lista_submarino()
    elif opcao == 2:
        lista_magazine()
    elif opcao == 3:
        lista_todos()
    elif opcao == 4:
        onlysubmarino()
    elif opcao == 5:
        onlymagazine()
    elif opcao == 6:
        comum()
    elif opcao == 7:
        total()
    elif opcao == 8:
        pesq_preco()
    else:
        break
