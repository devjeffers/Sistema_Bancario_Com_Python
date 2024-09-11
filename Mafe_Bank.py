import streamlit as st
st.title("Mafê Bank")

import pytz
from datetime import datetime

# Função para obter a data e hora atual formatada
def get_formatted_datetime():
    return datetime.now(pytz.timezone("America/Manaus")).strftime("%d/%m/%Y %H:%M:%S")

import textwrap

def menu():
    menu = """\n
    =================== M a f ê  B a n k =====================
    ||
    ||  [0]\tDepositar 
    ||  [1]\tSacar
    ||  [2]\tExtrato
    ||  [3]\tNova conta
    ||  [4]\tListar contas
    ||  [5]\tNovo usuário
    ||  [6]\tSair
    ||
    ||    ==> """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    data_deposito = get_formatted_datetime()
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print(f"Déposito realizado com sucesso: {data_deposito}")
    else:
        print(f"Desculpe, não entendi. Por favor informe um valor válido! {data_deposito}") 
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques_diario):
    data_sacar = get_formatted_datetime()
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques_diario

    if excedeu_saldo:
        print(f"Ops! Parece que a operação falhou por falta de saldo! {data_sacar}")
    elif excedeu_limite:
        print(f"Ops! Parece que a operação falhou! Valor do saque excede o limite! {data_sacar}")
    elif excedeu_saques:
        print(f"Desculpe! A operação falhou! Número máximo de saques excedido. Por favor, volte amanhã. Obrigado(a)! {data_sacar}")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque foi realizado com sucesso! Registro em: {data_sacar}")
    else:
        print(f"Desculpe! Valor informado é inválido. Insira outro valor! {data_sacar}")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    data_extrato = get_formatted_datetime()
    print("\n==================== Extrato =========================")
    print("Até o momento não houve registro de movimentações." if not extrato else extrato)
    print(f"\nSaldo: \tR$ {saldo:.2f} em {data_extrato}")
    print("========================================================")

def criar_nova_conta(agencia, numero_conta, usuarios):
    data_nova_conta = get_formatted_datetime()
    cpf = input("Digite o CPF do Usuário: ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print(f"\n=== Conta criada com sucesso em {data_nova_conta}! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print(f"\n=^^=Ops! Usuário não cadastrado, operação encerrada em {data_nova_conta}! =^^=")

def listar_contas(contas_existentes):
    data_listar_contas = get_formatted_datetime()
    for conta in contas_existentes:
        l = f"""\
            Agência: \t{conta["agencia"]}
            C/C: \t\t{conta["numero_conta"]}
            Nome_Titular:\t{conta["usuario"]["nome"]}
            Criado em: \t{data_listar_contas}
        """
        print("=" * 1000)
        print(textwrap.dedent(l))

def criar_novo_usuario(usuarios):
    data_novo_usuario = get_formatted_datetime()
    cpf = input("Por favor, escreva seu CPF (somente números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print(f"\nJá existe um usuário com esse CPF! {data_novo_usuario} ")
        return
    nome = input("Escreva o seu nome completo, por gentileza: ")
    data_nascimento = input("Agora, escreva a data de nascimento nesse formato(dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logradouro, nº, bairro, Cidade/sigla do Estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print(f"=== Usuário cadastrado com sucesso em {data_novo_usuario}! ===")

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def principal():
    AGENCIA = "0001"
    LIMITE_SAQUES_DIARIO = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas_existentes = []

    while True:
        opcao = menu()

        if opcao == "0":
            valor = float(input(f"Por favor, informe o valor do Depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "1":
            valor = float(input(f"Por favor, informe o valor do Saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques_diario=LIMITE_SAQUES_DIARIO,
            )

        elif opcao == "2":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "3":
            numero_conta = len(contas_existentes) + 1
            conta = criar_nova_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas_existentes.append(conta)

        elif opcao == "4":
            listar_contas(contas_existentes)

        elif opcao == "5":
            criar_novo_usuario(usuarios)

        elif opcao == "6":
            data_sair = get_formatted_datetime()
            print(f"Você saiu. Para retornar, reinicie e escolha uma operação. {data_sair}")
            break

        else:
            data_sair = get_formatted_datetime()
            print(f"Ops! Parece que a operação selecionada é inválida. Por favor tente novamente! {data_sair}")

if __name__ == "__main__":
    principal()
