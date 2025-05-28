from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import yaml

# Load configuration
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)



# Step 1: Initialize the embedding model
embedding = HuggingFaceEmbeddings(
    model_name=config["embedding"]["name"]
)


# Step 2: Load and prepare documents from text files
txt_folder = "./data"
txt_paths = [os.path.join(txt_folder, f) for f in os.listdir(txt_folder) if f.endswith(".txt")]
splitter = RecursiveCharacterTextSplitter()


# Step 3: Load documents, split, and add to vector store

all_docs = []

for filepath in txt_paths:
    loader = TextLoader(filepath)
    docs = loader.load()
    docs = splitter.split_documents(docs)

    all_docs.extend(docs)


# Step 4: Finalize FAISS store if needed
vectorstore = FAISS.from_documents(all_docs, embedding)
vectorstore.save_local("faiss_index")
print("✅ FAISS index saved locally.")

print("🎉 All documents have been added to the vector store.")
