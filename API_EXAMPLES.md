# API Examples: MedGemma 27B vLLM Endpoint

Complete examples for using the MedGemma 27B endpoint with OpenAI-compatible API.

## Setup

Replace these placeholders in all examples:
- `YOUR_ENDPOINT_ID`: Your RunPod endpoint ID
- `YOUR_RUNPOD_API_KEY`: Your RunPod API key
- `google/medgemma-27b-text-it`: Model name (or override if configured)

## Python Examples

### Basic Chat Completion

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

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

### Streaming Response

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

stream = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[
        {"role": "user", "content": "Explain the mechanism of action of metformin."}
    ],
    max_tokens=512,
    temperature=0.7,
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # New line after stream
```

### Multi-Turn Conversation

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

messages = [
    {"role": "system", "content": "You are a helpful medical AI assistant."},
    {"role": "user", "content": "What is diabetes?"},
]

# First turn
response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=messages,
    max_tokens=256,
)

assistant_message = response.choices[0].message.content
print(f"Assistant: {assistant_message}")

# Add assistant response and continue conversation
messages.append({"role": "assistant", "content": assistant_message})
messages.append({"role": "user", "content": "What are the treatment options?"})

# Second turn
response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=messages,
    max_tokens=256,
)

print(f"Assistant: {response.choices[0].message.content}")
```

### Advanced Parameters

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[
        {"role": "user", "content": "List common cardiovascular diseases."}
    ],
    max_tokens=512,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.5,  # Encourage diverse vocabulary
    presence_penalty=0.3,    # Encourage new topics
    stop=["\n\n"],           # Stop at double newline
)

print(response.choices[0].message.content)
```

### Error Handling

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
)

try:
    response = client.chat.completions.create(
        model="google/medgemma-27b-text-it",
        messages=[
            {"role": "user", "content": "What are diabetes symptoms?"}
        ],
        max_tokens=100,
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

## cURL Examples

### Basic Request

```bash
curl https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "model": "google/medgemma-27b-text-it",
    "messages": [
      {"role": "user", "content": "What are diabetes symptoms?"}
    ],
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

### Streaming Request

```bash
curl https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "model": "google/medgemma-27b-text-it",
    "messages": [
      {"role": "user", "content": "Explain hypertension."}
    ],
    "max_tokens": 512,
    "temperature": 0.7,
    "stream": true
  }'
```

### With Stop Sequences

```bash
curl https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "model": "google/medgemma-27b-text-it",
    "messages": [
      {"role": "user", "content": "List 5 common medications."}
    ],
    "max_tokens": 300,
    "temperature": 0.7,
    "stop": ["\n\n", "6."]
  }'
```

## JavaScript/Node.js Examples

### Basic Request

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.RUNPOD_API_KEY,
  baseURL: 'https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1',
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'google/medgemma-27b-text-it',
    messages: [
      { role: 'user', content: 'What are diabetes symptoms?' }
    ],
    max_tokens: 256,
    temperature: 0.7,
  });

  console.log(response.choices[0].message.content);
}

main();
```

### Streaming Request

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.RUNPOD_API_KEY,
  baseURL: 'https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1',
});

async function main() {
  const stream = await client.chat.completions.create({
    model: 'google/medgemma-27b-text-it',
    messages: [
      { role: 'user', content: 'Explain hypertension.' }
    ],
    max_tokens: 512,
    stream: true,
  });

  for await (const chunk of stream) {
    if (chunk.choices[0].delta.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
  console.log(); // New line
}

main();
```

## Request Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model identifier: `google/medgemma-27b-text-it` |
| `messages` | array | Array of message objects with `role` and `content` |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_tokens` | integer | varies | Maximum tokens to generate |
| `temperature` | float | 0.7 | Sampling temperature (0.0-2.0) |
| `top_p` | float | 1.0 | Nucleus sampling (0.0-1.0) |
| `top_k` | integer | -1 | Top-k sampling (-1 for all) |
| `frequency_penalty` | float | 0.0 | Frequency penalty (-2.0 to 2.0) |
| `presence_penalty` | float | 0.0 | Presence penalty (-2.0 to 2.0) |
| `stop` | array | null | Stop sequences |
| `stream` | boolean | false | Enable streaming |
| `n` | integer | 1 | Number of completions |
| `seed` | integer | null | Random seed |

## Response Format

### Non-Streaming Response

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "google/medgemma-27b-text-it",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Type 2 diabetes symptoms include..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

### Streaming Response Chunk

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion.chunk",
  "created": 1234567890,
  "model": "google/medgemma-27b-text-it",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": "Type 2"
      },
      "finish_reason": null
    }
  ]
}
```

## Medical Use Cases

### Symptom Analysis

```python
response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[
        {"role": "user", "content": "A patient presents with increased thirst, frequent urination, and fatigue. What condition should be considered?"}
    ],
    max_tokens=300,
    temperature=0.5,  # Lower temperature for more factual responses
)
```

### Drug Mechanism Explanation

```python
response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[
        {"role": "user", "content": "Explain how metformin works to treat type 2 diabetes."}
    ],
    max_tokens=400,
    temperature=0.7,
)
```

### Treatment Options

```python
response = client.chat.completions.create(
    model="google/medgemma-27b-text-it",
    messages=[
        {"role": "system", "content": "You are a medical AI assistant providing evidence-based information."},
        {"role": "user", "content": "What are the first-line treatment options for hypertension?"}
    ],
    max_tokens=500,
    temperature=0.6,
)
```

## Best Practices

1. **Use System Messages**: Provide context about the assistant's role
2. **Set Appropriate Temperature**: Lower (0.3-0.5) for factual, higher (0.7-0.9) for creative
3. **Set Max Tokens**: Prevent excessively long responses
4. **Handle Errors**: Always wrap API calls in try-catch blocks
5. **Use Streaming**: For better UX with long responses
6. **Monitor Usage**: Track token usage to manage costs

## Rate Limits

RunPod endpoints handle concurrent requests efficiently. The `MAX_CONCURRENCY` environment variable controls the limit (default: 30).

For high-volume applications:
- Monitor endpoint metrics in RunPod dashboard
- Adjust `MAX_CONCURRENCY` based on GPU capacity
- Consider multiple endpoints for load distribution

## Troubleshooting

### Common Errors

- **401 Unauthorized**: Check API key
- **404 Not Found**: Verify endpoint ID
- **Model Not Found**: Check model name matches exactly
- **Timeout**: Increase request timeout or reduce max_tokens

See [DEPLOYMENT.md](DEPLOYMENT.md) for more troubleshooting tips.
