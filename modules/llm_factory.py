import os
import sys
from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

try:
    from langchain_anthropic import ChatAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    print("[LLM FACTORY WARNING] langchain-anthropic not available", file=sys.stderr)
    ANTHROPIC_AVAILABLE = False

# Since Azure "Claude" and "Grok" might not have standard LangChain classes yet, 
# we treat them as OpenAI-compatible or use custom wrappers. 
# For this code, we assume they follow Azure OpenAI standards or we use generic requests if needed.
# Below is a simplified unifying factory.

def get_llm(model_type="gpt-5-mini"):
    """
    Factory to return the requested LLM object.
    """
    try:
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_key = os.getenv("AZURE_OPENAI_KEY")
        claude_endpoint = os.getenv("AZURE_ANTHROPIC_ENDPOINT", "https://rbinbdo-vismai-mbr-resource.services.ai.azure.com")
        claude_key = os.getenv("AZURE_ANTHROPIC_KEY", azure_key)
        
        # If using the new env format
        if not claude_endpoint or "anthropic/v1/messages" in claude_endpoint:
            claude_base = os.getenv("CLAUDE_SONNET_ENDPOINT", "https://rbinbdo-vismai-mbr-resource.services.ai.azure.com/anthropic/v1/messages")
            # Extract base URL without the path
            if "/anthropic/v1/messages" in claude_base:
                claude_endpoint = claude_base.replace("/anthropic/v1/messages", "")
            else:
                claude_endpoint = claude_base
        
        print(f"\n[LLM FACTORY] Initializing model: {model_type}", file=sys.stderr)
        
        # Validate environment variables
        if not azure_key:
            raise ValueError("AZURE_OPENAI_KEY not found in environment variables")
        if not azure_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT not found in environment variables")
        
        # 1. GPT-5 Mini (Azure)
        if model_type == "gpt-5-mini":
            print(f"[LLM FACTORY] Using endpoint: {azure_endpoint}", file=sys.stderr)
            return AzureChatOpenAI(
                azure_deployment="gpt-5-mini",
                api_version="2024-05-01-preview",
                azure_endpoint=azure_endpoint,
                api_key=azure_key,
                temperature=1.0,  # GPT-5 mini only supports temperature=1.0
                timeout=120,
                max_retries=2
            )

        # 2. Grok (Azure - Assuming OpenAI Compatible Endpoint)
        elif model_type == "grok-4":
            print(f"[LLM FACTORY] Using endpoint: {azure_endpoint}", file=sys.stderr)
            return AzureChatOpenAI(
                azure_deployment="grok-4-fast-reasoning",
                api_version="2024-05-01-preview",
                azure_endpoint=azure_endpoint,
                api_key=azure_key,
                temperature=1.0,
                timeout=120,
                max_retries=2
            )

        # 3. Claude Sonnet 4.5 (Azure Anthropic - Uses Anthropic API format, NOT OpenAI)
        elif model_type == "claude-sonnet":
            print(f"[LLM FACTORY] Using Claude base endpoint: {claude_endpoint}", file=sys.stderr)
            
            if not ANTHROPIC_AVAILABLE:
                print(f"[LLM FACTORY WARNING] Anthropic library not available, using GPT-5 Mini", file=sys.stderr)
                return AzureChatOpenAI(
                    azure_deployment="gpt-5-mini",
                    api_version="2024-05-01-preview",
                    azure_endpoint=azure_endpoint,
                    api_key=azure_key,
                    temperature=1.0,
                    timeout=120,
                    max_retries=2
                )
            
            try:
                # Claude uses Anthropic's native API
                # The base_url should be the base endpoint, ChatAnthropic will add the path
                return ChatAnthropic(
                    model="claude-sonnet-4-5",
                    api_key=claude_key,
                    base_url=f"{claude_endpoint}/anthropic/v1",
                    temperature=1.0,
                    timeout=120,
                    max_retries=1,
                    default_headers={"anthropic-version": "2023-06-01"}
                )
            except Exception as claude_error:
                print(f"[LLM FACTORY WARNING] Claude initialization failed: {claude_error}", file=sys.stderr)
                print(f"[LLM FACTORY] Falling back to GPT-5 Mini for review tasks", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                return AzureChatOpenAI(
                    azure_deployment="gpt-5-mini",
                    api_version="2024-05-01-preview",
                    azure_endpoint=azure_endpoint,
                    api_key=azure_key,
                    temperature=1.0,
                    timeout=120,
                    max_retries=2
                )

        # 4. Local Ollama Models (Best for summarization & cost saving)
        elif model_type == "deepseek-r1":
            print(f"[LLM FACTORY] Using local Ollama model: deepseek-r1:8b", file=sys.stderr)
            try:
                # Check if Ollama is available before initializing
                import requests
                requests.get("http://localhost:11434", timeout=2)
                return ChatOllama(model="deepseek-r1:8b", temperature=0.6)
            except Exception as ollama_err:
                print(f"[LLM FACTORY WARNING] Ollama not available: {ollama_err}", file=sys.stderr)
                raise ConnectionError("Ollama service not available")
        
        elif model_type == "llama3.2":
            print(f"[LLM FACTORY] Using local Ollama model: llama3.2", file=sys.stderr)
            try:
                # Check if Ollama is available before initializing
                import requests
                requests.get("http://localhost:11434", timeout=2)
                return ChatOllama(model="llama3.2:latest", temperature=0.5)
            except Exception as ollama_err:
                print(f"[LLM FACTORY WARNING] Ollama not available: {ollama_err}", file=sys.stderr)
                raise ConnectionError("Ollama service not available")

        else:
            # Fallback
            print(f"[LLM FACTORY] Unknown model type '{model_type}', falling back to GPT-5 Mini", file=sys.stderr)
            return AzureChatOpenAI(
                azure_deployment="gpt-5-mini",
                api_version="2024-05-01-preview",
                azure_endpoint=azure_endpoint,
                api_key=azure_key,
                temperature=1.0,
                timeout=120,
                max_retries=2
            )
            
    except Exception as e:
        print(f"\n[LLM FACTORY ERROR] Failed to initialize {model_type}: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise