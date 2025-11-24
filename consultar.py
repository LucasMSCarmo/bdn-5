def findCliente(cliente):
    print(
        f"Nome: {cliente['nome']}",
        f"\nCPF: {cliente['cpf']}",
        f"\nEmail: {cliente['email']}",
        f"\nTelefone: {cliente['telefone']}",
        )
    numero_enderecos = len(cliente["enderecos"])
    if numero_enderecos > 0:
        print(f"Endereço:" if numero_enderecos == 1 else "Endereços:")
        for endereco in cliente["enderecos"]:
            numero_enderecos -= 1
            print(
                f"\n    {endereco['logradouro']}, {endereco['numero']}{' - ' + endereco['complemento'] if endereco['complemento'] else ''}",
                f"\n    {endereco['bairro']}",
                f"\n    {endereco['cidade']} - {endereco['estado']}"
            )
            if numero_enderecos != 0:
                print(f"    --------------------------------")

def findVendedor(vendedor):
    print(
        f"\nNome: {vendedor['nome']}",
        f"\nCPF: {vendedor['cpf']}",
        f"\nEmail: {vendedor['email']}",
        f"\nTelefone: {vendedor['telefone']}",
    )
    numero_enderecos = len(vendedor["enderecos"])
    if numero_enderecos > 0:
        print(f"Endereço:" if numero_enderecos == 1 else "Endereços:")
        for endereco in vendedor["enderecos"]:
            numero_enderecos -= 1
            print(
                f"\n    {endereco['logradouro']}, {endereco['numero']}{' - ' + endereco['complemento'] if endereco['complemento'] else ''}",
                f"\n    {endereco['bairro']}",
                f"\n    {endereco['cidade']} - {endereco['estado']}"
            )
            if numero_enderecos != 0:
                print(f"    --------------------------------")

def findFavoritos(favoritos):
    numero_favoritos = len(favoritos)
    favoritos_ordenados = sorted(favoritos, key=lambda x: x['produto'])
    if numero_favoritos > 0:
        for favorito in favoritos_ordenados:
            numero_favoritos -= 1
            print(
                f"\nVendedor: {favorito['vendedor_nome']}",
                f"\nProduto: {favorito['produto']}",
                f"\nPreço: R${favorito['preco']:.2f}"
            )
            if numero_favoritos != 0:
                print(f"--------------------------------")

    else:
        print("Nenhum favorito cadastrado.")

def findCompras(conexao, cliente, compras):
    if not compras:
        print("Nenhuma compra realizada.")
        return

    compras_ordenadas = sorted(compras, key=lambda x: x['data'], reverse=True)

    for i, compra in enumerate(compras_ordenadas, 1):
        print(f"{i}. Data: {compra['data'].strftime('%d/%m/%Y %H:%M:%S')}    Valor: R${compra['total']:.2f}")

    while True:
        if input("\nDeseja ver os detalhes de alguma compra? (s/n): ").strip().lower() != 's':
            break
        while True:
            id_compra = input("Digite o número da compra (ou 0 para cancelar): ").strip()
            if '0' == id_compra:
                print("Operação cancelada.")
                break
            if 1 <= int(id_compra) <= len(compras_ordenadas):
                break
            print("ID inválido.")

        compra = conexao.find_one({"_id": compras_ordenadas[int(id_compra) - 1]['_id']})

        print("\n" + "=" * 70)
        print(f"{'Detalhes da Compra':^70}")
        print("=" * 70)
        print(f"{'Data: ' + compra['data'].strftime('%d/%m/%Y'):<35}{'Hora: ' + compra['data'].strftime('%H:%M:%S'):>35}")
        print(f"Nome: {cliente}")
        print("-" * 70)

        itens = compra['produtos']
        print(f"{'Qtd':>3}  {'Produto':<30} {'Vlr Unit.':>10}     {'Subtotal':>10}")
        print("-" * 70)
        for item in itens:
            qtd = item.get('quantidade', 0)
            nome = item.get('nome', '')[:30]
            preco = item.get('preco', 0.0)
            subtotal = qtd * preco
            print(f"{qtd:>3}  {nome:<30} R${preco:>8.2f}     R${subtotal:>8.2f}")

        print("-" * 70)
        print(f"TOTAL: R${compra['total']:.2f}")
        print("=" * 70 + "\n")

def findProdutosVendedor(produtos):
    numero_produtos = len(produtos)
    if numero_produtos > 0:
        print(f"Produto:" if numero_produtos == 1 else "Produtos:")
        for produto in produtos:
            numero_produtos -= 1
            print(
                f"\n    Produto: {produto['nome']}",
                f"\n    Descrição: {produto['descricao']}",
                f"\n    Preço: R${produto['preco']:.2f}",
                f"\n    Estoque: {produto['estoque']}"
            )
            if numero_produtos != 0:
                print(f"    --------------------------------")
    else:
        print("Nenhum produto cadastrado.")