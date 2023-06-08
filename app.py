import chainlit as cl
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import UnstructuredHTMLLoader, PyPDFLoader, CSVLoader
import os

welcome_message = """### Welcome to Chat with 👋
You can upload a file or paste a url to chat with.
I support many types of files and urls.
"""

supported_file_types = [
    "text/plain",  # Text
    "text/html",  # HTML
    "application/pdf",  # PDF
    "text/csv",  # CSV
]


embeddings = OpenAIEmbeddings()
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True
)
llm = ChatOpenAI(temperature=0, model="gpt-4")
condense_question_llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)


def create_vectorstore(file):

    with open(file.name, 'wb') as _file:
        _file.write(file.content)

    file_path = os.path.abspath(file.name)

    if file.type == "text/plain":
        text = file.content.decode("utf-8")
        texts = text_splitter.split_text(text)
        vectorstore = Chroma.from_texts(texts, embeddings)
        return vectorstore

    if file.type == "text/html":
        loader = UnstructuredHTMLLoader(file_path)

    if file.type == "application/pdf":
        loader = PyPDFLoader(file_path)

    if file.type == "text/csv":
        loader = CSVLoader(file_path)

    documents = loader.load()
    documents = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents, embeddings)

    if os.path.exists(file_path):
        os.remove(file_path)

    return vectorstore


@cl.langchain_factory
def main():
    cl.Message(content=welcome_message).send()

    cleaned_resp = None
    valid_responses = ["file", "url"]
    while cleaned_resp not in valid_responses:
        resp = cl.AskUserMessage(
            "What would you like to chat with, a File or a URL?"
        ).send()
        if 'content' in resp:
            cleaned_resp = resp['content'].strip().lower()

            if cleaned_resp == "url":
                cl.Message(
                    content="URLs are not supported yet. Please upload a file."
                ).send()
                cleaned_resp = "file"

    if cleaned_resp == "file":
        file = None
        while file is None:
            file = cl.AskFileMessage(
                content='Upload your file:', accept=supported_file_types, timeout=180
            ).send()

        vectorstore = create_vectorstore(file)

        chain = ConversationalRetrievalChain.from_llm(
            llm,
            vectorstore.as_retriever(),
            condense_question_llm=condense_question_llm,
            memory=memory,
        )

        cl.Message(
            content=f"`{file.name}` uploaded! How can I help you?"
        ).send()

        return chain

    # if cleaned_resp == "url":
    #     pass
