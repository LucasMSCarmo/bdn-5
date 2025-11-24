import hashlib

def updateDados(conexao, usuario):
    print("Dados atuais:",
            f"\n    --------------------------------",
            f"\n    Nome: {usuario.get('nome')}",
            f"\n    CPF: {usuario.get('cpf')}",
            f"\n    Email: {usuario.get('email')}",
            f"\n    Telefone: {usuario.get('telefone')}")

    print("\nNovos dados (deixe vazio para manter o atual):")
    print("    --------------------------------")
    nome = input("    Nome: ").strip()
    cpf = input("    CPF: ").strip()
    email = input("    Email: ").strip()
    senha_raw = input("    Senha: ").strip()
    telefone = input("    Telefone: ").strip()

    dados = {}
    if nome:
        dados['nome'] = nome
    if cpf:
        dados['cpf'] = cpf
    if email:
        dados['email'] = email
    if senha_raw:
        dados['senha'] = hashlib.sha256(senha_raw.encode('utf-8')).hexdigest()
    if telefone:
        dados['telefone'] = telefone

    for dado in dados:
        result = conexao.update_one(
            {"_id": usuario['_id']},
            {"$set": {dado: dados[dado]}},
        )
        if result.modified_count > 0:
            print(f"{dado.title()} atualizado com sucesso.")
        else:
            print(f"Falha ao atualizar {dado}.")
    return dados

def updateEndereco(conexao, id, enderecos):
    numero_enderecos = len(enderecos)
    if numero_enderecos == 0:
        print("Nenhum endereço cadastrado.")
        return

    enderecos_ordenados = []
    print(f"Endereço atual:" if numero_enderecos == 1 else "Endereços atuais:")
    for endereco in enderecos:
        enderecos_ordenados.append(endereco)
        if numero_enderecos != 1:
            print(f"\n  ID: {len(enderecos_ordenados)}")
        print(
            f"\n    Logradouro: {endereco['logradouro']}",
            f"\n    Número: {endereco['numero']}",
            f"\n    Complemento: {endereco['complemento']}",
            f"\n    Bairro: {endereco['bairro']}",
            f"\n    Cidade: {endereco['cidade']}",
            f"\n    Estado: {endereco['estado']}"
        )
        if numero_enderecos != 1:
            print(f"  --------------------------------")
    
    if numero_enderecos != 1:
        while True:
            id_selecionado = input("\nDigite o ID do endereço que deseja atualizar(digite 0 para cancelar): ").strip()
            if '0' == id_selecionado:
                print("Operação cancelada.")
                return
            if 1 <= int(id_selecionado) <= len(enderecos_ordenados):
                id_selecionado = int(id_selecionado)
                break
            print("ID inválido.")
    else:
        id_selecionado = 1
        if input("\nDeseja atualizar esse endereço? (s/n): ").strip().lower() != 's':
            print("Operação cancelada.")
            return

    print("\nNovos dados (digite '-' para manter o atual):")
    print("--------------------------------")

    logradouro = input("Logradouro: ").strip()
    numero = input("Número: ").strip()
    complemento = input("Complemento: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("Estado: ").strip()
    
    dados = {
        "_id": enderecos_ordenados[id_selecionado - 1]['_id'],
        "logradouro": logradouro if logradouro != '-' else enderecos_ordenados[id_selecionado - 1]['logradouro'],
        "numero": numero if numero != '-' else enderecos_ordenados[id_selecionado - 1]['numero'],
        "complemento": complemento if complemento != '-' else enderecos_ordenados[id_selecionado - 1]['complemento'],
        "bairro": bairro if bairro != '-' else enderecos_ordenados[id_selecionado - 1]['bairro'],
        "cidade": cidade if cidade != '-' else enderecos_ordenados[id_selecionado - 1]['cidade'],
        "estado": estado if estado != '-' else enderecos_ordenados[id_selecionado - 1]['estado']
    }

    result = conexao.update_one(
        {"_id": id, "enderecos._id": dados['_id']},
        {"$set": {"enderecos.$": dados}}
    )
    if result.modified_count > 0:
        print("\nEndereço atualizado com sucesso.")
        return dados
    else:
        print("\nFalha ao atualizar o endereço.")

def updateProduto(conexao, id, produtos):
    numero_produtos = len(produtos)
    if numero_produtos == 0:
        print("Nenhum produto cadastrado.")
        return
    
    produtos_ordenados = []
    print(f"Produto atual:" if numero_produtos == 1 else "Produtos atuais:")
    for produto in produtos:
        produtos_ordenados.append(produto)
        if numero_produtos != 1:
            print(f"\n  ID: {len(produtos_ordenados)}")
        print(
            f"\n    Nome: {produto['nome']}",
            f"\n    Descrição: {produto['descricao']}",
            f"\n    Preço: R${produto['preco']:.2f}",
            f"\n    Estoque: {produto['estoque']}"
        )
        if numero_produtos != 1:
            print(f"  --------------------------------")

    if numero_produtos != 1:
        while True:
            id_selecionado = input("\nDigite o ID do produto que deseja atualizar(digite 0 para cancelar): ")
            if '0' in id_selecionado:
                print("Operação cancelada.")
                return
            if 1 <= int(id_selecionado) <= len(produtos_ordenados):
                id_selecionado = int(id_selecionado)
                break
            print("ID inválido.")
    else:
        id_selecionado = 1
        if input("\nDeseja atualizar esse produto? (s/n): ").strip().lower() != 's':
            print("Operação cancelada.")
            return
        
    print("\nNovos dados (deixe vazio para manter o atual):")
    print("--------------------------------")

    nome = input("Nome: ").strip()
    descricao = input("Descrição: ").strip()
    preco = input("Preço: R$").strip()
    estoque = input("Estoque: ").strip()

    dados = {
        "_id": produtos_ordenados[id_selecionado - 1]['_id'],
        "nome": nome if nome != '' else produtos_ordenados[id_selecionado - 1]['nome'],
        "descricao": descricao if descricao != '' else produtos_ordenados[id_selecionado - 1]['descricao'],
        "preco": float(preco) if preco != '' else produtos_ordenados[id_selecionado - 1]['preco'],
        "estoque": int(estoque) if estoque != '' else produtos_ordenados[id_selecionado - 1]['estoque']
    }

    result = conexao.update_one(
        {"_id": id, "produtos._id": dados['_id']},
        {"$set": {"produtos.$": dados}}
    )
    if result.modified_count > 0:
        print("\nProduto atualizado com sucesso.")
        return dados
    else:
        print("\nFalha ao atualizar o produto.")
