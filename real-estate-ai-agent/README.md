# Real Estate Data Extractor

Automated extraction of public real estate listing data into clean, analytics‑ready JSON.

---

## Project Overview

The Real Estate Data Extractor is a small, configurable Python project that automates pulling public property details from popular listing sites and outputs a standardized JSON record for downstream marketing analytics.

- Sources: Zillow, Realtor.com, Redfin, and similar public listing pages
- Output: structured JSON (snake_case) suitable for warehousing and campaign targeting
- Typical use: generate leads and enrich property metrics for audience segmentation

---

## How It Works

```
1) Load config (.env)
2) Initialize agent (LLM + scraping tools)
3) Fetch listing URL(s)
4) Extract key fields
5) Validate against schema
6) Write JSON output
```

---

## Quickstart

1) Create and activate a virtual environment

   macOS/Linux
   ```sh
   python3.9 -m venv venv
   source venv/bin/activate
   ```

   Windows
   ```sh
   python3.9 -m venv venv
   .\venv\Scripts\activate
   ```

2) Install dependencies

```sh
pip install "crewai-tools[mcp]" crewai mcp python-dotenv pandas
```

3) Configure environment

Copy `env.example` (or `.env.example` if visible) to `.env` and fill in your values.

4) Run a single extraction

```sh
python real_estate_agents.py --url "https://www.zillow.com/homedetails/123-Main-St-City-State-12345/123456_zpid/"
```

---

## Sample JSON Output (annotated)

```jsonc
{
  "address": "123 Main Street, City, State 12345", // Full property address
  "price": "$450,000",                              // As displayed on the page
  "bedrooms": 3,                                     // Integer
  "bathrooms": 2,                                    // Integer (full baths)
  "square_feet": 1850,                               // Living area
  "lot_size": "0.25 acres",                         // As displayed
  "year_built": 1995,                                // Integer
  "property_type": "Single Family Home",             // Standardized string
  "listing_agent": "John Doe, ABC Realty",           // As displayed
  "days_on_market": 45,                               // Integer if available
  "mls_number": "MLS123456",                         // If available
  "description": "Beautiful home with updated kitchen...",
  "image_urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
  "neighborhood": "Downtown Historic District"
}
```

---

## Configuration

All environment variables are consolidated in `.env.example`.

- `API_TOKEN`: API token for your scraping tool stack
- `PROXY_ZONE`: Proxy or browser zone identifier
- `WEB_UNBLOCK_ZONE`: Zone or profile for anti-bot/unblocking
- `LLM_API_KEY`: API key for your preferred LLM provider

The application loads these via `python-dotenv` at startup.

---

## Security and Compliance

- Use responsibly: follow each website’s terms and robots.txt
- Store secrets in `.env`; never commit real keys
- Validate and sanitize data before downstream use

---

## Extensibility

- Add new fields: update the extraction goal/schema and post-processing
- New sites: point the agent at another listing URL pattern and adjust parsing prompts/tools
- Swap LLMs: change the model and key via environment variables

---

## License

MIT
