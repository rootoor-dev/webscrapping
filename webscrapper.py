# This script fetches CSV files from Football Data API website and saves them into specified folders based on their countries and seasons.

import os
import re
import json
import requests
from bs4 import BeautifulSoup

# Function to extract CSV links from an HTML page
def get_csv_links(link):
    # Initialize empty list to store CSV links
    csv_links = []

    # Fetch the webpage content
    response = requests.get(link)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags followed by anchor tag that contains CSV links
    img = soup.find('img')
    while img:
        img_link = img.find_next_sibling('a')
        if img_link and img_link.get('href', '').endswith('.csv'):
            # Append each valid CSV link to the list
            csv_links.append({
                "href": img_link.get('href'),
                "text": img.get("alt") if img.get("alt") else ""
            })

        # Move to next image tag
        img = soup.find_next('img')

    return csv_links

# Function to extract year information from a given link
def seasonify_from(link):
    # Split the link into its components
    parts = link.split('/')

    # Extract the last two elements which represent the country name and the year range
    country, year_range = parts[-2], parts[-1]

    # Transform the year range into a format suitable for folder names
    year_parts = year_range.split('-')
    start_year, end_year = map(int, year_parts)

    # Return the formatted year string
    return f"{start_year}/{end_year}"

# Main function to process the entire website and save the CSV files accordingly
def process_weblink(base_url):
    # Get all available countries and their corresponding CSV links
    all_links_dict = {}
    for link in get_csv_links(base_url):
        country = link.pop("text")
        all_links_dict[link["href"]] = country

    # Store the processed data in a dictionary
    football_data = {}

    # Iterate through all available countries and their respective CSV links
    for link, country in all_links_dict.items():
        csv_links = get_csv_links(link)

        # Create nested dictionaries inside 'football_data' to store CSV files per country, season
        if country not in football_data:
            football_data[country] = {}

        for entry in csv_links:
            link = entry["href"]
            season = seasonify_from(link)
            season_formatted = f"{season}"

            # If the country doesn't have any seasons yet, create an empty list
            if season_formatted not in football_data[country]:
                football_data[country][season_formatted] = []

            # Add the complete filename and link to the list of CSV files
            final_filename = f"{country}_{entry['text']}_{season}.csv"
            football_data[country][season_formatted].append((final_filename, link))

    return football_data

# Save the processed data into a file
def save_data_in_file(output_folder, data_structure, filetype='json'):
    output_file = os.path.join(output_folder, f"data_{filetype}")

    if filetype == "json":
        with open(output_file, "w") as outfile:
            json.dump(data_structure, outfile, indent=4)
        print(f"Data structure saved to {output_file}")

    elif filetype == "csv":
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for country, seasons in data_structure.items():
                writer.writerow(["Country", "Season"] + ["File Name", "Link"])
                for season, csv_files in seasons.items():
                    for filename, link in writer.writerow([country, season])
                        for file in csv_files:
                            writer.writerow([country, season] + [file[0].split("/")[-1], file[1]])

        print(f"Data structure saved to {output_file}")

    elif filetype == "txt":
        output_file = os.path.join(output_folder, f"data_{filetype}")

        with open(output_file, "w") as text_file:
            for country, seasons in data_structure.items():
                text_file.write(f"{country}:\n")
                for season, files in seasons.items():
                    text_file.write(f"  {season}:\n")
                    for file in files:
                        text_file.write(f"    {file[0]}: {file[1]}\n")

        print(f"Data structure saved to {output_file}")

# Print the data structure without saving it
def print_data_structure(data_structure):
    for country, seasons in data_structure.items():
        print(f"Country: {country}")
        for season, files in seasons.items():
            print(f"  Season: {season}")
            for file in files:
                print(f"    File: {file[0]}")
                print(f"      Link: {file[1]}")

# Download CSV files using the provided data structure
def download_csv_files(data_structure, output_folder):
    for country, seasons in data_structure.items():
        for season, files in seasons.items():
            season_folder = os.path.join(output_folder, country, season.replace("/", "_"))
            os.makedirs(season_folder, exist_ok=True)

            for file in files:
                filename, link = file
                output_path = os.path.join(season_folder, filename)

                response = requests.get(link)
                if response.status_code == 200:
                    with open(output_path, "wb") as file:
                        file.write(response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download: {filename}")

if __name__ == "__main__":
    output_folder = "./"
    base_url = "https://www.football-data.org/"
    structured_data = process_weblink(base_url)
    download_csv_files(structured_data, output_folder)

    # Uncomment this line to see the printed data structure instead of downloading the files
    # print_data_structure(structured_data)
