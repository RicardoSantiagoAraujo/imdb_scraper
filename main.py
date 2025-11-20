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
    print(f"[blue]***** IMDB Scraper *****[/blue]\n")
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
        stopAt = len(pages)

    for count, row in pages.iloc[startAt:stopAt].iterrows():
        print(
            f"Processing {count + 1}/{stopAt} ({count+1-startAt}/{stopAt-startAt}): {row['Title']} ({row['Const']}) : {row['URL']}"
        )
        if row["Const"] in existing_rows["Const"].values:
            print("\t [yellow]Entry already scraped. Skipping row.[/yellow]\n")
            continue
        film_data = utils.scrape_film_data(row)
        scraped_data.append(film_data)

        # Progress display
        elapsed_time = datetime.now() - start_time
        progress_percent = round(((count + 1 - startAt) / (stopAt - startAt) * 100), 2)
        print(
            f"\t [green]Entry added. {progress_percent}% done!\
            Elapsed time: {elapsed_time}.\
            Remaining time estimation:  {elapsed_time*(100 - progress_percent)/100} [/green]\n"
        )
        # SAVE PROGRESS EVERY N ROWS
        if (count + 1) % config.save_every_n_rows == 0:  # Save progress every N rows
            if len(scraped_data) > 0:
                print(f"[cyan]Saving progress ({config.save_every_n_rows})...[/cyan]")
                utils.append_or_create_csv(scraped_data, config.scraped_data_file) 
                existing_rows = utils.get_existing_rows(config.scraped_data_file) # Update existing rows
                print("[cyan]Progress saved.[/cyan]\n")

    if len(scraped_data) == 0:
        print("\n[yellow] No new entries added. Terminating.[/yellow]")
        return

    # Step 1: Save remaining scraped data to CSV
    print("\n[cyan]Saving final scraped data...[/cyan]")
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
