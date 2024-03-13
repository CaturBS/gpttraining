from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


def __init_index():
    os.environ["OPENAI_API_KEY"] = "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"
    pdf_file = os.path.join(os.getcwd(), "docs", "5discp.pdf")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    docs = PyPDFLoader(file_path=pdf_file).load_and_split(text_splitter=text_splitter)
    # docs = RecursiveUrlLoader(url='https://www.kpu.go.id/',max_depth=2,prevent_outside=True).load()
    # ConversationBufferWindowMemory(k=1)
    embeddings = OpenAIEmbeddings()
    # spllited_documents = text_splitter.split_documents(docs)
    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=os.path.join(os.getcwd(), "chroma_db")
    )


if __name__ == '__main__':
    __init_index()

