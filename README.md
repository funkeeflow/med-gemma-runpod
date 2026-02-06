# MedGemma 27B RunPod Serverless Endpoint (vLLM)

A production-ready RunPod serverless endpoint for deploying Google's MedGemma 27B text model using the high-performance vLLM inference engine. This deployment provides OpenAI-compatible API with 2-10x better performance than standard transformers.

## Features

- **MedGemma 27B Text Model**: Deploy Google's state-of-the-art medical language model
- **vLLM Powered**: Blazing-fast inference with continuous batching and PagedAttention
- **OpenAI-Compatible API**: Drop-in replacement for OpenAI API - change only 3 lines of code
- **Serverless Architecture**: Auto-scaling endpoint with RunPod's serverless infrastructure
- **Production Ready**: Battle-tested infrastructure with built-in concurrency handling
- **High Performance**: 2-10x throughput improvement over standard transformers

## Prerequisites

1. **RunPod Account**: Sign up at [runpod.io](https://www.runpod.io)
2. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
3. **Hugging Face Access Token**: 
   - Go to [Hugging Face Settings > Access Tokens](https://huggingface.co/settings/tokens)
   - Create a new token with read permissions
   - Accept Google Health AI Developer Foundation terms for MedGemma models
4. **RunPod API Key**: Get from [RunPod API Keys](https://www.runpod.io/console/user-settings)

## Model Access

MedGemma models require accepting Google's Health AI Developer Foundation terms:
1. Visit the [MedGemma model page](https://huggingface.co/google/medgemma-27b-text-it)
2. Accept the terms of use
3. Ensure your Hugging Face token has access

## Quick Start

### Deploy via RunPod Console (Recommended)

1. **Go to RunPod Serverless Dashboard**: [console.runpod.io/serverless](https://www.runpod.io/console/serverless)
2. **Click "New Endpoint"**
3. **Select Docker Image**: `runpod/worker-v1-vllm:latest`
4. **Configure Environment Variables** (see `.env.example`):
   - `MODEL_NAME=google/medgemma-27b-text-it`
   - `HF_TOKEN=your_huggingface_token_here`
   - `MAX_MODEL_LEN=8192`
   - `GPU_MEMORY_UTILIZATION=0.95`
   - `MAX_CONCURRENCY=30`
5. **Select GPU**: A100 40GB or 80GB recommended
6. **Deploy**: RunPod will automatically start your endpoint

For detailed step-by-step instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Usage: OpenAI-Compatible API

The vLLM worker provides a fully OpenAI-compatible API. You can use it with any OpenAI-compatible client.

### Python Example

```python
from openai import OpenAI
import os

# Initialize OpenAI client with RunPod endpoint
client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

# Make a chat completion request
response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[
        {"role": "user", "content": "What are the symptoms of type 2 diabetes?"}
    ],
    max_tokens=512,
    temperature=0.7,
)

print(response.choices[0].message.content)
```

### cURL Example

```bash
curl https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "model": "google/medgemma-27b-text-it",
    "messages": [
      {"role": "user", "content": "Explain the mechanism of action of metformin."}
    ],
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

### Streaming Example

```python
response_stream = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[{"role": "user", "content": "What are diabetes symptoms?"}],
    stream=True,
)

for chunk in response_stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

For more API examples, see [API_EXAMPLES.md](API_EXAMPLES.md).

## Environment Variables

Configure your endpoint using these environment variables in the RunPod console:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MODEL_NAME` | Yes | - | Hugging Face model ID: `google/medgemma-27b-text-it` |
| `HF_TOKEN` | Yes | - | Your Hugging Face access token |
| `MAX_MODEL_LEN` | No | - | Maximum context length (e.g., `8192`) |
| `GPU_MEMORY_UTILIZATION` | No | `0.95` | GPU memory usage (0.0-1.0) |
| `MAX_CONCURRENCY` | No | `30` | Maximum concurrent requests |
| `QUANTIZATION` | No | - | Quantization method: `awq`, `gptq`, `squeezellm`, `bitsandbytes` |
| `TENSOR_PARALLEL_SIZE` | No | `1` | Number of GPUs for tensor parallelism |

See `.env.example` for a complete template with all available options.

## GPU Requirements

- **Recommended**: NVIDIA A100 (40GB or 80GB)
- **Minimum**: GPU with 48GB+ VRAM for full precision
- **Alternative**: Use quantization (`QUANTIZATION=awq` or `QUANTIZATION=gptq`) for lower memory GPUs

## Performance

- **Cold Start**: 30-60 seconds (model loading)
- **Warm Requests**: 2-5 seconds per request
- **Throughput**: 2-10x better than standard transformers
- **Concurrency**: Handles 30+ concurrent requests efficiently
- **Continuous Batching**: Automatically batches requests for optimal GPU utilization

## Local Testing

Test your deployed endpoint locally using the OpenAI client:

```bash
# Install dependencies
pip install -r requirements.txt

# Set your RunPod API key
export RUNPOD_API_KEY="your_runpod_api_key"

# Test with Python
python -c "
from openai import OpenAI
import os
client = OpenAI(
    api_key=os.environ.get('RUNPOD_API_KEY'),
    base_url='https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1'
)
response = client.chat.completions.create(
    model='google/medgemma-27b-text-it',
    messages=[{'role': 'user', 'content': 'What are diabetes symptoms?'}],
    max_tokens=100
)
print(response.choices[0].message.content)
"
```

## Troubleshooting

### Model Loading Errors

- **"HF_TOKEN not set"**: Ensure `HF_TOKEN` environment variable is set in RunPod endpoint settings
- **"Access denied"**: Verify you've accepted Google Health AI terms on Hugging Face
- **"Out of memory"**: 
  - Use a larger GPU (A100 80GB)
  - Enable quantization: `QUANTIZATION=awq`
  - Reduce `GPU_MEMORY_UTILIZATION` (e.g., `0.85`)

### API Errors

- **"Model not found"**: Check that `MODEL_NAME` matches exactly: `google/medgemma-27b-text-it`
- **"401 Unauthorized"**: Verify your RunPod API key is correct
- **"Timeout"**: Increase endpoint timeout in RunPod settings

### Performance Issues

- **Slow responses**: Check GPU utilization in RunPod dashboard
- **High latency**: Ensure endpoint is warm (not cold start)
- **Low throughput**: Increase `MAX_CONCURRENCY` if GPU has capacity

## Migration from Custom Handler

This repository was migrated from a custom transformers-based handler to vLLM for better performance and reliability. The old handler is preserved in `handler.py.old` for reference.

**Benefits of vLLM migration:**
- Eliminates thread safety issues
- 2-10x better performance
- OpenAI API compatibility
- Less code to maintain
- Production-ready infrastructure

## File Structure

```
med-gemma-runpod/
├── .env.example          # Environment variables template
├── Dockerfile            # Reference Dockerfile (uses pre-built image)
├── requirements.txt      # Dependencies for local testing
├── test_input.json       # OpenAI-format test input
├── handler.py.old        # Previous custom handler (archived)
├── DEPLOYMENT.md         # Detailed deployment guide
├── API_EXAMPLES.md       # API usage examples
├── CODE_REVIEW.md        # Code review documentation
├── .gitignore            # Git ignore patterns
├── .runpodignore         # RunPod ignore patterns
└── README.md             # This file
```

## Resources

- [RunPod vLLM Documentation](https://docs.runpod.io/serverless/vllm/get-started)
- [RunPod vLLM Worker Template](https://github.com/runpod-workers/worker-vllm)
- [vLLM Documentation](https://docs.vllm.ai/)
- [MedGemma Documentation](https://developers.google.com/health-ai-developer-foundations/medgemma)
- [Hugging Face MedGemma Models](https://huggingface.co/google/medgemma-27b-text-it)
- [RunPod Discord](https://discord.gg/cUpRmau42Vd)

## License

This project is provided as-is. MedGemma models are subject to Google's Health AI Developer Foundation terms of use.

## Support

For issues related to:
- **RunPod**: Check [RunPod Documentation](https://docs.runpod.io) or [Discord](https://discord.gg/cUpRmau42Vd)
- **MedGemma**: Refer to [Google Health AI Documentation](https://developers.google.com/health-ai-developer-foundations/medgemma)
- **vLLM**: See [vLLM Documentation](https://docs.vllm.ai/)
- **This Repository**: Open an issue on GitHub
