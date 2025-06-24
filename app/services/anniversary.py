import wikipediaapi as wa
import re
import pandas as pd
from random import choice
import sqlite3
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


def calculate_dates(target_month=None, target_year=None):
    """Calculate dates based on input or current date"""
    now = datetime.now()

    if target_month:
        current_month_digit = f"{int(target_month):02d}"
        # Convert month number to name
        current_month_name = datetime(2000, int(target_month), 1).strftime("%B")
    else:
        current_month_name = now.strftime("%B")
        current_month_digit = now.strftime("%m")

    current_year = target_year if target_year else now.year

    return current_month_name, current_month_digit, current_year


def load_data(db, current_month_name, current_month_digit, sender_email=None):
    """Load data from the database and Wikipedia"""

    # Get records filtered by month directly from the database
    film_records = db.get_films_by_month(current_month_digit)
    film_df = pd.DataFrame(film_records)
    if not film_df.empty:
        film_df["release_date"] = pd.to_datetime(film_df["release_date"])

    music_records = db.get_albums_by_month(current_month_digit)
    music_df = pd.DataFrame(music_records)
    if not music_df.empty:
        music_df["release_date"] = pd.to_datetime(music_df["release_date"])

    faber_records = db.get_books_by_month(current_month_digit)
    faber_df = pd.DataFrame(faber_records)
    if not faber_df.empty:
        faber_df["release_date"] = pd.to_datetime(faber_df["release_date"])

    # Get author data by birth and death month
    birth_records = db.get_authors_by_birth_month(current_month_digit)
    death_records = db.get_authors_by_death_month(current_month_digit)

    # Combine birth and death records into a single DataFrame
    faber_authors_records = birth_records + death_records
    faber_authors_df = pd.DataFrame(faber_authors_records)
    if not faber_authors_df.empty:
        faber_authors_df["birth"] = pd.to_datetime(faber_authors_df["birth"])
        faber_authors_df["death"] = pd.to_datetime(faber_authors_df["death"])

    # Access Wikipedia API
    wiki = wa.Wikipedia(f"AnniversariesUpdater/1.0 (example@example.com)", "en")
    monthly_anniversaries = wiki.page(
        f"Wikipedia:Selected_anniversaries/{current_month_name}"
    )

    return film_df, music_df, faber_df, faber_authors_df, monthly_anniversaries


