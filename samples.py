"""
Sample phishing emails for testing and demonstration.
"""

SAMPLES = [
    {
        "id": 1,
        "name": "PayPal Spoofing",
        "email": """From: security@paypa1-alerts.com
Subject: URGENT: Your account has been limited!

Dear Valued Customer,

Your PayPal account access is limited. Verify immediately at 
http://paypa1-alerts.com/verify?token=abc123 or your account 
will be permanently closed within 24 hours.

Thank you for your immediate attention.
PayPal Security Team"""
    },
    {
        "id": 2,
        "name": "Bank BEC",
        "email": """From: ceo.johnson@company-corp.net
Subject: Urgent Wire Transfer Needed

Hi,

I need you to process a confidential wire transfer of $47,000 
immediately. This is time sensitive. Do not discuss with anyone.

Reply directly to: finance.dept.urgent@gmail.com

Best regards,
John Johnson
CEO"""
    },
    {
        "id": 3,
        "name": "Google Phishing",
        "email": """From: no-reply@g00gle-security.com
Subject: Your Google account was accessed from new device

Dear User,

Someone signed into your account from Russia. Click here to 
secure your account: http://g00gle-security.com/secure-now

If this wasn't you, verify your identity immediately.

Google Security Team"""
    },
    {
        "id": 4,
        "name": "Fake Invoice",
        "email": """From: billing@microsoft-invoice.net
Subject: Invoice #INV-2024-8821 Payment Due

Dear Customer,

Please find attached invoice for $899.99 Microsoft 365 renewal.

To cancel this charge call: +1-888-555-0199 immediately.

Billing will occur in 24 hours if not cancelled.

Microsoft Billing Department"""
    },
    {
        "id": 5,
        "name": "Legitimate Email",
        "email": """From: newsletter@github.com
Subject: Your GitHub digest for this week

Hi there,

Here are the trending repositories this week on GitHub:

1. awesome-ai-tools - A curated list of AI tools
2. machine-learning-course - Free ML course materials
3. python-best-practices - Clean code guidelines

Visit github.com/trending to explore more.

Happy coding!
The GitHub Team"""
    }
]


# Individual sample constants for easy access
SAMPLE_PAYPAL = SAMPLES[0]["email"]
SAMPLE_BEC = SAMPLES[1]["email"]
SAMPLE_GOOGLE = SAMPLES[2]["email"]
SAMPLE_FAKE_INVOICE = SAMPLES[3]["email"]
SAMPLE_LEGITIMATE = SAMPLES[4]["email"]
