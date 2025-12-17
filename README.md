# EV Report System - Multi-Agent Document Generator

## Issue Fixed
The application was stuck due to:
1. **Incorrect LLM configurations** - Claude API was configured incorrectly
2. **Missing error handling** - No feedback when LLMs failed to initialize
3. **Missing environment variables** - Claude endpoint was not configured

## Setup Instructions

### 1. Install Dependencies
```powershell
conda activate EV
pip install -r requirements.txt
```

### 2. Verify LLM Configuration
Run the test script to ensure all LLMs are properly configured:
```powershell
python test_llm_config.py
```

This will test:
- GPT-5 Mini
- Grok-4 Fast Reasoning
- Claude Sonnet 4.5
- Llama3.2 (local, optional)

### 3. Run the Application
```powershell
streamlit run main.py
```

## Environment Variables

Your `.env` file should contain:
```
AZURE_OPENAI_KEY=FbvhfQPxVUsrFhzJYB4889t1HyBGm82PGn5eGK6vlrNqpkQnj1xeJQQJ99BLACHYHv6XJ3w3AAAAACOGfIZc
AZURE_OPENAI_ENDPOINT=https://rbinbdo-vismai-mbr-resource.cognitiveservices.azure.com/
AZURE_ANTHROPIC_KEY=FbvhfQPxVUsrFhzJYB4889t1HyBGm82PGn5eGK6vlrNqpkQnj1xeJQQJ99BLACHYHv6XJ3w3AAAAACOGfIZc
AZURE_ANTHROPIC_ENDPOINT=https://rbinbdo-vismai-mbr-resource.services.ai.azure.com
```

## LLM Configuration Details

### GPT-5 Mini
- **Endpoint**: `https://rbinbdo-vismai-mbr-resource.cognitiveservices.azure.com/openai/deployments/gpt-5-mini/chat/completions`
- **API Version**: `2024-05-01-preview`
- **Role**: Primary writer

### Grok-4 Fast Reasoning
- **Endpoint**: `https://rbinbdo-vismai-mbr-resource.cognitiveservices.azure.com/openai/deployments/grok-4-fast-reasoning/chat/completions`
- **API Version**: `2024-05-01-preview`
- **Role**: Researcher

### Claude Sonnet 4.5
- **Endpoint**: `https://rbinbdo-vismai-mbr-resource.services.ai.azure.com/anthropic/v1/messages`
- **Role**: Reviewer/fact-checker

## Error Handling

All agents now include comprehensive error handling that will:
- Print detailed error messages to the terminal (stderr)
- Show stack traces for debugging
- Display user-friendly errors in the Streamlit UI
- Prevent silent failures

## Debugging

If the app gets stuck:
1. Check the PowerShell terminal for error messages
2. All errors are now printed to stderr with `[AGENT NAME ERROR]` prefix
3. Run `python test_llm_config.py` to verify LLM configurations
4. Check the Streamlit UI for error messages

## Changes Made

1. **Fixed `llm_factory.py`**:
   - Added comprehensive error handling with try-catch blocks
   - Added logging to stderr for all operations
   - Added proper Claude endpoint configuration
   - Added timeout and retry parameters
   - Added environment variable validation

2. **Fixed `agents.py`**:
   - Added error handling to all agent functions
   - Added detailed logging for each operation
   - Added try-catch blocks with stack traces
   - Added initialization error reporting

3. **Fixed `main.py`**:
   - Added error handling for file processing
   - Added error handling for workflow execution
   - Added error display in Streamlit UI
   - Added traceback display for debugging

4. **Updated `.env`**:
   - Added `AZURE_ANTHROPIC_ENDPOINT` variable
