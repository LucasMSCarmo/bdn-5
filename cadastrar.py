import hashlib
from neo4j import GraphDatabase

# --- FUNÇÕES DE BANCO (CYPHER) ---

def verificar_duplicidade(tx, chave, valor):
    query = f"MATCH (n) WHERE (n:Cliente OR n:Vendedor) AND n.{chave} = $valor RETURN n"
    result = tx.run(query, valor=valor)
    return result.single() is not None

def criar_vendedor_neo4j(tx, dados):
    query = """
    CREATE (v:Vendedor {
        nome: $nome,
        cpf: $cpf,
        email: $email,
        senha: $senha,
        telefone: $telefone
    })
    
    FOREACH (end IN $enderecos |
        CREATE (e:Endereco {
            logradouro: end.logradouro,
            numero: end.numero,
            complemento: end.complemento,
            bairro: end.bairro,
            cidade: end.cidade,
            estado: end.estado
        })
        CREATE (v)-[:POSSUI_ENDERECO]->(e)
    )

    FOREACH (prod IN $produtos |
        CREATE (p:Produto {
            nome: prod.nome,
            descricao: prod.descricao,
            preco: prod.preco,
            estoque: prod.estoque
        })
        CREATE (v)-[:VENDE]->(p)
    )
    """
    tx.run(query, **dados)

def add_endereco_neo4j(tx, cpf_pessoa, novo_endereco):
    query = """
    MATCH (p) WHERE (p:Cliente OR p:Vendedor) AND p.cpf = $cpf
    CREATE (e:Endereco {
        logradouro: $logradouro,
        numero: $numero,
        complemento: $complemento,
        bairro: $bairro,
        cidade: $cidade,
        estado: $estado
    })
    CREATE (p)-[:POSSUI_ENDERECO]->(e)
    """
    tx.run(query, cpf=cpf_pessoa, **novo_endereco)

def registrar_compra_neo4j(tx, cpf_cliente, lista_produtos, total):
    query_compra = """
    MATCH (c:Cliente {cpf: $cpf})
    CREATE (compra:Compra {data: datetime(), total: $total})
    CREATE (c)-[:REALIZOU]->(compra)
    RETURN elementId(compra) as id_compra
    """
    result = tx.run(query_compra, cpf=cpf_cliente, total=total)
    record = result.single()
    
    if not record:
        raise Exception("Cliente não encontrado ou erro ao criar compra.")
        
    id_compra = record["id_compra"]

    query_itens = """
    MATCH (compra:Compra) WHERE elementId(compra) = $id_compra
    MATCH (p:Produto {nome: $nome_prod}) 
    CREATE (compra)-[:CONTEM {quantidade: $qtd, preco_momento: $preco}]->(p)
    SET p.estoque = p.estoque - $qtd
    """
    
    for item in lista_produtos:
        tx.run(query_itens, 
               id_compra=id_compra, 
               nome_prod=item['nome'], 
               qtd=item['quantidade'], 
               preco=item['preco'])

def favoritar_neo4j(tx, cpf_cliente, nome_produto):
    query = """
    MATCH (c:Cliente {cpf: $cpf})
    MATCH (p:Produto {nome: $nome_prod})
    MERGE (c)-[:FAVORITOU]->(p)
    """
    tx.run(query, cpf=cpf_cliente, nome_prod=nome_produto)

def get_produtos_disponiveis(tx):
    query = "MATCH (v:Vendedor)-[:VENDE]->(p:Produto) RETURN p.nome as nome, p.preco as preco, p.estoque as estoque, v.nome as vendedor"
    result = tx.run(query)
    return [record.data() for record in result]

def insertVendedor(driver):
    with driver.session() as session:
        print("\n--- Cadastro de Vendedor ---")
        nome = input("Nome: ").strip()
        
        while True:
            cpf = input("CPF: ").strip()
            if session.execute_read(verificar_duplicidade, "cpf", cpf):
                print("CPF já cadastrado.")
                if input("Tentar novamente? (s/n): ").lower() != 's': return
            else: break
        
        while True:
            email = input("Email: ").strip()
            if session.execute_read(verificar_duplicidade, "email", email):
                print("Email já cadastrado.")
                if input("Tentar novamente? (s/n): ").lower() != 's': return
            else: break

        senha = hashlib.sha256(input("Senha: ").strip().encode('utf-8')).hexdigest()
        telefone = input("Telefone: ").strip()
        
        # Lista de Endereços
        enderecos = []
        while True:
            if input("Adicionar endereço? (s/n): ").lower() != 's': break
            enderecos.append({
                "logradouro": input("   Logradouro: ").strip(),
                "numero": input("   Número: ").strip(),
                "complemento": input("   Complemento: ").strip(),
                "bairro": input("   Bairro: ").strip(),
                "cidade": input("   Cidade: ").strip(),
                "estado": input("   Estado: ").strip()
            })

        # Lista de Produtos Iniciais
        produtos = []
        while True:
            if input("Adicionar produto inicial? (s/n): ").lower() != 's': break
            produtos.append({
                "nome": input("   Nome do Produto: ").strip(),
                "descricao": input("   Descrição: ").strip(),
                "preco": float(input("   Preço: R$").strip()),
                "estoque": int(input("   Estoque: ").strip())
            })

        dados = {
            "nome": nome, "cpf": cpf, "email": email, 
            "senha": senha, "telefone": telefone, 
            "enderecos": enderecos, "produtos": produtos
        }

        try:
            session.execute_write(criar_vendedor_neo4j, dados)
            print("Vendedor cadastrado com sucesso.")
        except Exception as e:
            print(f"Falha ao cadastrar vendedor: {e}")

