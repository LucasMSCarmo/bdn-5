import hashlib
import datetime
from bson import ObjectId

def insertCliente(conexao):

    nome = input("Nome: ").strip()
    while True:
        cpf = input("CPF: ").strip()
        if conexao.find_one({"cpf": cpf}):
            print("CPF já cadastrado.")
            if input("Tentar novamente? (s/n): ").lower() != 's':
                return
        else:
            break
    while True:
        email = input("Email: ").strip()
        if conexao.find_one({"email": email}):
            print("Email já cadastrado.")
            if input("Tentar novamente? (s/n): ").lower() != 's':
                return
        else:
            break
    senha = hashlib.sha256(input("Senha: ").strip().encode('utf-8')).hexdigest()
    telefone = input("Telefone: ").strip()
    enderecos = []
    while True:
        if input("Adicionar endereço? (s/n): ").lower() != 's':
            break
        enderecos.append({
            "_id": ObjectId(),
            "logradouro": input("   Logradouro: ").strip(),
            "numero": input("   Número: ").strip(),
            "complemento": input("   Complemento: ").strip(),
            "bairro": input("   Bairro: ").strip(),
            "cidade": input("   Cidade: ").strip(),
            "estado": input("   Estado: ").strip()
        })

    dados = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": senha,
        "telefone": telefone,
        "enderecos": enderecos,
        "favoritos": [],
        }

    resposta = conexao.insert_one(dados)
    if resposta.inserted_id:
        print("Cliente cadastrado com sucesso.")
    else:
        print("Falha ao cadastrar o cliente.")

def insertVendedor(conexao):

    nome = input("Nome: ").strip()
    while True:
        cpf = input("CPF: ").strip()
        if conexao.find_one({"cpf": cpf}):
            print("CPF já cadastrado.")
            if input("Tentar novamente? (s/n): ").lower() != 's':
                return
        else:
            break
    while True:
        email = input("Email: ").strip()
        if conexao.find_one({"email": email}):
            print("Email já cadastrado.")
            if input("Tentar novamente? (s/n): ").lower() != 's':
                return
        else:
            break
    senha = hashlib.sha256(input("Senha: ").strip().encode('utf-8')).hexdigest()
    telefone = input("Telefone: ").strip()
    endereco = []
    while True:
        if input("Adicionar endereço? (s/n): ").lower() != 's':
            break
        endereco.append({
            "_id": ObjectId(),
            "logradouro": input("   Logradouro: ").strip(),
            "numero": input("   Número: ").strip(),
            "complemento": input("   Complemento: ").strip(),
            "bairro": input("   Bairro: ").strip(),
            "cidade": input("   Cidade: ").strip(),
            "estado": input("   Estado: ").strip()
        })
    produtos = []
    while True:
        if input("Adicionar produto? (s/n): ").lower() != 's':
            break
        produtos.append({
            "_id": ObjectId(),
            "nome": input("   Nome: ").strip(),
            "descricao": input("   Descrição: ").strip(),
            "preco": float(input("   Preço: R$").strip()),
            "estoque": int(input("   Estoque: ").strip())
        })

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cpf": cpf,
        "telefone": telefone,
        "enderecos": endereco,
        "produtos": produtos
        }

    resposta = conexao.insert_one(dados)
    if resposta.inserted_id:
        print("Vendedor cadastrado com sucesso.")
    else:
        print("Falha ao cadastrar o vendedor.")

def insertEndereco(conexao, id):
    enderecos = []
    while True:
        logradouro = input("Logradouro: ").strip()
        numero = input("Número: ").strip()
        complemento = input("Complemento: ").strip()
        bairro = input("Bairro: ").strip()
        cidade = input("Cidade: ").strip()
        estado = input("Estado: ").strip()
        
        dados = {
            "_id": ObjectId(),
            "logradouro": logradouro,
            "numero": numero,
            "complemento": complemento,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }

        if input("Confirmar endereço? (s/n): ").lower() == 's':
            enderecos.append(dados)

        if input("\nDeseja adicionar outro endereço? (s/n): ").lower() != 's':
            break

    if enderecos:
        resposta = conexao.update_one(
            {"_id": id},
            {"$push": {"enderecos": {"$each": enderecos}}}
        )
        if resposta.modified_count > 0:
            print("\nEndereço(s) cadastrado(s) com sucesso.")
            return enderecos
        else:
            print("\nFalha ao cadastrar o endereço.")
    else:
        print("\nNenhum endereço foi cadastrado.")

