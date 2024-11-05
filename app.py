import streamlit as st
import csv
import pandas as pd
from datetime import datetime

# Definir o nome do arquivo CSV
arquivo_csv = 'agendamentos.csv'

# Criar um cabeçalho para o arquivo CSV se ele estiver vazio
try:
    pd.read_csv(arquivo_csv)
except pd.errors.EmptyDataError:
    with open(arquivo_csv, 'w') as arquivo:
        arquivo.write("id,data,hora,servico,nome,telefone,pago,manutenção")


# Função para ler agendamentos do arquivo CSV
def ler_agendamentos():
    try:
        return pd.read_csv(arquivo_csv)
    except FileNotFoundError:
        return pd.DataFrame(columns=['id', 'data', 'hora','servico', 'nome', 'telefone', 'adiantado', 'manutenção'])

# Função para salvar agendamento no arquivo CSV
def salvar_agendamento(agendamento):
    agendamentos = ler_agendamentos()
    if agendamentos.empty:
        agendamento['id'] = 1
    else:
        agendamento['id'] = agendamentos['id'].max() + 1
    agendamentos = agendamentos._append(agendamento, ignore_index=True)
    agendamentos.to_csv(arquivo_csv, index=False)

# Interface de Usuário
st.title("Agenda 💅")

# Opções de Serviço
servicos = ["Banho de Gel", "Alongamento", "Esmaltação em Gel", "Mão Comum", "Pé Comum","Mão e Pé Comum"]

# Opções de Pagamento
pago_opcoes = ["Sim", "Não"]

manu_op = ["Sim", "Não"]

# Formulário de Agendamento
with st.form("agendamento"):
    col1, col2 = st.columns(2)
    data_agendamento = col1.date_input("Selecione a Data do Agendamento", format="DD/MM/YYYY")
    data_agendamento_formatada = data_agendamento.strftime('%d/%m/%Y')
    hora_agendamento = col2.text_input("Escreva o Horário")
    servico_escolhido = st.selectbox("Selecione o Serviço", servicos)
    nome_cliente = st.text_input("Nome da Cliente")
    telefone_cliente = st.text_input("Telefone da Cliente")
    col1, col2 = st.columns(2)
    pago_escolhido = col1.selectbox("Adiantamento Pago?", pago_opcoes)
    manutencao = col2.selectbox("Manutenção?", manu_op)
    submitted = st.form_submit_button("Agendar")

    if submitted:
        agendamento = {
            'data': data_agendamento_formatada,
            'hora': hora_agendamento,
           'servico': servico_escolhido,
            'nome': nome_cliente,
            'telefone': telefone_cliente,
            'pago': pago_escolhido,
            'manutenção': manutencao
        }
        salvar_agendamento(agendamento)
        st.success("Agendamento Realizado com Sucesso!")

# Exibir Agendamentos
st.title("Agendamentos Realizados")
if st.button("Consultar Agendamentos"):
    agendamentos = ler_agendamentos()
    if not agendamentos.empty:
        st.write(agendamentos)
        
    else:
        st.write("Nenhum agendamento realizado até o momento.")