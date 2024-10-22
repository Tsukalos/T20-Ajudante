__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from argparse import ArgumentParser
from generation import T20Gen
import streamlit as st

parser = ArgumentParser("Ajudante do Mestre - Atlas de Arton")
parser.add_argument("--generate_embeddings", action="store_true",
                    help="Gera os documentos e embeddings, sobreescrevendo o vectorstore existente.")
parser.add_argument("--reveal_retrieved_docs", action="store_true")
args = parser.parse_args()

st.set_page_config(page_title='AjudanTe20', page_icon='img/128px-D20_icon.png')

@st.cache_resource
def init_data():
    textgen = T20Gen(args.generate_embeddings, args.reveal_retrieved_docs)
    textgen.initialize_data()
    return textgen

t20 = init_data()

st.title("AjudanTe20 (AT20)")
st.write("Um assistente para mestres do sistema Tormenta20 para ajudar na criação de ganchos e NPCs. O assistente AT20 também consegue tirar dúvidas sobre regras do sistema.")

with st.expander("Como funciona?"):
    st.divider()
    st.write("""
Imagine um sistema que organiza informações de um livro de regras e outras fontes em "gavetas" especiais.
Essas gavetas agrupam informações parecidas, como se fossem pastas com temas específicos.

Quando você faz uma pergunta, o sistema transforma sua pergunta em uma "chave" que procura nas gavetas certas.
As gavetas mais relevantes são encontradas, e as informações dentro delas são usadas para criar uma resposta completa e precisa.

É como ter um assistente que encontra rapidamente as informações mais importantes para responder às suas perguntas,
usando um sistema inteligente de organização.
             
Confira exemplos de uso [aqui](https://github.com/Tsukalos/T20-Ajudante/tree/main/exemplos).
"""
             )
with st.form('ask_llm'):
    text = st.text_area(
        'Coloque sua entrada/prompt aqui...', key='llm_input_text')
    with st.expander("Parâmetros de configuração"):
        st.selectbox("Modelo", ['gemini-1.5-pro',
                     'gemini-1.5-flash'], key='model_name')
        st.slider("Temperatura", 0.0, 1.0, value=1.0,
                  step=0.05, key='temperature')
        st.write(
            "[O que é isso?](https://github.com/Tsukalos/T20-Ajudante?#par%C3%A2metros)")
    submitted = st.form_submit_button('Enviar')
    if submitted and text != '':
        t20.generate_response(text, st)


footer = """<style>
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
left: 0;
bottom: 0;
width: 99%;
text-align: right;
}
</style>
<div class="footer">
<p>Código fonte no <a style='color:inherit;' href="https://github.com/Tsukalos/T20-Ajudante" target="_blank">Github</a>.</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)