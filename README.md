# AI-Powered Cold Outreach System: PropertyVisualizer Automated Lead Generation and Email Campaign Tool

This project is a fully automated system that showcases the use of Python, AI, and web technologies to scrape leads from Gelbe Seiten (the German Yellow Pages) in Berlin. It then generates personalized emails in German using the OpenAI API and sets up an email-sending sequence, complete with a test email feature.

This solution demonstrates expertise in scripting, data handling, and AI-driven automation, delivering a robust tool tailored for *Immobilienmakler* (real estate agents).

**To see the fully structured article and visuals, you can visit my portfolio at:** [https://damilareadekeye.com/works/software/automated-lead-gen/](https://damilareadekeye.com/works/software/automated-lead-gen/)

---

### System Overview

![System Overview](https://damilareadekeye.com/images/Software/1/overview-thumb.webp)![Detailed Overview](https://damilareadekeye.com/images/Software/1/overview-full.webp)

---

### Aim and Objectives

**Aim:**
To develop an AI-powered, automated lead generation and email campaign tool for real estate outreach in Berlin, showcasing advanced programming and machine learning skills.

**Objectives:**
1.  Scrape 20+ real estate leads (company names and emails) from Gelbe Seiten using ethical web scraping techniques.
2.  Generate personalized German emails for each lead using the OpenAI API, ensuring professionalism and relevance.
3.  Implement an automated email-sending sequence with a test email feature to validate functionality.
4.  Document the solution comprehensively, including setup instructions and impact analysis.
5.  Produce a video demo to explain the system, thought process, and business value.
6.  Organize and submit all deliverables for seamless evaluation.

---

### Features & Deliverables

*   **Lead Scraping:** Automated extraction of 20 real estate leads from Gelbe Seiten, saved to `leads.csv`.
*   **AI-Powered Personalization:** Generation of unique, professional German emails for each lead using OpenAI's `gpt-3.5-turbo`, saved to `generated_emails.csv`.
*   **Email Automation:** A test email feature implemented via Gmail SMTP.
*   **Comprehensive Documentation:** A detailed README.md covering project structure, setup, and cost estimates.
*   **Video Demonstration:** A 2-3 minute video explaining the system and its business impact.
*   **Organized Submission:** All project files (scripts, CSVs, README, video link) are organized and accessible.

---

### Libraries and Tools Used

*   **Playwright:** For dynamic web scraping of JavaScript-rendered content.
*   **Pandas:** For data manipulation and handling of CSV files.
*   **OpenAI API:** Utilized `gpt-3.5-turbo` for generating personalized email content.
*   **smtplib:** For configuring Gmail SMTP to send emails securely.
*   **Google Drive & ClickUp:** For organizing and submitting project files.
*   **Custom Python Scripting:** For scraping, email generation, and automation workflows.

---

### Process / Methodology

The development workflow was structured as follows:

1.  **Planning (15 mins):** Defined objectives and outlined the necessary scripts.
2.  **Lead Scraping (30 mins):** Developed `scrape_leads.py` to extract emails, handling dynamic content.
3.  **Email Generation (20 mins):** Created `generate_emails.py` to integrate the OpenAI API for personalized emails.
4.  **Automation (30 mins):** Built `send_emails.py` with a test email feature.
5.  **Documentation (15 mins):** Wrote a detailed `README.md`.
6.  **Video Demo (20 mins):** Recorded a video showcasing the system.
7.  **Submission (15 mins):** Organized and submitted all files.

#### Workflow Diagram
![Workflow Diagram](https://damilareadekeye.com/images/Software/1/workflow-diagram.webp)

---

### Results & Impact

*   **Successful Lead Scraping:** Extracted 20 leads with their emails into `leads.csv`.
*   **Personalized Emails:** Generated unique and professional emails for each lead, enhancing outreach potential.
*   **Test Email Success:** Successfully sent a test email, validating the functionality of the email automation script.
*   **Business Value:** The documentation outlines a potential 10-15% improvement in conversion rates and a cost-effective scaling plan.

#### Terminal Results
**`scrape_leads.py` Results**
![Terminal Result 1](https://damilareadekeye.com/images/Software/1/result1.webp)![Terminal Result 2](https://damilareadekeye.com/images/Software/1/result2.webp)![Terminal Result 3](https://damilareadekeye.com/images/Software/1/result3.webp)

**`generate_emails.py` Results**
![Terminal Result 5](https://damilareadekeye.com/images/Software/1/result5.webp)![Terminal Result 4](https://damilareadekeye.com/images/Software/1/result4.webp)

**`send_emails.py` Results**
![Terminal Result 6](https://damilareadekeye.com/images/Software/1/result6.webp)![Terminal Result 7](https://damilareadekeye.com/images/Software/1/result7.webp)

---

### Challenges & Solutions

*   **Challenge:** Handling dynamic content on Gelbe Seiten for email extraction.
    *   **Solution:** Implemented multiple Playwright methods and increased timeouts for robust scraping.
*   **Challenge:** Ensuring unique, professional emails from OpenAI.
    *   **Solution:** Crafted a precise and detailed prompt to guide the AI.
*   **Challenge:** Securely setting up Gmail SMTP.
    *   **Solution:** Used an App Password with 2-Factor Authentication for secure email delivery.
*   **Challenge:** Initial time constraints with a no-code approach.
    *   **Solution:** Proactively switched to a coded solution to demonstrate technical skills.

---

### What I Learned

*   Mastery of web scraping dynamic content ethically with Playwright.
*   Integration of the OpenAI API for AI-driven content generation.
*   Automation of email workflows using SMTP with secure configurations.
*   Effective project documentation and video production to communicate technical solutions.
*   Proactive problem-solving and adaptability under time constraints.

---

### Demonstration & Access

*   **Google Drive Repository:** [View files & documentation](https://drive.google.com/drive/folders/12if07mLQYLKrdxJwnhP8XT6s0USyfATK?usp=sharing)
*   **Demo Video:** [Watch demonstration](https://drive.google.com/file/d/1Nzt1u7EXoa1kOv0W9nGHkXsEIVy5AViB/view?usp=sharing)

---

### Code Snippets

<details>
<summary><strong>View scrape_leads.py</strong></summary>

```python
from playwright.sync_api import sync_playwright
import pandas as pd
import re
import time

# Start Playwright
with sync_playwright() as p:
    # Launch a browser in non-headless mode for debugging
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # URL to scrape
    url = "https://www.gelbeseiten.de/branchen/immobilienmakler/berlin"
    try:
        page.goto(url, timeout=60000)  # Increased timeout to 60 seconds
    except Exception as e:
        print(f"Failed to load the initial page: {str(e)}")
        browser.close()
        exit()

    # ... (rest of the script)
```
</details>

<details>
<summary><strong>View generate_emails.py</strong></summary>

```python
import pandas as pd
import openai
from openai import OpenAI
import os

# Set your OpenAI API key
openai_api_key = 'sk-proj-z-****************************7vaMdMA'
if not openai_api_key:
    raise ValueError("Please set your OpenAI API key in the script.")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# ... (rest of the script)
```
</details>

<details>
<summary><strong>View send_emails.py</strong></summary>

```python
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import os

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "adekeyedamilarelekan@gmail.com"
SENDER_PASSWORD = "r**j **** v**u ****"

# ... (rest of the script)
```
</details>

---

### Future Enhancements

1.  Integrate a scheduler (e.g., `schedule` library) for automated daily email campaigns.
2.  Enhance personalization by scraping company-specific data from their websites.
3.  Add error logging and analytics to track campaign performance.
4.  Expand to other German cities with multi-threaded scraping for scalability.

---

### Thank You

Thank you for exploring this project. It reflects my passion for AI automation, data engineering, and creating innovative software solutions. I welcome any opportunities for collaboration or discussions about my work.

For inquiries, please reach out via the [Contact](https://damilareadekeye.com/contact/) section on my portfolio.

**Best regards,**
*Damilare Lekan Adekeye*
