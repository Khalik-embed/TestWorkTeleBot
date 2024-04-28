from config import CONFIG

if CONFIG.django_config.lang == "ru":
  from lexicon.lexicon_ru import *
elif CONFIG.django_config.lang == "en":
  from lexicon.lexicon_en import *
elif CONFIG.django_config.lang == "es":
  from lexicon.lexicon_es import *