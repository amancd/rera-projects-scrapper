# RERA Odisha Projects Scraper

This Python script scrapes the first 6 projects listed on the [RERA Odisha Projects](https://rera.odisha.gov.in/projects/project-list) page.  
It extracts key project details from the project detail pages, including:

- Project Name  
- RERA Registration Number  
- Promoter Company Name (or Proprietor Name if company name unavailable)  
- Promoter Registered Office Address (or Permanent Address if company address unavailable)  
- GST Number  

## Features

- Uses Selenium with ChromeDriver managed by `webdriver-manager`  
- Handles dynamic loading and navigation  
- Outputs results in both JSON and CSV formats  
- Gracefully falls back when some fields are missing  

## Requirements

- Python 3.7+  
- Google Chrome browser installed  

## Installation

1. Clone or download this repository  
2. Install dependencies using pip:

```bash
pip install -r requirements.txt
```

## Run The Script
1. Clone or download this repository
2. Unzip the folder
3. Open command prompt or terminal inside the folder
4. cd rera-projects-scrapper-main
5. python main.py

## Why Selenium?

The RERA Odisha Projects website relies heavily on dynamic content that loads after the initial page load, such as project cards and details that appear only after clicking links or switching tabs. Traditional static scraping tools like requests and BeautifulSoup cannot interact with such dynamic elements or execute JavaScript.

Selenium is a powerful browser automation tool that allows us to:

- Interact with the page like a real user by clicking buttons and navigating tabs  
- Wait explicitly for elements to load or become clickable before scraping  
- Handle JavaScript-rendered content that doesn't appear in the initial HTML source  
- Simulate scrolling and other user actions to trigger lazy-loaded elements  

These capabilities make Selenium the ideal choice for scraping this site reliably and accurately.
