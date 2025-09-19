import argparse
from typing import List, Tuple

import nltk
for pkg in ('stopwords', 'punkt', 'punkt_tab'):
    nltk.download(pkg, quiet=True)

import re

from rake_nltk import Rake


def explain_phrase(phrase: str, rake: Rake) -> Tuple[List[Tuple[str, int, int, float]], float]:
    """
    Explain a RAKE phrase score.

    Computes the standard RAKE score for a phrase as the sum over its tokens
    of degree(word) / frequency(word). Returns both the per-token breakdown and
    the total phrase score.

    Parameters
    ----------
    phrase: str
        The key phrase string to analyze.
    rake: Rake
        rake_nltk.Rake instance that already extracted
        keywords from the target text.

    Returns
    -------
    Tuple[List[Tuple[str, int, int, float]], float]
        breakdown: List[Tuple[str, int, int, float]]
            List of tuples (token, degree, frequency, degree/frequency)
            for each token included in the phrase.
        phrase_score: float 
            The sum of degree/frequency across tokens.
    """
    pattern = r"[^A-Za-zА-Яа-яЁё0-9_'’\-\u2010\u2011]+"
    words = [w for w in re.split(pattern, phrase.lower()) if w]

    freq_map = rake.get_word_frequency_distribution()
    deg_map = rake.get_word_degrees()

    breakdown = []
    for w in words:
            freq = freq_map.get(w, 0)
            deg = deg_map.get(w, 0)
            wscore = (deg / freq) if freq else 0.0
            breakdown.append((w, deg, freq, wscore))
    phrase_score = sum(ws for _, _, _, ws in breakdown)
    return breakdown, phrase_score

def extract_keyphrases(
    text: str, 
    top_k: int = 5, 
    language: str = 'russian'
) -> Tuple[List[Tuple[float, str]], Rake]:
    """
    Extract top-N key phrases from text using RAKE.

    Parameters
    ----------
    text: str
        Input text (UTF-8) to analyze.
    top_k: int
        Number of top-ranked phrases to return (default 5).
    language: str 
        Language for stopwords configuration passed to RAKE(e.g., 'english', 'russian').

    Returns
    -------
    Tuple[List[Tuple[float, str]], Rake]
        ranked_phrases: 
            List of (score, phrase) sorted descending by score,truncated to top_k.
        rake: Rake 
            Rake instance.
    """
    rake = Rake(language=language)
    rake.extract_keywords_from_text(text)
    ranked = rake.get_ranked_phrases_with_scores()

    seen = set()
    unique_ranked = []
    for score, phrase in ranked:
        key = phrase.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique_ranked.append((score, phrase))

    return unique_ranked[:top_k], rake

def main():
    parser = argparse.ArgumentParser(description="RAKE keyword extraction")
    parser.add_argument("-f", "--file", help="Path to text file (utf-8)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of top phrases")
    parser.add_argument("--language", type=str, default="russian", help="Language of the text" )
    parser.add_argument("--explain", action="store_true", help="Show score decomposition for each phrase")
    parser.add_argument("--normalize", action="store_true", help="Print normalized scores (0..1)")
    args = parser.parse_args()
    
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except FileNotFoundError:
            print(f"'{args.file}' not found.")
            return
    else:
        text = (
            "Владимир Владимирович Путин — российский государственный и политический деятель. " 
            "Действующий президент Российской Федерации, председатель Государственного Совета Российской Федерации" 
            "и Совета Безопасности Российской Федерации;" 
            "Верховный главнокомандующий Вооружёнными силами Российской Федерации с 7 мая 2012 года. "
        )

    top, rake = extract_keyphrases(text, top_k=args.top_k, language=args.language)
    if not top:
        print("Key phrases are not found.")
        return

    max_score = top[0][0]

    print(f"Top {len(top)} key phrases:")
    for i, (score, phrase) in enumerate(top, 1):
        shown = (score / max_score) if (args.normalize and max_score) else score
        print(f"{i:>2}. {phrase}  (score={shown:.3f})")
        if args.explain:
            breakdown, pscore = explain_phrase(phrase, rake)
            for w, deg, freq, ws in breakdown:
                print(f"      - {w}: degree={deg}, freq={freq}, deg/freq={ws:.3f}")
            if args.normalize and max_score:
                print(f"      Phrase sum = {pscore:.3f} (normalized {pscore/max_score:.3f})")

if __name__ == "__main__":
    main()
