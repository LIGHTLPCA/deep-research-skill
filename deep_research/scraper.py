"""
Web Scraper & Content Cleaner Module.
Fetches web pages, cleans HTML clutter, and extracts dense, LLM-ready markdown summaries.
"""

import re
import urllib.parse
from dataclasses import dataclass
from typing import List, Optional, Dict
import requests
from bs4 import BeautifulSoup


@dataclass
class ScrapedPage:
    url: str
    title: str
    content_markdown: str
    status_code: int
    dimension: str
    word_count: int
    snippets: List[str]


class WebScraper:
    """
    Robust web fetcher and HTML-to-Markdown cleaner optimized for zero-noise AI intake.
    """

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 LIGHT-LPCA/1.0"

    def __init__(self, timeout: int = 8, max_content_words: int = 1500):
        self.timeout = timeout
        self.max_content_words = max_content_words
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    def search_duckduckgo_lite(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Executes a web search. We use Wikipedia Open API here for guaranteed
        bot-unblocked factual testing, bypassing the brittle DDG scraper.
        """
        results = []
        try:
            # Safe, unblocked Wikipedia API
            api_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
            resp = self.session.get(api_url, timeout=self.timeout)
            
            if resp.status_code == 200:
                data = resp.json()
                search_hits = data.get("query", {}).get("search", [])
                
                for i in range(min(len(search_hits), max_results)):
                    hit = search_hits[i]
                    page_id = hit["pageid"]
                    title = hit["title"]
                    snippet = hit["snippet"]
                    # Clean HTML tags from Wikipedia snippet
                    snippet = re.sub(r'<[^>]+>', '', snippet)
                    actual_url = f"https://en.wikipedia.org/?curid={page_id}"
                    
                    results.append({
                        "title": title,
                        "url": actual_url,
                        "snippet": snippet
                    })
        except Exception as e:
            pass

        return results

    def clean_html_to_markdown(self, html_text: str) -> tuple[str, str]:
        """Strips scripts, styles, navs, and converts main article content to clean markdown text."""
        soup = BeautifulSoup(html_text, "html.parser")

        # Extract title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled Document"

        # Remove irrelevant tags
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]):
            element.decompose()

        # Extract text from paragraph & heading elements
        text_blocks = []
        for elem in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            txt = elem.get_text(" ", strip=True)
            if len(txt) > 20:  # Filter out short menu buttons
                if elem.name.startswith("h"):
                    text_blocks.append(f"\n### {txt}\n")
                elif elem.name == "li":
                    text_blocks.append(f"- {txt}")
                else:
                    text_blocks.append(txt)

        raw_markdown = "\n\n".join(text_blocks)
        cleaned_markdown = re.sub(r"\n{3,}", "\n\n", raw_markdown).strip()

        return title, cleaned_markdown

    def fetch_page(self, url: str, dimension: str = "general") -> ScrapedPage:
        """Fetches a single page and converts content into ScrapedPage object."""
        try:
            resp = self.session.get(url, timeout=self.timeout)
            status_code = resp.status_code

            if status_code == 200:
                title, markdown = self.clean_html_to_markdown(resp.text)
            else:
                title = f"HTTP Error {status_code}"
                markdown = f"Failed to retrieve content from {url}. Status code: {status_code}"

        except Exception as err:
            status_code = 500
            title = "Fetch Connection Exception"
            markdown = f"Connection error while attempting to reach {url}: {str(err)}"

        words = markdown.split()
        truncated_markdown = " ".join(words[: self.max_content_words])
        word_count = len(words)

        # Generate key sentences as snippets
        sentences = [s.strip() for s in re.split(r"[.\n]", truncated_markdown) if len(s.strip()) > 30]
        snippets = sentences[:4]

        return ScrapedPage(
            url=url,
            title=title,
            content_markdown=truncated_markdown,
            status_code=status_code,
            dimension=dimension,
            word_count=word_count,
            snippets=snippets,
        )
