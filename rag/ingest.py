import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Define paths strictly based on the project architecture
DOCUMENTS_PATH = "./rag/documents"
EMBEDDINGS_PATH = "./rag/embeddings"

def ingest_documents():
    # 1. Load documents from the rag/documents/ folder
    print(f"Loading documents from {DOCUMENTS_PATH}...")
    loader = DirectoryLoader(DOCUMENTS_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No documents found. Please add some .txt files to rag/documents/")
        return

    # 2. Split text into manageable chunks
    print("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    # 3. Generate embeddings using a lightweight local model
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Store the vectors in the local Chroma database at rag/embeddings/
    print(f"Storing vectors in {EMBEDDINGS_PATH}...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=EMBEDDINGS_PATH
    )
    vector_db.persist()
    print("Ingestion complete! Educational data is now ready for retrieval.")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(DOCUMENTS_PATH, exist_ok=True)
    os.makedirs(EMBEDDINGS_PATH, exist_ok=True)
    ingest_documents()