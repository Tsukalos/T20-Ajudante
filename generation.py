from getpass import getpass
import os

from langchain.text_splitter import MarkdownTextSplitter
from langchain_chroma import Chroma


from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from loaders import book_loader, get_grimoire_docs

from pathlib import Path

class T20Gen():

    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH : HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT : HarmBlockThreshold.BLOCK_NONE,
    }   

    def __init__(self, generate_embeddings=False, reveal_retrieved_docs=False, data_path="./data/"):
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass("Provide your Google API key here: ")

        self.generate_embeddings = generate_embeddings
        self.reveal_retrieved_docs = reveal_retrieved_docs

        self.data_dir = Path(data_path)
        
    def initialize_data(self):
        
        # define o modelo para gerar os embeddings
        embedding_function = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004")
        # aonde salvar os embeddings
        chroma_dir = self.data_dir / "chroma_db/"
        if self.generate_embeddings:
            # with open(os.path.join(DATA_DIR, 'atlas/output_clean.md'), 'r') as file:
            #     md_text = file.read()

            md_text = (self.data_dir / 'atlas/output_clean.md').read_text()

            docs = []
            # define o divisor de arquivos para o .md do atlas de arton
            splitter = MarkdownTextSplitter(chunk_size=1024, chunk_overlap=256)

            # seções do livro
            texts, metadatas = book_loader()
            # divide os documentos dado o divisor.
            docs += splitter.create_documents([md_text] + texts, metadatas=[
                                            {"source": "atlas/output_clean.md"}] + metadatas)
            docs += get_grimoire_docs()

            print(f'Num. docs: {len(docs)}')

            vectorstore = Chroma.from_documents(
                collection_name="t20",
                documents=docs, 
                embedding=embedding_function, 
                persist_directory=str(chroma_dir)
            )
        else:
            vectorstore = Chroma(
                collection_name="t20",
                persist_directory=str(chroma_dir),
                embedding_function=embedding_function)
        
        self.retriever = vectorstore.as_retriever(
            search_type="mmr", 
            search_kwargs={"k": 3}
        )

        prompt_file = Path(self.data_dir) / 'prompt' / 't20.md'
        template = (prompt_file).read_text()
        self.custom_rag_prompt = PromptTemplate.from_template(template)

    def format_docs(self, docs):
        if self.reveal_retrieved_docs:
            for doc in docs:
                print(f'{doc}\n\n\n')
        return "\n\n".join(doc.page_content for doc in docs)
        
    def generate_response(self, text, st):
        with st.spinner('Gerando...'):
            llm = ChatGoogleGenerativeAI(
                model=st.session_state.model_name,
                temperature=st.session_state.temperature, 
                max_tokens=8192, 
                max_output_tokens=8192, 
                max_retries=12, 
                timeout=30,
                safety_settings=self.safety_settings)
            
            rag_chain = (
                {"context": self.retriever | self.format_docs,
                    "question": RunnablePassthrough()}
                | self.custom_rag_prompt
                | llm
                | StrOutputParser()
            )
            full = st.write_stream(rag_chain.stream(text))
            with st.expander("Código markdown"):
                st.code(full, language="markdown")
