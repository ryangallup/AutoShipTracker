import tkinter as tk
from tkinter import ttk, simpledialog

from playwright.sync_api import Playwright, sync_playwright

def get_input(prompt, validation=None):
    while True:
        user_input = simpledialog.askstring("Input", prompt)
        if validation is None or validation(user_input):
            return user_input
        else:
            print("Invalid input. Please try again.")

def is_valid_incident_number(incident_number):
    return incident_number.startswith("INC") and incident_number[3:].isdigit() and len(incident_number) == 10

def sign_in(page, email_address):
    page.wait_for_load_state("networkidle")
    page.goto("https://big.dx.foc.zone/report/6615")
    page.wait_for_load_state("networkidle")
    page.get_by_label("Email address*").fill(email_address)
    page.wait_for_load_state("networkidle")
    page.get_by_label("Email address*").press("Enter")
    page.wait_for_load_state("networkidle")

def load_report(page, incident_number):
    page.wait_for_load_state("networkidle")
    page.goto("https://big.dx.foc.zone/report/6615")
    page.wait_for_load_state("networkidle")
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("combobox", name="Cherwell Ticket").locator("div").click()
    page.wait_for_load_state("networkidle")
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("textbox", name="Search").fill(incident_number)
    page.wait_for_load_state("networkidle")
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("textbox", name="Search").press("Enter")
    page.wait_for_load_state("networkidle")

def select_incident(page, incident_number):
    page.wait_for_load_state("networkidle")
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_role("option", name=incident_number).locator("div span").click()
    page.wait_for_load_state("networkidle")

def copy_tracking_number(page, index):
    page.wait_for_timeout(500)
    page.frame_locator(f"iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").locator(f".mid-viewport > div > div > .scrollable-cells-viewport > .scrollable-cells-container > div:nth-child({index})").first.click(button="right")
    page.wait_for_load_state("networkidle")
    page.frame_locator("iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_label("Copy", exact=True).click()
    page.wait_for_load_state("networkidle")
    page.frame_locator(f"iframe[title=\"report-solutionId-b3320618-8f74-404b-9d9b-ee75901ce8eb\"]").get_by_test_id("pbimenu-item.Copy value").click()
    page.wait_for_load_state("networkidle")

def google_search_tracking_number(page):
    page.wait_for_load_state("networkidle")
    clipboard_content = page.evaluate('() => navigator.clipboard.readText()')
    page.wait_for_load_state("networkidle")
    google_search_url = f"https://www.google.com/search?q={clipboard_content}"
    page.wait_for_load_state("networkidle")
    page.goto(google_search_url)
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Track via UPS").click()
    page.wait_for_load_state("networkidle")

def run_with_gui(playwright: Playwright):
    def search(browser, context):
        email = email_entry.get()
        incident = incident_entry.get()
        hardware = hardware_combobox.get()

        page = context.new_page()

        sign_in(page, email)
        load_report(page, incident)
        select_incident(page, incident)

        hardware_indices = {
            "Latitude 54 Series": 4, "Precision 55 Series": 5, "MacBook Pro": 6, "MicroTower": 7,
            "2 Monitors": 8, "1 Monitor": 9, "Docking Station": 10, "Keyboard": 11, "Headset": 12,
            "Mouse": 13, "Webcam": 14
        }
        copy_tracking_number(page, hardware_indices[hardware])

        google_search_tracking_number(page)

    def on_search(event=None):  # function to be called when Enter key is pressed
        search_button.invoke()  # simulate a button click

    root = tk.Tk()
    root.title("Incident Tracker")

    # Calculate center position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - root.winfo_reqwidth()) / 2
    y_coordinate = (screen_height - root.winfo_reqheight()) / 2

    # Set geometry
    root.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")

    # Frame for inputs
    input_frame = ttk.Frame(root, padding="20")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Email Address Entry
    email_label = ttk.Label(input_frame, text="Email Address:")
    email_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    email_entry = ttk.Entry(input_frame, width=35)
    email_entry.grid(row=0, column=1, padx=5, pady=5)
    email_entry.focus()

    # Incident Number Entry
    incident_label = ttk.Label(input_frame, text="Incident Number:")
    incident_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    incident_entry = ttk.Entry(input_frame, width=30)
    incident_entry.grid(row=1, column=1, padx=5, pady=5)

    # Hardware Selection
    hardware_label = ttk.Label(input_frame, text="Select Hardware:")
    hardware_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    hardware_combobox = ttk.Combobox(input_frame, values=["Latitude 54 Series", "Precision 55 Series", "MacBook Pro", "MicroTower",
                                                          "2 Monitors", "1 Monitor", "Docking Station", "Keyboard", "Headset", "Mouse", "Webcam"], width=27)
    hardware_combobox.grid(row=2, column=1, padx=5, pady=5)

    # Search Button
    search_button = ttk.Button(input_frame, text="Search", command=lambda: search(browser, context))
    search_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Bind Enter key to search button
    root.bind('<Return>', on_search)

    # Initialize browser and context
    browser = playwright.chromium.launch(headless=False, args=["--enable-clipboard"])
    context = browser.new_context()

    root.mainloop()

    # Close browser and context when the GUI is closed
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run_with_gui(playwright)
