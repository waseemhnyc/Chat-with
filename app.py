import os
from langchain import PromptTemplate, OpenAI, LLMChain
import chainlit as cl

template = """Question: {question}
Answer: Let's think step by step."""


@cl.langchain_factory
def factory():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(
        prompt=prompt, llm=OpenAI(temperature=0), verbose=True
    )

    return llm_chain


@cl.on_chat_start
def start():
    file = None

    while file == None:
        file = cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["text/plain"]
        ).send()

    text = file.content.decode("utf-8")

    cl.Message(
        content=f"`{file.name}` uploaded, it contains {len(text)} characters!"
    ).send()
