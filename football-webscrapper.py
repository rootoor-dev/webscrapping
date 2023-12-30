import requests
import re
import json
import csv
import os
import pandas as pd
from bs4 import BeautifulSoup

def get_csv_links(url):
    base_url = "https://football-data.co.uk/"

    response = requests.get(url).content

    soup = BeautifulSoup(response, 'html.parser')

    csv_links = []

    for img in soup.find_all('img'):
        img_link = img.find_next_sibling('a')
        if img_link and img_link.get('href', '').endswith('.csv'):
            csv_links.append({
                "href": base_url + img_link["href"],
                "text": img_link.get_text() or img.get("alt"),
            })

    return csv_links

# to modify the structure of the links obtained from the web scraping process.
# the function looks for a 4-digit season in the "text" value using the regular expression r'\d{4}'.

def split_link(link, separator='/'):
    # Split the path using '/'
    path_components = link.split(separator)

    # Remove empty components
    path_components = [component for component in path_components if component]

    # Print the result and use key = -2 to get the season
    #print(path_components)

    return path_components

def transform_to_years(years):
    years_str = str(years)
    if len(years_str) == 4:
        start_year = int(years_str[:2])
        end_year = int(years_str[2:])

        if start_year >=70 or end_year >=70: # data on football have begun to be stored since 1970 everywhere in the world
            start_year = 1900 + start_year
            end_year = start_year + 1
            return f"{start_year}/{end_year}"
        else:
            start_year = 2000 + start_year
            end_year = start_year + 1
            return f"{start_year}/{end_year}"
    else:
        return  # we should never enter here for the season is still in 4-digits

def seasonify_from(csv_link):
    # the csv_link must be in this format strictly : "https://football-data.co.uk/mmz4281/5051/E0.csv"
    return transform_to_years(split_link(csv_link)[-2])

def get_all_csvlinks_webpages_as_dictionnary(base_url):

    """ the mandatory link to provide is ====> base_url = "https://football-data.co.uk/data.php" """

    #url = "https://www.football-data.co.uk"
    # Fetching the HTML content
    html_content = requests.get(base_url).content
    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the tbody tag containing the table data
    table_body = soup.find_all('div', class_="menus")

    # Initialize an empty list to store the extracted links and labels
    links = []

    # Iterate through each div in the table
    for div in table_body:
        # Get the image element and extract the link
        a_tag = div.find('a')  # Trouver la balise <a> à l'intérieur de la balise <div>
        if a_tag and a_tag.has_attr('href'):  # Vérifier si la balise <a> a un attribut href
            a_tag_link = a_tag['href']
            links.append(a_tag_link)



    """
    Voici les liens qu'on cible en réalité

    https://www.football-data.co.uk/englandm.php
    https://www.football-data.co.uk/scotlandm.php
    https://www.football-data.co.uk/germanym.php
    https://www.football-data.co.uk/italym.php
    https://www.football-data.co.uk/spainm.php
    https://www.football-data.co.uk/francem.php
    https://www.football-data.co.uk/netherlandsm.php
    https://www.football-data.co.uk/belgiumm.php
    https://www.football-data.co.uk/portugalm.php
    https://www.football-data.co.uk/turkeym.php
    https://www.football-data.co.uk/greecem.php
    https://www.football-data.co.uk/argentina.php
    https://www.football-data.co.uk/austria.php
    https://www.football-data.co.uk/brazil.php
    https://www.football-data.co.uk/china.php
    https://www.football-data.co.uk/denmark.php
    https://www.football-data.co.uk/finland.php
    https://www.football-data.co.uk/ireland.php
    https://www.football-data.co.uk/japan.php
    https://www.football-data.co.uk/mexico.php
    https://www.football-data.co.uk/norway.php
    https://www.football-data.co.uk/poland.php
    https://www.football-data.co.uk/romania.php
    https://www.football-data.co.uk/russia.php
    https://www.football-data.co.uk/sweden.php
    https://www.football-data.co.uk/switzerland.php
    https://www.football-data.co.uk/usa.php

    on remarque qu'après  "https://www.football-data.co.uk/" il faut au plus douze (12)
    caractères (netherlandsm) joints à ".php" pour former le lien complet recherché.
    Sauf les liens suivants:
    - "https://www.football-data.co.uk/data.php"
    - "https://www.football-data.co.uk/books.php"
    - "https://www.football-data.co.uk/links.php"
    - "https://www.football-data.co.uk/matches.php"
    - "https://www.football-data.co.uk/downloadm.php"

    Donc la regex qui permet cela est : ^https:\/\/www\.football-data\.co\.uk\/[a-z]{1,12}\.php$

    Et pour tenir compte des assertions négatives sus-mentionnées, on écrit la regex comme suit :

    regex = re.compile(r'^https://www\.football-data\.co\.uk\/(?!data\.php|books\.php|links\.php|matches\.php|downloadm\.php)([a-z]{1,12})\.php$')

    La partie (?!data\.php|books\.php|links\.php|matches\.php|downloadm\.php)
    dans la regex est une assertion négative anticipée qui exclut les liens spécifiés de la correspondance.

    """

    #links_list = []
    links_dict = {} # dictionnaire des liens stockant le lien et le nom du pays correspondant

    #links_set = set() # Set vide pour unicité des liens

    # Afficher les liens extraits
    for link in links:
        # regex
        #regex = re.compile(r'^{url}\/(?!data\.php|books\.php|links\.php|matches\.php|downloadm\.php)([a-z]{1,12})\.php$') # don't use for not working
        regex = re.compile(r'^https://www\.football-data\.co\.uk\/(?!data\.php|books\.php|links\.php|matches\.php|downloadm\.php)([a-z]{1,12})\.php$')
        # Correspondance avec le modèle
        match = regex.match(link)

        if match:
            # Récupérer le nom du pays à partir du groupe capturé dans la regex en supprimant le "m" final pour certains pays de la liste
            country_name = match.group(1).rstrip("m")
            # Ajouter le lien à la liste, au set et au dictionnaire
            #links_list.append(link)
            #links_set.add(link)
            links_dict[link] = country_name

    # Afficher les résultats
    #print("Liste des liens:")
    #print(links_list)

    #print("\nSet de liens (pour unicité):")
    #print(links_set)

    #print("\nDictionnaire des liens avec noms de pays:\n")
    #for link, country_name in links_dict.items():
    #    print(f"{link} : {country_name}")

    return links_dict

