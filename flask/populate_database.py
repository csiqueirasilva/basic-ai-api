import argparse
import os
import shutil
import sys
# Add a print to show the Python version
print(f"Running on Python version: {sys.version}")

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from constants import CHROMA_PATH, DATA_PATH
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("--dir", type=str, help="Path to the data directory.")
    args = parser.parse_args()

    if not args.dir:
        print("Need a directory with --dir")
        exit(-1)

    dir = args.dir

    if args.reset:
        print("✨ Clearing Database")
        clear_database(dir)

    # Create (or update) the data store.
    print("Loading documents...")
    documents = load_documents(dir)
    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")
    chunks = split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    print("Adding chunks to Chroma...")
    add_to_chroma(chunks, dir)

def load_documents(dir : str):
    print(f"In load_documents function reading {DATA_PATH}/{dir}...")
    document_loader = PyPDFDirectoryLoader(f"{DATA_PATH}/{dir}")
    return document_loader.load()

# If you're using Python version < 3.9, change the type hints as shown below
def split_documents(documents: "list[Document]"):  # Add quotes for forward reference
    print("In split_documents function...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: "list[Document]", dir: str):  # Add quotes for forward reference
    print("In add_to_chroma function...")
    # Load the existing database.
    db = Chroma(
        persist_directory=f"{CHROMA_PATH}/{dir}", embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database(dir : str):
    p = f"{CHROMA_PATH}/{dir}"
    if os.path.exists(p):
        shutil.rmtree(p)

if __name__ == "__main__":
    main()
