import chainlit as cl
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


@cl.langchain_factory
def start():
    file = None
    while file == None:
        file = cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["text/plain"]
        ).send()

    text = file.content.decode("utf-8")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    texts = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(texts, embeddings)
    cl.Message(
        content=f"`{file.name}` uploaded, you can now ask questions!"
    ).send()
    chain = RetrievalQA.from_chain_type(
        ChatOpenAI(temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
    )
    return chain
