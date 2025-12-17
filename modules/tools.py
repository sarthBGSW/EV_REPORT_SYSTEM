import requests
import os
import sys
from bs4 import BeautifulSoup

try:
    import streamlit as st
except ImportError:
    st = None

# Initialize search tool with error handling
search_tool = None
try:
    from duckduckgo_search import DDGS
    search_tool = DDGS()
    print("[TOOLS] DuckDuckGo search initialized successfully", file=sys.stderr)
except ImportError as e:
    print(f"[TOOLS WARNING] Could not initialize DuckDuckGo search: {e}", file=sys.stderr)
    print(f"[TOOLS WARNING] Web search functionality will be limited", file=sys.stderr)

# Import PDF loader separately
try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    print(f"[TOOLS WARNING] Could not import PyPDFLoader", file=sys.stderr)
    PyPDFLoader = None

def web_search_tool(query: str):
    """
    Performs a web search to get latest 2025 data.
    """
    try:
        if search_tool is None:
            print(f"[TOOLS] Search tool not available, returning empty results", file=sys.stderr)
            return "Web search is currently unavailable. Please ensure 'duckduckgo-search' package is installed."
        
        # Force '2025' into query to ensure freshness
        enhanced_query = f"{query} data December 2025"
        
        # Use DDGS directly
        results = search_tool.text(enhanced_query, max_results=5)
        
        # Format results
        formatted_results = []
        for r in results:
            formatted_results.append(f"{r.get('title', '')}\n{r.get('body', '')}\n{r.get('href', '')}\n")
        
        return "\n".join(formatted_results) if formatted_results else "No results found"
        
    except Exception as e:
        print(f"[TOOLS ERROR] web_search_tool failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return f"Search error: {str(e)}"

def scrape_url(url: str):
    """
    Simple scraper for specific news sites found in search.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text from paragraphs
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return "\n".join(paragraphs[:10]) # Return first 10 paragraphs to save context
    except Exception as e:
        return f"Error scraping: {e}"

def process_uploaded_files(uploaded_files):
    """
    Reads PDFs uploaded via Streamlit.
    """
    try:
        text_content = ""
        if not uploaded_files:
            return text_content
        
        if PyPDFLoader is None:
            print("[TOOLS ERROR] PyPDFLoader not available", file=sys.stderr)
            return "PDF loading not available"
            
        for file in uploaded_files:
            try:
                if file.type == "application/pdf":
                    # Save temp to read
                    temp_path = f"temp_{file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    loader = PyPDFLoader(temp_path)
                    pages = loader.load()
                    for page in pages:
                        text_content += page.page_content + "\n"
                    
                    # Clean up temp file
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                        
            except Exception as e:
                print(f"[TOOLS] Error processing file {file.name}: {e}", file=sys.stderr)
                
        return text_content
        
    except Exception as e:
        print(f"[TOOLS ERROR] process_uploaded_files failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return ""