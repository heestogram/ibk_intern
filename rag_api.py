
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

# 환경변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 문서 불러오기 및 벡터화
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
A: 나비얌은 나라사랑카드 포인트로 기부할 수 있는 플랫폼입니다.

Q: 기부 내역은 어떻게 확인하나요?
A: 마이페이지 > 기부 내역 메뉴에서 확인 가능합니다.

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
