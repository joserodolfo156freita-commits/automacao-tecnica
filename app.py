import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# Configuração da página
st.set_page_config(
    page_title="Plataforma de Automação Técnica",
    page_icon="⚙️",
    layout="wide"
)

# ==========================================
# SISTEMA DE LICENCIAMENTO / PAYWALL
# ==========================================
st.sidebar.markdown("## 🔐 Painel de Assinatura")
st.sidebar.markdown("Insira sua chave de acesso para desbloquear a plataforma profissional.")

# Chave de demonstração (pode alterar ou gerir dinamicamente)
CHAVE_DEMO = "VIP-2026-BRASIL"

chave_input = st.sidebar.text_input("Chave de Licença:", type="password")

# Simulação de compra / aquisição
st.sidebar.markdown("---")
st.sidebar.markdown("### Não tem uma?")
st.sidebar.info("Adquira o acesso mensal por **R$ 97/mês** para automatizar sua empresa.")
if st.sidebar.button("🛒 Comprar Acesso (Simulação Pix)"):
    st.sidebar.success("Link de pagamento simulado! Use a chave de demonstração abaixo para testar.")

st.sidebar.markdown("---")
st.sidebar.success(f"**Chave de demonstração para teste:** `{CHAVE_DEMO}`")

# Verifica se a licença é válida
licenca_valida = (chave_input == CHAVE_DEMO)

if not licenca_valida:
    st.warning("Por favor, insira uma **Chave de Licença Válida** na barra lateral para acessar os Módulos de Automação.")
    st.stop()  # Interrompe a execução do resto do app se não estiver autorizado

# Se a licença for válida, exibe a aplicação principal
st.sidebar.success("✅ Licença Ativa com Sucesso!")

# ==========================================
# CORPO PRINCIPAL DA APLICAÇÃO
# ==========================================
st.title("⚙️ Plataforma Comercial - Automação Técnica")
st.markdown("Soluções rápidas para engenharia, orçamentos e gestão.")

# MENU DE NAVEGAÇÃO NO TOPO (Horizontal e sempre visível)
menu = st.radio("Selecione o Módulo de Trabalho:", ["Orçamentos Técnicos", "Análise de Custos e Planilhas"], horizontal=True)

st.markdown("---")

# ==========================================
# MÓDULO 1: Orçamentos Técnicos (PDF)
# ==========================================
if menu == "Orçamentos Técnicos":
    st.subheader("📄 Gerador de Orçamentos Técnicos")
    
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nome do Cliente / Empresa:")
        equipamento = st.text_input("Equipamento / Sistema:")
    with col2:
        prazo = st.text_input("Prazo de Execução:", value="5 dias úteis")
        validade = st.text_input("Validade da Proposta:", value="15 dias")

    escopo = st.text_area("Escopo / Detalhes Técnicos:")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        custo_materiais = st.number_input("Custo de Materiais (R$)", min_value=0.0, value=0.0, step=100.0)
    with col_m2:
        custo_mao_obra = st.number_input("Custo de Mão de Obra (R$)", min_value=0.0, value=0.0, step=100.0)
    with col_m3:
        margem_lucro = st.slider("Margem de Lucro (%)", min_value=0, max_value=100, value=30)

    # Cálculo do orçamento
    subtotal = custo_materiais + custo_mao_obra
    lucro = subtotal * (margem_lucro / 100)
    total_geral = subtotal + lucro

    st.markdown(f"### 💰 Valor Total do Orçamento: **R$ {total_geral:,.2f}**")

    if st.button("Gerar Orçamento em PDF"):
        if not cliente or not equipamento:
            st.error("Por favor, preencha o Nome do Cliente e o Equipamento.")
        else:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "ORCAMENTO TECNICO - AUTOMACAO", ln=True, align="C")
                pdf.ln(10)
                
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 8, f"Cliente: {cliente}", ln=True)
                pdf.cell(0, 8, f"Equipamento: {equipamento}", ln=True)
                pdf.cell(0, 8, f"Prazo: {prazo} | Validade: {validade}", ln=True)
                pdf.ln(5)
                
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Escopo Tecnico:", ln=True)
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 6, escopo)
                pdf.ln(10)
                
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Resumo Financeiro:", ln=True)
                pdf.set_font("Arial", "", 11)
                pdf.cell(0, 6, f"Custo de Materiais: R$ {custo_materiais:,.2f}", ln=True)
                pdf.cell(0, 6, f"Custo de Mao de Obra: R$ {custo_mao_obra:,.2f}", ln=True)
                pdf.cell(0, 6, f"Margem Aplicada: {margem_lucro}%", ln=True)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, f"TOTAL GERAL: R$ {total_geral:,.2f}", ln=True)
                
                pdf_output = pdf.output(dest='S').encode('latin1')
                
                st.download_button(
                    label="📥 Descarregar PDF do Orçamento",
                    data=pdf_output,
                    file_name="orcamento_tecnico.pdf",
                    mime="application/pdf"
                )
                st.success("Orçamento gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")

# ==========================================
# MÓDULO 2: Análise de Planilhas / Custos
# ==========================================
elif menu == "Análise de Custos e Planilhas":
    st.subheader("📊 Análise de Custos e Dados (Excel / CSV)")
    
    arquivo_enviado = st.file_uploader("Carregar planilha (.csv ou .xlsx)", type=["csv", "xlsx"])

    if arquivo_enviado is not None:
        try:
            if arquivo_enviado.name.endswith('.csv'):
                df = pd.read_csv(arquivo_enviado)
            else:
                df = pd.read_excel(arquivo_enviado)

            st.success("Ficheiro carregado com sucesso!")
            st.dataframe(df.head())
            st.info(f"Total de registos analisados: **{len(df)}** linhas.")

            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                coluna_escolhida = st.selectbox("Selecione a coluna para gerar gráfico:", numeric_cols)
                st.bar_chart(df[coluna_escolhida])
            else:
                st.warning("O ficheiro não contém colunas numéricas adequadas para gráficos automáticos.")
        except Exception as e:
            st.error(f"Erro ao processar o ficheiro: {e}")