def process_weblink(football_data_co_uk_link):

    # ALGORITHME POUR UNE PAGE
    # on se rend sur cette page...
    #csv_links = get_csv_links("https://football-data.co.uk/englandm.php")
    # ...puis on en extrait le nom du pays à partir de lui
    # ensuite on le parse entièrement pour en extraire les liens des fichiers csv que contient sa page.
    # une fois fait, on télécharge les fichiers puis on les range par pays et par saison
    # donc tous les liens de la même saison sont sauvegardés dans le même répertoire
    # tout lien de csv est sous ce format csv = "https://football-data.co.uk/mmz4281/5051/E0.csv"
    #print(seasonify(csv))
    #get_dict_items(csv_links)[0]

    # ALGORITHME POUR TOUTES LES PAGES

    # recupérer tous les liens dans un dictionnaire
    all_links_dict = get_all_csvlinks_webpages_as_dictionnary(football_data_co_uk_link)

    #print(len(all_links)) # 27 pays
    #print(all_links) # contenu du dictionnaire

    football_data = {} # Structured data

    # Extracting items from the dictionary using the generator
    for link, country_name in all_links_dict.items():
        #print(f"Link: {link}, Country Name: {country_name}")
        # extract the csv links from 'link' into a list of dictionnaries
        csv_links_list_dict = get_csv_links(link)

        #print(csv_links_list_dict)
        # Extracting href values
        #href_values = [item['href'] for item in csv_links_list_dict]
        # Extracting text values
        #text_values = [item['text'] for item in csv_links_list_dict]

        # Extracting href values
        #csv_urls_list = [item['href'] for item in csv_links_list_dict]  # E0.csv, E1.csv, E2.csv ....
        # Extracting text values
        #league_names_list = [item['text'] for item in csv_links_list_dict] # PL, C1, C2,...

        """ OR DO EXTRACTIONS LIKE THIS """
        # Initialize an empty dictionary to store the structured data
        
        for entry in csv_links_list_dict:
            link = entry['href']  # as a string which we name "csv_url"
            text = entry['text']  # as a string which we name "league_name"
            # Extract country name and season from the link
            season = seasonify_from(link)
            #print(f"{country_name} and {season}")
            #break
            # Convert season to the desired format
            season_formatted = f"Season {season}"
            #print(f"{season_formatted}")
            #break

            # Create the nested dictionary structure
            if country_name not in football_data:
                football_data[country_name] = {}

            if season_formatted not in football_data[country_name]:
                football_data[country_name][season_formatted] = []
            
            # Append the CSV file to the corresponding season
            final_csv_file_name = [country_name + "_" + text.replace(' ', '_') + "_"+ season.replace('/', '-') + '.csv', link]
            football_data[country_name][season_formatted].append(final_csv_file_name)
        #break    
    return football_data

