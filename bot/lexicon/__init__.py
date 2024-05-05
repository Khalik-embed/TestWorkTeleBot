from config.config import CONFIG

if CONFIG.tg_bot.lang == "ru":
  from lexicon.lexicon_ru import *
elif CONFIG.tg_bot.lang == "en":
  from lexicon.lexicon_en import *
elif CONFIG.tg_bot.lang == "es":
  from lexicon.lexicon_es import *