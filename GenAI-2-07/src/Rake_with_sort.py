import argparse
from rake_keyphrase_extraction import extract_keyphrases, explain_phrase

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_worldcloud (all_phrases) :

    """
    Создает и отображает облако ключевых фраз с размерами, пропорциональными их важности.
    
    Функция принимает список фраз с оценками их значимости, нормализует оценки,
    генерирует визуальное облако тегов и отображает его с помощью matplotlib.
    
    Parameters
    ----------
    all_phrases : list of tuples
        Список кортежей в формате (score: float, phrase: str), где:
        - score: числовая оценка важности фразы (чем выше, тем важнее)
        - phrase: текстовая фраза для отображения в облаке
        
    Returns
    -------
    None
        Функция отображает график с помощью plt.show() и не возвращает значений.
    
    Notes
    -----
    - Оценки нормализуются относительно максимального значения в переданном списке
    - Размер шрифта каждой фразы пропорционален ее нормализованной важности
    - Используется цветовая карта 'viridis' на черном фоне
    - Предполагается наличие русского шрифта по указанному пути

    # Отобразит облако тегов с фразами разного размера в зависимости от важности
    """

    
    phrase_weights = {}
    
    # Находим максимальную оценку для нормализации
    if all_phrases:
        max_score = max(score for score, phrase in all_phrases)
    else:
        max_score = 1.0
    
    # Заполняем словарь весов
    for score, phrase in all_phrases:
        # Нормализуем оценку от 0 до 1
        normalized_score = score / max_score if max_score > 0 else 0
        phrase_weights[phrase] = normalized_score
    
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='black',
        colormap='viridis',
        max_words=100,
        prefer_horizontal=0.7,
        min_font_size=10,
        max_font_size=200,
        font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # для русского
    ).generate_from_frequencies(phrase_weights)
    
    # Отображаем
    plt.figure(figsize=(14, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Облако ключевых фраз (размер = важность)', fontsize=16, pad=20)
    plt.tight_layout()
    
    plt.show()

def main():

    parser = argparse.ArgumentParser(description="RAKE keyword extraction")
    parser.add_argument("-f", "--file", help="Path to text file (utf-8)")
    parser.add_argument("--top-k", type=int, default=20, help="The number of phrases among which we are looking for the top 5 lengths is 2-4")
    parser.add_argument("--language", type=str, default="russian", help="Language of the text" )
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

    top_n = 5

    top, rake = extract_keyphrases(text, top_k = args.top_k, language=args.language)

    if not top:
        print("Key phrases are not found.")
        return
    
    print("Top 5 key phrases :")

    all_phrases = []

    print_count = 0
    for _, (score, phrase) in enumerate(top, 1):

        if print_count == top_n :
            break

        # В общем смотрим сколько слов в фразе и если нам не подходит идем на следующую итерацию
        temp_phrase = phrase.split(' ')
        if len(temp_phrase) < 2 or len(temp_phrase) > 4 :
            continue
        print(f"{print_count+1:>2}. {phrase}  {score}")

        all_phrases.append((score, phrase))
        
        print_count += 1
    
    if print_count != top_n :
        print("Increase the top_k value !!!")

    create_worldcloud(all_phrases)

if __name__ == "__main__" :
    main()
