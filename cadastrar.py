import hashlib
from os import system
from neo4j import GraphDatabase


def limpar():
    system('cls' if system == 'nt' else 'clear')

def verificar_duplicidade(tx, usuario, chave, valor):
    query = f"MATCH (n) WHERE (n:{usuario}) AND n.{chave} = $valor RETURN n"
    result = tx.run(query, valor=valor)
    return result.single() is not None

def criar_cliente_neo4j(tx, dados):
    query = """
    CREATE (v:Cliente {
        nome: $nome,
        cpf: $cpf,
        email: $email,
        senha: $senha,
        telefone: $telefone
    })
    WITH v
    
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
    """
    tx.run(query, **dados)

def insertCliente(driver):
    with driver.session() as session:
        print("\n--- Cadastro de Cliente ---")
        nome = input("Nome: ").strip()
        
        while True:
            cpf = input("CPF: ").strip()
            if session.execute_read(verificar_duplicidade, "Cliente", "cpf", cpf):
                print("CPF já cadastrado.")
                if input("Tentar novamente? (s/n): ").lower() != 's': return
            else: break
        
        while True:
            email = input("Email: ").strip()
            if session.execute_read(verificar_duplicidade, "Cliente", "email", email):
                print("Email já cadastrado.")
                if input("Tentar novamente? (s/n): ").lower() != 's': return
            else: break

        senha = hashlib.sha256(input("Senha: ").strip().encode('utf-8')).hexdigest()
        telefone = input("Telefone: ").strip()
        
        enderecos = []
        while True:
            if input("Adicionar endereço? (s/n): ").lower() != 's': break

            logadouro = input("   Logradouro: ").strip()
            numero = input("   Número: ").strip()
            complemento = input("   Complemento: ").strip()
            bairro = input("   Bairro: ").strip()
            cidade = input("   Cidade: ").strip()
            estado = input("   Estado: ").strip()

            if input("Confirmar este endereço? (s/n): ").lower() == 's':
                enderecos.append({
                    "logradouro": logadouro,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado
                })

        dados = {
            "nome": nome, "cpf": cpf, "email": email, 
            "senha": senha, "telefone": telefone, 
            "enderecos": enderecos
        }

        try:
            session.execute_write(criar_cliente_neo4j, dados)
            print("Cliente cadastrado com sucesso.")
        except Exception as e:
            print(f"Falha ao cadastrar cliente: {e}")