def add_date_to_wiki_events(current_month_name, monthly_anniversaries):
    events_dict = {}
    date = ""
    date_object = None
    for line in monthly_anniversaries.text.splitlines():
        if line.strip():
            if line.startswith(current_month_name):
                date = line.split(":")[0].strip()
                date_object = datetime.strptime(date, "%B %d")
            elif date_object is not None:
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
    """Check for anniversaries using vectorized operations where possible"""
    if df.empty:
        return pd.DataFrame(columns=ANNIV_DF_COLS)

    temp_df_list = []

    if is_author:
        # Process birth anniversaries
        authors_df = df.copy()
        authors_df["event_year"] = authors_df["birth"].dt.year
        authors_df["yrs_since_event"] = search_year - authors_df["event_year"]
        authors_df["event_day"] = authors_df["birth"].dt.strftime("%d %B")

        # Filter to only keep significant anniversaries
        significant_births = authors_df[
            authors_df["yrs_since_event"].isin(ANNIVERSARIES)
        ]

        for _, row in significant_births.iterrows():
            anniv_date = row["birth"] + pd.DateOffset(years=row["yrs_since_event"])
            temp_df_list.append(
                create_new_row(
                    ANNIV_DF_COLS,
                    DATA_TYPES["birth_data"],
                    row["birth"],
                    anniv_date,
                    row["event_day"],
                    row["yrs_since_event"],
                    row["author"],
                    "",
                    "",
                )
            )

        # Process death anniversaries for authors with death dates
        death_df = df.dropna(subset=["death"]).copy()
        if not death_df.empty:
            death_df["event_year"] = death_df["death"].dt.year
            death_df["yrs_since_event"] = search_year - death_df["event_year"]
            death_df["event_day"] = death_df["death"].dt.strftime("%d %B")

            # Filter to only keep significant anniversaries
            significant_deaths = death_df[
                death_df["yrs_since_event"].isin(ANNIVERSARIES)
            ]

            for _, row in significant_deaths.iterrows():
                anniv_date = row["death"] + pd.DateOffset(years=row["yrs_since_event"])
                temp_df_list.append(
                    create_new_row(
                        ANNIV_DF_COLS,
                        DATA_TYPES["death_data"],
                        row["death"],
                        anniv_date,
                        row["event_day"],
                        row["yrs_since_event"],
                        row["author"],
                        "",
                        "",
                    )
                )
    else:
        # Process regular anniversaries (films, albums, books)
        events_df = df.copy()
        events_df["event_year"] = events_df["release_date"].dt.year
        events_df["yrs_since_event"] = search_year - events_df["event_year"]
        events_df["event_day"] = events_df["release_date"].dt.strftime("%d %B")

        # Filter to only keep significant anniversaries
        significant_events = events_df[events_df["yrs_since_event"].isin(ANNIVERSARIES)]

        for _, row in significant_events.iterrows():
            anniv_date = row["release_date"] + pd.DateOffset(
                years=row["yrs_since_event"]
            )
            binding = row.get("binding", "").lower() if is_book else ""

            temp_df_list.append(
                create_new_row(
                    ANNIV_DF_COLS,
                    DATA_TYPES[data_type],
                    row["release_date"],
                    anniv_date,
                    row["event_day"],
                    row["yrs_since_event"],
                    row["artist"],
                    row["title"],
                    binding,
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


def format_anniversaries(db, current_month_name, anniv_df, search_year):
    """Format anniversaries for display in web interface"""
    # Get a random fact
    opening_fact = db.get_random_fact()

    # First, add a numeric day field for proper sorting
    anniv_df["day_num"] = anniv_df["anniv_day"].str.extract(r"^(\d+)").astype(int)

    # Sort by the numeric day
    df = anniv_df.sort_values(["day_num"])

    # Prepare categories
    categories = {"Wiki": [], "Film": [], "Album": [], "Faber": []}

    for _, row in df.iterrows():
        anniv_day = row["anniv_day"]
        anniv = row["anniv"]
        artist = row["artist"]
        title = row["title"]
        binding = row["binding"]
        data_type = row["data_type"]

        # Create consistent formatting with HTML spans for styling
        date_span = f'<span class="date">{anniv_day}</span>'
        anniversary_span = f'<span class="anniversary">{anniv} years since</span>'

        # Set event description based on data type
        event_desc = ""
        if data_type == "Wiki":
            event_desc = f'<span class="event-desc">{title}</span>'
        elif data_type == "Film":
            event_desc = f'<span class="event-desc">the release of <em>{title}</em> - {artist}</span>'
        elif data_type == "Album":
            event_desc = f'<span class="event-desc">the release of <em>{title}</em> - {artist}</span>'
        elif data_type == "Faber_Book":
            event_desc = f'<span class="event-desc">the {binding} release of <em>{title}</em> - {artist}</span>'
        elif data_type == "Faber_Death":
            event_desc = f'<span class="event-desc">the death of {artist}</span>'
        elif data_type == "Faber_Birth":
            event_desc = f'<span class="event-desc">the birth of {artist}</span>'

        formatted_item = f"{date_span} {anniversary_span} {event_desc}"

        if data_type in ["Faber_Book", "Faber_Death", "Faber_Birth"]:
            categories["Faber"].append(formatted_item)
        else:
            categories[data_type].append(formatted_item)

    return {
        "fact": opening_fact,
        "month": current_month_name,
        "year": search_year,
        "categories": categories,
    }
