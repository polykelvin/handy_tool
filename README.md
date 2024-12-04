# README: CEF Course Scraper

## Background of the Continuing Education Fund (CEF)
The Continuing Education Fund (CEF) is a scheme established by the **Hong Kong Government** to encourage Hong Kong residents to pursue further education and training. It aims to assist individuals in enhancing their skills and knowledge to meet the challenges of a fast-changing economy.

## Overview
This script scrapes all available course information from the Continuing Education Fund (CEF) website and saves it into a CSV file. It is specifically designed for users who want to download the entire dataset and later use tools like ChatGPT or other AI tools to help analyze and decide which courses to explore further.

Instead of selecting specific courses during the scraping process, this script gathers all course data, allowing users to perform offline analysis and filtering. By providing complete data, users can leverage AI tools to make informed decisions about which courses to focus on based on their individual needs and preferences. For example:

"Which courses are under HKD 20,000 in Data Science?"<br>
"Show me Master's programs from HKUST related to Business."

The script supports multiple languages (English, Traditional Chinese, and Simplified Chinese) and ensures missing course names ("---") are replaced with their English equivalent, making the data as complete and user-friendly as possible.

---

## Features
1. **Multilingual Support**:
   - User can choose between English (`en`), Traditional Chinese (`tc`), or Simplified Chinese (`sc`) for the output data.
   
2. **Fallback for Missing Course Names**:
   - If the course name in the selected language is missing (`"---"`), the script automatically replaces it with the English name (`course_en`).

3. **CSV Output**:
   - Data is saved in a structured CSV file named `cef_courses_<language>.csv`, where `<language>` corresponds to the selected language.

4. **Detailed Links**:
   - Each course includes a link to its detailed page on the CEF website.

---

## How It Works
1. **User Language Selection**:
   - At runtime, the user selects the preferred language (`en`, `tc`, or `sc`).
   - The script defaults to English if the input is invalid.

2. **Fetch Course Data**:
   - The script makes AJAX requests to the CEF website for course data.
   - Pagination is handled automatically, and the script stops when no more data is available.

3. **Data Processing**:
   - For each course, the script retrieves details such as:
     - **Course Name** (`course_<language>`)
     - **Institution Name** (`institution_<language>`)
     - **Area of Study** (`area_<language>`)
     - **Award Type** (`award_<language>`)
     - **Course Code**
     - **Course Fee**
     - **Link to Details Page**
   - If the course name is `"---"`, the English course name is used as a fallback.

4. **Output**:
   - Data is saved into a CSV file with columns specific to the selected language.

---

## Output File
The CSV file will include the following columns:
- `course_<language>`: The course name in the selected language (with fallback to English if missing).
- `institution_<language>`: The institution name in the selected language.
- `area_<language>`: The area of study in the selected language.
- `award_<language>`: The award type in the selected language.
- `course_code`: The unique identifier for the course.
- `fee`: The course fee (in HKD).
- `detail_link`: A link to the detailed course page on the CEF website.

Example:
```
course_tc,institution_tc,area_tc,award_tc,course_code,fee,detail_link
理學碩士(環境健康及安全),香港科技大學,A12 - 理學科,碩士,42M12568A,145000,https://www.wfsfaa.gov.hk/tc/resources/course_search/cef_details.php?course_code=42M12568A
```

---

## Disclaimer
1. **Compliance with Website Policies**:
   - Users must adhere to the terms and policies set by the CEF website. 
   - The script is provided for educational and personal use only. Unauthorized or inappropriate use may violate the website’s terms of service.

2. **User Responsibility**:
   - Any legal or ethical issues arising from the use of this script are the sole responsibility of the user.
   - The script author does not assume liability for misuse.

3. **Accuracy**:
   - While the script strives for accuracy, the CEF website data may change, and the script’s output may not always reflect the latest updates.

---

## Requirements
- **Python 3.x**: Make sure you have Python installed.
- **Libraries**:
  - `requests`
  - `csv`

Install missing libraries using:
```bash
pip install requests
```

---

## How to Run
1. Save the script as `cef_scraper.py`.
2. Open a terminal and run the script:
   ```bash
   python cef_scraper.py
   ```
3. Follow the prompt to select a language (`en`, `tc`, or `sc`).
4. The script will create a CSV file with the course data in the selected language.

---

## Notes
- The script fetches data up to 1000 pages, but stops automatically when no more results are found.
- The generated CSV file will be saved in the same directory as the script.
- Ensure an active internet connection while running the script.