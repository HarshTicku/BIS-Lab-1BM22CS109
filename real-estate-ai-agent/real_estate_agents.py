"""Real Estate Data Extractor

This module provides a minimal, dependency-light agent that fetches a real estate
listing page and extracts a standardized set of fields. It is designed to be
customized and extended for additional data sources and fields.

Key steps:
1) Load configuration from environment variables
2) Initialize a simple agent orchestrator
3) Fetch and parse a listing URL
4) Validate the extracted data against a schema
5) Return JSON suitable for analytics pipelines

Environment variables (see `.env.example`):
- API_TOKEN: Optional token for your scraping stack
- PROXY_ZONE: Optional proxy or browser zone identifier
- WEB_UNBLOCK_ZONE: Optional anti-bot/unblock profile
- LLM_API_KEY: Optional key if you later integrate an LLM
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup  # type: ignore
from dotenv import load_dotenv


load_dotenv()  # Loads .env at process start


@dataclass
class PropertyRecord:
    """Schema for extracted property data.

    Extend this schema by adding new fields and updating `from_html` accordingly.
    """

    address: Optional[str] = None
    price: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[int] = None
    lot_size: Optional[str] = None
    year_built: Optional[int] = None
    property_type: Optional[str] = None
    listing_agent: Optional[str] = None
    days_on_market: Optional[int] = None
    mls_number: Optional[str] = None
    description: Optional[str] = None
    image_urls: List[str] = field(default_factory=list)
    neighborhood: Optional[str] = None

    @staticmethod
    def from_html(html_text: str) -> "PropertyRecord":
        """Very lightweight HTML parsing as a starting point.

        This function intentionally uses conservative parsing so the project
        runs out-of-the-box without specialized tools. For production-grade
        extraction, integrate site-specific logic or an LLM-assisted parser.
        """
        soup = BeautifulSoup(html_text, "html.parser")

        # Minimal heuristics as placeholders. Update per website structure.
        address = None
        address_el = soup.find(attrs={"data-testid": "address"}) or soup.find("address")
        if address_el:
            address = address_el.get_text(strip=True) or None

        price = None
        price_el = soup.find(attrs={"data-testid": "price"}) or soup.find(
            string=lambda s: isinstance(s, str) and "$" in s
        )
        if price_el:
            price = price_el.get_text(strip=True) if hasattr(price_el, "get_text") else str(price_el).strip()

        description = None
        desc_el = soup.find(attrs={"data-testid": "home-description-text"}) or soup.find("meta", attrs={"name": "description"})
        if desc_el:
            description = (
                desc_el.get("content").strip() if desc_el.name == "meta" else desc_el.get_text(strip=True)
            ) or None

        # Placeholders for fields that require site-specific parsing
        return PropertyRecord(
            address=address,
            price=price,
            description=description,
            image_urls=[img.get("src") for img in soup.find_all("img") if img.get("src")][:5],
        )


class SimpleExtractionAgent:
    """A minimal orchestrator for fetching, parsing, and validating data."""

    def __init__(self, api_token: Optional[str] = None, proxy_zone: Optional[str] = None, web_unblock_zone: Optional[str] = None,
                 llm_api_key: Optional[str] = None) -> None:
        self.api_token = api_token
        self.proxy_zone = proxy_zone
        self.web_unblock_zone = web_unblock_zone
        self.llm_api_key = llm_api_key

    def fetch_listing_html(self, listing_url: str) -> str:
        """Fetches raw HTML. Replace with your preferred HTTP client or scraper."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
            )
        }
        response = requests.get(listing_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text

    @staticmethod
    def validate_schema(record: PropertyRecord) -> PropertyRecord:
        """Basic validation: ensure keys exist; coerce types if needed.

        For stronger guarantees, integrate `pydantic` or jsonschema.
        """
        # Example: type coercion placeholders
        return record

    def extract(self, listing_url: str) -> PropertyRecord:
        """End-to-end: fetch, parse, validate."""
        html_text = self.fetch_listing_html(listing_url)
        parsed = PropertyRecord.from_html(html_text)
        validated = self.validate_schema(parsed)
        return validated


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Real Estate Data Extractor")
    parser.add_argument("--url", required=True, help="Listing URL to extract")
    parser.add_argument("--output", default="output.json", help="Path to write JSON output")
    return parser


def main() -> int:
    """CLI entry point for single-URL extraction."""
    args = _build_arg_parser().parse_args()

    agent = SimpleExtractionAgent(
        api_token=os.getenv("API_TOKEN"),
        proxy_zone=os.getenv("PROXY_ZONE"),
        web_unblock_zone=os.getenv("WEB_UNBLOCK_ZONE"),
        llm_api_key=os.getenv("LLM_API_KEY"),
    )

    record = agent.extract(args.url)
    payload = {
        "metadata": {
            "extracted_at": datetime.utcnow().isoformat() + "Z",
            "source_url": args.url,
            "schema_version": "1.0",
        },
        "data": asdict(record),
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Next Steps
# - Add new data fields: extend PropertyRecord and update from_html parsing.
# - Integrate additional websites: add site-specific parsers and dispatch by domain.
# - Swap in a different LLM: wire your provider using LLM_API_KEY and implement
#   an LLM-assisted parser that converts raw HTML to structured fields.