def insertProduto(conexao, id):
    produtos = []
    while True:
        nome = input("Nome do Produto: ").strip()
        descricao = input("Descrição do Produto: ").strip()
        preco = float(input("Preço do Produto: R$").strip())
        estoque = int(input("Estoque do Produto: ").strip())

        dados = {
            "_id": ObjectId(),
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque
        }
        produtos.append(dados)

        if input("Deseja adicionar outro produto? (s/n): ").lower() != 's':
            break
        print("\n")

    resposta = conexao.update_one(
        {"_id": id},
        {"$push": {"produtos": {"$each": produtos}}}
    )

    if resposta.modified_count > 0:
        print("Produto adicionado com sucesso.")
        return produtos
    else:
        print("Falha ao adicionar o produto.")

def insertCompra(bd, id, produtos_disponiveis):
    produtos = []
    total = 0
    print("\nDigite o ID do produto e a quantidade desejada. Digite '0' para cancelar.")
    while True:
        produto_id = input("ID do Produto: ").strip()
        if int(produto_id) < 0 or int(produto_id) > len(produtos_disponiveis):
            print(f"ID inválido.")
            continue
        if produto_id == '0':
            print("Operação cancelada.")
            return
        quantidade = input("Quantidade: ").strip()

        if not quantidade.isdigit() or int(quantidade) <= 0:
            print("Quantidade inválida.")
            continue
        if produtos_disponiveis[int(produto_id) - 1]['estoque'] < int(quantidade):
            print("Estoque insuficiente.")
            continue

        produtos.append({
            "_id": produtos_disponiveis[int(produto_id) - 1]['_id'],
            "vendedor_id": produtos_disponiveis[int(produto_id) - 1]['vendedor_id'],
            "vendedor_nome": produtos_disponiveis[int(produto_id) - 1]['vendedor_nome'],
            "nome": produtos_disponiveis[int(produto_id) - 1]['nome'],
            "preco": produtos_disponiveis[int(produto_id) - 1]['preco'],
            "quantidade": int(quantidade)
        })
        total += produtos_disponiveis[int(produto_id) - 1]['preco'] * int(quantidade)
        if input("Deseja adicionar outro produto? (s/n): ").lower() != 's':
            break
    dados = {
        "_id": ObjectId(),
        "cliente_id": id,
        "produtos": produtos,
        "total": total,
        "data": datetime.datetime.utcnow()
    }

    resultado = bd.compra.insert_one(dados)
    if resultado.inserted_id:
        dados_compra = {
            "_id": resultado.inserted_id,
            "data": dados["data"],
            "total": total
        }
        print(
            f"\nCompra registrada com sucesso.",
            f"\nTotal da Compra: R${total:.2f}\n"
        )
        bd.cliente.update_one(
            {"_id": id},
            {"$push": {"compras": dados_compra}}
        )
        for produto in produtos:
            bd.vendedor.update_one(
                {"_id": produto["vendedor_id"], "produtos._id": produto["_id"]},
                {"$inc": {"produtos.$.estoque": -produto["quantidade"]}}
            )
        return dados_compra
    else:
        print("\nFalha ao registrar a compra.\n")

def insertFavorito(conexao, cliente_id, produtos_disponiveis):
    while True:
        ids_favoritos = input("\nDigite os IDs dos produtos que deseja favoritar (digite 0 para cancelar): ").strip().split()
        print("\n")
        if '0' in ids_favoritos:
            return
        if all(1 <= int(id) <= len(produtos_disponiveis) for id in ids_favoritos if id.isdigit()):
            break
        print("ID inválido")

    favoritos = []
    for id in ids_favoritos:
        id = int(id)
        produto = produtos_disponiveis[id - 1]
        favoritos.append({
            "_id": produto['_id'],
            "vendedor_nome": produto['vendedor_nome'],
            "produto": produto['nome'],
            "preco": produto['preco'],
        })

    resposta = conexao.update_one(
        {"_id": cliente_id},
        {"$push": {"favoritos": {"$each": favoritos}}}
    )
    if resposta.modified_count > 0:
        print("\nFavorito(s) cadastrado(s) com sucesso!")
        return favoritos
    else:
        print("\nFalha ao cadastrar o(s) favorito(s).")