import streamlit as st

import os
import time

from langchain.text_splitter import MarkdownTextSplitter
from langchain_chroma import Chroma
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import PromptTemplate

from IPython.display import display, Markdown
from argparse import ArgumentParser
from grimoire_loader import create_grimoire_docs

parser = ArgumentParser("Ajudante do Mestre - Atlas de Arton")
parser.add_argument("--generate_embeddings", action="store_true", help="Gera os documentos e embeddings, sobreescrevendo o vectorstore existente.")
args = parser.parse_args()

@st.cache_resource
def initialize_data():
    DATA_DIR = "./data/"

    # define o modelo para gerar os embeddings
    embedding_function = VertexAIEmbeddings("text-embedding-004", location="us-central1")
    # aonde salvar os embeddings
    chroma_dir = os.path.join(DATA_DIR, "chroma_db/")
    if args.generate_embeddings:
        with open(os.path.join(DATA_DIR, 'atlas/output_clean.md'), 'r') as file:
            md_text = file.read()

        docs = []
        # define o divisor de arquivos para o .md do atlas de arton
        splitter = MarkdownTextSplitter(chunk_size=2048, chunk_overlap=128)
        # divide os documentos dado o divisor.
        docs += splitter.create_documents([md_text])
        docs += create_grimoire_docs()
        print(docs)
        vectorstore = Chroma.from_documents(documents=docs, embedding=embedding_function, persist_directory=chroma_dir)
    vectorstore = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)

    retriever = vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 7})

    template = """
    Você é um ajudante de um mestre de RPG, no sistema Tormenta 20, utilizando o cenário padrão de Arton. Não utilize informações de outros sistemas.
    Sua tarefa é responder perguntas sobre itens, equipamentos, classes, raças, poderes, e regras. Considere somente o contexto dado para responder tais perguntas.
    Caso não tenha uma resposta diga que não sabe, não tente inventar uma resposta.
    Em um pedido de criação, você vai ajudar na criação de ganchos, personagens e descrições, assim como responder perguntas sobre o mundo e sistema a partir do contexto disponível.
    Caso o contexto forneça um personagem, tente utiliza-lo.
    Em um pedido de criação, ambientes e personagens devem ter descrições bem desenvolvidas e longas.
    Formate a saída em markdown.

    Contexto: {context}

    Entrada: {question}

    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    return retriever, custom_rag_prompt

retriever, custom_rag_prompt = initialize_data()

st.title("Ajudante do Mestre")



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_response(text):
    llm = ChatVertexAI(model=model, temperature=temperature, max_tokens=8192, location="us-central1")
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )
    st.divider()
    st.write_stream(rag_chain.stream(text))

with st.form('ask_llm'):
    model = st.sidebar.selectbox("Modelo", ['gemini-1.5-pro-preview-0514', 'gemini-1.5-flash-preview-0514', 'gemini-1.0-pro'])
    temperature = st.sidebar.slider("Temperatura", 0.0, 1.0, value=1.0, step=0.05)      
    text = st.text_area('Pergunte aqui...')
    submitted = st.form_submit_button('Enviar')
    if submitted:
        with st.spinner('Gerando...'):
            generate_response(text)
