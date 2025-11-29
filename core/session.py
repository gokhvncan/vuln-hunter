import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3 

# mute HTTPS warnings 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session_with_retries():
    session = requests.Session()
    
    # Retry 
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Global User-Agent
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    
    
    session.verify = False
    
    return session