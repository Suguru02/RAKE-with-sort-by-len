# RAKE with filter by len 2-4

Extract top 5 key phrases with len 2-4 from text using RAKE (Rapid Automatic Keyword Extraction) with `rake_nltk`. Includes optional interpretable score breakdown (degree/frequency per word).

## Requirements

- Python 3.12+
- Dependencies are declared in `pyproject.toml`

## Setup

Install uv(if needed) and sync dependencies:

```
git clone https://github.com/Suguru02/RAKE-with-sort-by-len
cd RAKE-with-sort-by-len

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Create .venv and install project deps
uv sync
source .venv/bin/activate

```
On first run, the script will download required NLTK resources (stopwords, punkt).

## Usage

Run the script:

```
python src/Rake_with_sort.py -f data/sample.txt --top-k 10 --language english

```

Flags:
- `-f, --file` — read text from a UTF-8 file; otherwise a sample is used
- `--top-k` — The number of phrases among which we are looking for the top 5 lengths is 2-4