def insertEndereco(driver, cpf_pessoa):
    print(f"\n--- Adicionar Endereço para CPF: {cpf_pessoa} ---")
    enderecos_novos = []
    
    while True:
        logradouro = input("Logradouro: ").strip()
        numero = input("Número: ").strip()
        complemento = input("Complemento: ").strip()
        bairro = input("Bairro: ").strip()
        cidade = input("Cidade: ").strip()
        estado = input("Estado: ").strip()
        
        dados_endereco = {
            "logradouro": logradouro, "numero": numero,
            "complemento": complemento, "bairro": bairro,
            "cidade": cidade, "estado": estado
        }
        
        if input("Confirmar este endereço? (s/n): ").lower() == 's':
            enderecos_novos.append(dados_endereco)
        
        if input("Adicionar outro? (s/n): ").lower() != 's':
            break
            
    with driver.session() as session:
        for end in enderecos_novos:
            try:
                session.execute_write(add_endereco_neo4j, cpf_pessoa, end)
                print(f"Endereço '{end['logradouro']}' adicionado.")
            except Exception as e:
                print(f"Erro ao salvar endereço: {e}")

def insertCompra(driver, cpf_cliente):
    print(f"\n--- Nova Compra para CPF: {cpf_cliente} ---")
    
    # 1. Buscar produtos do banco para mostrar ao usuário
    with driver.session() as session:
        produtos_disponiveis = session.execute_read(get_produtos_disponiveis)
    
    if not produtos_disponiveis:
        print("Não há produtos cadastrados no sistema.")
        return

    carrinho = []
    total_compra = 0.0

    while True:
        print("\n--- Produtos Disponíveis ---")
        for i, p in enumerate(produtos_disponiveis):
            print(f"{i + 1}. {p['nome']} (R${p['preco']:.2f}) - Vendido por: {p['vendedor']} - Estoque: {p['estoque']}")
        
        opcao = input("\nDigite o número do produto (ou '0' para finalizar): ").strip()
        
        if opcao == '0':
            break
            
        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(produtos_disponiveis):
                prod_selecionado = produtos_disponiveis[idx]
                
                qtd = int(input(f"Quantidade de '{prod_selecionado['nome']}': "))
                
                if qtd <= 0:
                    print("Quantidade inválida.")
                elif qtd > prod_selecionado['estoque']:
                    print(f"Estoque insuficiente (Disponível: {prod_selecionado['estoque']}).")
                else:
                    # Adiciona ao carrinho temporário
                    carrinho.append({
                        "nome": prod_selecionado['nome'],
                        "preco": prod_selecionado['preco'],
                        "quantidade": qtd
                    })
                    total_compra += prod_selecionado['preco'] * qtd
                    # Atualiza estoque localmente só para visualização
                    prod_selecionado['estoque'] -= qtd 
                    print("Adicionado ao carrinho!")
            else:
                print("Opção inválida.")
        except ValueError:
            print("Digite um número válido.")

    if not carrinho:
        print("Compra cancelada (carrinho vazio).")
        return

    # Efetivar a compra no banco
    with driver.session() as session:
        try:
            session.execute_write(registrar_compra_neo4j, cpf_cliente, carrinho, total_compra)
            print(f"\nCompra finalizada com sucesso! Total: R${total_compra:.2f}")
        except Exception as e:
            print(f"Erro ao processar compra: {e}")

def insertFavorito(driver, cpf_cliente):
    print(f"\n--- Favoritar Produto para CPF: {cpf_cliente} ---")
    
    with driver.session() as session:
        produtos_disponiveis = session.execute_read(get_produtos_disponiveis)
    
    if not produtos_disponiveis:
        print("Sem produtos para favoritar.")
        return

    while True:
        print("\nLista de Produtos:")
        for i, p in enumerate(produtos_disponiveis):
            print(f"{i + 1}. {p['nome']} - {p['vendedor']}")
            
        opcao = input("\nDigite o número do produto para favoritar (ou '0' para sair): ")
        if opcao == '0': break
        
        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(produtos_disponiveis):
                nome_prod = produtos_disponiveis[idx]['nome']
                with driver.session() as session:
                    session.execute_write(favoritar_neo4j, cpf_cliente, nome_prod)
                print(f"Produto '{nome_prod}' favoritado!")
            else:
                print("Opção inválida.")
        except ValueError:
            print("Entrada inválida.")

def insertProduto(driver):
    with driver.session() as session:
        print("\n--- Cadastro de Produto ---")
        cpf_vendedor = input("Digite o CPF do Vendedor: ").strip()

        try:
            query = """
            MATCH (v:Vendedor {cpf: $cpf})
            RETURN v
            """
            result = session.run(query, cpf=cpf_vendedor)
            if not result.single():
                print("Vendedor não encontrado.")
                return
        except Exception as e:
            print(f"Erro ao verificar vendedor: {e}")
            return
        
        produtos = []

        while True:
            nome = input("Nome do Produto: ").strip()
            descricao = input("Descrição: ").strip()
            preco = float(input("Preço: ").strip())
            estoque = int(input("Estoque: ").strip())

            if input("Confirmar este produto? (s/n): ").lower() == 's':
                produtos.append({
                    "nome": nome,
                    "descricao": descricao,
                    "preco": preco,
                    "estoque": estoque
                })

            if input("Adicionar outro produto? (s/n): ").lower() != 's':
                break
        
        query = """
        MATCH (v:Vendedor {cpf: $cpf})
        FOREACH (prod IN $produtos |
            CREATE (p:Produto {
                nome: prod.nome,
                descricao: prod.descricao,
                preco: prod.preco,
                estoque: prod.estoque
            })
            CREATE (v)-[:VENDE]->(p)
        )
        """
        session.run(query, cpf=cpf_vendedor, produtos=produtos)