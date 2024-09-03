import streamlit as st
import pytz
from datetime import datetime

# Função para obter a data e hora atual em Manaus
def obter_data_hora_manaus():
    return datetime.now(pytz.timezone("America/Manaus"))

# Funções principais
def depositar():
    valor = st.number_input("Por favor, informe o valor do Depósito:", min_value=0.0, step=0.01)
    data_deposito = obter_data_hora_manaus()
    if st.button("Confirmar Depósito"):
        if valor > 0:
            st.session_state.saldo += valor
            st.session_state.extrato += f"Depósito: \tR$ {valor:.2f} em {data_deposito}\n"
            st.success(f"Depósito realizado com sucesso em {data_deposito}!")
        else:
            st.error(f"Valor inválido! Depósito não realizado. {data_deposito}")

def sacar():
    valor = st.number_input("Por favor, informe o valor do Saque:", min_value=0.0, step=0.01)
    data_sacar = obter_data_hora_manaus()
    if st.button("Confirmar Saque"):
        excedeu_saldo = valor > st.session_state.saldo
        excedeu_limite = valor > st.session_state.limite
        excedeu_saques = st.session_state.numero_saques >= st.session_state.limite_saques_diario

        if excedeu_saldo:
            st.error(f"Saldo insuficiente! Operação falhou. {data_sacar}")
        elif excedeu_limite:
            st.error(f"Valor do saque excede o limite permitido! Operação falhou. {data_sacar}")
        elif excedeu_saques:
            st.error(f"Número máximo de saques diários excedido! {data_sacar}")
        elif valor > 0:
            st.session_state.saldo -= valor
            st.session_state.extrato += f"Saque: \t\tR$ {valor:.2f} em {data_sacar}\n"
            st.session_state.numero_saques += 1
            st.success(f"Saque realizado com sucesso em {data_sacar}!")
        else:
            st.error(f"Valor inválido! Saque não realizado. {data_sacar}")

def exibir_extrato():
    data_extrato = obter_data_hora_manaus()
    st.write("### Extrato")
    st.write("Até o momento não houve registro de movimentações." if not st.session_state.extrato else st.session_state.extrato)
    st.write(f"**Saldo:** R$ {st.session_state.saldo:.2f} em {data_extrato}")

def criar_nova_conta():
    data_nova_conta = obter_data_hora_manaus()
    cpf = st.text_input("Digite o CPF do Usuário:")
    usuario = filtrar_usuarios(cpf)

    if st.button("Criar Conta"):
        if usuario:
            st.success(f"Conta criada com sucesso em {data_nova_conta}!")
            conta = {"agencia": st.session_state.agencia, "numero_conta": len(st.session_state.contas_existentes) + 1, "usuario": usuario}
            st.session_state.contas_existentes.append(conta)
        else:
            st.error(f"Usuário não cadastrado. Operação encerrada em {data_nova_conta}.")

def listar_contas():
    data_listar_contas = obter_data_hora_manaus()
    st.write("### Contas Existentes ###")
    for conta in st.session_state.contas_existentes:
        st.write(f"Agência: {conta['agencia']} | C/C: {conta['numero_conta']} | Nome Titular: {conta['usuario']['nome']} - {data_listar_contas}")

def criar_novo_usuario():
    data_novo_usuario = obter_data_hora_manaus()
    cpf = st.text_input("Por favor, escreva seu CPF (somente números):")
    usuario = filtrar_usuarios(cpf)

    if st.button("Cadastrar Usuário"):
        if usuario:
            st.error(f"Já existe um usuário com esse CPF! {data_novo_usuario}")
        else:
            nome = st.text_input("Escreva o seu nome completo, por gentileza:")
            data_nascimento = st.text_input("Escreva a data de nascimento (dd-mm-aaaa):")
            endereco = st.text_input("Informe seu endereço (logradouro, nº, bairro, cidade/sigla do estado):")
            st.session_state.usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
            st.success(f"Usuário cadastrado com sucesso em {data_novo_usuario}!")

def filtrar_usuarios(cpf):
    usuarios_filtrados = [usuario for usuario in st.session_state.usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função principal
def principal():

    if 'saldo' not in st.session_state:
        st.session_state.saldo = 0.0
    
    if 'limite' not in st.session_state:
        st.session_state.limite = 500.0

    if 'extrato' not in st.session_state:
        st.session_state.extrato = ""
    
    if 'numero_saques' not in st.session_state:
        st.session_state.numero_saques = 0
    
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = []

    if 'contas_existentes' not in st.session_state:
        st.session_state.contas_existentes = []

    if 'agencia' not in st.session_state:
        st.session_state.agencia = "0001"

    if 'limite_saques_diario' not in st.session_state:
        st.session_state.limite_saques_diario = 3

    st.title("Mafê Bank")

    option = st.selectbox(
        'Escolha uma operação:',
        ['Depositar', 'Sacar', 'Extrato', 'Nova conta', 'Listar contas', 'Novo usuário', 'Sair'])

    if option == 'Depositar':
        depositar()
    elif option == 'Sacar':
        sacar()
    elif option == 'Extrato':
        exibir_extrato()
    elif option == 'Nova conta':
        criar_nova_conta()
    elif option == 'Listar contas':
        listar_contas()
    elif option == 'Novo usuário':
        criar_novo_usuario()
    elif option == 'Sair':
        st.write("Você saiu. Para retornar, reinicie e escolha uma operação.")

if __name__ == "__main__":
    principal()
