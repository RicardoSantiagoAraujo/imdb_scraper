# IMDb Scraper

## Overview

The `main.py` script is the entry point for the IMDb Scraper. It processes a list of movies, scrapes data for each film from IMDb, and saves the results to a CSV file. The script also merges the scraped data with an existing ratings dataset to create an extended dataset.

## Features

- Reads a list of movies from a CSV file.
- Scrapes IMDb data for each movie.
- Saves progress periodically to avoid data loss.
- Merges scraped data with existing ratings data.

## Prerequisites

- Python 3.8 or higher
- Required Python packages listed in requirements.txt file

## Configuration

Update the following settings in `config.py`:
- `ratings_file`: Path to the input CSV file containing movie URLs.
- `scraped_data_file`: Path to the file where scraped data will be saved.
- `extended_ratings_file`: Path to the file where the merged dataset will be saved.
- `startAt`: Row index to start scraping from.
- `stopAt`: Row index to stop scraping at (optional).
- `save_every_n_rows`: Number of rows to process before saving progress.

## Usage

1. Ensure the configuration in `config.py` is correct.
2. Run the script:
   ```bash
   python main.py
   ```
3. Monitor the console output for progress and any errors.

If you wish to re-scrape specific (a) film(s), you them remove it/them from **scraped_data.csv** and re-run script.

## Example

```bash
python main.py
```

The script will scrape IMDb data for the movies listed in the input CSV file and save the results.

## Notes

- The script uses the `rich` library for enhanced console output.
- Progress is saved periodically to avoid data loss in case of interruptions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
