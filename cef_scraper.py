import requests
import csv

# Base URL for AJAX calls
ajax_url = "https://www.wfsfaa.gov.hk/include/course_search_ajax.php"

# Base URL for course details
detail_base_url = "https://www.wfsfaa.gov.hk/tc/resources/course_search/cef_details.php?course_code="

# Prompt user to select language preference
language = input("Choose language (en for English, tc for Traditional Chinese, sc for Simplified Chinese): ").strip().lower()
if language not in ["en", "tc", "sc"]:
    print("Invalid choice. Defaulting to English (en).")
    language = "en"

# Parameters for the request (change page number dynamically)
params_template = {
    "action": "search",
    "page": 1,  # Start from page 1
    "category": "cef",
    "area": "",
    "course_fee": "",
    "qf_level": "",
    "institution_name": "",
    "institution_code": "",
    "course_name": "",
    "course_code": "",
    "qr_number": "",
    "qsearch": "",
    "online_course": "",
}

# Output CSV file
output_file = f"cef_courses_{language}.csv"

# Define the columns to save based on language
columns = [
    f"course_{language}",
    f"institution_{language}",
    f"area_{language}",
    f"award_{language}",
    "course_code",
    "fee",
    "detail_link",
]

# Open the CSV file for writing
with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    # Loop through pages
    for page in range(1, 1000):  # Set an upper limit for pages
        params_template["page"] = page  # Update the page number
        print(f"Fetching page {page}...")

        response = requests.get(ajax_url, params=params_template)
        if response.status_code == 200:
            data = response.json()
            if not data:  # If the data is an empty list
                print("No more results. Reached the final page.")
                break

            # Write rows to the CSV
            for item in data:
                # Handle course name replacement if it's missing ("---")
                course_name = item.get(f"course_{language}", "N/A")
                if course_name == "---":
                    course_name = item.get("course_en", "N/A")  # Fallback to English name

                row = {
                    f"course_{language}": course_name,
                    f"institution_{language}": item.get(f"institution_{language}", "N/A"),
                    f"area_{language}": item.get(f"area_{language}", "N/A"),
                    f"award_{language}": item.get(f"award_{language}", "N/A"),
                    "course_code": item.get("course_code", "N/A"),
                    "fee": item.get("fee", "N/A"),
                    "detail_link": f"{detail_base_url}{item.get('course_code', '')}",
                }
                writer.writerow(row)
        else:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break

print("Data scraping complete.")
