import requests 
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import csv
import argparse
import string
from pygal.maps.world import World
#from pygal.style import CleanStyle
from pygal.maps.world import COUNTRIES


def main():

	#"https://www.statbunker.com/competitions/Nationalities?comp_id=564"
		
	premier = '556'
	laliga = '564'
	bundesliga = '561'
	seriea = '562'
	ligue1 = '563'
	mls = '577'
	champions = '571'
	europa = '572'
	eredivisie = '565'
	scottish = '566'

	# dict for specific league
	league_dict = extract(laliga)

	# change it up so color differentiation isnt too strong
	# 4 categories: 1, <avg, >avg, top

	# find the avg num
	avg_num = find_avg(league_dict)

	# create 4 different dicts that will all be added to the map
	league_dict_1 = {} # for countries with 1 player
	league_dict_2 = {} # for countries less than half
	league_dict_3 = {} # for countries greater than half
	league_dict_4 = {} # for country with most players

	# add to respective dicts
	top_num = find_top_num(league_dict)
	for country, num in league_dict.items():
		if num == top_num:
			league_dict_4[country] = num
		elif num == 1:
			league_dict_1[country] = num
		elif num <= avg_num:
			league_dict_2[country] = num
		else:
			league_dict_3[country] = num

	# create the world map
	wm = World()
	wm.title = 'Nationalities in the la liga'
	# added order due to coloring differences 
	wm.add('players < avg',league_dict_2)
	wm.add('players > avg',league_dict_3)
	wm.add('most players',league_dict_4)
	wm.add('players = 1',league_dict_1)
	wm.render_to_file('player_nationalities_laliga.svg')


def extract(id):
	"""will extract the data from the url given"""
	data = OrderedDict()
	url = "https://www.statbunker.com/competitions/Nationalities?comp_id=%s"%(id)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	edited = soup.find('tbody')
	country = ''
	nat_number = 0
	for a in edited.find_all('tr'):
		count = 0
		for s in a.find_all('td'):
			if count == 0:
				country = get_country_code(s.get_text())
				count += 1
			else:
				nat_number = int(s.get_text())
				
		# add the values for those grouped countries 
		if country == 'gb':
			if 'gb' in data:
				data['gb'] += nat_number
			else:
				data.update({country:nat_number})
		elif country == 'ie':
			if 'ie' in data:
				data['ie'] += nat_number
			else:
				data.update({country:nat_number})
		else:
			data.update({country:nat_number})
		#data.update({country:nat_number})
		
	return data

	"""url = "https://www.youtube.com/watch?v=RiAEnSoWIUU"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	print(soup.prettify())"""

def get_country_code(country_name):
	"""Return the Pygal 2-digit country code for the given country"""
	# fix the country name to be fitting 
	country_name = fix_country_name(country_name)

	# South Korea giving some issues
	"""if country_name == 'South Korea':
		return 'kp'"""
	for code, name in COUNTRIES.items():
		if name == country_name:
			return code
	# If the country wasn't found, return None
	return None

def fix_country_name(country_name):
	"""for all the countries that need specifiying"""
	if country_name == 'England':
		return 'United Kingdom'
	elif country_name == 'Wales':
		return 'United Kingdom'
	elif country_name == 'Scotland':
		return 'United Kingdom'
	elif country_name == 'Republic of Ireland':
		return 'Ireland'
	elif country_name == 'Northern Ireland':
		return 'Ireland'
	elif country_name == 'South Korea':
		return 'Korea, Republic of'
	elif country_name == 'Democratic Republic of Congo':
		return 'Congo, the Democratic Republic of the'
	elif country_name == 'Republic of the Congo':
		return 'Congo'
	elif country_name == 'Venezuela':
		return 'Venezuela, Bolivarian Republic of'
	elif country_name == 'The Gambia':
		return 'Gambia'
	elif country_name == 'Russia':
		return 'Russian Federation'
	elif country_name == 'Iran':
		return 'Iran, Islamic Republic of'
	else:
		return country_name

# could combine 2 below into nested function for less step count

def find_avg(nat_dict):
	"""will find avg of the total amount of nationalities in a specified dict (league)"""
	total = 0
	count = 0
	for x in nat_dict:
		count += 1
		total += nat_dict[x]
	avg = int(total/count)
	return avg 

def find_top_num(nat_dict):
	"""will find the top number of players from a nationality, mostly to prevent outliers"""
	top_num = 0
	for x in nat_dict:
		if nat_dict[x] > top_num:
			top_num = nat_dict[x]

	return top_num


main()




