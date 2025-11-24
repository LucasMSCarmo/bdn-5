import os
import hashlib
from cadastrar import insertCliente, insertVendedor, insertEndereco, insertCompra, insertFavorito, insertProduto
from consultar import findCliente, findFavoritos, findCompras, findVendedor, findProdutosVendedor
from atualizar import updateDados, updateEndereco, updateProduto
from deletar import deleteEndereco, deleteFavorito, deleteUsuario, deleteEndereco, deleteProduto
from listar import findClientes, findProdutos, findVendedores
from neo4j import GraphDatabase

uri = "neo4j+s://9c671abc.databases.neo4j.io"
user = "neo4j"
password = "ih09QaNZ1RCmKT67lpHPZLZASDicB6ZQqHRO2ZJTfME"

# Driver simples, conexão segura automática
driver = GraphDatabase.driver(uri, auth=(user, password))

def ping(tx):
    result = tx.run("RETURN 1 AS ping")
    return result.single()["ping"]

with driver.session() as session:
    resposta = session.execute_read(ping)

print(f"Conexão OK! Ping retornou: {resposta}")

# def limpar():
#     os.system("cls" if os.name == "nt" else "clear")

# def login(conexao):
#     while True:
#         email = input("Email: ")
#         senha = hashlib.sha256(input("Senha: ").encode()).hexdigest()
#         usuario = conexao.find_one({"email": email, "senha": senha})
#         if usuario:
#             limpar()
#             print(f"\nBem-vindo, {usuario['nome']}!")
#             break
#         else:
#             print("Email ou senha incorretos.")
#             if input("Tentar novamente? (s/n): ").lower() != 's':
#                 break
#             limpar()
#     return usuario


# def menuCliente(cliente):
#     while True:
#         print("""
# ============================================================
#                 SISTEMA DE GERENCIAMENTO
# ============================================================

# ➕ CADASTRAR
# ------------------------------------------------------------
# |  1  | 🛒 Compra          |  2  | 🏠 Endereço
# |  3  | ⭐ Favoritos
# ------------------------------------------------------------

# 🔍 CONSULTAR
# ------------------------------------------------------------
# |  4  | 👤 Perfil          |  5  | ⭐ Favoritos
# |  6  | 🛒 Compras
# ------------------------------------------------------------

# 🔄 ATUALIZAR
# ------------------------------------------------------------
# |  7  | 👤 Dados pessoais  |  8  | 🏠 Endereço
# ------------------------------------------------------------

# 🗑️  DELETAR
# ------------------------------------------------------------
# |  9  | 🏠 Endereço        |  10 | ⭐ Favoritos
# |  11 | ❌ Conta
# ============================================================
# 🔚 SISTEMA
# ------------------------------------------------------------
# |  0  | ❌ Logout
# ============================================================
#     """)
#         opcao = int(input("Digite a opção desejada: "))
#         limpar()

