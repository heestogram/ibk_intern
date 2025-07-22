
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


loader = TextLoader("gibu_qna.txt", encoding="utf-8")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings(openai_api_key=openai_api_key))
retriever = vectorstore.as_retriever()

# Few-shot prompt
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 나비얌 기부 서비스에 대해 설명하는 챗봇입니다.

예시:
Q: 나비얌 앱이란 무엇인가요?
A: 나비얌은 우리 동네 착한 가게들과 제휴를 맺어, 사회 각층의 결식 문제를 해결하기 위한 디지털 플랫폼입니다.

Q: 기부 내역은 어떻게 확인하나요?
A: 하단 탭 MY나비 > 기브 내역 메뉴에서 확인 가능합니다.

------------------
검색된 문서:
{context}
------------------

사용자 질문:
Q: {question}
A:
"""
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key),
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    result = qa_chain(query.question)
    return {"answer": result["result"]}