def save_data_in_file(output_folder, data_structure, filetype='json'):
    if filetype not in ['json', 'csv', 'txt']:
        print("Invalid file type. Supported types are 'json', 'csv', and 'txt'.")
        return

    output_file = os.path.join(output_folder, f'data_structure.{filetype}')

    if filetype == 'json':
        with open(output_file, 'w') as json_file:
            json.dump(data_structure, json_file, indent=4)
        print(f"Data structure saved to {output_file}")

    elif filetype == 'csv':
        with open(output_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for country, seasons in data_structure.items():
                for season, csv_files in seasons.items():
                    for csv_file in csv_files:
                        csv_writer.writerow([country, season] + csv_file)
        print(f"Data structure saved to {output_file}")

    elif filetype == 'txt':
        with open(output_file, 'w') as txt_file:
            for country, seasons in data_structure.items():
                txt_file.write(f"{country}:\n")
                for season, csv_files in seasons.items():
                    txt_file.write(f"  {season}:\n")
                    for csv_file in csv_files:
                        txt_file.write(f"    {', '.join(csv_file)}\n")
        print(f"Data structure saved to {output_file}")

"""
def print_special_structured_data(football_data_dict):
    # Print the structured data
    for country, seasons in football_data_dict.items():
        print(f"Country: {country}")
        for season, csv_files in seasons.items():
            print(f"{season}: {', '.join(csv_files)}")
"""

def print_data_structure(data_structure):
    for country, seasons in data_structure.items():
        print(f"Country: {country}")
        for season, csv_files in seasons.items():
            print(f"  Season: {season}")
            for csv_file in csv_files:
                file_name, file_url = csv_file
                print(f"    {file_name}: {file_url}")

def download_csv_files(data_structure, output_folder):
    for country, seasons in data_structure.items():
        for season, csv_files in seasons.items():
            for csv_file in csv_files:
                file_name, file_url = csv_file
                output_path = os.path.join(output_folder, country, season, file_name)

                # Create directories if they don't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Download the file
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {file_name}")
                else:
                    print(f"Failed to download: {file_name}")

def download_csv_files_by_country_and_season(data_structure, output_folder):
    for country, seasons in data_structure.items():
        for season, csv_files in seasons.items():
            #print(season) # Season 2023/2024 not recommanded for folder names
            #break
            season_folder = os.path.join(output_folder, country, season.replace('/', '_')) # ./england/Season 2023_2024
            #print(season_folder)
            #break
            os.makedirs(season_folder, exist_ok=True)

            for csv_file in csv_files:
                file_name, file_url = csv_file
                output_path = os.path.join(season_folder, file_name)
                #print(file_name)
                #print(file_url)
                #print(output_path)
                #break

                # Download the file
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {country}/{season}/{file_name}")
                else:
                    print(f"Failed to download: {country}/{season}/{file_name}")
                #break

def run():
    # CHANGES NEEDED HERE !
    # Please change these variables values before executing the run() function !
    output_folder = "."

    # DON'T TOUCH ANYTHING HERE
    mandatory_base_url = "https://football-data.co.uk/data.php"
    structured_data = process_weblink(mandatory_base_url)
    #print_data_structure(structured_data)
    save_data_in_file(output_folder, structured_data, filetype='json')
    download_csv_files_by_country_and_season(structured_data, output_folder)

################################### TEST ZONE ###################################
# use
"""
    Actually, the script will :
      - web scrape the website "https://football-data.co.uk/data.php"
      - store data into a data structure named "data_structure" or what you want
      - save all downloaded files by country and season

    Add more function you want and Enjoy !

"""
run()

