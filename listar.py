def findClientes(conexao):
    clientes = list(conexao.find().sort("nome"))

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

def findVendedores(conexao):
    vendedores = list(conexao.find().sort("nome"))

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
                
def findProdutos(conexao, retorno):
    vendedores = conexao.find()
    
    dados_produtos = []
    for vendedor in vendedores:
        for produto in vendedor['produtos']:
            produto_com_vendedor = produto.copy()
            produto_com_vendedor['vendedor_nome'] = vendedor['nome']
            produto_com_vendedor['vendedor_id'] = vendedor['_id']
            dados_produtos.append(produto_com_vendedor)
    
    if not dados_produtos:
        print("Nenhum produto cadastrado.")
        return []
    
    if retorno == 'compra':
        dados_produtos = [produto for produto in dados_produtos if produto['estoque'] > 0]
        if not dados_produtos:
            print("Nenhum produto com estoque disponível para compra.")
            return []
    
    dados_produtos = sorted(dados_produtos, key=lambda x: x['nome'])

    espacamento = "  " * 2 if retorno != 'lista' else ""
    numero_produtos = len(dados_produtos)
    for i, produto in enumerate(dados_produtos, 1):
        numero_produtos -= 1
        if retorno != 'lista':
            print(f"  ID: {i}")
        print(
            f"\n{espacamento}Nome: {produto['nome']}",
            f"\n{espacamento}Descrição: {produto['descricao']}",
            f"\n{espacamento}Preço: R$ {produto['preco']:.2f}",
            f"\n{espacamento}Estoque: {produto['estoque']}"
        )
        if numero_produtos != 0:
            print(f"--------------------------------\n")
    if retorno != 'lista':
        return dados_produtos