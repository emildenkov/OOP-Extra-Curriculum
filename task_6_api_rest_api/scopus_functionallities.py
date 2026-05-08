import requests
import json
import os
import re
from datetime import datetime


# ======================================================================
# Configuration
# ======================================================================

SCOPUS_API_KEY = os.environ.get('SCOPUS_API_KEY')
SCOPUS_BASE_URL = "https://api.elsevier.com/content"
HEADERS = {
    "X-ELS-APIKey": SCOPUS_API_KEY,
    "Accept": "application/json",
}
SCIHUB_BASE_URL = "https://sci-hub.se"


# ======================================================================
# TASK 1: Scopus API — 3 services
# ======================================================================

class ScopusClient:

    def __init__(self, api_key=SCOPUS_API_KEY):
        self.api_key = api_key
        self.headers = {
            "X-ELS-APIKey": api_key,
            "Accept": "application/json",
        }
        self.last_results = []

    # ------------------------------------------------------------------
    # Service 1: Search by keyword (title, abstract, keywords)
    # ------------------------------------------------------------------

    def search_by_keyword(self, keyword, count=10):
        print(f"\n{'='*60}")
        print(f"  SERVICE 1: Keyword search for '{keyword}'")
        print(f"{'='*60}")

        url = f"{SCOPUS_BASE_URL}/search/scopus"
        params = {
            "query": f"TITLE-ABS-KEY({keyword})",
            "count": count,
            "sort": "-citedby-count",
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = self._parse_search_results(data)
            self.last_results = results

            print(f"  Total results available: {data.get('search-results', {}).get('opensearch:totalResults', 0)}")
            print(f"  Retrieved: {len(results)}")
            self._print_results(results)

            return results

        except requests.exceptions.HTTPError as e:
            print(f"  HTTP Error: {e}")
            print(f"  Response: {response.text[:200]}")
            return []
        except Exception as e:
            print(f"  Error: {e}")
            return []

    # ------------------------------------------------------------------
    # Service 2: Search by author name
    # ------------------------------------------------------------------

    def search_by_author(self, author_name, count=10):
        print(f"\n{'='*60}")
        print(f"  SERVICE 2: Author search for '{author_name}'")
        print(f"{'='*60}")

        url = f"{SCOPUS_BASE_URL}/search/scopus"
        params = {
            "query": f"AUTHOR-NAME({author_name})",
            "count": count,
            "sort": "-citedby-count",
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = self._parse_search_results(data)
            self.last_results = results

            print(f"  Total results available: {data.get('search-results', {}).get('opensearch:totalResults', 0)}")
            print(f"  Retrieved: {len(results)}")
            self._print_results(results)

            return results

        except requests.exceptions.HTTPError as e:
            print(f"  HTTP Error: {e}")
            return []
        except Exception as e:
            print(f"  Error: {e}")
            return []

    # ------------------------------------------------------------------
    # Service 3: Search by DOI (fetch specific publication metadata)
    # ------------------------------------------------------------------

    def search_by_doi(self, doi):
        print(f"\n{'='*60}")
        print(f"  SERVICE 3: DOI lookup for '{doi}'")
        print(f"{'='*60}")

        url = f"{SCOPUS_BASE_URL}/search/scopus"
        params = {
            "query": f"DOI({doi})",
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = self._parse_search_results(data)
            self.last_results = results

            if results:
                print(f"  Found publication:")
                self._print_results(results)
            else:
                print(f"  No publication found for DOI: {doi}")

            return results

        except requests.exceptions.HTTPError as e:
            print(f"  HTTP Error: {e}")
            return []
        except Exception as e:
            print(f"  Error: {e}")
            return []

    # ------------------------------------------------------------------
    # Parsing and formatting helpers
    # ------------------------------------------------------------------

    def _parse_search_results(self, data):
        results = []
        entries = data.get("search-results", {}).get("entry", [])

        for entry in entries:
            # Skip error entries
            if "error" in entry:
                continue

            pub = {
                "scopus_id": entry.get("dc:identifier", "").replace("SCOPUS_ID:", ""),
                "title": entry.get("dc:title", "N/A"),
                "author": entry.get("dc:creator", "N/A"),
                "journal": entry.get("prism:publicationName", "N/A"),
                "volume": entry.get("prism:volume", ""),
                "issue": entry.get("prism:issueIdentifier", ""),
                "pages": entry.get("prism:pageRange", ""),
                "date": entry.get("prism:coverDate", "N/A"),
                "year": entry.get("prism:coverDate", "")[:4] if entry.get("prism:coverDate") else "",
                "doi": entry.get("prism:doi", ""),
                "cited_by": entry.get("citedby-count", "0"),
                "type": entry.get("subtypeDescription", ""),
                "abstract_url": entry.get("prism:url", ""),
            }
            results.append(pub)

        return results

    def _print_results(self, results):
        for i, pub in enumerate(results, 1):
            print(f"\n  [{i}] {pub['title'][:80]}")
            print(f"      Author:  {pub['author']}")
            print(f"      Journal: {pub['journal']}")
            print(f"      Year:    {pub['year']} | Cited by: {pub['cited_by']}")
            if pub['doi']:
                print(f"      DOI:     {pub['doi']}")

    # ------------------------------------------------------------------
    # BibTeX export
    # ------------------------------------------------------------------

    def to_bibtex(self, results=None, filename=None):
        if results is None:
            results = self.last_results

        if not results:
            print("  No results to export.")
            return ""

        bibtex_entries = []

        for pub in results:
            author_key = pub["author"].split(",")[0].split()[-1] if pub["author"] != "N/A" else "Unknown"
            author_key = re.sub(r'[^a-zA-Z]', '', author_key)
            cite_key = f"{author_key}{pub['year']}"

            # Determine entry type
            entry_type = "article"
            if "conference" in pub["type"].lower() or "proceeding" in pub["type"].lower():
                entry_type = "inproceedings"
            elif "book" in pub["type"].lower():
                entry_type = "book"
            elif "review" in pub["type"].lower():
                entry_type = "article"

            entry = f"@{entry_type}{{{cite_key},\n"
            entry += f'    author = {{{pub["author"]}}},\n'
            entry += f'    title = {{{pub["title"]}}},\n'
            entry += f'    journal = {{{pub["journal"]}}},\n'
            entry += f'    year = {{{pub["year"]}}},\n'

            if pub["volume"]:
                entry += f'    volume = {{{pub["volume"]}}},\n'
            if pub["pages"]:
                entry += f'    pages = {{{pub["pages"]}}},\n'
            if pub["doi"]:
                entry += f'    doi = {{{pub["doi"]}}},\n'

            entry += "}"
            bibtex_entries.append(entry)

        bibtex_str = "\n\n".join(bibtex_entries)

        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(bibtex_str)
            print(f"\n  BibTeX exported to: {filename} ({len(bibtex_entries)} entries)")

        return bibtex_str

    def to_json(self, results=None, filename=None):
        if results is None:
            results = self.last_results

        json_str = json.dumps(results, indent=2, ensure_ascii=False)

        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"  JSON exported to: {filename}")

        return json_str


# ======================================================================
# TASK 2: Sci-Hub download by DOI
# ======================================================================

class SciHubDownloader:

    MIRRORS = [
        "https://sci-hub.se",
        "https://sci-hub.st",
        "https://sci-hub.ru",
    ]

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def download(self, doi, output_dir="."):
        print(f"\n{'='*60}")
        print(f"  SCI-HUB: Downloading DOI '{doi}'")
        print(f"{'='*60}")

        for mirror in self.MIRRORS:
            url = f"{mirror}/{doi}"
            print(f"  Trying mirror: {mirror}...")

            try:
                response = self.session.get(url, timeout=20, allow_redirects=True)

                if response.status_code != 200:
                    print(f"    Status {response.status_code}, trying next mirror...")
                    continue

                pdf_url = self._extract_pdf_url(response.text, mirror)

                if not pdf_url:
                    print(f"    Could not find PDF link on this mirror.")
                    continue

                print(f"  Found PDF: {pdf_url[:80]}...")

                pdf_response = self.session.get(pdf_url, timeout=30)
                if pdf_response.status_code == 200 and len(pdf_response.content) > 1000:
                    safe_doi = doi.replace("/", "_").replace(":", "_")
                    filepath = os.path.join(output_dir, f"{safe_doi}.pdf")
                    with open(filepath, "wb") as f:
                        f.write(pdf_response.content)

                    size_mb = len(pdf_response.content) / (1024 * 1024)
                    print(f"  Downloaded successfully: {filepath} ({size_mb:.2f} MB)")
                    return filepath
                else:
                    print(f"    PDF download failed (status={pdf_response.status_code})")

            except requests.exceptions.ConnectionError:
                print(f"    Connection error — mirror may be blocked or down.")
            except requests.exceptions.Timeout:
                print(f"    Timeout — mirror is too slow.")
            except Exception as e:
                print(f"    Error: {e}")

        print(f"\n  Publication not found on Sci-Hub for DOI: {doi}")
        print(f"  Possible reasons:")
        print(f"    - The DOI may not exist in Sci-Hub's database")
        print(f"    - All mirrors may be blocked by your ISP")
        print(f"    - The publication may be too recent")
        return None

    def _extract_pdf_url(self, html, mirror_base):
        match = re.search(r'<iframe[^>]+src=["\']([^"\']+\.pdf[^"\']*)', html)
        if match:
            url = match.group(1)
            if url.startswith("//"):
                return "https:" + url
            elif url.startswith("/"):
                return mirror_base + url
            return url

        match = re.search(r'<embed[^>]+src=["\']([^"\']+\.pdf[^"\']*)', html)
        if match:
            url = match.group(1)
            if url.startswith("//"):
                return "https:" + url
            elif url.startswith("/"):
                return mirror_base + url
            return url

        match = re.search(r'location\.href\s*=\s*["\']([^"\']+\.pdf[^"\']*)', html)
        if match:
            url = match.group(1)
            if url.startswith("//"):
                return "https:" + url
            return url

        return None


# ======================================================================
# TASK 3: Interesting public APIs — overview
# ======================================================================

def demonstrate_public_apis():
    print(f"\n{'='*60}")
    print(f"  TASK 3: Public APIs with interesting data")
    print(f"{'='*60}")

    apis = [
        {
            "name": "Open Library (books)",
            "url": "https://openlibrary.org/search.json?q=machine+learning&limit=3",
            "description": "Free book metadata from the Internet Archive",
        },
        {
            "name": "NASA APOD (Astronomy Picture of the Day)",
            "url": "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY",
            "description": "NASA's daily astronomy image with explanation",
        },
        {
            "name": "REST Countries",
            "url": "https://restcountries.com/v3.1/name/bulgaria",
            "description": "Country data — population, area, currencies, languages",
        },
    ]

    for api_info in apis:
        print(f"\n  --- {api_info['name']} ---")
        print(f"  Description: {api_info['description']}")
        print(f"  URL: {api_info['url']}")

        try:
            response = requests.get(api_info["url"], timeout=10)
            if response.status_code == 200:
                data = response.json()
                preview = json.dumps(data, indent=2, ensure_ascii=False)
                lines = preview.split("\n")
                for line in lines[:15]:
                    print(f"    {line}")
                if len(lines) > 15:
                    print(f"    ... ({len(lines) - 15} more lines)")
                print(f"  Status: OK ({response.status_code})")
            else:
                print(f"  Status: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
            print(f"  (Run locally to test — this API may be blocked in restricted environments)")


# ======================================================================
# TASK 4: Chat Bot API for academic report
# ======================================================================

def _call_chatbot(prompt, max_tokens=500):
    api_key = os.environ.get("GROQ_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def chatbot_report(topic="quantitative finance and machine learning"):
    """
    Task 4: Uses the Groq API (Llama 3) as a chat bot to generate
    an academic-style report.
    """
    print(f"\n{'='*60}")
    print(f"  TASK 4: Chat Bot API — Academic Report (Groq Llama)")
    print(f"  Topic: '{topic}'")
    print(f"{'='*60}")

    report = {
        "title": f"Academic Report: {topic.title()}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sections": []
    }

    print(f"\n  Step 1: Requesting outline from Groq API...")

    outline_prompt = (
        f"You are an academic assistant. Give me a concise outline for a report on "
        f"'{topic}'. Return ONLY a numbered list of 5 section titles, nothing else."
    )

    try:
        outline_raw = _call_chatbot(outline_prompt, max_tokens=300)
        print(f"  Bot response:\n")
        print(f"    {outline_raw.strip()}")

        outline = []
        for line in outline_raw.strip().split("\n"):
            line = line.strip()
            cleaned = re.sub(r"^\d+[\.\)]\s*", "", line).strip()
            if cleaned:
                outline.append(cleaned)

        if not outline:
            outline = ["Introduction", "Methods", "Results", "Discussion", "Conclusion"]

    except Exception as e:
        print(f"  API call failed: {e}")
        print(f"  Using default outline.")
        outline = [
            "Introduction and Historical Context",
            "Key Mathematical Foundations",
            "Machine Learning Models in Finance",
            "Risk Management and Portfolio Optimization",
            "Conclusion and Future Directions",
        ]

    print(f"\n  Parsed outline ({len(outline)} sections):")
    for i, section in enumerate(outline, 1):
        print(f"    {i}. {section}")

    print(f"\n  Step 2: Expanding each section in academic style...\n")

    for i, section_title in enumerate(outline, 1):
        expand_prompt = (
            f"Write one detailed academic paragraph (100-150 words) about "
            f"'{section_title}' in the context of {topic}. "
            f"Use formal academic writing style with precise terminology."
        )

        print(f"  [{i}/{len(outline)}] Generating: {section_title}...")

        try:
            content = _call_chatbot(expand_prompt, max_tokens=400)
            content = content.strip()
            print(f"    -> {len(content)} chars generated")
        except Exception as e:
            content = f"(Could not generate content: {e})"
            print(f"    -> Error: {e}")

        report["sections"].append({
            "title": section_title,
            "content": content,
        })

    print(f"\n{'='*60}")
    print(f"  GENERATED REPORT")
    print(f"{'='*60}")
    print(f"  Title: {report['title']}")
    print(f"  Date:  {report['date']}")

    for section in report["sections"]:
        print(f"\n  --- {section['title']} ---")
        words = section["content"].split()
        line = "  "
        for word in words:
            if len(line) + len(word) + 1 > 80:
                print(line)
                line = "  " + word
            else:
                line += " " + word if line.strip() else "  " + word
        if line.strip():
            print(line)

    report_json = json.dumps(report, indent=2, ensure_ascii=False)
    report_filename = "academic_report.json"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report_json)
    print(f"\n  Full report saved to: {report_filename}")

    return report


# ======================================================================
# Main
# ======================================================================

def main():
    print("=" * 60)
    print("  TASK 6: API & REST APIs")
    print("=" * 60)

    client = ScopusClient()

    results_kw = client.search_by_keyword("machine learning finance", count=5)

    results_author = client.search_by_author("Fama, E.", count=5)

    results_doi = client.search_by_doi("10.1016/j.jfineco.2010.08.016")

    all_results = results_kw + results_author + results_doi

    if all_results:
        print(f"\n{'='*60}")
        print(f"  BIBTEX EXPORT")
        print(f"{'='*60}")

        bibtex = client.to_bibtex(all_results, filename="scopus_results.bib")
        print(f"\n  Preview (first 500 chars):")
        print(f"  {bibtex[:500]}")

        client.to_json(all_results, filename="scopus_results.json")
    else:
        print("\n  No Scopus results to export (API may not be accessible from this network).")
        print("  Run this script from your university network for full functionality.")

    scihub = SciHubDownloader()
    scihub.download("10.1016/0304-405X(93)90023-5")

    demonstrate_public_apis()

    chatbot_report("quantitative finance and machine learning")


if __name__ == "__main__":
    main()