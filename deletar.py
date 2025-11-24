def deleteEndereco(conexao, usuario_id, enderecos):
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
            ids_enderecos = input("\nDigite os IDs dos endereços que deseja deletar(digite 0 para cancelar): ").strip().split()
            if '0' in ids_enderecos:
                print("Operação cancelada.")
                return
            if all(1 <= int(id) <= len(enderecos_ordenados) for id in ids_enderecos if id.isdigit()):
                break
            print("ID inválido")
    else:
        ids_enderecos = ['1']
        escolha = input("\nDeseja deletar esse endereço? (s/n): ").strip().lower()
        if escolha != 's':
            print("Operação cancelada.")
            return

    ids_limpos = []
    for endereco in ids_enderecos:
        endereco = int(endereco)
        if enderecos_ordenados[endereco - 1]['_id'] not in ids_limpos:
            ids_limpos.append(enderecos_ordenados[endereco - 1]['_id'])

    resposta = conexao.update_one(
        {"_id": usuario_id},
        {"$pull": {"enderecos": {"_id": {"$in": ids_limpos}}}}
    )
    if resposta.modified_count > 0:
        print(f"\nEndereço(s) deletado(s) com sucesso!")
        return [endereco for endereco in enderecos_ordenados if endereco['_id'] in ids_limpos]
    else:
        print("Falha ao deletar endereço(s).")

def deleteFavorito(conexao, id, favoritos):
    numero_favoritos = len(favoritos)
    if numero_favoritos == 0:
        print("Nenhum favorito cadastrado.")
        return

    favoritos_ordenados = []
    print(f"Favorito atual:" if numero_favoritos == 1 else "Favoritos atuais:")
    for favorito in favoritos:
        favoritos_ordenados.append(favorito)
        if numero_favoritos != 1:
            print(f"\n  ID: {len(favoritos_ordenados)}")
        print(
            f"\n    Vendedor: {favorito['vendedor']}",
            f"\n    Produto: {favorito['produto']}",
            f"\n    Preço: R${favorito['preco']:.2f}"
        )
        if numero_favoritos != 1:
            print(f"  --------------------------------")
    
    if numero_favoritos != 1:
        while True:
            ids_favoritos = input("\nDigite os IDs dos favoritos que deseja deletar(digite 0 para cancelar): ").strip().split()
            if '0' in ids_favoritos or not ids_favoritos:
                print("Operação cancelada.")
                return
            if all(1 <= int(id) <= len(favoritos_ordenados) for id in ids_favoritos if id.isdigit()):
                break
            print("ID inválido.")
    else:
        ids_favoritos = ['1']
        escolha = input("\nDeseja deletar esse favorito? (s/n): ").strip().lower()
        if escolha != 's':
            print("Operação cancelada.")
            return
    
    favoritos_deletados = []
    for favorito in ids_favoritos:
        favoritos_deletados.append(favoritos_ordenados[int(favorito) - 1])

    resposta = conexao.update_many(
        {"_id": id},
        {"$pull": {"favoritos": {"$in": favoritos_deletados}}}
    )
    if resposta.modified_count > 0:
        print(f"Favorito(s) deletado(s) com sucesso!")
        return favoritos_deletados
    else:
        print("Falha ao deletar favorito(s).")

def deleteUsuario(conexao, id):
    resposta = conexao.delete_one({"_id": id})
    if resposta.deleted_count > 0:
        print("Conta deletada com sucesso!")
        return True
    else:
        print("Falha ao deletar a conta.")

def deleteProduto(conexao, id, produtos):
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
            ids_produtos = input("\nDigite os IDs dos produtos que deseja deletar(digite 0 para cancelar): ").strip().split()
            if '0' in ids_produtos:
                print("Operação cancelada.")
                return
            if all(1 <= int(id) <= len(produtos_ordenados) for id in ids_produtos if id.isdigit()):
                break
            print("ID inválido.")
    else:
        ids_produtos = ['1']
        escolha = input("\nDeseja deletar esse produto? (s/n): ").strip().lower()
        if escolha != 's':
            print("Operação cancelada.")
            return
        
    ids_limpos = []
    for produto in ids_produtos:
        produto = int(produto)
        if produtos_ordenados[produto - 1]['_id'] not in ids_limpos:
            ids_limpos.append(produtos_ordenados[produto - 1]['_id'])

    resposta = conexao.update_one(
        {"_id": id, },
        {"$pull": {"produtos": {"_id": {"$in": ids_limpos}}}}
    )
    if resposta.modified_count > 0:
        print(f"\nProduto(s) deletado(s) com sucesso!")
        return ids_limpos
    else:
        print("\nFalha ao deletar produto(s).")