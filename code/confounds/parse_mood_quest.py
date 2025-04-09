import requests
import re

import pandas as pd


def parse_issue(text):
    # Normalize line endings and delimiters
    text = text.replace("\r\n", "\n")

    # Split entries using '### ' as a delimiter
    entries = re.split(r"### ", text)[1:]  # Skip the first empty split if any

    # Extract key-value pairs
    data = {}
    for entry in entries:
        lines = entry.strip().split("\n\n")
        key = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else "n/a"

        # Special handling for 'Slept during scan' checkboxes
        if key.lower().startswith("slept during scan"):
            sleep_stages = {
                "scan": "Slept during session",
                "T1w": "Slept during T1w",
                "diffusion": "Slept during diffusion",
                "QCT task": "Slept during QCT task",
                "rest task": "Slept during rest task",
                "BHT task": "Slept during BHT task",
            }
            for stage, col_name in sleep_stages.items():
                match = re.search(
                    rf"- \[\s*(x?)\s*\]\s*I slept during the {re.escape(stage)}",
                    value,
                    re.IGNORECASE,
                )
                if match:
                    data[col_name] = "Yes" if match.group(1).lower() == "x" else "No"
                else:
                    data[col_name] = "n/a"
        else:
            # Remove indications in parentheses from the value (except for kind of precipitations)
            if key != "Kind of precipitation":
                value = re.sub(r"\s*\(.*?\)", "", value).strip()

            # Handle generic checkboxes
            if "- [X]".lower() in value.lower():
                value = "Yes"
            elif "- [ ]" in value:
                value = "No"

            data[key] = value

    return data


