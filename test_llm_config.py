"""
Test script to verify LLM configurations are working correctly
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("TESTING LLM CONFIGURATIONS")
print("=" * 80)

# Check environment variables
print("\n1. Checking Environment Variables...")
azure_key = os.getenv("AZURE_OPENAI_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
claude_key = os.getenv("AZURE_ANTHROPIC_KEY")
claude_endpoint = os.getenv("AZURE_ANTHROPIC_ENDPOINT")

print(f"   AZURE_OPENAI_KEY: {'✓ Set' if azure_key else '✗ Missing'}")
print(f"   AZURE_OPENAI_ENDPOINT: {azure_endpoint if azure_endpoint else '✗ Missing'}")
print(f"   AZURE_ANTHROPIC_KEY: {'✓ Set' if claude_key else '✗ Missing'}")
print(f"   AZURE_ANTHROPIC_ENDPOINT: {claude_endpoint if claude_endpoint else '✗ Missing'}")

if not azure_key or not azure_endpoint:
    print("\n✗ ERROR: Missing required environment variables")
    sys.exit(1)

# Test each LLM
print("\n2. Testing LLM Initializations...")

try:
    from modules.llm_factory import get_llm
    print("   ✓ llm_factory module imported successfully")
except Exception as e:
    print(f"   ✗ Failed to import llm_factory: {e}")
    sys.exit(1)

# Test GPT-5 Mini
print("\n3. Testing GPT-5 Mini...")
try:
    llm_gpt = get_llm("gpt-5-mini")
    print("   ✓ GPT-5 Mini initialized")
    
    # Test a simple call
    from langchain_core.messages import HumanMessage
    response = llm_gpt.invoke([HumanMessage(content="Say 'Hello' in one word")])
    print(f"   ✓ GPT-5 Mini response: {response.content[:50]}")
except Exception as e:
    print(f"   ✗ GPT-5 Mini failed: {e}")
    import traceback
    traceback.print_exc()

# Test Grok-4
print("\n4. Testing Grok-4...")
try:
    llm_grok = get_llm("grok-4")
    print("   ✓ Grok-4 initialized")
    
    response = llm_grok.invoke([HumanMessage(content="Say 'Hello' in one word")])
    print(f"   ✓ Grok-4 response: {response.content[:50]}")
except Exception as e:
    print(f"   ✗ Grok-4 failed: {e}")
    import traceback
    traceback.print_exc()

# Test Claude
print("\n5. Testing Claude Sonnet 4.5...")
try:
    llm_claude = get_llm("claude-sonnet")
    print("   ✓ Claude Sonnet initialized")
    
    response = llm_claude.invoke([HumanMessage(content="Say 'Hello' in one word")])
    print(f"   ✓ Claude response: {response.content[:50]}")
except Exception as e:
    print(f"   ✗ Claude failed: {e}")
    import traceback
    traceback.print_exc()

# Test Local Ollama (optional)
print("\n6. Testing Local Ollama (llama3.2)...")
try:
    llm_local = get_llm("llama3.2")
    print("   ✓ Llama3.2 initialized")
    
    response = llm_local.invoke([HumanMessage(content="Say 'Hello' in one word")])
    print(f"   ✓ Llama3.2 response: {response.content[:50]}")
except Exception as e:
    print(f"   ⚠ Llama3.2 failed (this is optional): {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
