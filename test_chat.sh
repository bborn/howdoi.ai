curl -X POST http://127.0.0.1:5001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, how are you?",
    "history": [],
    "model": "text-davinci-003",
    "temperature": 0.5,
    "max_tokens": 512
  }'
