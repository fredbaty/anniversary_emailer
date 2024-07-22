import functions

# Calculate dates
current_month_name, current_month_digit, current_year = functions.calculate_dates()

# Define required search year
search_year = current_year + 2

# Load and prepare data
film_df, music_df, faber_df, faber_authors_df, monthly_anniversaries = (
    functions.load_data(current_month_name)
)

# Create Wiki events dictionary
events_dict = functions.add_date_to_wiki_events(
    current_month_name, monthly_anniversaries
)

# Create anniversary DataFrame
anniv_df = functions.process_anniversaries(
    current_month_digit,
    search_year,
    events_dict,
    film_df,
    music_df,
    faber_df,
    faber_authors_df,
)

# Construct email
plain_text, html = functions.construct_email(current_month_name, anniv_df, search_year)

# Send email
functions.send_email(current_month_name, search_year, plain_text, html)
