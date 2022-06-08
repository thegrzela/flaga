  
from email.quoprimime import quote
from unicodedata import name
from flask import Flask, render_template, redirect, url_for
from moje_programy.character_wiki import character
from moje_programy.open_poem import open_poem
from moje_programy.open_poem_ukr import open_poem_ukr
from moje_programy.hero_wikipedia import hero_character
import random
import os
import wikipedia
import requests
from lxml import html




app=Flask(__name__)
app.config['SECRET_KEY'] = 'tajnehaslo'
app.config['UPLOAD_FOLDER'] = 'static'



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/xd')
def xd():
    text = open('dane/xd.txt').read()
    return render_template("xd.html", text=text)

@app.route('/yt')
def yt():
    return render_template('yt.html')

@app.route('/projekty')
def projects():
    return render_template('projects.html')


@app.route('/brudnopis')
def brudnopis():
    super_heroes = ['Bruce Lee', 'Kubuś Puchatek', 'Kopernik', 'Małysz']
    chosen_hero = random.choice( super_heroes)
    description = character(chosen_hero).encode('utf-8').decode()
    poem_lines = open_poem()
    return render_template("brudnopis.html", hero=chosen_hero, description=description, poem_lines=poem_lines)


"""Flaga dla Ukrainy"""

@app.route('/flaga-dla-ukrainy')
def flaga_dla_ukrainy():
    return render_template("ukraina_templates/flaga_dla_ukrainy.html")

@app.route('/slava-ukraini')
def slavia_ukraina():
    return render_template("ukraina_templates/slava_ukraini.html")   


@app.route('/ukraina-za-10-lat')
def ukraina_za_10_lat():
    #text = open('dane/poem_ukr.txt').read()
    poem_lines_ukr = open_poem_ukr()
    return render_template("ukraina_templates/ukraina_za_10_lat.html", poem_lines_ukr=poem_lines_ukr)

@app.route('/kubus_puchatek')
def kubus_puchatek():
    return render_template("kubus_puchatek.html")


@app.route('/ciekawe-postacie')
def ciekawe_postacie():
    lista_ciekawych_postaci = [
        'Pudzianowski',         # 0
        'Małysz',               # 1
        'Kopernik',             # 2
        'Maria Skłodowska',     # 3
        'Kościuszko',           # 4
        'Kaczor Donald',        # 5
        'Myszka Miki',          # 6
    ]
    opisy_postaci = []
    for i in range(3):
        postac = random.choice(lista_ciekawych_postaci)
        indeks = lista_ciekawych_postaci.index(postac)
        lista_ciekawych_postaci.pop(indeks)

        opis_postaci = character(postac)
        info = [postac, opis_postaci]
        opisy_postaci.append(info)

    return render_template("ciekawe-postacie.html", opisy_postaci=opisy_postaci)


@app.route('/login')
def login():
    return render_template('login_templates/index.html')

	

'''*********************************************************'''



@app.route('/flaga', methods=["GET", "POST"])
def flaga():
	create_folders()

	# Flag.
	xd = random.choice(range(22))
	if len(os.listdir('static/flag_image')) < 10:
		#print(os.listdir)
		xd = 11
	ta_flaga = os.path.join(app.config['UPLOAD_FOLDER'], 'Polska_Flaga__{}.jpg'.format(xd))
	
	# Gather heroes.
	heroes = gather_heroes()
	random.shuffle(heroes)

	return render_template("flaga.html", xd=xd, flaga=ta_flaga, heroes=heroes,)



