from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import atexit

from app.models.database import Database
from app.services import anniversary as services

# Initialize the Flask app
app = Flask(
    __name__,
    template_folder="/app/templates",
    static_folder="/app/static",
)
app.config["SECRET_KEY"] = os.urandom(24)

# Initialize the database
db_path = "/app/database.db"
db = Database(db_path)

# Register a function to close the database connection when the app shuts down
atexit.register(db.close_connection)


def index():
    """Home page with form to select month and year"""
    current_year = datetime.now().year

    # Default to current month and year
    default_month = datetime.now().month
    default_year = current_year

    if request.method == "POST":
        # Get form data
        month = request.form.get("month", default_month)
        year = request.form.get("year", default_year)

        # Redirect to results page
        return redirect(url_for("results", month=month, year=year))

    # Generate list of months for the dropdown
    months = [(i, datetime(2000, i, 1).strftime("%B")) for i in range(1, 13)]

    # Generate list of years for the dropdown (current year to current year + 10)
    years = list(range(current_year, current_year + 11))

    return render_template(
        "index.html",
        months=months,
        years=years,
        default_month=default_month,
        default_year=default_year,
    )


def results(month, year):
    """Results page showing anniversaries for the selected month and year"""
    # Calculate dates
    current_month_name, current_month_digit, _ = services.calculate_dates(month, year)

    # Load data
    film_df, music_df, faber_df, faber_authors_df, monthly_anniversaries = (
        services.load_data(db, current_month_name, current_month_digit)
    )

    # Create Wiki events dictionary
    events_dict = services.add_date_to_wiki_events(
        current_month_name, monthly_anniversaries
    )

    # Create anniversary DataFrame
    anniv_df = services.process_anniversaries(
        current_month_digit,
        year,
        events_dict,
        film_df,
        music_df,
        faber_df,
        faber_authors_df,
    )

    # Format anniversaries for display
    formatted_data = services.format_anniversaries(
        db, current_month_name, anniv_df, year
    )

    return render_template("results.html", data=formatted_data)
