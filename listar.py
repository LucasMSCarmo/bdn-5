def findClientes(driver):
    query = """
    MATCH (c:Cliente)
    OPTIONAL MATCH (c)-[:POSSUI_ENDERECO]->(e:Endereco)
    OPTIONAL MATCH (c)-[:FAVORITOU]->(p:Produto)
    WITH c,
            collect(DISTINCT e { .logradouro, .numero, .complemento, .bairro, .cidade, .estado }) AS enderecos,
            collect(DISTINCT p { .nome, .descricao, .preco, .estoque, id: elementId(p) }) AS favoritos
    RETURN c {
        .nome, .cpf, .email, .telefone,
        enderecos: enderecos,
        favoritos: favoritos
    } AS cliente
    ORDER BY cliente.nome
    """

    def buscar(tx):
        result = tx.run(query)
        return [record['cliente'] for record in result]

    try:
        with driver.session() as session:
            clientes = session.execute_read(buscar)
    except Exception as e:
        print("Erro ao buscar clientes:", e)
        return

    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
        return
    for cliente in clientes:
        print(
            "\nNome: ", cliente['nome'],
            "\nCPF: ", cliente['cpf'],
            "\nEmail: ", cliente['email'],
            "\nTelefone: ", cliente['telefone'],
        )
        numero_enderecos = len(cliente['enderecos'])
        if numero_enderecos > 0:
            print(f"Endereço:" if numero_enderecos == 1 else "Endereços:")
            for endereco in cliente['enderecos']:
                numero_enderecos -= 1
                print(
                    f"\n    {endereco['logradouro']}, {endereco['numero']}{' - ' + endereco['complemento'] if endereco['complemento'] else ''}",
                    f"\n    {endereco['bairro']}",
                    f"\n    {endereco['cidade']} - {endereco['estado']}"
                )
                if numero_enderecos != 0:
                    print(f"    --------------------------------")

        numero_favoritos = len(cliente['favoritos'])
        if numero_favoritos > 0:
            print("\nFavoritos:")
            for fav in cliente['favoritos']:
                numero_favoritos -= 1
                preco = fav['preco'] or 0.0
                print(f"    {fav['nome']} - R$ {preco:.2f}")
                if numero_favoritos != 0:
                    print(f"    --------------------------------")

def findVendedores(driver):
    query = """
    MATCH (v:Vendedor)
    OPTIONAL MATCH (v)-[:POSSUI_ENDERECO]->(e:Endereco)
    OPTIONAL MATCH (v)-[:VENDE]->(p:Produto)
    WITH v,
            collect(DISTINCT e { .logradouro, .numero, .complemento, .bairro, .cidade, .estado }) AS enderecos,
            collect(DISTINCT p { .nome, .descricao, .preco, .estoque, id: elementId(p) }) AS produtos
    RETURN v {
        .nome, .email, .cpf, .telefone,
        enderecos: enderecos,
        produtos: produtos
    } AS vendedor
    ORDER BY vendedor.nome
    """

    def buscar(tx):
        result = tx.run(query)
        return [record['vendedor'] for record in result]
    
    try:
        with driver.session() as session:
            vendedores = session.execute_read(buscar)
    except Exception as e:
        print("Erro ao buscar vendedores:", e)
        return

    if len(vendedores) == 0:
        print("Nenhum vendedor cadastrado.")
        return
    for vendedor in vendedores:
        print(
            "\nNome: ", vendedor['nome'],
            "\nEmail: ", vendedor['email'],
            "\nCPF: ", vendedor['cpf'],
            "\nTelefone: ", vendedor['telefone'],
        )
        numero_enderecos = len(vendedor['enderecos'])
        if numero_enderecos > 0:
            print(f"Endereço:" if numero_enderecos == 1 else "Endereços:")
            for endereco in vendedor['enderecos']:
                numero_enderecos -= 1
                print(
                    f"\n    {endereco['logradouro']}, {endereco['numero']}{' - ' + endereco['complemento'] if endereco['complemento'] else ''}",
                    f"\n    {endereco['bairro']}",
                    f"\n    {endereco['cidade']} - {endereco['estado']}"
                )
                if numero_enderecos != 0:
                    print(f"    --------------------------------")
        
        numero_produtos = len(vendedor['produtos'])
        if numero_produtos > 0:
            print("\nProdutos:")
            for produto in vendedor['produtos']:
                numero_produtos -= 1
                preco = produto['preco'] or 0.0
                print(
                    f"\n    {produto['nome']} - R$ {preco:.2f}"
                    f"\n    {produto['descricao']}")

                if numero_produtos != 0:
                    print(f"    --------------------------------")
                
