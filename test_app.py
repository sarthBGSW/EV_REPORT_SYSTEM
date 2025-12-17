"""
Minimal Streamlit app to test if basic deployment works
This helps isolate if the issue is with imports or configuration
"""
import streamlit as st

st.set_page_config(page_title="Test App", layout="wide")

st.title("🧪 Deployment Test")
st.success("✅ App is running!")

st.write("Python version:", st.__version__)
st.write("If you see this, basic Streamlit deployment is working.")

# Test imports one by one
status = {}

try:
    import langchain
    status["langchain"] = "✅"
except Exception as e:
    status["langchain"] = f"❌ {str(e)}"

try:
    from langchain_openai import AzureChatOpenAI
    status["langchain-openai"] = "✅"
except Exception as e:
    status["langchain-openai"] = f"❌ {str(e)}"

try:
    from langgraph.graph import StateGraph
    status["langgraph"] = "✅"
except Exception as e:
    status["langgraph"] = f"❌ {str(e)}"

try:
    from duckduckgo_search import DDGS
    status["duckduckgo-search"] = "✅"
except Exception as e:
    status["duckduckgo-search"] = f"❌ {str(e)}"

try:
    from docx import Document
    status["python-docx"] = "✅"
except Exception as e:
    status["python-docx"] = f"❌ {str(e)}"

st.subheader("Import Status:")
for package, result in status.items():
    st.write(f"{package}: {result}")

# Test if secrets are configured
st.subheader("Secrets Check:")
if hasattr(st, 'secrets') and len(st.secrets) > 0:
    st.write("✅ Secrets are configured")
    st.write(f"Number of secrets: {len(st.secrets)}")
else:
    st.warning("⚠️ No secrets configured")
