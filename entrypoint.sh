#!/bin/sh
set -e

echo "Starting the application..."

# Execute the main application
poetry run streamlit run acetube_streamlit/gui_app.py --server.port=80 --server.address=0.0.0.0