#         if opcao == 1:
#             print("\n--- REALIZAR COMPRA ---\n")
#             produtos_disponiveis = findProdutos(mydb.vendedor, 'compra')
#             if produtos_disponiveis:
#                 compra = insertCompra(mydb, cliente['_id'], produtos_disponiveis)
#                 if compra:
#                     cliente['compras'].append(compra)
#         elif opcao == 2:
#             print("\n--- CADASTRAR ENDEREÇO ---\n")
#             enderecos = insertEndereco(mydb.cliente, cliente['_id'])
#             if enderecos:
#                 cliente['enderecos'].extend(enderecos)
#         elif opcao == 3:
#             print("\n--- CADASTRAR FAVORITO ---\n")
#             produtos_disponiveis = findProdutos(mydb.vendedor, 'favorito')
#             if produtos_disponiveis:
#                 favoritos = insertFavorito(mydb.cliente, cliente['_id'], produtos_disponiveis)
#                 if favoritos:
#                     cliente['favoritos'].extend(favoritos)
#         elif opcao == 4:
#             print("\n--- PERFIL DO USUÁRIO ---\n")
#             findCliente(cliente)
#         elif opcao == 5:
#             print("\n--- FAVORITOS ---\n")
#             findFavoritos(cliente['favoritos'])
#         elif opcao == 6:
#             print("\n--- MINHAS COMPRAS ---\n")
#             findCompras(mydb.compra, cliente['nome'], cliente['compras'])
#         elif opcao == 7:
#             print("\n--- ATUALIZAR DADOS PESSOAIS ---\n")
#             dados = updateDados(mydb.cliente, cliente)
#             if dados:
#                 for dado in dados:
#                     cliente[dado] = dados[dado]
#         elif opcao == 8:
#             print("\n--- ATUALIZAR ENDEREÇO ---\n")
#             endereco = updateEndereco(mydb.cliente, cliente['_id'], cliente['enderecos'])
#             if endereco:
#                 for endereco_atual in cliente['enderecos']:
#                     if endereco_atual['_id'] == endereco['_id']:
#                         endereco_atual.update(endereco)
#                         break
#         elif opcao == 9:
#             print("\n--- DELETAR ENDEREÇO ---\n")
#             enderecos = deleteEndereco(mydb.cliente, cliente['_id'], cliente['enderecos'])
#             if enderecos:
#                 for endereco in enderecos:
#                     cliente['enderecos'].remove(endereco)
#         elif opcao == 10:
#             print("\n--- DELETAR FAVORITOS ---\n")
#             favoritos = deleteFavorito(mydb.cliente, cliente['_id'], cliente['favoritos'])
#             if favoritos:
#                 for favorito in favoritos:
#                     cliente['favoritos'].remove(favorito)
#         elif opcao == 11:
#             print("\n--- DELETAR CONTA ---\n")
#             resultado = deleteUsuario(mydb.cliente, cliente['_id'])
#             if resultado:
#                 break
#         elif opcao == 0:
#             break
#         else:
#             print("Opção inválida.")
    
# def menuVendedor(vendedor):
#     while True:
#         print("""
# ============================================================
#                 SISTEMA DE GERENCIAMENTO
# ============================================================

# ➕ CADASTRAR
# ------------------------------------------------------------
# |  1  | 📦 Produto         |  2  | 🏠 Endereço
# ------------------------------------------------------------
              
# 🔍 CONSULTAR
# ------------------------------------------------------------
# |  3  | 📦 Meus Produtos   |  4  | 👤 Perfil
# ------------------------------------------------------------

# 🔄 ATUALIZAR
# ------------------------------------------------------------
# |  5  | 👤 Dados pessoais  |  6  | 🏠 Endereço
# |  7  | 📦 Produto
# ------------------------------------------------------------

