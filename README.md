![img-logo](./img/128px-D20_icon.png)
# AjudanTe20  

AjudanTe20 é um assistente que utiliza das capacidades geracionais dos modelos Gemini, juntamente técnicas de RAG ("*Retrieval-augmented generation*"), para fornecer informações relevantes ao mestre de RPG referentes ao sistema Tormenta 20.

Adicionalmente, o assistente pode ajudar na criação de ganchos e personagens para uma aventura, utilizando do contexto do mundo de Arton presente em sua base de conhecimento.

https://ajudante20.com/

## Funcionamento
![ex-gif](./img/example.gif)

## Requerimentos
Para usar a IA Generativa do Vertex AI, você deve ter o pacote Python `langchain-google-vertexai` instalado e uma das seguintes opções:

- Ter as credenciais configuradas para o seu ambiente (gcloud, identidade de carga de trabalho, etc...)
- Armazenar o caminho para um arquivo JSON da conta de serviço como a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS.

Veja a [documentação oficial](https://cloud.google.com/docs/authentication/application-default-credentials#GAC) para mais informações.

#### requirements.txt
```
langchain
langchain_chroma
langchain_google_vertexai
streamlit
jq
```

### Agradecimentos

@pyanderson pelos [dados extraídos](https://github.com/pyanderson/roll20_tormenta20_grimoire) do livro.
