# bibfetcher/main.py
import re
import time
import csv
import requests
import urllib.parse
from tqdm import tqdm
from collections import defaultdict


def run():
    titles = []
    with open(f'titles.txt', 'r') as f:
      for line in f:
        titles.append(line.strip()) # .strip() removes leading/trailing whitespace
    print("You have "+str(len(titles))+" articles.")

    results = []

    print("Fetching...")
    for title in tqdm(titles, desc="Processing titles"):
        query_title = urllib.parse.quote(title)
        url = f"https://api.crossref.org/works?query={query_title}"

        bibtex_text = "N/A"
        found_bib = "No"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data["message"].get("items", [])

            if items:
                first_match = items[0]
                doi = first_match.get("DOI", "")

                if doi:
                    bibtex_url = f"https://doi.org/{doi}"
                    headers = {"Accept": "application/x-bibtex"}
                    bibtex_response = requests.get(bibtex_url, headers=headers, timeout=10)

                    if bibtex_response.status_code == 200:
                        # Ensure consistent UTF-8 decoding
                        bibtex_response.encoding = 'utf-8'
                        bibtex_text = bibtex_response.text.strip().encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                        found_bib = "Yes"

        except requests.exceptions.RequestException as e:
            print(f"\nError searching for '{title}': {e}")

        results.append([title, bibtex_text, found_bib])
        time.sleep(0.5) 

    # Write with UTF-8 encoding and handle any special characters safely
    with open("citations.csv", mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "BibTeX", "Found"])
        for row in results:
            safe_row = [str(cell).encode('utf-8', errors='replace').decode('utf-8', errors='replace') for cell in row]
            writer.writerow(safe_row)

    print("The rest has been writed.")

    # Your multiline bibtex string
    bibtex_text = '\n'.join(entry[1] for entry in results if entry[1]!="N/A")

    # Step 1: Split entries
    entries = re.findall(r'@.*?{.*?}\s*(?=@|\Z)', bibtex_text, re.DOTALL)

    # Step 2: Extract current key and author+year for uniqueness
    key_to_entry = {}
    author_year_count = defaultdict(int)
    new_entries = []

    for entry in entries:
        # Extract the original key
        key_match = re.match(r'@.+?{(.+?),', entry)
        if not key_match:
            continue
        original_key = key_match.group(1)

        # Extract author last name and year
        author_match = re.search(r'author\s*=\s*{([^}]+)}', entry)
        year_match = re.search(r'year\s*=\s*{(\d{4})}', entry)

        if not author_match or not year_match:
            continue

        authors = author_match.group(1).split(" and ")
        last_name = authors[0].split(",")[0].strip().replace(" ", "_")
        year = year_match.group(1)

        author_year = f"{last_name}_{year}"
        count = author_year_count[author_year]
        new_key = f"{author_year}" if count == 0 else f"{author_year}_{count}"
        author_year_count[author_year] += 1

        # Replace the old key with new key
        new_entry = re.sub(r'(@.+?{)' + re.escape(original_key), r'\1' + new_key, entry, count=1)
        new_entries.append(new_entry)

    # Step 3: Join all entries back
    cleaned_bibtex = "\n\n".join(new_entries)

    # Save BibTeX entries to file
    with open("citations.bib", "w", encoding="utf-8") as f:
        f.write(cleaned_bibtex)

    print("BibTeX files generated: 'citations.bib'; \nIndicator file generated: 'citations.csv'.")
