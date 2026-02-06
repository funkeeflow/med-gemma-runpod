# Deployment Guide: MedGemma 27B on RunPod vLLM

Step-by-step guide for deploying MedGemma 27B using RunPod's vLLM worker template.

## Prerequisites

Before starting, ensure you have:
1. RunPod account ([sign up](https://www.runpod.io))
2. Hugging Face account with access to MedGemma models
3. Hugging Face access token ([create token](https://huggingface.co/settings/tokens))
4. Accepted Google Health AI Developer Foundation terms for MedGemma

## Step 1: Access RunPod Serverless Console

1. Go to [RunPod Serverless Dashboard](https://www.runpod.io/console/serverless)
2. Log in to your RunPod account
3. Click **"New Endpoint"** button

## Step 2: Configure Docker Image

1. In the **"Docker Image"** field, enter:
   ```
   runpod/worker-v1-vllm:latest
   ```
2. Or select from the dropdown if available
3. **Note**: This is RunPod's pre-built vLLM worker image - no custom Docker build needed

## Step 3: Configure Environment Variables

Click **"Environment Variables"** and add the following:

### Required Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `MODEL_NAME` | `google/medgemma-27b-text-it` | MedGemma model identifier |
| `HF_TOKEN` | `your_huggingface_token` | Your Hugging Face access token |

### Recommended Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `MAX_MODEL_LEN` | `8192` | Maximum context length |
| `GPU_MEMORY_UTILIZATION` | `0.95` | GPU memory usage (0.0-1.0) |
| `MAX_CONCURRENCY` | `30` | Maximum concurrent requests |

### Optional Variables (for optimization)

| Variable | Value | Description |
|----------|-------|-------------|
| `QUANTIZATION` | `awq` or `gptq` | For lower memory GPUs |
| `TENSOR_PARALLEL_SIZE` | `1` | Number of GPUs (for multi-GPU) |
| `OPENAI_SERVED_MODEL_NAME_OVERRIDE` | `medgemma-27b` | Custom model name in API |

**Example Configuration:**
```
MODEL_NAME=google/medgemma-27b-text-it
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
MAX_MODEL_LEN=8192
GPU_MEMORY_UTILIZATION=0.95
MAX_CONCURRENCY=30
```

## Step 4: Select GPU

1. Choose **GPU Type**:
   - **Recommended**: NVIDIA A100 (40GB or 80GB)
   - **Minimum**: GPU with 48GB+ VRAM
   - **Budget Option**: Use quantization with smaller GPU

2. Select **GPU Count**: Usually 1 GPU is sufficient

## Step 5: Configure Advanced Settings

### Container Disk
- **Default**: Usually sufficient (model downloads on first run)
- **Optional**: Increase if you want to cache the model

### Network Volume (Optional)
- Useful for caching models across deployments
- Set to persistent storage location

### Timeout Settings
- **Idle Timeout**: 5-10 minutes (keeps endpoint warm)
- **Request Timeout**: 300 seconds (5 minutes) for large requests

## Step 6: Deploy Endpoint

1. Review all settings
2. Click **"Deploy"** or **"Create Endpoint"**
3. Wait for deployment (usually 2-5 minutes)
4. Endpoint will show status: **"Running"** when ready

## Step 7: Get Endpoint Information

After deployment, note:
- **Endpoint ID**: Found in the endpoint URL or dashboard
- **Endpoint URL**: `https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1`
- **API Key**: Your RunPod API key (from [API Keys](https://www.runpod.io/console/user-settings))

## Step 8: Test Deployment

### Quick Test with cURL

```bash
curl https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "model": "google/medgemma-27b-text-it",
    "messages": [
      {"role": "user", "content": "What are diabetes symptoms?"}
    ],
    "max_tokens": 100
  }'
```

### Test with Python

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[{"role": "user", "content": "What are diabetes symptoms?"}],
    max_tokens=100,
)

print(response.choices[0].message.content)
```

## Step 9: Verify Model Loading

1. Check **Logs** in RunPod dashboard
2. Look for: `"Model loaded successfully"` or similar
3. First request may take 30-60 seconds (cold start)
4. Subsequent requests should be faster (2-5 seconds)

## Troubleshooting Deployment

### Endpoint Won't Start

- **Check Logs**: Look for error messages in RunPod dashboard
- **Verify HF_TOKEN**: Ensure token is correct and has access
- **Check GPU**: Ensure selected GPU has enough memory
- **Model Access**: Verify you've accepted Google Health AI terms

### Model Loading Fails

- **Error**: "Access denied" or "401"
  - **Solution**: Verify HF_TOKEN is correct and has read access
  - **Solution**: Ensure you've accepted model terms on Hugging Face

- **Error**: "Out of memory"
  - **Solution**: Use larger GPU (A100 80GB)
  - **Solution**: Enable quantization: `QUANTIZATION=awq`
  - **Solution**: Reduce `GPU_MEMORY_UTILIZATION` to `0.85`

### API Errors

- **Error**: "Model not found"
  - **Solution**: Verify `MODEL_NAME` is exactly `google/medgemma-27b-text-it`
  - **Solution**: Check model name in API request matches

- **Error**: "401 Unauthorized"
  - **Solution**: Verify RunPod API key is correct
  - **Solution**: Check API key has proper permissions

## Updating Configuration

To update environment variables after deployment:

1. Go to endpoint settings
2. Click **"Edit"** or **"Configure"**
3. Update environment variables
4. Click **"Save"** - endpoint will restart with new config

## Monitoring

Monitor your endpoint in RunPod dashboard:
- **Request Count**: Number of requests processed
- **Average Latency**: Response time metrics
- **GPU Utilization**: GPU usage statistics
- **Error Rate**: Failed requests percentage
- **Cost**: Usage and billing information

## Cost Optimization

1. **Idle Timeout**: Set appropriate timeout to avoid unnecessary costs
2. **GPU Selection**: Choose right-sized GPU for your workload
3. **Quantization**: Use quantization for lower memory requirements
4. **Monitoring**: Track usage to optimize costs

## Next Steps

- See [API_EXAMPLES.md](API_EXAMPLES.md) for usage examples
- Check [README.md](README.md) for API documentation
- Join [RunPod Discord](https://discord.gg/cUpRmau42Vd) for support
