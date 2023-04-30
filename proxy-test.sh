#!/bin/bash
curl $PROXY_API_URL \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Say this is a test!"}],
        "temperature": 0.7
      }'