def extract_issues_info(
    issue_title_pattern,
    token_path="/home/cprovins/token_axonlab.txt",
    repo_owner="TheAxonLab",
    repo_name="hcph-mood-quest",
):
    # Read token
    with open(token_path, "r") as file:
        token = file.read().strip()

    # GitHub API headers
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    issues_info = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
        params = {"state": "all", "per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 404:
            raise ValueError(
                f"GitHub API returned 404: Resource not found at {url}. "
                "This could be due to insufficient permissions. Please check your token's access rights."
            )

        issues = response.json()

        # Stop if no more issues
        if not issues:
            break

        for issue in issues:
            title = issue["title"]
            if re.search(issue_title_pattern, title):
                # Get the issue body
                issue_body = issue["body"]

                # Parse the text
                info_dict = parse_issue(issue_body)

                # Extract session and subject number from the title
                match = re.search(r"sub-(\d+)_ses-([a-zA-Z0-9]+)", title)
                if match:
                    subject_number = match.group(1)
                    session_number = match.group(2)
                    # Add subject and session number at the beginning of the data_dict
                    info_dict = {
                        "subject_number": subject_number,
                        "session_number": session_number,
                        **info_dict,
                    }

                # Append the data_dict to the list
                issues_info.append(info_dict)

        page += 1

    return issues_info


## Parse the confounds of the reliability sessions first
## Parse the confounds registered before and after the sessions separately and then merge the dataframes
issues_before_info = extract_issues_info(r"\[MOOD\](?:\[BEFORE\])? sub-001_ses-0\d{2}")
issues_after_info = extract_issues_info(r"\[MOOD\]\[AFTER\] sub-001_ses-0\d{2}")

# Convert the list of dictionaries to a DataFrame
df_before = pd.DataFrame(issues_before_info)
df_after = pd.DataFrame(issues_after_info)

# Merge the confounds collected after the session into the confounds collected before the session
df = pd.merge(
    df_before,
    df_after,
    how="left",
    on=["subject_number", "session_number"],
    suffixes=(None, "_after"),
)

# Merge same column before and after
df["Slept during session"] = df["Slept during session"].combine_first(
    df["Slept during session_after"]
)
df["Slept during T1w"] = df["Slept during T1w"].combine_first(
    df["Slept during T1w_after"]
)
df["Slept during diffusion"] = df["Slept during diffusion"].combine_first(
    df["Slept during diffusion_after"]
)
df["Slept during QCT task"] = df["Slept during QCT task"].combine_first(
    df["Slept during QCT task_after"]
)
df["Slept during rest task"] = df["Slept during rest task"].combine_first(
    df["Slept during rest task_after"]
)
df["Slept during BHT task"] = df["Slept during BHT task"].combine_first(
    df["Slept during BHT task_after"]
)
df["Rumination"] = df["Rumination"].combine_first(df["Rumination_after"])
df["Anxiety"] = df["Anxiety"].combine_first(df["Anxiety_after"])
df["Physical pain during scan"] = df["Physical pain during scan"].combine_first(
    df["Physical pain during scan_after"]
)
df.drop(
    columns=[
        "Rumination_after",
        "Anxiety_after",
        "Physical pain during scan_after",
        "Are you sure you filled all entries ?_after",
        "Slept during session_after",
        "Slept during T1w_after",
        "Slept during diffusion_after",
        "Slept during QCT task_after",
        "Slept during rest task_after",
        "Slept during BHT task_after",
    ],
    inplace=True,
)

## Manual corrections
# Indicate units or scale range in the column name
df.rename(columns={"Scan date": "Scan date (MM-DD-AAAA)"}, inplace=True)
df.rename(columns={"Scan time": "Scan time (HH-MM)"}, inplace=True)
df.rename(
    columns={"Outside temperature range": "Outside temperature range (°C)"},
    inplace=True,
)
df.rename(columns={"Wind": "Wind (km/h)"}, inplace=True)
df.rename(columns={"Precipitation": "Precipitation (mm)"}, inplace=True)
df.rename(columns={"Atmospheric pressure": "Atmospheric pressure (hPa)"}, inplace=True)
df.rename(columns={"Relative humidity": "Relative humidity (%)"}, inplace=True)
df.rename(
    columns={"NSAIDs intake in the last 24h": "NSAIDs intake in the last 24h (mg)"},
    inplace=True,
)
# Remove "mg" from values in the "NSAIDs intake in the last 24h (mg)" column
df["NSAIDs intake in the last 24h (mg)"] = (
    df["NSAIDs intake in the last 24h (mg)"]
    .str.replace("mg", "", regex=False)
    .str.strip()
)
df.rename(
    columns={"General health rating": "General health rating (1=worst, 6=best)"},
    inplace=True,
)
df.rename(
    columns={"General stress rating": "General stress rating (1=worst, 6=best)"},
    inplace=True,
)
df.rename(
    columns={
        "Ease of concentration": "Ease of concentration (1=low concentration, 6=high concentration)"
    },
    inplace=True,
)
df.rename(columns={"Sleep quality": "Sleep quality (1=worst, 6=best)"}, inplace=True)
df.rename(
    columns={
        "Time spent in bed the previous night": "Hours spent in bed the previous night"
    },
    inplace=True,
)
df.rename(
    columns={
        "Alcohol intake in the last 24h": "Alcohol intake in the last 24h (alcohol unit; 25-33cl beer = 1, 1 glass of wine = 1)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Rumination": "Rumination (1 = high rumination, 6 = low rumination)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Anxiety": "Anxiety (1 = high anxiety, 6 = low anxiety)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Physical pain during scan": "Physical pain during scan (1 = high pain, 6 = no pain)"
    },
    inplace=True,
)
# Remove "k" and indicate thousands in the column name
df.rename(
    columns={"Distance walked in the last 24h": "Distance walked in the last 24h (km)"},
    inplace=True,
)
df["Distance walked in the last 24h (km)"] = (
    df["Distance walked in the last 24h (km)"]
    .str.replace("k", "", regex=False)
    .str.strip()
)
df.rename(
    columns={"Calories burned in the last 24h": "Kilocalories burned in the last 24h"},
    inplace=True,
)
df["Kilocalories burned in the last 24h"] = (
    df["Kilocalories burned in the last 24h"]
    .str.replace("k", "", regex=False)
    .str.strip()
)


# PANAS questionnaire
df.rename(
    columns={
        "Interested": "Interested (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Distressed": "Distressed (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Excited": "Excited (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Upset": "Upset (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Strong": "Strong (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Guilty": "Guilty (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Scared": "Scared (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Hostile": "Hostile (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Enthusiastic": "Enthusiastic (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Proud": "Proud (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Irritable": "Irritable (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Alert": "Alert (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Ashamed": "Ashamed (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Inspired": "Inspired (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Nervous": "Nervous (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Determined": "Determined (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Attentive": "Attentive (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Jittery": "Jittery (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Active": "Active (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)
df.rename(
    columns={
        "Afraid": "Afraid (1 = Very slightly or not at all, 2 = A little, 3 = Moderately, 4 = Quite a bit, 5 = Extremely)"
    },
    inplace=True,
)

# Now that we indicated scale range in the column name, we can remove it from values
df.replace("1 (worst)", "1", inplace=True)
df.replace("6 (high concentration)", "2", inplace=True)
df.replace("6 (best)", "2", inplace=True)

# Remove commas that indicate thousands
df["Number of steps made in the last 24h"] = df[
    "Number of steps made in the last 24h"
].str.replace(",", "", regex=False)

# BIDS specification indicates to encode missing values as "n/a"
df.fillna("n/a", inplace=True) 
df.replace("_No response_", "n/a", inplace=True)
df.replace("NONE", "n/a", inplace=True)

# Impute "Slept during session" if it is "n/a", with the union of the columns encoding sleep
slept_columns = [col for col in df.columns if col.startswith("Slept during")]
for index, row in df.iterrows():
    if row["Slept during session"] == "n/a":
        if any(row[col] == "Yes" for col in slept_columns):
            df.at[index, "Slept during session"] = "Yes"
        else:
            df.at[index, "Slept during session"] = "No"

# Session 14 was not finished if the tickbox were not ticked it's not because the subject did not sleep, but because the form was not filled
df.loc[df["session_number"] == "014", slept_columns] = "n/a"

# Save to CSV
df.to_csv("parsed_data.tsv", sep="\t", index=False)
