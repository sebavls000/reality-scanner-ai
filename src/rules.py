import re

MANIPULATION_KEYWORDS = [
    "ellos no quieren que sepas",
    "la verdad oculta",
    "control total",
    "manipulación",
    "élite",
    "agenda secreta",
]

SCIENCE_KEYWORDS = [
    "evidencia",
    "datos",
    "estudio",
    "investigación",
    "análisis",
]

RELIGION_KEYWORDS = [
    "dios",
    "fe",
    "espiritual",
    "religión",
    "creencia",
]

PHILOSOPHY_KEYWORDS = [
    "existencia",
    "sentido",
    "realidad",
    "conciencia",
    "filosofía",
]


def score_text(text):
    text = text.lower()

    def count_keywords(keywords):
        return sum(1 for k in keywords if k in text)

    return {
        "manipulation": count_keywords(MANIPULATION_KEYWORDS),
        "science": count_keywords(SCIENCE_KEYWORDS),
        "religion": count_keywords(RELIGION_KEYWORDS),
        "philosophy": count_keywords(PHILOSOPHY_KEYWORDS),
    }


def classify(scores):
    return max(scores, key=scores.get)