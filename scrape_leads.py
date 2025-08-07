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

    # Accept cookies if there's a consent dialog
    try:
        accept_button = page.query_selector('button#onetrust-accept-btn-handler')
        if accept_button:
            accept_button.click()
            print("Accepted cookies")
            page.wait_for_timeout(2000)
    except Exception as e:
        print(f"No cookie dialog found or error: {str(e)}")

    # Wait for the page to load
    page.wait_for_timeout(5000)

    # Scroll to the bottom to load all listings
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)  # Wait for lazy-loaded content

    # Find all company elements and extract names and details URLs upfront
    companies = page.query_selector_all('h2.mod-Treffer__name')
    print(f"Found {len(companies)} company names")

    # Store company names and details URLs in a list to avoid context issues
    company_data = []
    for company in companies:
        company_name = company.inner_text().strip()
        details_url = page.evaluate("""
            (element) => {
                let parent = element.closest('article');
                if (parent) {
                    let link = parent.querySelector('a[href]');
                    return link ? link.getAttribute('href') : null;
                }
                return null;
            }
        """, company)
        if company_name and details_url:
            company_data.append({"name": company_name, "details_url": details_url})

    leads = []
    for idx, data in enumerate(company_data):
        company_name = data["name"]
        details_url = data["details_url"]
        print(f"[{idx+1}/{len(company_data)}] Processing: {company_name}")
        
        # Construct full URL
        full_details_url = f"https://www.gelbeseiten.de{details_url}" if not details_url.startswith('http') else details_url
        
        try:
            # Navigate to the company page
            page.goto(full_details_url, timeout=30000)
            page.wait_for_timeout(3000)  # Wait longer for the page to fully load
            
            # Scroll down to ensure all content is loaded
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            
            # IMPROVED METHOD 1: Try to get the email directly from the button with data attributes
            email_found = False
            
            # First try to get the email from the "email_versenden" element
            email_button = page.query_selector('div[id="email_versenden"]')
            if email_button:
                data_link = email_button.get_attribute('data-link')
                if data_link and 'mailto:' in data_link:
                    email_match = re.search(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+)', data_link)
                    if email_match:
                        email = email_match.group(1)
                        leads.append({"Company Name": company_name, "Email": email})
                        print(f"✓ Found email: {email}")
                        email_found = True
            
            # IMPROVED METHOD 2: If not found, try alternate method with aktionsleiste-button
            if not email_found:
                # Look for elements with data-link attribute containing mailto
                email_elements = page.query_selector_all('[data-link*="mailto:"]')
                for element in email_elements:
                    data_link = element.get_attribute('data-link')
                    if data_link:
                        email_match = re.search(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+)', data_link)
                        if email_match:
                            email = email_match.group(1)
                            leads.append({"Company Name": company_name, "Email": email})
                            print(f"✓ Found email: {email}")
                            email_found = True
                            break
            
            # IMPROVED METHOD 3: Try JavaScript approach to find all elements with mailto links
            if not email_found:
                try:
                    email_element = page.evaluate_handle("""
                        () => {
                            const elements = document.querySelectorAll('[data-link]');
                            for (let el of elements) {
                                const dataLink = el.getAttribute('data-link');
                                if (dataLink && dataLink.includes('mailto:')) {
                                    return el;
                                }
                            }
                            return null;
                        }
                    """)
                    
                    if email_element:
                        data_link = email_element.get_attribute('data-link')
                        if data_link:
                            email_match = re.search(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+)', data_link)
                            if email_match:
                                email = email_match.group(1)
                                leads.append({"Company Name": company_name, "Email": email})
                                print(f"✓ Found email: {email}")
                                email_found = True
                except Exception as e:
                    print(f"JavaScript evaluation error: {str(e)}")
            
            # IMPROVED METHOD 4: Locate by class name from your screenshot
            if not email_found:
                email_element = page.query_selector('.detailseite_e-mail-button')
                if email_element:
                    data_link = email_element.get_attribute('data-link')
                    if data_link and 'mailto:' in data_link:
                        email_match = re.search(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+)', data_link)
                        if email_match:
                            email = email_match.group(1)
                            leads.append({"Company Name": company_name, "Email": email})
                            print(f"✓ Found email: {email}")
                            email_found = True
            
            if not email_found:
                # Try directly capturing data-link from the span containing "E-Mail"
                email_spans = page.query_selector_all('span')
                for span in email_spans:
                    if "E-Mail" in span.inner_text():
                        # Try to get data-link from parent
                        parent = span.evaluate("el => el.closest('[data-link]')")
                        if parent:
                            data_link = parent.get_attribute('data-link')
                            if data_link and 'mailto:' in data_link:
                                email_match = re.search(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+)', data_link)
                                if email_match:
                                    email = email_match.group(1)
                                    leads.append({"Company Name": company_name, "Email": email})
                                    print(f"✓ Found email: {email}")
                                    email_found = True
                                    break
            
            if not email_found:
                print(f"⨯ No email found for: {company_name}")
                
        except Exception as e:
            print(f"Error processing {company_name}: {str(e)}")
        
        # Optional: limit the number of companies to process
        if len(leads) >= 20:
            print(f"Reached limit of 20 leads. Stopping.")
            break
            
        # Avoid rate limiting
        time.sleep(2)

    # Save to CSV
    if leads:
        df = pd.DataFrame(leads)
        
        desktop_path = "C:/Users/Aorus15/Desktop/PropertyVisualizer/"
        csv_path = desktop_path + "leads.csv"  # Changed to relative path
        df.to_csv(csv_path, index=False)
        print(f"Scraped and saved {len(leads)} leads with emails to {csv_path}")
    else:
        print("No leads with emails were scraped.")

    # Keep the browser open for inspection
    print("Browser will close in 10 seconds. Inspect the page now!")
    page.wait_for_timeout(10000)
    browser.close()
    