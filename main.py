import pandas as pd
from datetime import datetime
from time import sleep
from random import randint
import utils as utils
import config as config
from rich import print


def main():
    """
    Main function to run the scraper on a list of movies and save the results to CSV.

    Reads the input CSV with IMDb URLs, scrapes data for each film, and saves the results to a CSV file.
    It also merges the scraped data with the original ratings data and saves the extended dataset.
    """
    start_time = datetime.now()
    print(f'[blue]***** IMDB Scraper *****[/blue]\n')
    print(f"Start time: {start_time}")

    # Read input CSV with movie URLs
    pages = pd.read_csv(config.ratings_file)[["Const", "Title", "URL"]]

    # Get already scraped entries
    existing_rows = utils.get_existing_rows(config.scraped_data_file)

    # Initialize empty list to store results
    scraped_data = []

    # How many rows to scrap
    startAt = config.startAt
    if stopAt:
        stopAt = config.stopAt
    else:
        stopAt= len(pages)

    for count, row in pages.iloc[startAt:stopAt].iterrows():
        print(f"Processing {count + 1}/{stopAt} ({count+1-startAt}/{stopAt-startAt}): {row['Title']} ({row['Const']}) : {row['URL']}")
        if row["Const"] in existing_rows["Const"].values:
            print("\t [yellow]Entry already scraped. Skipping row.[/yellow]\n")
            continue
        film_data = utils.scrape_film_data(row)
        scraped_data.append(film_data)
        print(f"\t [green]Entry added. {(count+1-startAt)/(stopAt-startAt)*100}% done! [/green]\n")

    if len(scraped_data)== 0:
        print("\n[yellow] No new entries added. Terminating.[/yellow]")
        return

    # Step 1: Append or create new csv
    merged_scraped_data = utils.append_or_create_csv(scraped_data, config.scraped_data_file)

    # Step 2: Merge the new data with the ratings file and save
    utils.merge_and_save(merged_scraped_data, config.ratings_file, config.extended_ratings_file)

    end_time = datetime.now()
    print("====================")
    print("\t [green]FINISHED[/green]")
    print(f"End time: {end_time}")
    print(f"Duration: {end_time - start_time}")
    print(f"Total new rows: {len(scraped_data)}")


if __name__ == "__main__":
    main()