import os
from neo4j import GraphDatabase
from cadastrar import insertCliente, insertVendedor, insertEndereco, insertCompra, insertFavorito, insertProduto
from listar import findClientes, findVendedores, findProdutos, findCompras

uri = "neo4j+ssc://9c671abc.databases.neo4j.io"
user = "neo4j"
password = "ih09QaNZ1RCmKT67lpHPZLZASDicB6ZQqHRO2ZJTfME"

driver = GraphDatabase.driver(uri, auth=(user, password))

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def buscar(tx, cpf, tipo):
    result = tx.run("MATCH (n:" + tipo + " {cpf: $cpf}) RETURN n LIMIT 1", cpf=cpf)
    return result.single()

while True:
    print("""
          
➕ CADASTRAR
------------------------------------------------------------
|  1  | 👤 Cliente            |  2  | 🧑‍💼 Vendedor
|  3  | 🏠 Endereço           |  4  | 📦 Produto
|  5  | 🧾 Compra             |  6  | ⭐ Favoritar
------------------------------------------------------------

🔍 CONSULTAR
------------------------------------------------------------
|  7  | 👤 Clientes           |  8  | 🧑‍💼 Vendedores
|  9  | 📦 Produtos           |  10 | 🧾 Compras
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
                    try:
                        if session.execute_read(buscar, cpf, "Cliente") is None:
                            limpar()
                            print("Cliente não encontrado.")
                            continue
                        insertEndereco(driver, cpf, "Cliente")
                    except Exception as e:
                        limpar()
                        print("Erro ao adicionar endereço:", e)
            case 2:
                with driver.session() as session:
                    cpf = input("Digite o CPF do Vendedor: ").strip()
                    try:
                        if session.execute_read(buscar, cpf, "Vendedor") is None:
                            limpar()
                            print("Vendedor não encontrado.")
                            continue
                        insertEndereco(driver, cpf, "Vendedor")
                    except Exception as e:
                        limpar()
                        print("Erro ao adicionar endereço:", e)

    elif opcao == 4:
        with driver.session() as session:
            cpf = input("Digite o CPF do Vendedor que cadastrará o produto: ").strip()
            try:
                if session.execute_read(buscar, cpf, "Vendedor") is None:
                    limpar()
                    print("Vendedor não encontrado.")
                    continue
            except Exception as e:
                limpar()
                print("Erro ao buscar vendedor:", e)
                continue
            insertProduto(driver, cpf)

    elif opcao == 5:
        with driver.session() as session:
            cpf = input("Digite o CPF do Cliente que fará a compra: ").strip()
            try:
                if session.execute_read(buscar, cpf, "Cliente") is None:
                    limpar()
                    print("Cliente não encontrado.")
                    continue
                insertCompra(driver, cpf)
            except Exception as e:
                limpar()
                print("Erro ao adicionar compra:", e)
    
    elif opcao == 6:
        with driver.session() as session:
            cpf = input("Digite o CPF do Cliente: ").strip()
            try:
                if session.execute_read(buscar, cpf, "Cliente") is None:
                    limpar()
                    print("Cliente não encontrado.")
                    continue
                insertFavorito(driver, cpf)
            except Exception as e:
                limpar()
                print("Erro ao adicionar favorito:", e)

    elif opcao == 7:
        findClientes(driver)

    elif opcao == 8:
        findVendedores(driver)

    elif opcao == 9:
        findProdutos(driver)

    elif opcao == 10:
        findCompras(driver)

    elif opcao == 0:
        print("Fechando conexão...")
        driver.close()
        break
        
    else:
        print("Opção inválida.")