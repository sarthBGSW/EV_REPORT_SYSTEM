# Quick Fix: Find Your Azure Deployment Names

If models are still failing, you need to verify the exact deployment names in Azure.

## How to Find Deployment Names

### Option 1: Azure AI Foundry Portal
1. Go to https://ai.azure.com/
2. Navigate to your resource: `rbinbdo-vismai-mbr-resource`
3. Go to **Deployments** section
4. Look for your model deployments and copy the exact names

### Option 2: Azure CLI
```powershell
az cognitiveservices account deployment list `
  --name rbinbdo-vismai-mbr-resource `
  --resource-group <your-resource-group>
```

### Option 3: Azure Portal
1. Go to https://portal.azure.com/
2. Search for "rbinbdo-vismai-mbr-resource"
3. Go to **Model deployments**
4. Note the deployment names

## Common Deployment Name Patterns

### Claude
Possible names:
- `claude-sonnet-4`
- `claude-3-5-sonnet`
- `claude-sonnet-3-5`
- `claude-sonnet-35`
- `claude-3-5-sonnet-20241022`

### GPT-5 Mini
Possible names:
- `gpt-5-mini`
- `gpt-5-mini-preview`
- `o4-mini`

### Grok
Possible names:
- `grok-4-fast-reasoning`
- `grok-4`
- `grok-fast`

## Update Configuration

Once you find the correct names, update `modules/llm_factory.py`:

### For GPT-5 Mini (line ~32):
```python
azure_deployment="YOUR_ACTUAL_DEPLOYMENT_NAME",
```

### For Grok-4 (line ~45):
```python
azure_deployment="YOUR_ACTUAL_DEPLOYMENT_NAME",
```

### For Claude (line ~61):
```python
azure_deployment="YOUR_ACTUAL_DEPLOYMENT_NAME",
```

## Test After Update

```powershell
conda activate EV
python test_llm_config.py
```

Look for "✓" marks next to each model test.
