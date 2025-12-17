"""
Script to help find the correct Azure deployment names
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

print("=" * 80)
print("AZURE DEPLOYMENT FINDER")
print("=" * 80)

azure_key = os.getenv("AZURE_OPENAI_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not azure_key or not azure_endpoint:
    print("ERROR: Environment variables not found!")
    exit(1)

print(f"\nEndpoint: {azure_endpoint}")
print(f"API Key: {azure_key[:20]}...")

# Try to list models/deployments
print("\n" + "=" * 80)
print("TESTING COMMON DEPLOYMENT NAMES")
print("=" * 80)

test_deployments = [
    "gpt-5-mini",
    "gpt-4o-mini", 
    "gpt-4o",
    "o4-mini",
    "grok-4-fast-reasoning",
    "grok-4",
    "claude-sonnet-4",
    "claude-sonnet-3-5",
    "claude-3-5-sonnet",
]

client = AzureOpenAI(
    api_key=azure_key,
    azure_endpoint=azure_endpoint,
    api_version="2024-05-01-preview"
)

for deployment in test_deployments:
    print(f"\nTesting: {deployment}")
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print(f"  ✓ SUCCESS - {deployment} works!")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "DeploymentNotFound" in error_msg:
            print(f"  ✗ NOT FOUND")
        elif "temperature" in error_msg.lower():
            print(f"  ✓ EXISTS (but has parameter restrictions)")
        else:
            print(f"  ? ERROR: {str(e)[:100]}")

print("\n" + "=" * 80)
print("To use a working deployment, update .env file:")
print("CLAUDE_DEPLOYMENT_NAME=<correct-name>")
print("=" * 80)
