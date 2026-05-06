import multiprocessing
import time
import os

import requests
from bs4 import BeautifulSoup


# ========================================================================
# Configuration
# ========================================================================

BASE_URL = "https://libgen.is/search.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
TIMEOUT = 15  # seconds per request


# ========================================================================
# HTML parsing — extracts book rows from libgen search results
# ========================================================================

def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []


    table = soup.find("table", {"class": "c"})
    if not table:

        tables = soup.find_all("table")
        table = tables[2] if len(tables) > 2 else None

    if not table:
        return results

    rows = table.find_all("tr")

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 9:
            continue

        book = {
            "id": cols[0].get_text(strip=True),
            "author": cols[1].get_text(strip=True)[:60],
            "title": cols[2].get_text(strip=True)[:80],
            "publisher": cols[3].get_text(strip=True)[:40],
            "year": cols[4].get_text(strip=True),
            "pages": cols[5].get_text(strip=True),
            "language": cols[6].get_text(strip=True),
            "size": cols[7].get_text(strip=True),
            "extension": cols[8].get_text(strip=True),
        }
        results.append(book)

    return results


# ========================================================================
# Search functions — each one runs as a separate process
# ========================================================================

def search_libgen(search_type, query, result_queue):
    process_name = multiprocessing.current_process().name
    pid = os.getpid()
    print(f"[{process_name}] PID={pid} | Starting '{search_type}' search for: '{query}'")

    start_time = time.time()

    params = {
        "req": query,
        "column": search_type,
        "res": 10,
        "view": "simple",
        "phrase": 1,
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        books = parse_search_results(response.text)
        elapsed = time.time() - start_time

        result_queue.put({
            "process": process_name,
            "pid": pid,
            "search_type": search_type,
            "query": query,
            "status": "success",
            "results_count": len(books),
            "books": books[:5],
            "elapsed": round(elapsed, 3),
            "url": response.url,
        })
        print(f"[{process_name}] Done in {elapsed:.3f}s — {len(books)} results found")

    except requests.exceptions.ConnectionError as e:
        elapsed = time.time() - start_time
        result_queue.put({
            "process": process_name,
            "pid": pid,
            "search_type": search_type,
            "query": query,
            "status": "connection_error",
            "error": f"Cannot reach libgen.is — site may be blocked or down: {e}",
            "elapsed": round(elapsed, 3),
        })
        print(f"[{process_name}] Connection error: {e}")

    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        result_queue.put({
            "process": process_name,
            "pid": pid,
            "search_type": search_type,
            "query": query,
            "status": "timeout",
            "error": f"Request timed out after {TIMEOUT}s",
            "elapsed": round(elapsed, 3),
        })
        print(f"[{process_name}] Timeout after {TIMEOUT}s")

    except requests.exceptions.HTTPError as e:
        elapsed = time.time() - start_time
        result_queue.put({
            "process": process_name,
            "pid": pid,
            "search_type": search_type,
            "query": query,
            "status": "http_error",
            "error": str(e),
            "elapsed": round(elapsed, 3),
        })
        print(f"[{process_name}] HTTP error: {e}")

    except Exception as e:
        elapsed = time.time() - start_time
        result_queue.put({
            "process": process_name,
            "pid": pid,
            "search_type": search_type,
            "query": query,
            "status": "error",
            "error": str(e),
            "elapsed": round(elapsed, 3),
        })
        print(f"[{process_name}] Unexpected error: {e}")


# ========================================================================
# Wrapper functions for the 4 different search types
# ========================================================================

def search_by_title(query, result_queue):
    search_libgen("title", query, result_queue)


def search_by_author(query, result_queue):
    search_libgen("author", query, result_queue)


def search_by_isbn(query, result_queue):
    search_libgen("isbn", query, result_queue)


def search_by_publisher(query, result_queue):
    search_libgen("publisher", query, result_queue)


# ========================================================================
# Pretty printer for results
# ========================================================================

def print_results(all_results, overall_elapsed):
    print(f"\n{'=' * 70}")
    print("RESULTS SUMMARY")
    print(f"{'=' * 70}")

    for r in all_results:
        print(f"\n  [{r['process']}] (PID {r['pid']})")
        print(f"  Search type : {r['search_type']}")
        print(f"  Query       : '{r['query']}'")
        print(f"  Status      : {r['status']}")
        print(f"  Time        : {r['elapsed']}s")

        if r["status"] == "success":
            print(f"  URL         : {r.get('url', 'N/A')}")
            print(f"  Results     : {r['results_count']}")
            if r.get("books"):
                print(f"  Top results :")
                for i, book in enumerate(r["books"], 1):
                    print(f"    {i}. [{book['year']}] {book['author'][:30]} — "
                          f"{book['title'][:50]} ({book['extension']}, {book['size']})")
        else:
            print(f"  Error       : {r.get('error', 'unknown')}")

    individual_sum = sum(r["elapsed"] for r in all_results)
    print(f"\n{'=' * 70}")
    print("TIMING ANALYSIS")
    print(f"{'=' * 70}")
    print(f"  Wall-clock time (parallel) : {overall_elapsed:.3f}s")
    print(f"  Sum of individual times    : {individual_sum:.3f}s")
    if overall_elapsed > 0:
        speedup = individual_sum / overall_elapsed
        print(f"  Parallel speedup           : {speedup:.2f}x")
    print(f"  Number of processes        : {len(all_results)}")


# ========================================================================
# Main
# ========================================================================

def main():
    print("=" * 70)
    print("PARALLEL BOOK SEARCH — 4 processes via multiprocessing")
    print(f"Parent process PID: {os.getpid()}")
    print("=" * 70)

    result_queue = multiprocessing.Queue()

    tasks = [
        ("Process-1-Title",     search_by_title,     "Python Programming"),
        ("Process-2-Author",    search_by_author,    "Knuth"),
        ("Process-3-ISBN",      search_by_isbn,      "978-0134685991"),
        ("Process-4-Publisher", search_by_publisher,  "O'Reilly"),
    ]

    processes = []
    for name, func, query in tasks:
        p = multiprocessing.Process(
            target=func,
            args=(query, result_queue),
            name=name,
        )
        processes.append(p)

    overall_start = time.time()
    print(f"\nLaunching {len(processes)} processes...\n")

    for p in processes:
        p.start()

    for p in processes:
        p.join(timeout=TIMEOUT + 5)

    overall_elapsed = time.time() - overall_start

    all_results = []
    while not result_queue.empty():
        try:
            all_results.append(result_queue.get_nowait())
        except Exception:
            break

    print_results(all_results, overall_elapsed)

    print(f"\n{'=' * 70}")
    print("PROCESS INFO")
    print(f"{'=' * 70}")
    for p in processes:
        status = "OK" if p.exitcode == 0 else f"exit code {p.exitcode}"
        alive = "running" if p.is_alive() else "finished"
        print(f"  {p.name}: PID={p.pid}, status={status}, {alive}")


if __name__ == "__main__":
    main()