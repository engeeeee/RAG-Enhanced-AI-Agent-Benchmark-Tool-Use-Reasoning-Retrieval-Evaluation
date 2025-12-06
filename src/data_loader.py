import os
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def download_bitcoin_pdf():
    url = "https://bitcoin.org/bitcoin.pdf"
    output_path = os.path.join(DATA_DIR, "bitcoin.pdf")
    if os.path.exists(output_path):
        print(f"Bitcoin PDF already exists at {output_path}")
        return

    print(f"Downloading Bitcoin PDF from {url}...")
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("Download complete.")

def download_ethereum_whitepaper():
    url = "https://ethereum.org/en/whitepaper/"
    output_path = os.path.join(DATA_DIR, "ethereum.md")
    
    if os.path.exists(output_path):
        print(f"Ethereum Whitepaper already exists at {output_path}")
        return

    print(f"Downloading Ethereum Whitepaper from {url}...")
    # Use WebBaseLoader to get content
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    # Save as markdown (simplistic conversion)
    content = docs[0].page_content
    
    # Clean up a bit (optional, but good for RAG)
    # For now, just save raw text
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Download complete.")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    download_bitcoin_pdf()
    download_ethereum_whitepaper()
