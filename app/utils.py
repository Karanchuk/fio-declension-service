import pymorphy2

import json
from pathlib import Path

EXCEPTIONS_PATH = Path(__file__).parent.parent / "data" / "exceptions.json"

with open(EXCEPTIONS_PATH, encoding="utf-8") as f:
    EXCEPTIONS = json.load(f)

UNCHANGING_PATH = Path(__file__).parent.parent / "data" / "unchanging_suffixes.json"

with open(UNCHANGING_PATH, encoding="utf-8") as f:
    UNCHANGING_SUFFIXES = json.load(f)["suffixes"]

RARE_NAMES_PATH = Path(__file__).parent.parent / "data" / "rare_names.json"
with open(RARE_NAMES_PATH, encoding="utf-8") as f:
    RARE_NAMES = json.load(f)

morph = pymorphy2.MorphAnalyzer()

CASES = {
    "nomn": "nomn",
    "gent": "gent",
    "datv": "datv",
    "accs": "accs",
    "ablt": "ablt",
    "loct": "loct",
}

GENDER_TAGS = {
    "masc": "masc",
    "femn": "femn",
}

def detect_gender(fio: str):
    parts = fio.split()
    if len(parts) < 2:
        return None
    name = parts[1]

    # проверяем редкие имена
    if name in RARE_NAMES:
        return RARE_NAMES[name]

    parsed = morph.parse(name)[0]
    if 'Name' in parsed.tag:
        if 'femn' in parsed.tag:
            return 'femn'
        elif 'masc' in parsed.tag:
            return 'masc'

    # fallback по окончанию
    if name.endswith(('а', 'я')):
        return 'femn'
    return 'masc'

def capitalize_like(original: str, word: str) -> str:
    if original[0].isupper():
        return word.capitalize()
    return word


def decline_word(word: str, case: str, gender: str = None):
    # Проверяем словарь исключений
    if word in EXCEPTIONS and case in EXCEPTIONS[word]:
        return EXCEPTIONS[word][case]

    # Раздельно склоняем двойные фамилии
    if '-' in word:
        parts = [decline_word(p, case, gender) for p in word.split('-')]
        return '-'.join(parts)

    # Проверка на неизменяемые казахские/редкие окончания
    for suffix in UNCHANGING_SUFFIXES:
        if word.endswith(suffix):
            return word  # не склоняем

    # Сначала пробуем pymorphy2
    parsed = morph.parse(word)[0]
    tags = {CASES.get(case, case)}
    if gender:
        tags.add(GENDER_TAGS[gender])
    inflected = parsed.inflect(tags)
    if inflected:
        word_inf = capitalize_like(word, inflected.word)
    else:
        word_inf = word

    # Особое правило для женских отчеств на -ична, -евна, -овна
    if gender == 'femn' and case == 'datv':
        if word.endswith('ична'):
            word_inf = word.replace('ична', 'ичне')
        elif word.endswith('евна'):
            word_inf = word.replace('евна', 'евне')
        elif word.endswith('овна'):
            word_inf = word.replace('овна', 'овне')

    # Если pymorphy2 не сработал, применяем простой фоллбек по окончанию
    if word_inf == word:
        fallback = word
        if case == 'datv':
            if word.endswith(('а', 'я')):
                fallback = word[:-1] + 'е'
            elif word.endswith('й'):
                fallback = word[:-1] + 'ю'
            else:
                fallback = word + 'у'
        elif case == 'gent':
            if word.endswith(('а', 'я')):
                fallback = word[:-1] + 'ы'
            else:
                fallback = word + 'а'
        elif case == 'ablt':
            if word.endswith(('а', 'я')):
                fallback = word[:-1] + 'ой'
            else:
                fallback = word + 'ом'
        elif case == 'loct':
            if word.endswith(('а', 'я')):
                fallback = word[:-1] + 'е'
            else:
                fallback = word + 'е'
        word_inf = capitalize_like(word, fallback)

    return word_inf


def decline_fio(fio: str, case: str):
    parts = fio.split()
    declined_parts = []
    gender = detect_gender(fio)

    for part in parts:
        declined_parts.append(decline_word(part, case, gender))

    return " ".join(declined_parts)