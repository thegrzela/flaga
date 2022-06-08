import wikipedia
wikipedia.set_lang("pl")

def hero_character(hero_name):
    content = wikipedia.summary(hero_name, sentences = 6)
    return content
    