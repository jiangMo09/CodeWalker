#!/bin/bash

# Clone the repository
git clone $1 .

# If index.html exists, start the Python HTTP server
if [ -f "index.html" ]; then
    python -m http.server 8000
else
    echo "index.html not found. Please check the repository content."
    exit 1
fi