![img-logo](./img/128px-D20_icon.png)
# AjudanTe20  

AjudanTe20 é um assistente que utiliza das capacidades geracionais dos modelos Gemini, juntamente técnicas de RAG ("*Retrieval-augmented generation*"), para fornecer informações relevantes ao mestre de RPG referentes ao sistema Tormenta 20.

Adicionalmente, o assistente pode ajudar na criação de ganchos e personagens para uma aventura, utilizando do contexto do mundo de Arton presente em sua base de conhecimento.

## Funcionamento
![ex-gif](./img/example.gif)

## Requerimentos
Para usar a IA Generativa do Vertex AI, você deve ter o pacote Python `langchain-google-vertexai` instalado e uma das seguintes opções:

- Ter as credenciais configuradas para o seu ambiente (gcloud, identidade de carga de trabalho, etc...)
- Armazenar o caminho para um arquivo JSON da conta de serviço como a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS.

Veja a [documentação oficial](https://cloud.google.com/docs/authentication/application-default-credentials#GAC) para mais informações.

#### requirements.txt
```
ipython==8.12.3
langchain==0.1.20
langchain_chroma==0.1.1
langchain_community==0.0.38
langchain_core==0.1.52
langchain_google_vertexai==1.0.3
streamlit==1.34.0
jq==1.7.0
```