# Anniversary Finder Web App

## Overview

A lightweight web application that helps you discover noteworthy cultural and historical anniversaries for any given month and year. The app integrates data from various sources:

- Books and authors (from Faber)
- Films from the "1001 Movies You Must See Before You Die" list
- Albums from the "1001 Albums You Must Hear Before You Die" list
- Historical events from Wikipedia's "On This Day" pages
- Random interesting facts from QI

## Features

- Simple, responsive web interface
- Select any month and year to find significant anniversaries
- Results organized by category (Books/Authors, Films, Music, Historical Events)
- SQLite database for efficient data storage
- Lightweight design for easy deployment with Docker

## Project Structure

```
anniversary_finder/
├── app/                       # Main application package
│   ├── models/                # Database models
│   ├── routes/                # Web routes and views
│   ├── services/              # Business logic
│   └── utils/                 # Helper utilities
├── data/                      # Data files (facts.txt)
├── static/                    # CSS, JS, and other static files
├── templates/                 # HTML templates
├── app.py                     # Application entry point
├── wsgi.py                    # WSGI entry point for production servers
├── gunicorn_config.py         # Gunicorn configuration
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── docker-entrypoint.sh       # Container initialization script
├── docker-manage.sh           # Helper script for Docker management
└── requirements.txt           # Python dependencies
```

## Deployment with Docker

The simplest way to deploy this application is using Docker:

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/anniversary_finder.git
cd anniversary_finder
```

2. **Start the application using the management script:**
```bash
./docker-manage.sh start
```

3. **Access the application:**
Open your browser and navigate to:
```
http://localhost:8989
```

4. **Management commands:**
```bash
./docker-manage.sh status    # Check container status
./docker-manage.sh logs      # View logs
./docker-manage.sh stop      # Stop the application
./docker-manage.sh restart   # Restart the application
./docker-manage.sh rebuild   # Rebuild after code changes
```

Alternatively, you can use Docker Compose commands directly:
```bash
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs
docker-compose ps             # Check status
```

## Docker Configuration

The application is configured to run in Docker with the following settings:

- **Port**: The application runs on port 8989
- **Data Persistence**: 
  - Database file is persisted outside the container
  - Logs are stored outside the container
  - Data files are mounted from the host
- **Health Checks**: The container includes automatic health monitoring

For more detailed Docker deployment information, see the [Docker Deployment Guide](DOCKER.md).

## Usage

1. Select a month and year from the dropdown menus
2. Click "Find Anniversaries" to see all significant anniversaries for that period
3. Browse the results organized by category

## Example Output

<html>
  <body>
    <strong>QI FACT OF THE MONTH</strong>
    <p style="margin-top: 0;margin-bottom: 25;"><em>Beyonce Knowles is an 8th cousin, four times removed, of Gustav Mahler.</em></p>
    <p>* * *</p>
    <p style="margin-top: 25; margin-bottom: 25;">In <strong>July 2026</strong> the following anniversaries will be marked:</p>
    <strong>FABER</strong>
    <p style="margin-top: 0">07 July - 10 years since the paperback release of <em>Strange Star</em> - Emma Carroll.<br>07 July - 10 years since the paperback release of <em>Doing Good Better</em> - Dr William MacAskill.<br>07 July - 10 
years since the paperback release of <em>A Strangeness in My Mind</em> - Orhan Pamuk.<br>09 July - 25 years since the paperback release of <em>That Summer</em> - Andrew Greig.<br>13 July - 75 years since the death of Arnold Schoenberg.<br>14 July - 10 years since the paperback release of <em>The Ex</em> - Alafair Burke.<br>23 July - 25 years since the paperback release of <em>Kitchen</em> - Banana Yoshimoto.<br>28 July - 10 years since the paperback release of <em>Secret Footballer</em> - Anon.<br></p>
    <strong>FILMS</strong>
    <p style="margin-top: 0">05 July - 30 years since the release of <em>Breaking the Waves</em> - Lars von Trier.<br>14 July - 10 years since the release of <em>Ghostbusters</em> - Paul Feig.<br>14 July - 10 years since the release of <em>Toni Erdmann</em> - Maren Ade.<br>17 July - 30 years since the release of <em>Crash</em> - David Cronenberg.<br>18 July - 40 years since the release of <em>Aliens</em> - James Cameron.<br>20 July - 25 years since the release of <em>Spirited Away</em> - Hayao Miyazaki.<br>26 July - 20 years since the release of <em>Little Miss Sunshine</em> - Jonathan Dayton.<br></p>
    <strong>MUSIC</strong>
    <p style="margin-top: 0">03 July - 25 years since the release of <em>White Blood Cells</em> - The White Stripes.<br>03 July - 20 years since the release of <em>Black Holes and Revelations</em> - Muse.<br>07 July - 70 years since the 
release of <em>Ellington at Newport</em> - Duke Ellington.<br>15 July - 60 years since the release of <em>Roger the Engineer</em> - The Yardbirds.<br>16 July - 25 years since the release of <em>Hot Shots II</em> - The Beta Band.<br>18 July - 60 years since the release of <em>Fifth Dimension</em> - The Byrds.<br>22 July - 60 years since the release of <em>Blues Breakers</em> - John Mayall.<br>23 July - 25 years since the release of <em>Rings Around The World</em> - Super Furry Animals.<br>23 July - 30 years since the release of <em>Logical Progression</em> - LTJ Bukem.<br>23 July - 30 years since the release of <em>Tidal</em> - Fiona Apple.<br>25 July - 20 years since the release of <em>Savane</em> - Ali Farka Touré.<br>30 July - 25 years since the release of <em>Is This It</em> - The Strokes.<br>31 July - 25 years since the release of <em>Time (The Revelator)</em> - Gillian Welch.<br></p>
    <strong>EVENTS</strong>
    <p style="margin-top: 0">06 July - 90 years since: A major breach of the Manchester Bolton & Bury Canal in England sent millions of gallons of water cascading 300 feet (90 m) into the River Irwell.<br>08 July - 60 years since: King Mwambutsa IV of Burundi was deposed in a coup d'état by his son, Prince Charles Ndizi.<br>10 July - 60 years since: Martin Luther King Jr. led a rally in support of the Chicago Freedom Movement, one of the most ambitious civil-rights campaigns in the northern United States.<br>10 July - 20 years since: Typhoon Ewiniar made landfall in South Korea, causing damages across the country amounting to 2.06 trillion won (US$1.4 billion).<br>11 July - 90 years since: New York City's Triborough Bridge, the "biggest traffic machine ever built", opened to traffic.<br>21 July - 80 years since: After weeks of unrest, rioters lynched Bolivian president Gualberto Villarroel, desecrating and hanging his corpse in the streets of La Paz.<br>26 July - 90 years since: The Canadian National Vimy Memorial, dedicated to the Canadian Expeditionary Force members killed in the First World War, was unveiled in Pas-de-Calais, France.<br></p>
  </body>
</html>