def criar_vendedor_neo4j(tx, dados):
    query = """
    CREATE (v:Vendedor {
        nome: $nome,
        cpf: $cpf,
        email: $email,
        senha: $senha,
        telefone: $telefone
    })
    WITH v

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
    WITH v

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

def insertVendedor(driver):
    with driver.session() as session:
        print("\n--- Cadastro de Vendedor ---")
        nome = input("Nome: ").strip()
        
        while True:
            cpf = input("CPF: ").strip()
            if session.execute_read(verificar_duplicidade, "Vendedor", "cpf", cpf):
                print("CPF já cadastrado.")
                if input("Tentar novamente? (s/n): ").lower() != 's': return
            else: break
        
        while True:
            email = input("Email: ").strip()
            if session.execute_read(verificar_duplicidade, "Vendedor", "email", email):
                print("Email já cadastrado.")
                if input("Tentar novamente? (s/n): ").lower() != 's': return
            else: break

        senha = hashlib.sha256(input("Senha: ").strip().encode('utf-8')).hexdigest()
        telefone = input("Telefone: ").strip()
        
        enderecos = []
        while True:
            if input("Adicionar endereço? (s/n): ").lower() != 's': break

            logradouro = input("   Logradouro: ").strip()
            numero = input("   Número: ").strip()
            complemento = input("   Complemento: ").strip()
            bairro = input("   Bairro: ").strip()
            cidade = input("   Cidade: ").strip()
            estado = input("   Estado: ").strip()

            if input("Confirmar este endereço? (s/n): ").lower() == 's':
                enderecos.append({
                    "logradouro": logradouro,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado
                })

        produtos = []
        while True:
            if input("Adicionar produto inicial? (s/n): ").lower() != 's': break

            nome = input("   Nome do Produto: ").strip()
            descricao = input("   Descrição: ").strip()
            try:
                preco = float(input("   Preço: R$").strip())
                estoque = int(input("   Estoque: ").strip())
            except ValueError:
                print("Preço ou estoque inválido. Tente novamente.")
                continue

            if input("Confirmar este produto? (s/n): ").lower() == 's':
                produtos.append({
                    "nome": nome,
                    "descricao": descricao,
                    "preco": preco,
                    "estoque": estoque
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

def add_endereco_neo4j(tx, dados):
    query = """
    MATCH (p:$usuario) 
    WHERE p.cpf = $cpf
    FOREACH (end IN $novos_enderecos |
        CREATE (e:Endereco {
            logradouro: end.logradouro,
            numero: end.numero,
            complemento: end.complemento,
            bairro: end.bairro,
            cidade: end.cidade,
            estado: end.estado
        })
        CREATE (p)-[:POSSUI_ENDERECO]->(e)
    )
    """
    tx.run(query, **dados)

def insertEndereco(driver, cpf, usuario):
    print("\n--- Cadastro de Endereço ---")
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

    dados = {
        "usuario": usuario,
        "cpf": cpf,
        "novos_enderecos": enderecos_novos
    }

    with driver.session() as session:
        try:
            session.execute_write(add_endereco_neo4j, dados)
            print("Endereço adicionado.")
        except Exception as e:
            print(f"Erro ao salvar endereço: {e}")

def criar_produto_neo4j(tx, dados):
    query = """
    MATCH (v:Vendedor {cpf: $cpf})
    FOREACH (prod IN $novos_produtos |
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

def insertProduto(driver, cpf):
    print("\n--- Cadastro de Produto ---")

    produtos_novos = []
    while True:
        nome = input("Nome do Produto: ").strip()
        descricao = input("Descrição: ").strip()
        try:
            preco = float(input("Preço: ").strip())
            estoque = int(input("Estoque: ").strip())
        except ValueError:
            print("Preço ou estoque inválido. Tente novamente.")
            continue

        dados_produto = {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque
        }

        if input("Confirmar este produto? (s/n): ").lower() == 's':
            produtos_novos.append(dados_produto)

        if input("Adicionar outro produto? (s/n): ").lower() != 's':
            break

    dados = {
        "cpf": cpf,
        "novos_produtos": produtos_novos
    }
    with driver.session() as session:
        try:
            session.execute_write(criar_produto_neo4j, dados)
            print("Produtos cadastrados com sucesso.")
        except Exception as e:
            print(f"Erro ao cadastrar produtos: {e}")

def get_produtos_disponiveis(tx, estoque):
    if estoque:
        query = "MATCH (p:Produto) WHERE p.estoque > 0 RETURN p.id, p.nome as nome, p.preco as preco, p.descricao as descricao, p.estoque as estoque"
    else:
        query = "MATCH (p:Produto) RETURN p.id, p.nome as nome, p.preco as preco, p.descricao as descricao, p.estoque as estoque"
    result = tx.run(query)
    return [record.data() for record in result]

def favoritar_neo4j(tx, dados):
    query = """
    MATCH (c:Cliente {cpf: $cpf})
    UNWIND $ids_produtos AS produto_id
    MATCH (p:Produto)
    WHERE elementId(p) = produto_id
    MERGE (c)-[:FAVORITOU]->(p)
    """
    tx.run(query, **dados)

def insertFavorito(driver, cpf):
    print(f"\n--- Favoritar Produto ---")
    
    with driver.session() as session:
        produtos_disponiveis = session.execute_read(get_produtos_disponiveis, False)
    
    if not produtos_disponiveis:
        print("Nenhum produto disponível.")
        return

    print("\nLista de Produtos:")
    for i, p in enumerate(produtos_disponiveis):
        print(f"{i + 1}. {p['nome']} - {p['preco']:.2f} - Descrição: {p['descricao']}")
    while True:
        opcao = input("\nDigite os números dos produtos para favoritar (ou '0' para sair): ").split()
        if '0' in opcao: break
        try:
            ids = list(map(int, opcao))
            if any(i < 1 or i > len(produtos_disponiveis) for i in ids):
                raise ValueError
        except ValueError:
            print("Digite apenas os números dos produtos separados por espaço.")
            continue

        dados = {
            "cpf": cpf,
            "ids_produtos": [produtos_disponiveis[i - 1]['id'] for i in ids]
        }
        
        try:
            with driver.session() as session:
                session.execute_write(favoritar_neo4j, dados)
                print("Produtos favoritados com sucesso.")
        except ValueError:
            print("Erro ao favoritar produtos.")

def registrar_compra_neo4j(tx, dados):
    query = """
    MATCH (c:Cliente {cpf: $cpf})
    CREATE (comp:Compra {data: datetime(), total: $total})
    CREATE (c)-[:REALIZOU]->(comp)
    WITH comp
    UNWIND $carrinho AS item
    MATCH (p:Produto)
    WHERE elementId(p) = item.id
    CREATE (comp)-[:INCLUI]->(p)
    SET p.estoque = p.estoque - item.quantidade
    """
    tx.run(query, **dados)

def insertCompra(driver, cpf):
    print(f"\n--- Nova Compra ---")
    
    with driver.session() as session:
        produtos_disponiveis = session.execute_read(get_produtos_disponiveis, True)
    
    if not produtos_disponiveis:
        print("Não há produtos disponíveis com estoque.")
        return

    carrinho = []
    total_compra = 0.0

    while True:
        limpar()
        print("\n--- Produtos Disponíveis ---")
        for i, p in enumerate(produtos_disponiveis):
            print(f"{i + 1}. {p['nome']} (R${p['preco']:.2f}) - Descrição: {p['descricao']} - Estoque: {p['estoque']}")
        try:
            opcao = int(input("\nDigite o número do produto (ou '0' para finalizar): ").strip())
            if opcao == 0: break
            if opcao > len(produtos_disponiveis) or opcao < 1:
                raise ValueError
        except ValueError:
            print("Digite um número válido.")
            continue
            
        try:
            id = opcao - 1
            produto_selecionado = produtos_disponiveis[id]
            item = next((produto for produto in carrinho if produto['id'] == produto_selecionado['id']), None)
            if item:
                print("Produto já adicionado ao carrinho.")
                if input(f"Deseja mudar a quantidade de {item['quantidade']}? (s/n): ").lower() != 's':
                    continue
                try:
                    print(f"Estoque disponível: {produto_selecionado['estoque'] + item['quantidade']}")
                    nova_quantidade = int(input(f"Nova quantidade para '{produto_selecionado['nome']}': ").strip())
                    if nova_quantidade <= 0 or nova_quantidade > produto_selecionado['estoque'] + item['quantidade']:
                        raise ValueError
                    total_compra += produto_selecionado['preco'] * (nova_quantidade - item['quantidade'])
                    produto_selecionado['estoque'] += item['quantidade'] - nova_quantidade
                    item['quantidade'] = nova_quantidade
                    continue
                except ValueError:
                    print("Quantidade inválida ou excede o estoque disponível.")
                    continue

            quantidade = int(input(f"Quantidade de '{produto_selecionado['nome']}' a adicionar: ").strip())
            if quantidade <= 0 or quantidade > produto_selecionado['estoque']:
                raise ValueError
            carrinho.append({
                "id": produto_selecionado['id'],
                "quantidade": quantidade
            })
            total_compra += produto_selecionado['preco'] * quantidade
            produto_selecionado['estoque'] -= quantidade
        except ValueError:
            print("Quantidade inválida ou excede o estoque disponível.")

    dados = {
        "cpf": cpf,
        "carrinho": carrinho,
        "total": total_compra
    }

    if not carrinho:
        print("Compra cancelada (carrinho vazio).")
        return

    with driver.session() as session:
        try:
            session.execute_write(registrar_compra_neo4j, dados)
            print("Compra registrada com sucesso.")
        except Exception as e:
            print(f"Erro ao processar compra: {e}")