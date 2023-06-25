from modal import Stub, web_endpoint, Image, Secret
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import os
import pinecone
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationalRetrievalChain


image = Image.debian_slim().pip_install(
    # langchain pkgs
    "langchain~=0.0.138",
    "openai~=0.27.4",
    "tiktoken==0.3.0",
    'pinecone-client==2.2.2',
)

stub = Stub(
    name="sensiocoders-blog-qa",
    image=image,
    secrets=[
        Secret.from_name("pinecone-api-key"),
        Secret.from_name("pinecone-environment"),
        Secret.from_name("openai-api-key")
    ],
)

def qa_pipeline():
    k = 1 # número de documentos a recuperar
    model = 'gpt-3.5-turbo' if k < 3 else 'gpt-3.5-turbo-16k' # modelo de OpenAI a usar

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'), disallowed_special=())
    pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment=os.environ['PINECONE_ENVIRONMENT'])
    vectorstore = Pinecone.from_existing_index('blog-qa', embeddings)
    llm = OpenAI(model_name=model, temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'], max_tokens=256)
    template = """Dado el siguiente contexto, reponde la pregunta.
    Si no sabes la respuesta, responde con "No lo sé". 
    No inventes respuestas.
    Responde siempre en español.

    Contexto:

    {context} 

    Pregunta:

    {question}"""
    prompt = PromptTemplate(template=template, input_variables=['context', 'question'])
    template = """Dado el siguiente historial de conversación, reformula la pregunta de forma que el modelo pueda responderla:

    Historial:

    {chat_history}

    Pregunta:

    {question}

    Progunta reformulada:"""
    condense_question_prompt = PromptTemplate.from_template(template)
    return ConversationalRetrievalChain.from_llm(
        llm, 
        vectorstore.as_retriever(search_kwargs={'k': k}), 
        return_source_documents=True, 
        condense_question_prompt=condense_question_prompt, 
        combine_docs_chain_kwargs={'prompt': prompt}
    )

@stub.function()
@web_endpoint(method="GET")
def api(query: str):
    qa = qa_pipeline()
    chat_history = [] # para usar history tendría que tener info del usuario y guardar conversaciones: https://modal.com/docs/guide/local-data
    result = qa({"question": query, "chat_history": chat_history})
    return {
        "answer": result['answer'],
        "sources": [source.metadata['source'] for source in result['source_documents']]
    }

@stub.function()
def cli(query: str):
    qa = qa_pipeline()
    chat_history = []
    result = qa({"question": query, "chat_history": chat_history})
    # chat_history.append((query, result['answer']))
    print(result['answer'])
    print("Source documents:")
    for source in result['source_documents']:
        print(source.metadata['source'])