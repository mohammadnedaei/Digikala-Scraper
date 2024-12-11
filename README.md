
# Digikala Product Image Scraper

This project is a Python-based web scraper designed to extract product images from Digikala product pages using Selenium and Requests. It navigates through product listings, opens each product page, and downloads all available images into a local folder.

---

## Features

- **Automated Navigation**: Uses Selenium to navigate through multiple pages of a product listing.
- **Image Extraction**: Downloads product images from individual product pages.
- **Pagination Handling**: Automatically processes multiple pages based on the `page` query parameter.
- **Multi-threaded Downloads**: Utilizes threading for efficient image downloading.
- **Headless Browser**: Operates in headless mode for improved performance and non-intrusive operation.

---

## Prerequisites

Before running the scraper, ensure you have the following installed:

1. **Python** (3.8 or later)
2. **Geckodriver** (Ensure it's in your system's PATH or specify its location in the code.)
3. **Firefox Browser**
4. **Required Python Libraries**:
   - `selenium`
   - `requests`

Install the required libraries using pip:

```bash
pip install selenium requests
```

---

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/mohammadnedaei/Digikala-Scraper.git
cd Digikala-Scraper
```

### 2. Prepare the Environment
Ensure `geckodriver` is installed and its path is correctly set in the script (`driver_path` variable).

### 3. Run the Script
Execute the script by running the following command:

```bash
python scraper.py
```

You will be prompted to enter the base URL of a Digikala product category. For example:
```text
https://www.digikala.com/search/category-notebook-netbook-ultrabook/asus/?page=1
```

### 4. Output
All downloaded product images will be saved in a folder named `product_images` in the script's working directory. Images are organized by product and page number.

---

## Code Overview

### Main Components
1. **`setup_driver()`**: Configures and initializes the Selenium WebDriver for Firefox in headless mode.
2. **`download_image()`**: Downloads images from provided URLs using the `requests` library.
3. **`extract_page_number()` / `update_url_with_page()`**: Helper functions to manage pagination.
4. **`scrape_digikala()`**: Main function to handle the scraping process, navigating through pages and downloading images.

### Workflow
1. Navigate to the specified Digikala product category.
2. Extract product links from the current page.
3. Visit each product page and download all product images.
4. Move to the next page and repeat until no more products are found.

---

## Notes

- **Rate Limiting**: Ensure compliance with Digikala's terms of service by avoiding excessive requests.
- **Error Handling**: The script includes basic error handling but may require enhancements for edge cases.
- **Performance**: For faster execution, the script uses multi-threaded image downloading.

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any feature requests or bugs.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