def findProdutos(driver):
    query = "MATCH (p:Produto) RETURN p ORDER BY p.nome"

    def buscar(tx):
        result = tx.run(query)
        return [record['p'] for record in result]

    try:
        with driver.session() as session:
            produtos = session.execute_read(buscar)
    except Exception as e:
        print("Erro ao buscar produtos:", e)
        return
    numero_produtos = len(produtos)
    for produto in produtos:
        numero_produtos -= 1
        print(
            f"\nNome: {produto['nome']}",
            f"\nDescrição: {produto['descricao']}",
            f"\nPreço: R$ {produto['preco']:.2f}",
            f"\nEstoque: {produto['estoque']}"
        )
        if numero_produtos != 0:
            print(f"--------------------------------")

def findCompras(driver):
    query = """
    MATCH (cl:Cliente)-[:REALIZOU]->(comp:Compra)-[inc:INCLUI]->(p:Produto)
    WITH comp,
            collect({ nome: p.nome, preco: p.preco, quantidade: inc.quantidade }) AS produtos,
            cl
    RETURN comp {
        .data, .total, id: elementId(comp),
        cliente: cl { .nome, .cpf },
        produtos: produtos
    } AS compra
    ORDER BY compra.data DESC
    """

    def buscar(tx):
        result = tx.run(query)
        return [record['compra'] for record in result]

    try:
        with driver.session() as session:
            compras = session.execute_read(buscar)
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return

    if len(compras) == 0:
        print("Nenhuma compra registrada.")
        return

    for compra in compras:
        cliente = compra.get('cliente', {})
        produtos = compra.get('produtos', [])
        total_persistido = compra.get('total', 0.0)
        data = compra.get('data')
        nota_id = compra.get('id', '')

        print("\n" + "=" * 60)
        print("               NOTA FISCAL / COMPROVANTE DE COMPRA")
        print("=" * 60)
        print(f"Loja:        E-Commerce LTDA")
        print(f"CNPJ:        00.000.000/0000-00")
        print(f"Data:        {str(data)}")
        print(f"Nº Nota:     {nota_id}")
        print("-" * 60)
        print(f"Cliente:     {cliente.get('nome','')} (CPF: {cliente.get('cpf','')})")
        print("-" * 60)
        print(f"{'ITEM':<4} {'PRODUTO':<36} {'QTD':>3} {'V.UNIT':>10} {'SUBTOTAL':>12}")
        print("-" * 60)

        soma = 0.0
        for idx, item in enumerate(produtos, start=1):
            nome = item.get('nome','')[:34]
            qtd = int(item.get('quantidade') or 0)
            preco = float(item.get('preco') or 0.0)
            subtotal = preco * qtd
            soma += subtotal
            print(f"{idx:<4} {nome:<36} {qtd:>3} R$ {preco:>8.2f} R$ {subtotal:>9.2f}")

        print("-" * 60)
        print(f"{'TOTAL ITENS:':<48} R$ {soma:>9.2f}")
        if abs(soma - total_persistido) > 0.009:
            print(f"{'TOTAL (persistido):':<48} R$ {total_persistido:>9.2f}   (diferença detectada)")
        else:
            print(f"{'TOTAL (persistido):':<48} R$ {total_persistido:>9.2f}")
        print("=" * 60 + "\n")