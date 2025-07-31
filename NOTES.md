# Israeli Group Chat Finder – Project Notes

## Overview
This Streamlit app helps users find Israeli group chats by city and interest. It collects user requests, sends them to a Slack channel, and logs each submission to a CSV file for record-keeping.

---

## How It Works

### 1. City Selection
- The app loads a list of cities from `deep-links-2025-07-21.csv`.
- Only cities containing 'Israel' in their name are shown in the dropdown.
- The city dropdown is presented in English (or Hebrew if you add a mapping).

### 2. Email Input
- Users must enter their email address. This is required to submit the form.

### 3. Interest Selection
- After selecting a city, the app loads all unique interests available for that city from the CSV.
- Interests are shown in a multiselect dropdown, grouped and sorted by category in this order:
  1. Buy/Sell
  2. Apartments
  3. Jobs
  4. Services
  5. Sports
  6. Hobbies
- Each dropdown option is formatted as `[Category] Interest` (e.g., `[Jobs] Business`).
- Users must select at least one interest to submit the form.

### 4. Submission
- When the user submits:
  - The request is sent to a Slack channel using a webhook URL stored in Streamlit secrets.
  - The app logs the submission to `submission_log.csv`.
    - Each interest is logged on a separate line, with:
      - A unique submission ID (incremented for each submission)
      - The user's email
      - The selected city
      - The interest name
      - The deep link for that interest/city (from the CSV)
    - The CSV is created with a header if it does not exist.

### 5. Error Handling
- The app checks that all required fields are filled before allowing submission.
- If the Slack API call fails, an error is shown to the user.

---

## File Structure
- `app.py` – Main Streamlit app
- `deep-links-2025-07-21.csv` – Source of cities, interests, and deep links
- `submission_log.csv` – Log of all user submissions (auto-created)
- `.streamlit/secrets.toml` – Contains the `SLACK_WEBHOOK_URL` for Slack integration

---

## Customization
- To support Hebrew city/interest names, add a mapping or a new column to the CSV.
- To change the Slack channel, update the webhook URL in `secrets.toml`.
- To add more categories or change their order, update the `category_order` list in `app.py`.

---

For further questions or improvements, see the code comments or ask the developer. 