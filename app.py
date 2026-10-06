import streamlit as st
from fpdf import FPDF
import pandas as pd
import os

# Configuração da página responsiva
st.set_page_config(
    page_title="Plataforma de Automação Técnica & Industrial",
    page_icon="🚀",
    layout="centered"
)

# ==========================================
# SISTEMA DE LICENCIAMENTO / PAYWALL
# ==========================================
# Lista de chaves válidas (No futuro, isto pode ser ligado a uma base de dados ou API de pagamento)
CHAVES_VALIDAS = ["VIP-2026-BRASIL", "CLIENTE-DEMO-99", "INDUSTRIAL-PRO"]

st.sidebar.title("🔐 Painel de Assinatura")
st.sidebar.markdown("Insira a sua chave de acesso para desbloquear a plataforma profissional.")

chave_inserida = st.sidebar.text_input("Chave de Licença:", type="password")

# Botão para simular compra / obter chave
st.sidebar.markdown("---")
st.sidebar.markdown("### Não tem uma licença?")
st.sidebar.info("Adquira o acesso mensal por **R$ 97/mês** para automatizar a sua empresa.")
if st.sidebar.button("🛒 Comprar Acesso (Simulação Pix)"):
    st.sidebar.success("Chave de demonstração para teste: `VIP-2026-BRASIL`")

# Verificar se a chave é válida
if chave_inserida not in CHAVES_VALIDAS:
    st.title("🔒 Acesso Restrito - Plataforma Comercial")
    st.warning("Por favor, insira uma **Chave de Licença Válida** na barra lateral para aceder aos Módulos de Automação.")
    st.stop( ) # Interrompe a execução do app se não tiver licença

# ==========================================
# APLICAÇÃO PRINCIPAL (Liberada para Assinantes)
# ==========================================
st.sidebar.success("✅ Licença Ativa com Sucesso!")

st.title("🚀 Plataforma de Automação")
st.markdown("### Soluções rápidas para engenharia e gestão.")

# Criação de abas otimizadas
aba1, aba2 = st.tabs(["⚡ Orçamentos", "📊 Planilhas"])

# ==========================================
# MÓDULO 1: Orçamentos e Laudos
# ==========================================
with aba1:
    st.subheader("Gerador de Orçamentos")

    with st.form("form_orcamento"):
        cliente_nome = st.text_input("Nome do Cliente / Empresa")
        servico_titulo = st.text_input("Título do Serviço")
        
        descricao_tecnica = st.text_area("Escopo / Detalhes Técnicos:")
        
        custo_materiais = st.number_input("Custo de Materiais (R$)", min_value=0.0, format="%.2f")
        custo_mao_obra = st.number_input("Custo de Mão de Obra (R$)", min_value=0.0, format="%.2f")
        margem_lucro = st.slider("Margem de Lucro (%)", min_value=0, max_value=100, value=30)
        
        submitted_orcamento = st.form_submit_button("Gerar Orçamento em PDF")

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, 'ORÇAMENTO & LAUDO TÉCNICO', 0, 1, 'C')
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def gerar_pdf(cliente, servico, escopo, total):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Serviço: {servico}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt="Escopo Técnico:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 7, txt=escopo)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt=f"Valor Total: R$ {total:.2f}", ln=True)
        
        nome_arquivo = "orcamento_tecnico.pdf"
        pdf.output(nome_arquivo)
        return nome_arquivo

    if submitted_orcamento:
        if not cliente_nome or not servico_titulo:
            st.error("Preencha o nome do cliente e o título.")
        else:
            subtotal = custo_materiais + custo_mao_obra
            valor_total = subtotal * (1 + (margem_lucro / 100))
            
            st.success("Gerado com sucesso!")
            st.metric(label="Valor Final", value=f"R$ {valor_total:.2f}")
            
            pdf_path = gerar_pdf(cliente_nome, servico_titulo, descricao_tecnica, valor_total)
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 Baixar PDF",
                    data=file,
                    file_name=f"Orcamento_{cliente_nome.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )

# ==========================================
# MÓDULO 2: Análise de Planilhas
# ==========================================
with aba2:
    st.subheader("Análise de Custos")
    arquivo_enviado = st.file_uploader("Carregar planilha (.csv ou .xlsx)", type=["csv", "xlsx"])

    if arquivo_enviado is not None:
        if arquivo_enviado.name.endswith('.csv'):
            df = pd.read_csv(arquivo_enviado)
        else:
            df = pd.read_excel(arquivo_enviado)

        st.dataframe(df.head())
        st.info(f"Total de registos analisados: **{len(df)}** linhas.")
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            coluna_escolhida = st.selectbox("Selecione a coluna para gráfico:", numeric_cols)
            st.bar_chart(df[coluna_escolhida])
        else:
            st.warning("Sem colunas numéricas para gráficos.")