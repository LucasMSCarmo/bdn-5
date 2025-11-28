def findClientes(driver):
    clientes = driver.execute_read("MATCH (c:Cliente) RETURN c ORDER BY c.nome").data()

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

def findVendedores(driver):
    vendedores = driver.execute_read("MATCH (v:Vendedor) RETURN v ORDER BY v.nome").data()

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
                
def findProdutos(driver):
    produtos = driver.execute_read("MATCH (p:Produto) RETURN p ORDER BY p.nome").data()
    
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
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
            print(f"--------------------------------\n")