import wikipediaapi as wa
import re
import pandas as pd
from random import choice
import auth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


ANNIVERSARIES = [
    10,
    20,
    25,
    30,
    40,
    50,
    60,
    70,
    75,
    80,
    90,
    100,
    125,
    150,
    175,
    200,
    250,
    300,
]

DATA_TYPES = {
    "wiki_data": "Wiki",
    "film_data": "Film",
    "album_data": "Album",
    "faber_data": "Faber_Book",
    "birth_data": "Faber_Birth",
    "death_data": "Faber_Death",
}

ANNIV_DF_COLS = [
    "data_type",
    "orig_date",
    "anniv_date",
    "anniv_day",
    "anniv",
    "artist",
    "title",
    "binding",
]


def calculate_dates():
    now = datetime.now()
    current_month_name = now.strftime("%B")
    current_month_digit = now.strftime("%m")
    current_year = now.year

    return current_month_name, current_month_digit, current_year


def load_data(current_month_name):
    film_df = pd.read_csv("./data/film_1001.csv")
    film_df["release_date"] = pd.to_datetime(
        film_df["release_date"], format="ISO8601", utc=True
    )

    music_df = pd.read_csv("./data/album_1001.csv")
    music_df["release_date"] = pd.to_datetime(
        music_df["release_date"], format="ISO8601", utc=True
    )

    faber_df = pd.read_csv("./data/faber_1001.csv")
    faber_df["release_date"] = pd.to_datetime(
        faber_df["release_date"], format="ISO8601", utc=True
    )

    faber_authors_df = pd.read_csv("./data/faber_authors.csv")
    faber_authors_df["birth"] = pd.to_datetime(
        faber_authors_df["birth"], format="ISO8601", utc=True
    )
    faber_authors_df["death"] = pd.to_datetime(
        faber_authors_df["death"], format="ISO8601", utc=True
    )

    wiki = wa.Wikipedia(f"AnniversariesUpdater/1.0 ({auth.SENDER})", "en")
    monthly_anniversaries = wiki.page(
        f"Wikipedia:Selected_anniversaries/{current_month_name}"
    )

    return film_df, music_df, faber_df, faber_authors_df, monthly_anniversaries


def add_date_to_wiki_events(current_month_name, monthly_anniversaries):
    events_dict = {}
    date = ""
    for line in monthly_anniversaries.text.splitlines():
        if line.strip():
            if line.startswith(current_month_name):
                date = line.split(":")[0].strip()
                date_object = datetime.strptime(date, "%B %d")
            else:
                events_dict.update({line.strip(): date_object})
    return events_dict


def create_new_row(columns, *args):
    return pd.DataFrame([dict(zip(columns, args))])


def check_wiki_anniversaries(data_type, events_dict, search_year):
    temp_df_list = []
    for event, date in events_dict.items():
        event = event.replace(" (pictured)", "")
        match = re.search(r"^\d{3,4}", event)
        if match:
            event_year = int(match.group())
            event_date = date.replace(year=event_year)
            event_day = event_date.strftime("%d %B")
            event = event.replace(match.group(), "")
            event = event[3:]
            yrs_since_event = search_year - event_year
            if yrs_since_event in ANNIVERSARIES:
                anniv_date = event_date + pd.DateOffset(years=yrs_since_event)
                temp_df_list.append(
                    create_new_row(
                        ANNIV_DF_COLS,
                        DATA_TYPES[data_type],
                        event_date,
                        anniv_date,
                        event_day,
                        yrs_since_event,
                        "",
                        event,
                        "",
                    )
                )
    return (
        pd.concat(temp_df_list, ignore_index=True)
        if temp_df_list
        else pd.DataFrame(columns=ANNIV_DF_COLS)
    )


def check_anniversaries(
    current_month_digit, data_type, df, search_year, is_book=False, is_author=False
):
    temp_df_list = []
    for _, row in df.iterrows():
        if is_author:
            artist = row["author"]
            event = row["birth"]
            event_month = event.strftime("%m")
            event_day = event.strftime("%d %B")
            if pd.notna(row["death"]):
                death = row["death"]
                death_month = death.strftime("%m")
                death_day = death.strftime("%d %B")
            else:
                death, death_month, death_day = None, None, None

        else:
            artist = row["artist"]
            event = row["release_date"]
            event_month = event.strftime("%m")
            event_day = event.strftime("%d %B")
            death, death_month, death_day = None, None, None

        title = row["title"] if "title" in df.columns else ""
        binding = row["binding"].lower() if is_book and "binding" in df.columns else ""

        if event_month == current_month_digit:
            event_year = int(event.strftime("%Y"))
            yrs_since_event = search_year - event_year
            if yrs_since_event in ANNIVERSARIES:
                anniv_date = event + pd.DateOffset(years=yrs_since_event)
                temp_df_list.append(
                    create_new_row(
                        ANNIV_DF_COLS,
                        DATA_TYPES[data_type],
                        event,
                        anniv_date,
                        event_day,
                        yrs_since_event,
                        artist,
                        title,
                        binding,
                    )
                )

        if is_author and death_month == current_month_digit:
            death_year = int(death.strftime("%Y"))
            yrs_since_death = search_year - death_year
            if yrs_since_death in ANNIVERSARIES:
                anniv_date = death + pd.DateOffset(years=yrs_since_death)
                temp_df_list.append(
                    create_new_row(
                        ANNIV_DF_COLS,
                        DATA_TYPES["death_data"],
                        death,
                        anniv_date,
                        death_day,
                        yrs_since_death,
                        artist,
                        "",
                        "",
                    )
                )
    return (
        pd.concat(temp_df_list, ignore_index=True)
        if temp_df_list
        else pd.DataFrame(columns=ANNIV_DF_COLS)
    )


