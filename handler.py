"""RunPod serverless handler for Google MedGemma 27B model."""
import os
import runpod
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Global model and tokenizer variables
model = None
tokenizer = None

def initialize_model():
    """Load the MedGemma 27B model and tokenizer."""
    global model, tokenizer
    
    if model is not None and tokenizer is not None:
        return
    
    model_id = "google/medgemma-27b-text-it"
    
    # Check for Hugging Face token
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "HF_TOKEN environment variable not set. "
            "Please set your Hugging Face token to access MedGemma models."
        )
    
    print(f"Loading model: {model_id}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=hf_token,
        trust_remote_code=True
    )
    
    # Load model with optimizations
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=hf_token,
        torch_dtype=torch.bfloat16,  # Use bfloat16 for memory efficiency
        device_map="auto",  # Automatically handle device placement
        trust_remote_code=True
    )
    
    print("Model loaded successfully")

def handler(job):
    """
    Process a job request for medical text generation.
    
    Expected input:
    {
        "prompt": "Medical question or text",
        "max_tokens": 512 (optional),
        "temperature": 0.7 (optional),
        "top_p": 0.9 (optional)
    }
    """
    try:
        # Initialize model if not already loaded
        if model is None or tokenizer is None:
            initialize_model()
        
        # Extract input parameters
        job_input = job.get("input", {})
        prompt = job_input.get("prompt")
        
        if not prompt:
            return {
                "error": "Missing required parameter: 'prompt'",
                "status": "error"
            }
        
        # Generation parameters
        max_tokens = job_input.get("max_tokens", 512)
        temperature = job_input.get("temperature", 0.7)
        top_p = job_input.get("top_p", 0.9)
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the input prompt from the output
        response = generated_text[len(prompt):].strip()
        
        return {
            "output": response,
            "status": "success"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

# Initialize model at startup
print("Initializing MedGemma 27B model...")
try:
    initialize_model()
except Exception as e:
    print(f"Warning: Could not initialize model at startup: {e}")
    print("Model will be initialized on first request")

# Start the serverless worker
runpod.serverless.start({"handler": handler})
