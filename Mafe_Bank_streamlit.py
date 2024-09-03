import streamlit as st
import pytz
from datetime import datetime

# Função para obter a data e hora atual em Manaus
def obter_data_hora_manaus():
    return datetime.now(pytz.timezone("America/Manaus"))

# Funções principais
def depositar(saldo, extrato):
    valor = st.number_input("Por favor, informe o valor do Depósito:", min_value=0.0, step=0.01)
    data_deposito = obter_data_hora_manaus()
    if st.button("Confirmar Depósito"):
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: \tR$ {valor:.2f} em {data_deposito}\n"
            st.success(f"Depósito realizado com sucesso em {data_deposito}!")
        else:
            st.error(f"Valor inválido! Depósito não realizado. {data_deposito}")
    return saldo, extrato

def sacar(saldo, extrato, limite, numero_saques, limite_saques_diario):
    valor = st.number_input("Por favor, informe o valor do Saque:", min_value=0.0, step=0.01)
    data_sacar = obter_data_hora_manaus()
    if st.button("Confirmar Saque"):
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques_diario

        if excedeu_saldo:
            st.error(f"Saldo insuficiente! Operação falhou. {data_sacar}")
        elif excedeu_limite:
            st.error(f"Valor do saque excede o limite permitido! Operação falhou. {data_sacar}")
        elif excedeu_saques:
            st.error(f"Número máximo de saques diários excedido! {data_sacar}")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: \t\tR$ {valor:.2f} em {data_sacar}\n"
            numero_saques += 1
            st.success(f"Saque realizado com sucesso em {data_sacar}!")
        else:
            st.error(f"Valor inválido! Saque não realizado. {data_sacar}")
    return saldo, extrato

def exibir_extrato(saldo, extrato):
    data_extrato = obter_data_hora_manaus()
    st.write("### Extrato")
    st.write("Até o momento não houve registro de movimentações." if not extrato else extrato)
    st.write(f"**Saldo:** R$ {saldo:.2f} em {data_extrato}")

def criar_nova_conta(agencia, numero_conta, usuarios):
    data_nova_conta = obter_data_hora_manaus()
    cpf = st.text_input("Digite o CPF do Usuário:")
    usuario = filtrar_usuarios(cpf, usuarios)

    if st.button("Criar Conta"):
        if usuario:
            st.success(f"Conta criada com sucesso em {data_nova_conta}!")
            return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        else:
            st.error(f"Usuário não cadastrado. Operação encerrada em {data_nova_conta}.")
    return None

def listar_contas(contas_existentes):
    data_listar_contas = obter_data_hora_manaus()
    st.write("### Contas Existentes")
    for conta in contas_existentes:
        st.write(f"Agência: {conta['agencia']} | C/C: {conta['numero_conta']} | Nome Titular: {conta['usuario']['nome']} - {data_listar_contas}")

def criar_novo_usuario(usuarios):
    data_novo_usuario = obter_data_hora_manaus()
    cpf = st.text_input("Por favor, escreva seu CPF (somente números):")
    usuario = filtrar_usuarios(cpf, usuarios)

    if st.button("Cadastrar Usuário"):
        if usuario:
            st.error(f"Já existe um usuário com esse CPF! {data_novo_usuario}")
        else:
            nome = st.text_input("Escreva o seu nome completo, por gentileza:")
            data_nascimento = st.text_input("Escreva a data de nascimento (dd-mm-aaaa):")
            endereco = st.text_input("Informe seu endereço (logradouro, nº, bairro, cidade/sigla do estado):")
            usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
            st.success(f"Usuário cadastrado com sucesso em {data_novo_usuario}!")

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função principal
def principal():
    AGENCIA = "0001"
    LIMITE_SAQUES_DIARIO = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas_existentes = []

    st.title("Mafê Bank")

    option = st.selectbox(
        'Escolha uma operação:',
        ['Depositar', 'Sacar', 'Extrato', 'Nova conta', 'Listar contas', 'Novo usuário', 'Sair'])

    if option == 'Depositar':
        saldo, extrato = depositar(saldo, extrato)
    elif option == 'Sacar':
        saldo, extrato = sacar(saldo, extrato, limite, numero_saques, LIMITE_SAQUES_DIARIO)
    elif option == 'Extrato':
        exibir_extrato(saldo, extrato)
    elif option == 'Nova conta':
        numero_conta = len(contas_existentes) + 1
        conta = criar_nova_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas_existentes.append(conta)
    elif option == 'Listar contas':
        listar_contas(contas_existentes)
    elif option == 'Novo usuário':
        criar_novo_usuario(usuarios)
    elif option == 'Sair':
        st.write("Você saiu. Para retornar, reinicie e escolha uma operação.")

if __name__ == "__main__":
    principal()
