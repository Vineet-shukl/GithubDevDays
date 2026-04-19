"""
Pydantic AI agent for phishing email detection with tools.
Uses Groq (LLaMA 3.3 70B) as the LLM backend.
"""

import os
import re
from dotenv import load_dotenv
from pydantic_ai import Agent
from models import ThreatReport

# Load .env file
load_dotenv()

# Validate API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not set. Get one free at https://console.groq.com/keys"
    )

# Create Pydantic AI agent using Groq
agent = Agent(
    model="groq:llama-3.3-70b-versatile",
    output_type=ThreatReport,
    system_prompt="""
    You are a senior cybersecurity analyst with 10+ years of 
    phishing detection experience.

    When analyzing an email always check:
    1. Sender domain vs claimed brand (e.g. paypa1.com vs paypal.com)
    2. Urgency or fear language ("account suspended", "act now")
    3. Suspicious or obfuscated URLs
    4. Grammar mistakes and inconsistencies
    5. Mismatched Reply-To headers
    6. Requests for credentials, OTP, or payment

    SEVERITY GUIDE:
    - critical: spoofed major brand + credential harvesting
    - high: malware link or BEC attempt
    - medium: suspicious signals but unclear intent
    - low: mild spam, unlikely phishing

    Use the available tools to extract URLs and check domains.
    Always populate red_flags as a list of specific observations.
    Never set confidence above 0.95.
    Be precise and conservative.
    """
)


@agent.tool_plain
def extract_urls(email_body: str) -> list[str]:
    """Extract all http/https URLs using regex from the email body."""
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+' 
    urls = re.findall(url_pattern, email_body)
    return urls if urls else []


@agent.tool_plain
def check_domain_suspicion(domain: str) -> dict:
    """
    Check if domain contains typosquatting patterns like:
    paypa1, amaz0n, g00gle, micros0ft, app1e, faceb00k
    
    Returns: {"domain": domain, "is_suspicious": bool, "reason": str}
    """
    domain_lower = domain.lower()
    
    # Common typosquatting patterns
    suspicious_patterns = {
        'paypal': ['paypa1', 'paypai', 'paypa', 'paypa11'],
        'amazon': ['amaz0n', 'arnazon', 'amazom', 'arnazon'],
        'google': ['g00gle', 'gooogle', 'googie', 'goog1e'],
        'microsoft': ['micros0ft', 'rnicrosoft', 'microsof', 'rnicr0soft'],
        'apple': ['app1e', 'appl', 'appie', 'app1'],
        'facebook': ['faceb00k', 'facebok', 'faceboook', 'facebo0k'],
        'netflix': ['netfl1x', 'netfllx', 'netfiix', 'netf1ix'],
        'bank': ['bankk', 'bnak', 'b4nk', 'baank'],
        'payoneer': ['pay0neer', 'payon3er', 'payoneer'],
        'chase': ['chas3', 'chasse', 'chace'],
        'wellsfargo': ['we11sfargo', 'wellsfarg0', 'wellsfarqo']
    }
    
    for brand, patterns in suspicious_patterns.items():
        for pattern in patterns:
            if pattern in domain_lower:
                return {
                    "domain": domain,
                    "is_suspicious": True,
                    "reason": f"Possible typosquatting of {brand} (found '{pattern}')"
                }
    
    return {
        "domain": domain,
        "is_suspicious": False,
        "reason": "No obvious typosquatting detected"
    }


@agent.tool_plain
def analyze_header_mismatch(from_header: str, reply_to: str) -> dict:
    """
    Check if From and Reply-To domains are different.
    
    Returns: {"mismatch_detected": bool, "from": str, "reply_to": str}
    """
    # Extract domain from email addresses
    def extract_domain(email: str) -> str:
        match = re.search(r'@([\w.-]+)', email)
        return match.group(1) if match else ""
    
    from_domain = extract_domain(from_header)
    reply_domain = extract_domain(reply_to)
    
    mismatch = from_domain != reply_domain and from_domain and reply_domain
    
    return {
        "mismatch_detected": mismatch,
        "from": from_domain,
        "reply_to": reply_domain
    }
