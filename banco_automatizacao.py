def menu():
    menu = """\n
    =========MENU=========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    ======================
    => """

    return input(menu)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR${valor:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("Operação falhou, valor inválido!")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saque):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saques >= limite_saque
    
    if excedeu_saldo:
        print("Operação falhou, você não tem saldo suficiente")
    elif excedeu_limite:
        print("Operação falhou, você excedeu o limite!")
    elif excedeu_saque:
        print("Operação falhou, número de saques excedido!")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR${valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso")
    else:
        print("\nOperação falhou")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, / , *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR${saldo:.2f}")
    print("=============================")

def criar_usuario(usuarios):
    cpf = input("Informe seu CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nUsuário não encontrado, criação de conta encerrada!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\n
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
"""
        print(linha)

def main():
    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ""
    usuarios = []
    contas = []

    LIMITE_SAQUE = 3
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Qual o valor do depósito? R$"))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Qual o valor do saque? R$"))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saque=LIMITE_SAQUE,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo... até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente.")

main()
