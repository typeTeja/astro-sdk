## v1.3.0

# Serve documentation
mkdocs serve

# Then visit: http://127.0.0.1:8000


# Build static site
mkdocs build

# Output in: site/

# Deploy to gh-pages branch
mkdocs gh-deploy


pip install -r requirements.txt


# Create a new virtual environment
python -m venv .venv

# Activate it
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate


# Install project in editable mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev,test]"
