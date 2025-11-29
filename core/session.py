import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session_with_retries():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.7,
        status_forcelist=[502, 503, 504, 429],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session