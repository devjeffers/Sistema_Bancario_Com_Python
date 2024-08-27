import pytz
from datetime import datetime

data_deposito = datetime.now(pytz.timezone("America/Manaus"))
data_sacar = datetime.now(pytz.timezone("America/Manaus"))
data_extrato = datetime.now(pytz.timezone("America/Manaus"))
data_sair = datetime.now(pytz.timezone("America/Manaus"))



menu = """
=================== M a f ê B a n k ======================

[0] Depositar
[1] Sacar
[2] Extrato
[3] Sair

==> """

saldo = 0
limite = 500
numero_saques = 0
extrato = ""
LIMITE_SAQUES = 3



while True:
    opcao = input(menu)

    if opcao == "0":
        
        valor = float(input(f"Por favor, informe o valor do Depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Déposito realizado com sucesso: {data_deposito}")
        else:
            print(f"Desculpe, não entendi. Por favor informe um valor válido! {data_deposito}")
         

    elif opcao == "1":
        
        valor = float(input(f"Por favor, informe o valor do Saque: "))
        
        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:

            print(f"Ops! Parece que a operação falhou por falta de saldo! {data_sacar}")
        
        elif excedeu_limite:

            print(f"Ops! Parece que a operação falhou! Valor do saque excede o limite! {data_sacar}")

        elif excedeu_saques:

            print(f"Desculpe! A operação falhou! Número máximo de saques excedido. Por favor, volte amanhã. Obrigado(a)! {data_sacar}")


        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Saque foi realizado com sucesso: {data_sacar}")

        else:
            print(f"Desculpe! Valor informado é inválido. Insira outro valor! {data_sacar}")


    elif opcao == "2":
        print("\n==================== Extrato =========================")

        print("Até o momento não houve registro de movimentações." if not extrato else extrato)

        print(f"\nSaldo: R$ {saldo:.2f} em {data_extrato}")

        print("========================================================")

    elif opcao == "3":
        print(f"Você saiu da sua conta. Para retornar, reenicie e escolha uma operação. {data_sair}")

        break

    else:
        print(f"Ops! Parece que a operação selecionada é inválida. Por favor tente novamente! {data_sair}")
