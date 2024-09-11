import streamlit as st
import pytz
from datetime import datetime
from abc import ABC, abstractmethod

# Função para obter a data e hora atual em Manaus
def obter_data_hora_manaus():
    return datetime.now(pytz.timezone("America/Manaus"))

# Vamos criar a Classe Cliente e PF
class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco

class PF(Cliente):
    pass

# Vamos criar a Classe Transação abstrata, não esquecer de fazer a importação...
class Transacao(ABC):
    @abstractmethod
    def registrar(self):
        pass

# Agora vamos criar a Classe Saque
class Saque(Transacao):
    def __init__(self, valor, conta, saldo):
        self.valor = valor
        self.conta = conta
        self.saldo = saldo

    def registrar(self):
        data_saque = obter_data_hora_manaus()
        if self.valor > self.conta.saldo:
            st.error(f"Saldo insuficiente! Operação falhou em {data_saque}.")
        elif self.valor > self.conta.limite:
            st.error(f"O valor do saque excede o limite permitido! Operação falhou em {data_saque}.")
        elif self.conta.numero_saques >= self.conta.limite_saques_diario:
            st.error(f"Número máximo de saques diários excedido em {data_saque}.")

        elif self.conta.valor > 0:
            self.conta.saldo -= self.valor
            self.conta.numero_saques += 1
            self.conta.extrato.append(f"Saque: R$ {self.valor:.2f} em {data_saque}")
            st.success(f"Saque de R$ {self.valor:.2f} realizado com sucesso em {data_saque}!")

        else:
            print(f"Desculpe! Valor informado é inválido. Insira outro valor! {data_saque}")

# Criando a Classe Depósito
class Deposito(Transacao):
    def __init__(self, valor, conta):
        self.valor = valor
        self.conta = conta

    def registrar(self):
        data_deposito = obter_data_hora_manaus()
        self.conta.saldo += self.valor
        self.conta.extrato.append(f"Depósito: R$ {self.valor:.2f} em {data_deposito}")
        st.success(f"Depósito de R$ {self.valor:.2f} realizado com sucesso em {data_deposito}!")

# Vamos criar a Classe Conta:
class Conta:
    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0.0
        self.limite = 1000.0
        self.extrato = []
        self.numero_saques = 0
        self.limite_saques_diario = 5

    def exibir_extrato(self):
        data_extrato = obter_data_hora_manaus()
        st.write("### Extrato")
        if not self.extrato:
            st.write("Até o momento não houve registro de movimentações.")
        else:
            for transacao in self.extrato:
                st.write(transacao)
        st.write(f"**Saldo:** R$ {self.saldo:.2f} em {data_extrato}")

# Classe Conta Corrente (CC)
class CC(Conta):
    pass

# Funções principais
def criar_novo_usuario():
    data_novo_usuario = obter_data_hora_manaus()
    cpf = st.text_input("Por favor, escreva seu CPF (somente números):")
    usuario_existente = filtrar_usuarios(cpf)

    if usuario_existente:
        st.error(f"Já existe um usuário com esse CPF! {data_novo_usuario}")
    else:
        nome = st.text_input("Escreva o seu nome completo, por gentileza:")
        data_nascimento = st.text_input("Escreva a data de nascimento (dd-mm-aaaa):")
        endereco = st.text_input("Informe seu endereço (Logradouro, nº, Bairro, Cidade/Sigla do Estado):")
        if st.button("Cadastrar Usuário"):
            novo_usuario = PF(nome, cpf, data_nascimento, endereco)
            st.session_state.usuarios.append(novo_usuario)
            st.success(f"Usuário {nome} cadastrado com sucesso!")

def criar_nova_conta():
    data_nova_conta = obter_data_hora_manaus()
    cpf = st.text_input("Digite o CPF do Usuário:")
    usuario = filtrar_usuarios(cpf)

    if usuario:
        conta = CC(st.session_state.agencia, len(st.session_state.contas_existentes) + 1, usuario)
        st.session_state.contas_existentes.append(conta)
        st.success(f"Conta criada com sucesso em {data_nova_conta}! Agência: {conta.agencia} Conta: {conta.numero_conta}")
    else:
        st.error(f"Usuário não cadastrado! {data_nova_conta}")

def depositar():
    if st.session_state.contas_existentes:
        conta_selecionada = st.selectbox(
            "Selecione a Conta:",
            st.session_state.contas_existentes,
            format_func=lambda c: f"Agência: {c.agencia}, Conta: {c.numero_conta}"
        )
        valor = st.number_input("Por favor, informe o valor do Depósito:", min_value=0.0, step=0.01)
        
        if st.button("Confirmar Depósito"):
            if valor > 0:
                # Criando a instância de Depósito
                deposito = Deposito(valor, conta_selecionada)
                
                # Chamando o método registrar() para efetivar o depósito
                deposito.registrar()
            else:
                st.error("Valor inválido! Depósito não realizado.")
    else:
        st.error("Nenhuma conta disponível para depósito.")

def sacar():
    # Verifica se há contas disponíveis
    if st.session_state.contas_existentes:
        # Seleciona a conta pelo selectbox
        conta_selecionada = st.selectbox(
            "Selecione a Conta:",
            st.session_state.contas_existentes,
            format_func=lambda c: f"Agência: {c.agencia}, Conta: {c.numero_conta}"
        )

        # Input para o valor do saque
        valor = st.number_input("Por favor, informe o valor do Saque:", min_value=0.0, step=0.01)

        # Ao clicar no botão, executa a lógica do saque
        if st.button("Confirmar Saque"):
            # Verifica se o valor é positivo
            if valor > 0:
                try:
                    # Cria um objeto Saque
                    saque = Saque(valor, conta_selecionada)
                    # Registra o saque
                    saque.registrar()
                except AttributeError as e:
                    st.error(f"Erro ao realizar o saque: {str(e)}")
            else:
                st.error("Valor inválido! Saque não realizado.")
    else:
        st.error("Nenhuma conta disponível para saque.")

def listar_contas():
    data_listar_contas = obter_data_hora_manaus()
    st.write("||||| Contas Existentes |||||")
    for conta in st.session_state.contas_existentes:
        st.write(f"Agência: {conta.agencia} | C/C: {conta.numero_conta} | Nome Titular: {conta.cliente.nome} - {data_listar_contas}")

def filtrar_usuarios(cpf):
    usuarios_filtrados = [usuario for usuario in st.session_state.usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Declaramos aqui a função principal sem perder a interação com o usuário...
# Função principal
def principal():
    
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = []
    if 'contas_existentes' not in st.session_state:
        st.session_state.contas_existentes = []
    if 'agencia' not in st.session_state:
        st.session_state.agencia = "0001"
    
    st.title("Mafê Bank")
    st.subheader("Bem-vindo ao Sistema de Operações Bancárias!")

# aqui ainda mantemos as seleções anteriores, não alteramos, apenas refatoramos o código...
    option = st.selectbox('Escolha uma operação:', ['Depositar', 'Sacar', 'Extrato', 'Nova conta', 'Listar contas', 'Novo usuário', 'Sair'])

    if option == 'Depositar':
        depositar()
    elif option == 'Sacar':
        sacar()
    elif option == 'Extrato':
        if st.session_state.contas_existentes:
            conta_selecionada = st.selectbox(
            "Selecione a Conta:",
            st.session_state.contas_existentes,
            format_func=lambda c: f"Agência: {c.agencia}, Conta: {c.numero_conta}"
        )
            conta_selecionada.exibir_extrato()  # Chama a função para exibir o extrato
        else:
            st.error("Nenhuma conta disponível para exibir o extrato.")

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
