import html
import os
from datetime import datetime

def generate_html_report(vulnerabilities, filename="Pentest_Report.html"):
    # Professional Remediation Suggestions database
    remediations = {
        "SQL Injection": "Implement <b>Prepared Statements</b> (Parameterized Queries) or use an ORM. Ensure input validation is strictly enforced.",
        "XSS": "Apply <b>Context-Aware Output Encoding</b> on all user-supplied data. Implement a Content Security Policy (CSP)."
    }
    
    # Constructing HTML Content
    content = f"""
    <html>
    <head>
        <title>Vulnerability Scan Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 40px; }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .summary {{ background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            .vuln {{ background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 6px solid #e74c3c; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            code {{ background: #f8f9fa; padding: 2px 6px; border-radius: 4px; color: #e83e8c; font-family: monospace; }}
            .remediation {{ background: #e8f4fd; color: #0c5460; padding: 10px; margin-top: 10px; border-radius: 4px; border: 1px solid #bee5eb; }}
        </style>
    </head>
    <body>
        <div class="summary">
            <h2>🛡️ Vulnerability Scan Report</h2>
            <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>Status:</strong> {len(vulnerabilities)} critical vulnerabilities detected.</p>
        </div>
        <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">
    """
    
    for v in vulnerabilities:
        remediation_text = remediations.get(v['type'], 'No specific remediation available.')
        
        content += f"""
        <div class="vuln">
            <h3>{v['type']}</h3>
            <p><b>URL:</b> <a href="{v['url']}" target="_blank">{v['url']}</a></p>
            <p><b>Payload:</b> <code>{html.escape(v['payload'])}</code></p>
            <div class="remediation">
                <b>💡 Remediation:</b> {remediation_text}
            </div>
        </div>
        """
        
    content += "</body></html>"
    
    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[+] Report generated successfully: {os.path.abspath(filename)}")