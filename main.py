from playwright.sync_api import Playwright, sync_playwright, expect


def get_email_address():
    # Prompt user for their email address
    email_address = input("What is your email address?: ")
    return email_address

def get_incident_number():
    # Prompt user for the incident number
    incident_number = input("What is the incident number?: ")
    return incident_number


def run(playwright: Playwright) -> None:
    # Get user's email address
    email_address = get_email_address()

    # Get incident number
    incident_number = get_incident_number()

    browser = playwright.chromium.launch(headless=False, args=["--enable-clipboard"])
    context = browser.new_context()
    page = context.new_page()

    # Sign in with SSO
    page.goto("https://big.dx.foc.zone/report/6615")
    page.goto("https://sso.authrock.com/u/login/identifier?state=hKFo2SBidGJldHZjMFRSRi1HUUpOb05GQWh1TmdOS21pQVlZNKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIEk5T3AxUlFHRXZ2RGlOOGVENjM3b2o2YVFZZThISlZ4o2NpZNkgQ2pyd0U0V1VyRUhwWEdVOEU3a0NmVWtYOXVBQU1QaDU")

    # Fill in email address
    page.get_by_label("Email address*").fill(email_address)
    page.get_by_label("Email address*").press("Enter")
    page.wait_for_load_state("networkidle")

    # Load RCD Tech Status
    page.goto("https://big.dx.foc.zone/report/6615")

    # Fill in incident number
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("combobox", name="Cherwell Ticket").locator("div").click()
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("textbox", name="Search").fill(incident_number)
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("textbox", name="Search").press("Enter")

    # Click incident number check box
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("option", name=incident_number).locator("div span").click()
    page.wait_for_load_state("networkidle")

    # Copy the tracking number
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").locator(".mid-viewport > div > div > .scrollable-cells-viewport > .scrollable-cells-container > div:nth-child(4)").first.click(button="right")
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_test_id("pbimenu-item.Copy value").click()

    # Do a Google search of the tracking number
    clipboard_content = page.evaluate('() => navigator.clipboard.readText()')
    google_search_url = f"https://www.google.com/search?q={clipboard_content}"
    page.goto(google_search_url)
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Track via UPS").click()

    # Wait for user input before exiting
    input("Press Enter to exit...")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