def process_anniversaries(
    current_month_digit,
    search_year,
    events_dict,
    film_df,
    music_df,
    faber_df,
    faber_authors_df,
):
    functions = [
        (check_wiki_anniversaries, ("wiki_data", events_dict, search_year)),
        (
            check_anniversaries,
            (current_month_digit, "film_data", film_df, search_year, False, False),
        ),
        (
            check_anniversaries,
            (current_month_digit, "album_data", music_df, search_year, False, False),
        ),
        (
            check_anniversaries,
            (current_month_digit, "faber_data", faber_df, search_year, True, False),
        ),
        (
            check_anniversaries,
            (
                current_month_digit,
                "birth_data",
                faber_authors_df,
                search_year,
                False,
                True,
            ),
        ),
    ]
    anniv_df = pd.DataFrame()

    for func, args in functions:
        result_df = func(*args)
        if not result_df.empty:
            anniv_df = pd.concat([anniv_df, result_df], ignore_index=True)

    return anniv_df


def strip_html_tags(string):
    tags = {"<br>": "\n", "<em>": "", "</em>": "", "<li>": "", "</li>": ""}
    pattern = re.compile("|".join(tags.keys()))
    plain_string = pattern.sub(lambda x: tags[re.escape(x.group(0))], string)
    return plain_string


def construct_email(current_month_name, anniv_df, search_year):
    df = anniv_df.sort_values(["anniv_day"])

    with open("./data/facts.txt", "r") as fact_file:
        facts = fact_file.readlines()
        opening_fact = choice(facts).strip()

    html_strings = {"Wiki": [], "Film": [], "Album": [], "Faber": []}
    plain_strings = {"Wiki": [], "Film": [], "Album": [], "Faber": []}

    for _, row in df.iterrows():
        anniv_day = row["anniv_day"]
        anniv = row["anniv"]
        artist = row["artist"]
        title = row["title"]
        binding = row["binding"]
        data_type = row["data_type"]

        format_strings = {
            "Wiki": f"{anniv_day} - {anniv} years since: {title}",
            "Film": f"{anniv_day} - {anniv} years since the release of <em>{title}</em> - {artist}.",
            "Album": f"{anniv_day} - {anniv} years since the release of <em>{title}</em> - {artist}.",
            "Faber_Book": f"{anniv_day} - {anniv} years since the {binding} release of <em>{title}</em> - {artist}.",
            "Faber_Death": f"{anniv_day} - {anniv} years since the death of {artist}.",
            "Faber_Birth": f"{anniv_day} - {anniv} years since the birth of {artist}.",
        }

        if data_type in ["Faber_Book", "Faber_Death", "Faber_Birth"]:
            html_strings["Faber"].append(format_strings[data_type] + "<br>")
            plain_strings["Faber"].append(strip_html_tags(format_strings[data_type]))
        else:
            html_strings[data_type].append(format_strings[data_type] + "<br>")
            plain_strings[data_type].append(strip_html_tags(format_strings[data_type]))

    for key in html_strings:
        html_strings[key] = "".join(html_strings[key])
        plain_strings[key] = "".join(plain_strings[key])

    plain_fact = strip_html_tags(opening_fact)

    replacements = {
        "[HTML_FACT]": opening_fact,
        "[PLAIN_FACT]": plain_fact,
        "[MONTH]": current_month_name,
        "[YEAR]": str(search_year),
        "[HTML_WIKI]": html_strings["Wiki"],
        "[HTML_FABER]": html_strings["Faber"],
        "[HTML_FILM]": html_strings["Film"],
        "[HTML_MUSIC]": html_strings["Album"],
        "[PLAIN_WIKI]": plain_strings["Wiki"],
        "[PLAIN_FABER]": plain_strings["Faber"],
        "[PLAIN_FILM]": plain_strings["Film"],
        "[PLAIN_MUSIC]": plain_strings["Album"],
    }
    pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))

    with open("./data/plain_text.txt", "r") as plain_template:
        template = plain_template.read()
        plain_text = pattern.sub(lambda x: replacements[x.group(0)], template)

    with open("./data/html.html", "r") as html_template:
        template = html_template.read()
        html = pattern.sub(lambda x: replacements[x.group(0)], template)

    return plain_text, html


def send_email(current_month_name, search_year, plain_text, html):
    subject = f"{current_month_name} {search_year} anniversaries"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = auth.SENDER
    message["To"] = auth.TO
    message["Bcc"] = auth.BCC

    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP(auth.SMTP_ADDR) as connection:
        connection.starttls()
        connection.login(user=auth.SENDER, password=auth.GM_PWD)
        connection.send_message(message)

    print("Email successfully sent.")