# 🗑️  DELETAR
# ------------------------------------------------------------
# |  8  | 🏠 Endereço        |  9  | 🛒 Produto
# |  10 | ❌ Conta
# ============================================================
# 🔚 SISTEMA
# ------------------------------------------------------------
# | 0  | ❌ Logout
# ============================================================
#     """)
#         opcao = int(input("Digite a opção desejada: "))
#         limpar()
#         if opcao == 1:
#             print("\n--- CADASTRAR PRODUTO ---\n")
#             produtos = insertProduto(mydb.vendedor, vendedor['_id'])
#             if produtos:
#                 vendedor['produtos'].extend(produtos)
#         elif opcao == 2:
#             print("\n--- CADASTRAR ENDEREÇO ---\n")
#             enderecos = insertEndereco(mydb.vendedor, vendedor['_id'])
#             if enderecos:
#                 vendedor['enderecos'].extend(enderecos)
#         elif opcao == 3:
#             print("\n--- LISTA DE PRODUTOS ---\n")
#             findProdutosVendedor(vendedor['produtos'])
#         elif opcao == 4:
#             print("\n--- PERFIL DO VENDEDOR ---\n")
#             findVendedor(vendedor)
#         elif opcao == 5:
#             print("\n--- ATUALIZAR DADOS PESSOAIS ---\n")
#             dados = updateDados(mydb.vendedor, vendedor)
#             if dados:
#                 for dado in dados:
#                     vendedor[dado] = dados[dado]
#         elif opcao == 6:
#             print("\n--- ATUALIZAR ENDEREÇO ---\n")
#             endereco = updateEndereco(mydb.vendedor, vendedor['_id'], vendedor['enderecos'])
#             if endereco:
#                 for endereco_atual in vendedor['enderecos']:
#                     if endereco_atual['_id'] == endereco['_id']:
#                         endereco_atual.update(endereco)
#                         break
#         elif opcao == 7:
#             print("\n--- ATUALIZAR PRODUTO ---\n")
#             produto = updateProduto(mydb.vendedor, vendedor['_id'], vendedor['produtos'])
#             if produto:
#                 for produto_atual in vendedor['produtos']:
#                     if produto_atual['_id'] == produto['_id']:
#                         produto_atual.update(produto)
#                         break
#         elif opcao == 8:
#             print("\n--- DELETAR ENDEREÇO ---\n")
#             enderecos = deleteEndereco(mydb.vendedor, vendedor['_id'], vendedor['enderecos'])
#             if enderecos:
#                 for endereco in enderecos:
#                     vendedor['enderecos'].remove(endereco)
#         elif opcao == 9:
#             print("\n--- DELETAR PRODUTO ---\n")
#             deleteProduto(mydb.vendedor, vendedor['_id'], vendedor['produtos'])
#         elif opcao == 10:
#             print("\n--- DELETAR CONTA ---\n")
#             resultado = deleteUsuario(mydb.vendedor, vendedor['_id'])
#             if resultado:
#                 break
#         elif opcao == 0:
#             break
#         else:
#             print("Opção inválida.")


# while True:
#     print("""
# 🔒 LOGIN
# ------------------------------------------------------------
# |  1  | 👤 Cliente        |  2  | 🛒 Vendedor

# ➕ CADASTRAR
# ------------------------------------------------------------
# |  3  | 👤 Cliente        |  4  | 🛒 Vendedor

# 🔍 CONSULTAR
# ------------------------------------------------------------
# |  5  | 👤 Clientes       |  6  | 🛒 Vendedores
# |  7  | 📦 Produtos
# ============================================================
# 🔚 SISTEMA
# ------------------------------------------------------------
# | 0  | ❌ Sair
# ============================================================
#     """)
#     opcao = int(input("Digite a opção desejada: "))
#     limpar()

#     if opcao == 1:
#         print("\n--- LOGIN DE CLIENTE ---\n")
#         cliente = login(mydb.cliente)
#         if cliente:
#             menuCliente(cliente)
#     elif opcao == 2:
#         print("\n--- LOGIN DE VENDEDOR ---\n")
#         vendedor = login(mydb.vendedor)
#         if vendedor:
#             menuVendedor(vendedor)
#     elif opcao == 3:
#         print("\n--- CADASTRO DE USUÁRIO ---\n")
#         insertCliente(mydb.cliente)
#     elif opcao == 4:
#         print("\n--- CADASTRO DE VENDEDOR ---\n")
#         insertVendedor(mydb.vendedor)
#     elif opcao == 5:
#         print("\n--- LISTA DE CLIENTES ---\n")
#         findClientes(mydb.cliente)
#     elif opcao == 6:
#         print("\n--- LISTA DE VENDEDORES ---\n")
#         findVendedores(mydb.vendedor)
#     elif opcao == 7:
#         print("\n--- LISTA DE PRODUTOS ---\n")
#         findProdutos(mydb.vendedor, 'lista')
#     elif opcao == 0:
#         print("Saindo do sistema...")
#         break
#     else:
#         limpar()