"""Capture a live cricket score from Cricbuzz with Playwright, Week 1 Day 3.

Run headed first so you can watch it, then headless:
    python cricbuzz_score.py
    python cricbuzz_score.py --headless

What it does: opens cricbuzz.com, waits for the first match card to appear
(no fixed sleep), prints the card text, saves score.png and a short video of
the browser run. If there is no match card, or the site blocks the browser,
it says so and exits with code 1 instead of crashing.
"""

import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

URL = "https://www.cricbuzz.com/"
# Found by inspecting the page: each match card at the top of the home page is
# a link to /live-cricket-scores/<id>/... that contains a column of team rows.
CARD = 'a[href^="/live-cricket-scores/"]:has(div.flex-col.gap-3)'
WAIT_MS = 20000  # upper limit; Playwright continues as soon as the card shows

HERE = Path(__file__).parent


def read_score(headless):
    """Open Cricbuzz, return the first score card text, or None."""
    # Remove an old picture first, so a failed run cannot leave a stale one.
    (HERE / "score.png").unlink(missing_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1366, "height": 900},
            record_video_dir=str(HERE / "video"),
            record_video_size={"width": 1366, "height": 900},
        )
        page = context.new_page()
        try:
            page.goto(URL, wait_until="domcontentloaded")
            try:
                page.wait_for_selector(CARD, timeout=WAIT_MS)
            except PlaywrightTimeout:
                if "denied" in page.title().lower():
                    print("Cricbuzz refused this browser (Access Denied).")
                else:
                    print("No live match card appeared within "
                          f"{WAIT_MS // 1000} seconds.")
                return None
            card = page.locator(CARD).first
            text = " | ".join(
                line.strip() for line in card.inner_text().splitlines()
                if line.strip()
            )
            card.screenshot(path=str(HERE / "score.png"))
            return text
        finally:
            context.close()  # saves the video
            browser.close()


def main():
    unknown = [a for a in sys.argv[1:] if a != "--headless"]
    if unknown:
        print(f"Unknown option: {' '.join(unknown)}")
        print("Usage: python cricbuzz_score.py [--headless]")
        sys.exit(2)
    headless = "--headless" in sys.argv
    score = read_score(headless)
    if score is None:
        sys.exit(1)
    print(score)
    print()
    print("saved score.png")


if __name__ == "__main__":
    main()
