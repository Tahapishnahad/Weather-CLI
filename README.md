# 🌦 Weather CLI

A command-line weather application built with Python that retrieves current weather information for a specified city and displays it in the terminal.

## ✨ Features

- 🌍 Search for a city by name
- 🌡 Get the current temperature
- 💨 Display wind speed
- ☁️ Show the current weather condition
- 📍 Display the city's geographic coordinates
- 🕒 Show the local date and time
- ⚠️ Handle network errors and invalid city names

## 🛠 Built With

- **Python** — application logic
- **Requests** — HTTP requests and API communication
- **Open-Meteo API** — geocoding and weather data
- **JSON** — processing API responses

## 📋 Prerequisites

Before running the application, make sure you have:

- Python installed
- An active internet connection

**Note:** This project uses the Open-Meteo API and does not require an API key for its current implementation.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tahapishnahad/Weather-CLI.git
```

### 2. Navigate to the project directory

```bash
cd Weather-CLI
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the program by providing a city name as a command-line argument:

```bash
python weather.py Tehran
```

You can replace `Tehran` with another city name, for example:

```bash
python weather.py London
```

The application retrieves the city's coordinates, fetches its current weather data, and displays the results in the terminal.

## 📷 Example Output

The application displays information similar to the following:

```text
╔══════════════════════════════════╗
║          🌦 WEATHER CLI          ║
╚══════════════════════════════════╝

📍 Tehran | Iran

🌡 Temperature : 24.5 °C
💨 Wind        : 12.0 km/h
☁️ Weather     : Mainly clear

🌎 Latitude    : 35.69
🌎 Longitude   : 51.42

──────────────────────────────────
🕐 Updated : 2026-10-17 | 14:30
```

*The values above are illustrative and do not represent live weather data.*

## 📚 What I Learned

While building this project, I practiced:

- Making HTTP requests with Python
- Working with REST APIs
- Parsing JSON responses
- Handling exceptions and network errors
- Organizing code into functions
- Building command-line applications
- Working with geographic coordinates

## 🔮 Future Improvements

- [ ] Display weather forecasts for upcoming days
- [ ] Improve error handling and input validation
- [ ] Enhance terminal formatting
- [ ] Add automated tests
- [ ] Support more weather information

## 👨‍💻 Author

**Taha** — [@Tahapishnahad](https://github.com/Tahapishnahad)

## 📝 Credits

This README was written with the assistance of ChatGPT by OpenAI. The project implementation is my own work; AI assistance was used to help write and organize the documentation.
This README was written with the assistance of ChatGPT by OpenAI. The project implementation is my own work; AI assistance was used to help write and organize the documentation.
