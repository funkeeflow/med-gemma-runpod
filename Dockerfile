# RunPod vLLM Worker - MedGemma 27B Deployment
# 
# This Dockerfile is for reference/documentation purposes.
# For production deployment, use the pre-built RunPod vLLM worker image
# via RunPod Console: runpod/worker-v1-vllm
#
# To deploy:
# 1. Go to RunPod Serverless Console
# 2. Create new endpoint
# 3. Select "runpod/worker-v1-vllm" image
# 4. Configure environment variables (see .env.example)
#
# For local testing with this Dockerfile:
# docker build -t medgemma-vllm .
# docker run -e MODEL_NAME=google/medgemma-27b-text-it -e HF_TOKEN=your_token medgemma-vllm

FROM runpod/worker-v1-vllm:latest

# The vLLM worker image handles everything
# Just configure via environment variables at runtime

# No additional setup needed - vLLM worker is production-ready