def gather_heroes():
	

	heroes = [
 		'Mikołaj Kopernik', 
 		'Maria Skłodowska-Curie',
 		'Fryderyk Chopin',
 		'Józef Piłsudski',
 		'Tadeusz Kościuszko',
 		'Adam Mickiewicz',
		'Jan Henryk Dąbrowski',
 		'Józef Haller',
 		'Władysław Sikorski',
		'Wojciech Korfanty',
 		'Mieczysław Paluch',
		'Ignacy Mościcki', 
		'Teresa Grodzińska',
		
	]

	greetings = [
		'pozdrawia',
		'/wave',
		'/wink',
		'wita',
	]

	wikipedia.set_lang("pl")
 
	saved_heroes = os.listdir('saved_heroes')
	saved_heroes = [h.split('.')[0] for h in saved_heroes]
	

	for hero in heroes:
		if hero not in saved_heroes:

			# Get some info and link.
			some_info = wikipedia.page(hero)
			print(some_info)
			
			info_intro = some_info.content.split('\n\n')[0] 
			print(info_intro)
			url = '<a href="'+some_info.url+'">Poszukaj więcej info o: '+hero+"</a>"
			
			# Get what hero thinks.
			hero_think(hero)
			
			# Get & save images.
			# images = some_info.images
			# n_photos = 0
			# for i, image_url in enumerate(images):
			# 	if i < 3:
			# 		hero_str = '11'.join(hero.split())
			# 		image_name = '{}_{}.legend'.format(hero_str, i)
			# 		save_image(image_url, image_name)
			# 		n_photos += 1

			# Save all.
			with open('saved_heroes/'+hero+".hero", "w+") as f:
				f.write(hero + '\n')
				f.write('\n') #str(n_photos) + '\n')
				f.write(info_intro + '\n')
				f.write(url)
				
			
		else:
			greeting = random.choice(greetings)
			print(hero, greeting)
			
			  

	heroes = []
	for hero_file in os.listdir('saved_heroes'):
		hero = {}
		#print(hero) gk
		some_info = open('saved_heroes/'+hero_file).readlines()
		hero['name'] = some_info[0]
		#print(hero['name']) gk
		print(some_info)
		#photo_nr = random.choice(range(int(some_info[1])))
		#hero_str = '11'.join(hero['name'][:-1].split())
		#hero['image'] = '{}_{}.legend'.format(hero_str, photo_nr)
		hero_quotes = open('hero_think/' + hero['name'][:-1] + ".hero").readlines()
		print(hero_quotes)
		hero['quote'] = random.choice(hero_quotes)
		hero['description'] = '\n'.join(some_info[2:-1])
		hero['description'] = bold(hero['description'])
		# print(hero['description']) gk
		hero['url'] = some_info[-1]
		#hero['greetings'] = [h.split()[0] for h in random.choice(greetings)] gk
		hero['greetings'] = random.choice(greetings)

		heroes.append(hero)
	return heroes

# def save_image(image_url, image_name): 
# 	image = requests.get(image_url).content
# 	save_as = 'static/hero_image/{}'.format(image_name)
# 	with open(save_as, 'wb') as ap:
# 		ap.write(image)
# 	return save_as

def bold(hero_info):

	nice = [
		'nauk',
		'gen',
		'zwy',
		'odk',
		'zał',
		'rod',
		'organizator',
		'astronom',
		'inżynier',
		'herbu',
		'wojska',
		'uczona',
		'nobla',
		'wybitniej',
		'romantyczny',
		'fizyk',
		'filozof',
		'kocha',
		'woli',
		'kawalerii',
		'skazany',
		'przywódca', 
	]

	right_desc = []
	words = [w for w in hero_info.split()] # wyrzuciłem metodę w.lower() gk
	for w in words:
		for woah in nice:
			if w.startswith(woah):
				w = '<b>'+w+'</b>'
		right_desc.append(w)
	right_desc = " ".join(right_desc)
	#print(type(right_desc)) gk
	#print(right_desc) gk
	return right_desc
	

def hero_think(name):
	url_name = name.replace(' ', '_')
	url = 'https://pl.wikiquote.org/wiki/{}'.format(url_name)
	hero_wikiquotes = requests.get(url)
	with open('hero_think/'+name+".hero", "w+") as f:
		
		for line in hero_wikiquotes.text.split('\n'):
			if line.startswith('<h2>O'):
				continue
			if line.startswith('<ul><li>'):
				
				tree = html.fromstring(line)
				quote = tree.text_content().strip()
				#print(tree) gk

				# if quote.startswith('Utworzyć'):
				# 	f.write('brak cytatu...\n')
					
				if not quote.startswith('Opis') and not quote.startswith('Autor') and not quote.startswith('Źródło') and not quote.startswith('Zobacz też'): 
					f.write(quote + '\n')
					print('-', quote)
			



def create_folders():
	os.system("mkdir static/hero_image")
	os.system("mkdir static/flag_image")
	os.system("mkdir saved_heroes")
	os.system("mkdir hero_think")




if __name__=="__main__":
    app.run(debug=True)
