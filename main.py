import os
from neo4j import GraphDatabase
from cadastrar import insertCliente, insertVendedor, insertEndereco, insertCompra, insertFavorito, insertProduto
from listar import findClientes, findVendedores, findProdutos

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
    
    opcao = int(input("Digite a opção desejada: "))

    limpar()

    if opcao == 1:
        insertCliente(driver)
    
    elif opcao == 2:
        insertVendedor(driver)
    
    elif opcao == 3:
        try:
            print("1 - Cliente\n2 - Vendedor")
            usuario = int(input("Digite o tipo de usuário para adicionar o endereço: "))
            if usuario not in [1, 2]:
                    raise ValueError
        except ValueError:
            limpar()
            print("Por favor, digite um número válido.")
            continue
        match usuario:
            case 1:
                with driver.session() as session:
                    cpf = input("Digite o CPF do Cliente: ").strip()
                    if session.execute_read("MATCH (n:Cliente {cpf: $cpf}) RETURN n LIMIT 1", cpf=cpf).single() is None:
                        limpar()
                        print("Cliente não encontrado.")
                        continue
                    insertEndereco(session, cpf, "Cliente")
            case 2:
                with driver.session() as session:
                    cpf = input("Digite o CPF do Vendedor: ").strip()
                    if session.execute_read("MATCH (n:Vendedor {cpf: $cpf}) RETURN n LIMIT 1", cpf=cpf).single() is None:
                        limpar()
                        print("Vendedor não encontrado.")
                        continue
                    insertEndereco(session, cpf, "Vendedor")

    elif opcao == 4:
        with driver.session() as session:
            
            insertProduto(session)

    elif opcao == 5:
        with driver.session() as session:
            cpf = input("Digite o CPF do Cliente que fará a compra: ").strip()
            if session.execute_read("MATCH (n:Cliente {cpf: $cpf}) RETURN n LIMIT 1", cpf=cpf).single() is None:
                limpar()
                print("Cliente não encontrado.")
                continue
            insertCompra(session, cpf)
    
    elif opcao == 6:
        with driver.session() as session:
            cpf = input("Digite o CPF do Cliente: ").strip()
            if session.execute_read("MATCH (n:Cliente {cpf: $cpf}) RETURN n LIMIT 1", cpf=cpf).single() is None:
                limpar()
                print("Cliente não encontrado.")
                continue
            insertFavorito(session, cpf)
    elif opcao == 7:
        findClientes(driver)
        input("\nPressione Enter para voltar...")

    elif opcao == 8:
        findVendedores(driver)
        input("\nPressione Enter para voltar...")

    elif opcao == 9:
        findProdutos(driver)
        input("\nPressione Enter para voltar...")

    elif opcao == 0:
        print("Fechando conexão...")
        driver.close()
        break
        
    else:
        print("Opção inválida.")