#!/bin/bash

cd "$(dirname "$0")"

source venv/bin/activate

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app="file://$(pwd)/index.html" &

python3 app.py