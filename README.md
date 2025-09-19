# RAKE Keyword Extraction (rake_nltk)

Extract top-N key phrases from text using RAKE (Rapid Automatic Keyword Extraction) with `rake_nltk`. Includes optional interpretable score breakdown (degree/frequency per word).

## Requirements

- Python 3.12+
- Dependencies are declared in `pyproject.toml`

## Setup

Install uv(if needed) and sync dependencies:

```
git clone https://github.com/tywin812/GenAI-1-07.git
cd GenAI-1-07

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
python src/rake_keyphrase_extraction.py -f data/sample.txt --top-k 5 --language english

```

Flags:
- `-f, --file` — read text from a UTF-8 file; otherwise a sample is used
- `--top-k` — number of top phrases to print (default: 5)
- `--explain` — print score decomposition per phrase
- `--normalize` — print scores normalized to [0..1] by the max in Top-K

Output example:

```
Top 5 key phrases:
 1. rake method for keyword extraction  (score=1.000)
 2. keyword extraction                  (score=0.735)
 ...
```

With `--explain`:

```
 1. keyword extraction  (score=0.735)
		 = sum(degree(word)/freq(word))
			 - keyword: degree=8, freq=2, deg/freq=4.000
			 - extraction: degree=7, freq=2, deg/freq=3.500
		 Phrase sum = 7.500 (normalized 0.735)
```

