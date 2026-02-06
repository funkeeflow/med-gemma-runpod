# MedGemma 27B RunPod Serverless Endpoint

A production-ready RunPod serverless endpoint for deploying Google's MedGemma 27B text model for medical AI inference.

## Features

- **MedGemma 27B Text Model**: Deploy Google's state-of-the-art medical language model
- **Serverless Architecture**: Auto-scaling endpoint with RunPod's serverless infrastructure
- **Optimized Inference**: Uses bfloat16 precision and automatic device mapping for efficient GPU utilization
- **Easy Deployment**: Simple GitHub integration or manual Docker deployment
- **Local Testing**: Test your handler locally before deployment

## Prerequisites

1. **RunPod Account**: Sign up at [runpod.io](https://www.runpod.io)
2. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
3. **Hugging Face Access Token**: 
   - Go to [Hugging Face Settings > Access Tokens](https://huggingface.co/settings/tokens)
   - Create a new token with read permissions
   - Accept Google Health AI Developer Foundation terms for MedGemma models
4. **GitHub Account** (for GitHub integration deployment)

## Model Access

MedGemma models require accepting Google's Health AI Developer Foundation terms:
1. Visit the [MedGemma model page](https://huggingface.co/google/medgemma-27b-text-it)
2. Accept the terms of use
3. Ensure your Hugging Face token has access

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/med-gemma-runpod.git
cd med-gemma-runpod
```

### 2. Local Testing

Before deploying, test your handler locally:

```bash
# Create a virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your Hugging Face token
export HF_TOKEN="your_huggingface_token_here"

# Test the handler
python handler.py
```

The handler will process `test_input.json` and output the result.

## Deployment

### Option 1: GitHub Integration (Recommended)

1. **Push to GitHub**: Ensure your code is pushed to a GitHub repository
2. **Connect to RunPod**:
   - Go to [RunPod Serverless Dashboard](https://www.runpod.io/console/serverless)
   - Click "New Endpoint"
   - Select "GitHub Integration"
   - Authorize RunPod to access your GitHub account
   - Select this repository and branch
3. **Configure Environment Variables**:
   - Add `HF_TOKEN` with your Hugging Face access token
4. **Deploy**: RunPod will automatically build and deploy your endpoint

### Option 2: Manual Docker Build & Push

1. **Build Docker Image**:
```bash
docker build -t medgemma-runpod:latest .
```

2. **Tag for Container Registry**:
```bash
docker tag medgemma-runpod:latest YOUR_REGISTRY/medgemma-runpod:latest
```

3. **Push to Registry**:
```bash
docker push YOUR_REGISTRY/medgemma-runpod:latest
```

4. **Create Endpoint in RunPod**:
   - Go to RunPod Serverless Dashboard
   - Create new endpoint
   - Point to your container image
   - Set `HF_TOKEN` environment variable

## API Usage

### Input Format

```json
{
  "input": {
    "prompt": "What are the symptoms of diabetes?",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

### Parameters

- `prompt` (required): The medical question or text to process
- `max_tokens` (optional): Maximum number of tokens to generate (default: 512)
- `temperature` (optional): Sampling temperature (default: 0.7)
- `top_p` (optional): Nucleus sampling parameter (default: 0.9)

### Output Format

```json
{
  "output": "Type 2 diabetes symptoms include increased thirst, frequent urination, fatigue, blurred vision, and slow-healing sores...",
  "status": "success"
}
```

### Error Response

```json
{
  "error": "Error message here",
  "status": "error"
}
```

### Example cURL Request

```bash
curl -X POST \
  https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
  -d '{
    "input": {
      "prompt": "Explain the mechanism of action of metformin.",
      "max_tokens": 256,
      "temperature": 0.7
    }
  }'
```

## GPU Requirements

- **Recommended**: NVIDIA A100 (40GB or 80GB)
- **Minimum**: GPU with 48GB+ VRAM for full precision
- **Alternative**: Use quantization (8-bit/4-bit) for lower memory GPUs

## Performance Considerations

- **Cold Start**: First request may take 30-60 seconds to load the model
- **Warm Requests**: Subsequent requests are much faster (~2-5 seconds)
- **Model Size**: 27B parameters require significant GPU memory
- **Concurrent Requests**: RunPod automatically scales based on demand

## Troubleshooting

### Model Loading Errors

- **"HF_TOKEN not set"**: Ensure `HF_TOKEN` environment variable is set in RunPod endpoint settings
- **"Access denied"**: Verify you've accepted Google Health AI terms on Hugging Face
- **"Out of memory"**: Consider using a larger GPU or implementing quantization

### Deployment Issues

- **Build failures**: Check Dockerfile syntax and dependency versions
- **Runtime errors**: Review RunPod logs in the dashboard
- **Timeout errors**: Increase endpoint timeout settings for large models

## File Structure

```
med-gemma-runpod/
├── handler.py          # Main serverless handler
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── test_input.json    # Local testing input
├── .gitignore         # Git ignore patterns
├── .runpodignore      # RunPod ignore patterns
└── README.md          # This file
```

## License

This project is provided as-is. MedGemma models are subject to Google's Health AI Developer Foundation terms of use.

## Resources

- [RunPod Documentation](https://docs.runpod.io/serverless/get-started)
- [MedGemma Documentation](https://developers.google.com/health-ai-developer-foundations/medgemma)
- [Hugging Face MedGemma Models](https://huggingface.co/google/medgemma-27b-text-it)
- [RunPod Python SDK](https://github.com/runpod/runpod-python)

## Support

For issues related to:
- **RunPod**: Check [RunPod Discord](https://discord.gg/cUpRmau42Vd) or [Documentation](https://docs.runpod.io)
- **MedGemma**: Refer to [Google Health AI Documentation](https://developers.google.com/health-ai-developer-foundations/medgemma)
- **This Repository**: Open an issue on GitHub
