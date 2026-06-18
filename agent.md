# Agent Notes

## Project Goal

This project crawls quote data from Goodreads tag pages and exports the results to CSV files.

## Important Files

- `goodreads_quotes_crawl.py`: Main crawler logic. It opens Goodreads pages, extracts quote and author data, removes duplicates per tag, and writes CSV files.
- `run_goodreads_crawl.bat`: Windows runner. It creates/uses the project `.venv`, installs dependencies, and runs the crawler.
- `run_goodreads_crawl.sh`: macOS/Linux runner. It creates/uses the project `.venv`, installs dependencies, and runs the crawler.
- `requirements.txt`: Python dependencies installed into `.venv`.
- `data/`: CSV output directory. The crawler creates it automatically if it does not exist.

## Editing Guidelines

- Keep the code simple and prefer the Python standard library when practical.
- Do not hard-code absolute paths from a local machine.
- Runner scripts should use the project-local `.venv` and install dependencies from `requirements.txt`.
- All generated CSV files must be saved inside the project-local `data` directory.
- Do not commit generated CSV output. `.gitignore` should continue to ignore CSV files.
- If Goodreads markup changes, check `QUOTE_XPATH` and `AUTHOR_RELATIVE_XPATH`.

## Quick Run

macOS/Linux:

```bash
chmod +x run_goodreads_crawl.sh
./run_goodreads_crawl.sh
```

Windows:

```bat
run_goodreads_crawl.bat
```

## Expected Output

After a successful run:

- The `data` directory exists.
- Each Goodreads tag has its own CSV file, for example `data/life.csv`.
- Each CSV contains the header `id,quote,author`.

## Notes

- CSV files are written with `utf-8-sig` encoding for better Excel compatibility.
- If one page fails, the crawler logs the error and continues with the next page or tag.
