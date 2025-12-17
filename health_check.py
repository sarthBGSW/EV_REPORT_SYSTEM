"""
Simple health check script to test if all imports work
Run this before main.py to diagnose startup issues
"""
import sys
print("=" * 50)
print("Starting health check...")
print("=" * 50)

try:
    print("✓ Python:", sys.version)
    
    print("\n[1/10] Testing streamlit...")
    import streamlit as st
    print("✓ Streamlit imported")
    
    print("\n[2/10] Testing dotenv...")
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv available")
    except ImportError:
        print("⚠ python-dotenv not available (OK for Streamlit Cloud)")
    
    print("\n[3/10] Testing langchain...")
    import langchain
    print("✓ LangChain imported")
    
    print("\n[4/10] Testing langchain-openai...")
    from langchain_openai import AzureChatOpenAI
    print("✓ AzureChatOpenAI imported")
    
    print("\n[5/10] Testing langgraph...")
    from langgraph.graph import StateGraph, END
    print("✓ LangGraph imported")
    
    print("\n[6/10] Testing duckduckgo...")
    from duckduckgo_search import DDGS
    print("✓ DuckDuckGo imported")
    
    print("\n[7/10] Testing python-docx...")
    from docx import Document
    print("✓ python-docx imported")
    
    print("\n[8/10] Testing pypdf...")
    from langchain_community.document_loaders import PyPDFLoader
    print("✓ PyPDFLoader imported")
    
    print("\n[9/10] Testing modules.state...")
    from modules.state import AgentState
    print("✓ modules.state imported")
    
    print("\n[10/10] Testing modules.agents...")
    from modules.agents import planner_agent
    print("✓ modules.agents imported")
    
    print("\n" + "=" * 50)
    print("✅ ALL CHECKS PASSED!")
    print("=" * 50)
    
except Exception as e:
    print("\n" + "=" * 50)
    print("❌ HEALTH CHECK FAILED!")
    print("=" * 50)
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
