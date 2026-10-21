from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from services.llm_service import call_llm

KNOWLEDGE_FILE = Path("knowledge/product_faq.txt")

COLLECTION_NAME = "product_faq"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

chromadb_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chromadb_client.get_or_create_collection(
    name = COLLECTION_NAME
)

def load_document()->str:
    return KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )

def split_text(
    text:str,
    chunk_size: int = 120,
    overlap: int = 20
)->list[str]:

  chunks =[]

  start = 0

  while start < len(text):
      end = start + chunk_size

      chunk = text[start:end].strip()

      if chunk:
          chunks.append(chunk)

      start += chunk_size -overlap
  return chunks

def create_embeddings(
    text:list[str]
)->list[list[float]]:
    embeddings = embedding_model.encode(
        text,
        normalize_embeddings=True
    )
    return embeddings.tolist()

def bulid_knowledge_base():
    text = load_document()
    chunks = split_text(text)
    embeddings = create_embeddings(chunks)

    ids =[
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print(
        f"Knowledge base built successfully. "
        f"Chunks: {len(chunks)}"
    )

def search_knowledge(
    question:str,
    top_k:int = 3
)->list[str]:

   question_embedding = create_embeddings(
       [question]
   )[0]

   result = collection.query(
       query_embeddings=[
           question_embedding
       ],
   )
   documents = result.get("documents")

   if not documents:
       return[]
   return documents[0]

async def answer_product_question(
    question:str
)->str:

   documents = search_knowledge(
       question=question,
       top_k=3
   )
   if not documents:
       return"知识库中没有找到相关产品信息"
   context ="\n\n".join(documents)
   system_prompt = f"""
   你是一个产品客服助手。

   你只能根据下面提供的产品知识回答用户问题。

   如果知识中没有明确答案，就回答：
   知识库中没有足够信息回答这个问题。

   不要编造不存在的信息。

   产品知识：
   {context}
   """
   answer = await call_llm(
       system_prompt=system_prompt,
       user_message=question
   )

   return answer