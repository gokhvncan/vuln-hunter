from bs4 import BeautifulSoup
import time
import concurrent.futures
from core.payloads import SQLI_PAYLOADS, XSS_PAYLOADS, ERROR_KEYWORDS

class Scanner:
    def __init__(self, session=None, proxies=None):
        self.session = session
        if proxies and self.session:
            self.session.proxies.update(proxies)
        self.vulnerabilities = []

    def extract_forms(self, url):
        try:
            # Rate limiting: Sleep 0.5s to avoid overwhelming the server
            time.sleep(0.5) 
            resp = self.session.get(url, timeout=10) # Increased timeout
            
            if 'text' not in resp.headers.get('Content-Type', ''):
                return []
            
            soup = BeautifulSoup(resp.content, "html.parser")
            forms = soup.find_all("form")
            
            # DEBUG: Log found forms per page
            if len(forms) > 0:
                print(f"\n[+] Form Found: {url} ({len(forms)} forms)")
            
            return forms
        except Exception as e:
            # Log errors instead of failing silently
            print(f"\n[!] Access Error ({url}): {e}") 
            return []

    def fill_form(self, form, payload):
        inputs = form.find_all('input')
        data = {}
        for inp in inputs:
            name = inp.get('name')
            type_ = inp.get('type', 'text')
            if not name:
                continue
            if type_ in ['text', 'search', 'email']:
                data[name] = payload
            elif type_ == 'password':
                data[name] = "123456"
            elif type_ == 'hidden':
                data[name] = inp.get('value', '')
            else:
                data[name] = inp.get('value', 'test')
        
        # Handle textarea fields as well
        textareas = form.find_all('textarea')
        for ta in textareas:
            name = ta.get('name')
            if name:
                data[name] = payload
                
        return data

    def test_sqli(self, url, form):
        for payload in SQLI_PAYLOADS:
            post_data = self.fill_form(form, payload)
            
            # Normalize Action URL
            action = form.get('action')
            if not action:
                action = url
            
            if not action.startswith('http'):
                 from urllib.parse import urljoin
                 target_url = urljoin(url, action)
            else:
                 target_url = action

            try:
                method = form.get('method', 'get').lower()
                if method == 'post':
                    resp = self.session.post(target_url, data=post_data, timeout=10)
                else:
                    resp = self.session.get(target_url, params=post_data, timeout=10)
                
                content = resp.text.lower()
                for err in ERROR_KEYWORDS:
                    if err in content:
                        print(f"[!!!] SQL Injection DETECTED: {url}")
                        print(f"      -> Payload: {payload}")
                        self.vulnerabilities.append({
                            "type": "SQL Injection",
                            "url": url,
                            "payload": payload,
                            "form": str(form)
                        })
                        return # Exit loop if vulnerable
            except:
                pass

    def test_xss(self, url, form):
        for payload in XSS_PAYLOADS:
            post_data = self.fill_form(form, payload)
            
            action = form.get('action')
            if not action:
                action = url

            if not action.startswith('http'):
                 from urllib.parse import urljoin
                 target_url = urljoin(url, action)
            else:
                 target_url = action

            try:
                method = form.get('method', 'get').lower()
                if method == 'post':
                    resp = self.session.post(target_url, data=post_data, timeout=10)
                else:
                    resp = self.session.get(target_url, params=post_data, timeout=10)
                
                if payload in resp.text:
                    print(f"[!] XSS DETECTED: {url}")
                    self.vulnerabilities.append({
                        "type": "XSS",
                        "url": url,
                        "payload": payload,
                        "form": str(form)
                    })
                    return
            except:
                pass

    def scan_single_url(self, url):
        """Scans a single URL for vulnerabilities"""
        forms = self.extract_forms(url)
        for form in forms:
            self.test_sqli(url, form)
            self.test_xss(url, form)

    def scan(self, urls):
        print(f"[*] Scanning {len(urls)} pages. (Threads: 3 - Safe Mode)...")
        
        # Using 3 threads to be safe
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(self.scan_single_url, urls)
            
        return self.vulnerabilities