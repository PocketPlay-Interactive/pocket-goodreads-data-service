import csv
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from cloakbrowser import launch


URLS = [
    "https://www.goodreads.com/quotes/tag/history?page=1",
]

# URLS = [
#     "https://www.goodreads.com/quotes/tag/life?page=1",
#     "https://www.goodreads.com/quotes/tag/success?page=1",
#     "https://www.goodreads.com/quotes/tag/love?page=1",
#     "https://www.goodreads.com/quotes/tag/humor?page=1",
#     "https://www.goodreads.com/quotes/tag/relationships?page=1",    
#     "https://www.goodreads.com/quotes/tag/motivational-quotes?page=1",
#     "https://www.goodreads.com/quotes/tag/wisdom?page=1",
#     "https://www.goodreads.com/quotes/tag/history?page=1",
#     "https://www.goodreads.com/quotes/tag/science?page=1",
#     "https://www.goodreads.com/quotes/tag/hope?page=1",
#     "https://www.goodreads.com/quotes/tag/philosophy?page=1",
# ]

START_PAGE = 1
END_PAGE = 1
QUOTE_XPATH = "//*[contains(@class,'mediumText')]//*[contains(@class,'quoteText')]"
DATA_DIR = Path(__file__).resolve().parent / "data"


def build_url(url, page_number):
    """Replace or append the page query parameter."""
    parsed = urlparse(url)
    query_items = parse_qsl(parsed.query, keep_blank_values=True)

    updated = False
    new_query_items = []
    for key, value in query_items:
        if key == "page":
            new_query_items.append((key, str(page_number)))
            updated = True
        else:
            new_query_items.append((key, value))

    if not updated:
        new_query_items.append(("page", str(page_number)))

    return urlunparse(parsed._replace(query=urlencode(new_query_items)))


def build_output_filename(url):
    """Create a CSV filename from the Goodreads tag in the URL."""
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]

    if "tag" in path_parts:
        tag_index = path_parts.index("tag")
        if tag_index + 1 < len(path_parts):
            tag = path_parts[tag_index + 1]
        else:
            tag = "quotes"
    else:
        tag = Path(parsed.path).stem or "quotes"

    safe_tag = re.sub(r"[^a-zA-Z0-9_-]+", "_", tag).strip("_")
    return f"{safe_tag or 'quotes'}.csv"


def normalize_text(text):
    """Trim text and collapse extra whitespace/newlines."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def remove_quote_marks(text):
    """Remove quote mark characters from extracted text."""
    return text.replace('"', "").replace("“", "").replace("”", "")


def parse_quote_text(raw_text):
    """Parse raw Goodreads quote text into quote, author, and book fields."""
    cleaned_text = remove_quote_marks(normalize_text(raw_text))
    quote = cleaned_text
    author_and_book = ""

    separator_match = re.search(r"\s+[―-]\s+", cleaned_text)
    if separator_match:
        quote = cleaned_text[: separator_match.start()]
        author_and_book = cleaned_text[separator_match.end() :]
    elif "-" in cleaned_text:
        quote, author_and_book = cleaned_text.split("-", 1)

    quote = quote.strip()
    author_and_book = author_and_book.strip()

    author = author_and_book
    book = ""
    if "," in author_and_book:
        author, book = author_and_book.split(",", 1)

    return {
        "quote": quote.strip(),
        "author": author.strip(),
        "book": book.strip(),
    }


def get_text(element):
    """Read visible text using common Playwright-like element APIs."""
    for method_name in ("inner_text", "text_content"):
        method = getattr(element, method_name, None)
        if callable(method):
            value = method()
            if value:
                return value
    return ""


def find_all_by_xpath(context, xpath):
    """Find elements using CloakBrowser/Playwright-like XPath APIs."""
    locator = getattr(context, "locator", None)
    if callable(locator):
        result = locator(f"xpath={xpath}")
        all_method = getattr(result, "all", None)
        if callable(all_method):
            return all_method()

        count_method = getattr(result, "count", None)
        nth_method = getattr(result, "nth", None)
        if callable(count_method) and callable(nth_method):
            return [nth_method(index) for index in range(count_method())]

    xpath_method = getattr(context, "xpath", None)
    if callable(xpath_method):
        result = xpath_method(xpath)
        return list(result or [])

    query_selector_all = getattr(context, "query_selector_all", None)
    if callable(query_selector_all):
        return list(query_selector_all(f"xpath={xpath}") or [])

    raise RuntimeError("CloakBrowser does not expose locator(), xpath(), or query_selector_all().")


def wait_for_page_load(page):
    """Wait until the document is fully loaded using native browser APIs."""
    wait_for_load_state = getattr(page, "wait_for_load_state", None)
    if callable(wait_for_load_state):
        try:
            wait_for_load_state("load")
            wait_for_load_state("networkidle")
            return
        except Exception:
            wait_for_load_state("load")
            return

    wait_for_selector = getattr(page, "wait_for_selector", None)
    if callable(wait_for_selector):
        wait_for_selector(f"xpath={QUOTE_XPATH}", timeout=30000)


def extract_quotes(page):
    """Extract and parse quote text directly from the Goodreads quote elements."""
    quote_elements = find_all_by_xpath(page, QUOTE_XPATH)
    quotes = []

    for quote_element in quote_elements:
        parsed_quote = parse_quote_text(get_text(quote_element))

        if parsed_quote["quote"]:
            quotes.append(parsed_quote)

    return quotes


def save_csv(rows, filename):
    """Save quote rows to CSV with id, quote, author, and book columns."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / filename

    with open(output_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "quote", "author", "book"])
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def main():
    browser = None

    try:
        browser = launch()
        page = browser.new_page()

        for base_url in URLS:
            rows = []
            seen_quotes = set()
            next_id = 1
            output_file = build_output_filename(base_url)

            print(f"[INFO] Crawling: {base_url}")

            try:
                for page_number in range(START_PAGE, END_PAGE + 1):
                    crawl_url = build_url(base_url, page_number)
                    print(f"[INFO] Page: {page_number}")

                    try:
                        page.goto(crawl_url)
                        wait_for_page_load(page)

                        extracted_quotes = extract_quotes(page)
                        print(f"[INFO] Found: {len(extracted_quotes)} quotes")

                        for item in extracted_quotes:
                            quote = item["quote"]
                            author = item["author"]
                            book = item["book"]

                            if not quote or quote in seen_quotes:
                                continue

                            seen_quotes.add(quote)
                            rows.append(
                                {
                                    "id": next_id,
                                    "quote": quote,
                                    "author": author,
                                    "book": book,
                                }
                            )
                            next_id += 1

                        print(f"[INFO] Total: {len(rows)} quotes")
                    except Exception as page_error:
                        print(f"[ERROR] Page failed: {crawl_url} | {page_error}")
                        continue
            except Exception as url_error:
                print(f"[ERROR] URL failed: {base_url} | {url_error}")
                continue

            saved_path = save_csv(rows, output_file)
            print(f"[INFO] Saved: {saved_path}")
    finally:
        if browser is not None:
            browser.close()


if __name__ == "__main__":
    main()
