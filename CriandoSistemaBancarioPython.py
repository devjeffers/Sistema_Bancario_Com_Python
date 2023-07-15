
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

        else:
            print("Desculpe, não entendi. Por favor informe um valor válido!")

    elif opcao == "1":
        
        valor = float(input(f"Por favor, informe o valor do Saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:

            print("Ops! Parece que a operação falhou por falta de saldo!")
        
        elif excedeu_limite:

            print("Ops! Parece que a operação falhou! Valor do saque excede o limite!")

        elif excedeu_saques:

            print("Desculpe! A operação falhou! Número máximo de saques excedido. Por favor, volte amanhã. Obrigado(a)!")


        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Desculpe! Valor informado é inválido. Insira outro valor!")


    elif opcao == "2":
        print("\n==================== Extrato =========================")

        print("Até o momento não houve registro de movimentações." if not extrato else extrato)

        print(f"\nSaldo: R$ {saldo:.2f}")

        print("========================================================")

    elif opcao == "3":

        break

    else:
        print("Ops! Parece que a operação selecionada é inválida. Por favor tente novamente!")
