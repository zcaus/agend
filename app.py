import streamlit as st
import sqlite3
import pandas as pd

# Conectar ao banco de dados (será recriado se não existir)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Criar tabela Agendamentos se não existir
c.execute("""CREATE TABLE IF NOT EXISTS Agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    servico TEXT NOT NULL,
    nome_cliente TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    pago TEXT,
    cancelado TEXT
)""")
conn.commit()

# Função para salvar agendamento
def salvar_agendamento(data, hora, servico, nome_cliente, telefone, email, pago):
    c.execute("""INSERT INTO Agendamentos (data, hora, servico, nome_cliente, telefone, email, pago, cancelado)
                 VALUES (?,?,?,?,?,?,?,?)""", (data, hora, servico, nome_cliente, telefone, email, pago, "Não"))
    conn.commit()

# Função para consultar agendamentos
def consultar_agendamentos():
    c.execute("SELECT * FROM Agendamentos")
    return c.fetchall()

# Função para cancelar agendamento
def cancelar_agendamento(id_agendamento):
    c.execute("UPDATE Agendamentos SET cancelado = 'Sim' WHERE id =?", (id_agendamento,))
    conn.commit()

# Interface de Usuário
st.title("Agenda - Studio Sabrina Azeredo ")

# Opções de Serviço
servicos = ["Manicure Básica", "Pedicure Completo", "Banho de Gel", "Design de Unha Personalizado"]

# Opções de Pagamento
pago_opcoes = ["Sim", "Não"]

# Formulário de Agendamento
with st.form("agendamento"):
    col1, col2 = st.columns(2)
    data_agendamento = col1.date_input("Selecione a Data do Agendamento")
    hora_agendamento = col2.selectbox("Selecione o Horário", ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:30"])
    servico_escolhido = st.selectbox("Selecione o Serviço Desejado", servicos)
    nome_cliente = st.text_input("Nome do Cliente")
    telefone_cliente = st.text_input("Telefone do Cliente")
    email_cliente = st.text_input("E-mail do Cliente")
    pago_escolhido = st.selectbox("Já está pago?", pago_opcoes)
    submitted = st.form_submit_button("Agendar")

    if submitted:
        salvar_agendamento(data_agendamento, hora_agendamento, servico_escolhido, nome_cliente, telefone_cliente, email_cliente, pago_escolhido)
        st.success("Agendamento Realizado com Sucesso!")

# Exibir Agendamentos
st.title("Agendamentos Realizados")
if st.button("Consultar Agendamentos"):
    resultados = consultar_agendamentos()
    if resultados:
        df = pd.DataFrame(resultados, columns=["ID", "Data", "Hora", "Serviço", "Nome do Cliente", "Telefone", "E-mail", "Pago", "Cancelado"])
        st.write(df)
        
        # Adicionar botão para cancelar agendamento
        for index, row in df.iterrows():
            if row["Cancelado"] == "Não":
                if st.button(f"Cancelar Agendamento {row['ID']}"):
                    cancelar_agendamento(row["ID"])
                    st.success(f"Agendamento {row['ID']} cancelado com sucesso!")
    else:
        st.write("Nenhum agendamento realizado até o momento.")

# Fechar conexão com o banco de dados quando a aplicação for fechada
try:
    # Código da aplicação aqui
    st.write("")
    
finally:
    # Fechar a conexão após a aplicação ser encerrada
    if conn:
        conn.close()
        st.write("")