import os
from neo4j import GraphDatabase
from cadastrar import insertCliente, insertVendedor, insertEndereco, insertCompra, insertFavorito, insertProduto
from listar import listar_clientes, listar_produtos, listar_vendedores

uri = "neo4j+ssc://9c671abc.databases.neo4j.io"
user = "neo4j"
password = "ih09QaNZ1RCmKT67lpHPZLZASDicB6ZQqHRO2ZJTfME"

driver = GraphDatabase.driver(uri, auth=(user, password))

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

while True:
    print("""
          
➕ CADASTRAR
------------------------------------------------------------
|  1  | 👤 Cliente            |  2  | 🛒 Vendedor
|  3  | 🏠 Endereço           |  4  | 📦 Produto
|  5  | 🛒 Compra             |  6  | ⭐ Favoritar
------------------------------------------------------------

🔍 CONSULTAR
------------------------------------------------------------
|  7  | 📄 Clientes           |  8  | 📄 Vendedores
|  9  | 📦 Produtos
============================================================
|  0  | ❌ Sair
============================================================
    """)
    
    try:
        opcao = int(input("Digite a opção desejada: "))
    except ValueError:
        limpar()
        print("Por favor, digite um número.")
        continue

    limpar()

    if opcao == 1:
        insertCliente(driver)
    
    elif opcao == 2:
        insertVendedor(driver)
    
    elif opcao == 3:
        try:
            usuario = int(input("Deseja cadastrar o endereço para qual tipo de usuário? (1-Cliente / 2-Vendedor): ").strip())
        except ValueError:
            limpar()
            print("Por favor, digite um número válido.")
            continue
        match usuario:
            case 1:
                cpf = input("Digite o CPF do Cliente: ").strip()
                insertEndereco(driver, cpf, "Cliente")
            case 2:
                cpf = input("Digite o CPF do Vendedor: ").strip()
                insertEndereco(driver, cpf, "Vendedor")

    elif opcao == 4:
        insertProduto(driver)

    elif opcao == 5:
        cpf = input("Digite o CPF do Cliente que fará a compra: ").strip()
        insertCompra(driver, cpf)
    
    elif opcao == 6:
        cpf = input("Digite o CPF do Cliente: ").strip()
        insertFavorito(driver, cpf)

    elif opcao == 7:
        listar_clientes(driver)
        input("\nPressione Enter para voltar...")

    elif opcao == 8:
        listar_vendedores(driver)
        input("\nPressione Enter para voltar...")

    elif opcao == 9:
        listar_produtos(driver)
        input("\nPressione Enter para voltar...")

    elif opcao == 0:
        print("Fechando conexão...")
        driver.close()
        break
        
    else:
        print("Opção inválida.")