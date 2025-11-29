import sys
import os
import argparse # Required for parsing terminal arguments

# Add core folder to path
sys.path.append(os.getcwd())

try:
    from core.crawler import Crawler
    from core.scanner import Scanner
    from core.report import generate_html_report
    from core.session import get_session_with_retries
except ImportError as e:
    print(f"[!!!] Critical File Missing: {e}")
    sys.exit()

def main():
    # 1. Get arguments from terminal
    parser = argparse.ArgumentParser(description="Advanced Web Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://site.com)")
    parser.add_argument("-t", "--threads", type=int, default=3, help="Scan speed/thread count (Default: 3)")
    parser.add_argument("-p", "--proxy", help="Proxy address (e.g., http://127.0.0.1:8080)")
    
    args = parser.parse_args()
    target_url = args.url
    
    # Banner
    print("-" * 50)
    print(f"🔥 VULN-HUNTER STARTING")
    print(f"[*] Target: {target_url}")
    print(f"[*] Speed: {args.threads} Threads")
    print("-" * 50)

    # Proxy Configuration
    proxies = None
    if args.proxy:
        proxies = {"http": args.proxy, "https": args.proxy}
        print(f"[*] Proxy Active: {args.proxy}")

    # Start Session
    session = get_session_with_retries()
    
    # 2. Start Crawler
    print("\n[1/3] Mapping Sitemap (Crawler)...")
    try:
        crawler = Crawler(target_url, max_threads=args.threads, session=session, proxies=proxies)
        found_urls = crawler.run()
    except Exception as e:
        print(f"[!!!] Connection Error: {e}")
        return

    # If no links found, scan at least the main page
    if not found_urls:
        print("[!] Crawler found no links. Scanning main page only.")
        found_urls = [target_url]
    else:
        print(f"[OK] Total {len(found_urls)} pages discovered.")

    # 3. Start Scanner
    print("\n[2/3] Starting Security Scan (SQLi & XSS)...")
    scanner = Scanner(session=session, proxies=proxies)
    
    # Note: You can make thread count dynamic in scanner.py, but keeping it standard for now.
    vulnerabilities = scanner.scan(found_urls)

    # 4. Reporting
    print(f"\n[3/3] Scan Completed. {len(vulnerabilities)} vulnerabilities found.")

    if len(vulnerabilities) > 0:
        generate_html_report(vulnerabilities)
        print(f"\n[✔] REPORT READY: {os.path.join(os.getcwd(), 'Pentest_Report.html')}")
    else:
        print("\n[?] No vulnerabilities found or target is secure.")

if __name__ == "__main__":
    main()