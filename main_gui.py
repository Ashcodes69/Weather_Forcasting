from tkinter import *
from weather_api import weather_forcast
from datetime import datetime


def get_weather_icon(code):
    """Convert WMO weather code to emoji"""
    icons = {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "☁️",
        45: "🌫️",
        48: "🌫️",
        51: "🌦️",
        53: "🌦️",
        55: "🌧️",
        61: "🌧️",
        63: "🌧️",
        65: "🌧️",
        71: "🌨️",
        73: "🌨️",
        75: "🌨️",
        80: "🌦️",
        81: "🌧️",
        82: "⛈️",
        95: "⛈️",
        96: "⛈️",
        99: "⛈️",
    }
    return icons.get(code, "🌤️")


def get_data():
    name = city_entry.get()
    if len(name) <= 1:
        return None
    else:
        data = weather_forcast(name)
        if data:
            get_date_time(data)
            place_lbl.config(text=name.capitalize())
            get_current_Weather_info(data)
            update_hourly_forecast(data)
            update_weekly_forecast(data)


def get_date_time(data):
    dt = datetime.fromisoformat(data["current_weather"]["time"])
    time_v = dt.strftime("%I:%M %p")
    date_v = dt.strftime("%A, %d %b")
    time_lbl.config(text=time_v)
    date_lbl.config(text=date_v)


def get_current_Weather_info(data):
    temp_lbl.config(text=f"{data['current_weather']['temperature']}°C")

    windspeed = data["current_weather"]["windspeed"]
    windDirection = data["current_weather"]["winddirection"]

    current_time = data["current_weather"]["time"]
    hourly_times = data["hourly"]["time"]
    rain = "N/A"
    rain_prob = "N/A"

    if current_time in hourly_times:
        idx = hourly_times.index(current_time)
        rain = data["hourly"]["rain"][idx]
        rain_prob = data["hourly"]["precipitation_probability"][idx]

    wInfo_lbl.config(
        text=(
            f"Wind: {windspeed} km/h\n"
            f"Wind Direction: {windDirection}°\n"
            f"Rain: {rain} mm\n"
            f"Rain Probability: {rain_prob}%"
        )
    )


def update_hourly_forecast(data):
    # Clear existing hourly cards
    for widget in hourly_cards_frame.winfo_children():
        widget.destroy()

    hourly_times = data["hourly"]["time"][:12]  # Next 12 hours
    hourly_temps = data["hourly"]["temperature_2m"][:12]
    hourly_codes = data["hourly"]["weather_code"][:12]

    for i, (time_str, temp, code) in enumerate(
        zip(hourly_times, hourly_temps, hourly_codes)
    ):
        dt = datetime.fromisoformat(time_str)
        hour = dt.strftime("%I%p")
        icon = get_weather_icon(code)

        card = Frame(hourly_cards_frame, bg=BG_CARD, width=90, height=110)
        card.pack(side=LEFT, padx=5)
        card.pack_propagate(False)

        Label(card, text=hour, bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica", 10)).pack(
            pady=5
        )
        Label(card, text=icon, bg=BG_CARD, fg=TEXT_MAIN, font=("Helvetica", 20)).pack()
        Label(
            card,
            text=f"{temp}°C",
            bg=BG_CARD,
            fg=ACCENT,
            font=("Helvetica", 12, "bold"),
        ).pack(pady=5)


def update_weekly_forecast(data):
    # Clear existing weekly cards
    for widget in weekly_cards_frame.winfo_children():
        widget.destroy()

    # Group by day - get daily max temp and most common weather code
    daily_data = {}

    for i, time_str in enumerate(data["hourly"]["time"]):
        dt = datetime.fromisoformat(time_str)
        day_key = dt.date()

        if day_key not in daily_data:
            daily_data[day_key] = {"temps": [], "codes": []}

        daily_data[day_key]["temps"].append(data["hourly"]["temperature_2m"][i])
        daily_data[day_key]["codes"].append(data["hourly"]["weather_code"][i])

    # Create cards for next 7 days
    for day_key in sorted(daily_data.keys())[:7]:
        day_data = daily_data[day_key]
        dt = datetime.combine(day_key, datetime.min.time())
        day_name = dt.strftime("%a")

        max_temp = max(day_data["temps"])
        most_common_code = max(set(day_data["codes"]), key=day_data["codes"].count)
        icon = get_weather_icon(most_common_code)

        card = Frame(weekly_cards_frame, bg=BG_CARD, width=100, height=130)
        card.pack(side=LEFT, padx=8)
        card.pack_propagate(False)

        Label(
            card, text=day_name, bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica", 12)
        ).pack(pady=6)
        Label(card, text=icon, bg=BG_CARD, fg=TEXT_MAIN, font=("Helvetica", 22)).pack()
        Label(
            card,
            text=f"{max_temp}°C",
            bg=BG_CARD,
            fg=ACCENT,
            font=("Helvetica", 14, "bold"),
        ).pack(pady=6)


root = Tk()
root.title("Weather Forecast")
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()
root.geometry(f"{scr_width}x{scr_height}")
root.config(bg="#121212")

# Color palette
BG_MAIN = "#121212"
BG_PANEL = "#1E1E1E"
BG_CARD = "#2A2A2A"
ACCENT = "#F9A826"
TEXT_MAIN = "#EAEAEA"
TEXT_MUTED = "#B0B0B0"

# ================= LEFT PANEL (Current Weather) =================
left_panel = Frame(root, bg=BG_PANEL)
left_panel.place(relx=0, rely=0, relwidth=0.35, relheight=1)

time_lbl = Label(
    left_panel, text="00:00", font=("Helvetica", 26, "bold"), bg=BG_PANEL, fg=TEXT_MAIN
)
time_lbl.pack(pady=(40, 5))

date_lbl = Label(
    left_panel, text="", font=("Helvetica", 14), bg=BG_PANEL, fg=TEXT_MUTED
)
date_lbl.pack(pady=(0, 30))

place_lbl = Label(
    left_panel, text="", font=("Helvetica", 22, "bold"), bg=BG_PANEL, fg=ACCENT
)
place_lbl.pack(pady=10)

temp_lbl = Label(
    left_panel, text="", font=("Helvetica", 48, "bold"), bg=BG_PANEL, fg=TEXT_MAIN
)
temp_lbl.pack(pady=20)

wInfo_lbl = Label(
    left_panel,
    text="",
    font=("Helvetica", 14),
    bg=BG_PANEL,
    fg=TEXT_MUTED,
    justify="center",
)
wInfo_lbl.pack(pady=10)

# ================= RIGHT PANEL =================
right_panel = Frame(root, bg=BG_MAIN)
right_panel.place(relx=0.35, rely=0, relwidth=0.65, relheight=1)

# ---- Top Search Bar ----
search_frame = Frame(right_panel, bg=BG_MAIN)
search_frame.pack(fill=X, pady=20, padx=30)

city_entry = Entry(
    search_frame,
    font=("Helvetica", 16),
    bg=BG_CARD,
    fg=TEXT_MAIN,
    insertbackground=TEXT_MAIN,
    relief="flat",
)
city_entry.pack(side=LEFT, fill=X, expand=True, ipady=8)

Button(
    search_frame,
    text="Search",
    font=("Helvetica", 14, "bold"),
    bg=ACCENT,
    fg="black",
    relief="flat",
    padx=20,
    command=get_data,
).pack(side=LEFT, padx=15)

# ---- Hourly Forecast ----
hourly_frame = Frame(right_panel, bg=BG_PANEL)
hourly_frame.pack(fill=X, padx=30, pady=15)

Label(
    hourly_frame,
    text="Hourly Forecast",
    font=("Helvetica", 16, "bold"),
    bg=BG_PANEL,
    fg=TEXT_MAIN,
).pack(anchor="w", pady=8, padx=10)

# Scrollable hourly cards container
hourly_container = Frame(hourly_frame, bg=BG_PANEL)
hourly_container.pack(fill=X, padx=10, pady=5)

canvas_hourly = Canvas(hourly_container, bg=BG_PANEL, height=130, highlightthickness=0)
scrollbar_hourly = Scrollbar(
    hourly_container, orient=HORIZONTAL, command=canvas_hourly.xview
)
hourly_cards_frame = Frame(canvas_hourly, bg=BG_PANEL)

hourly_cards_frame.bind(
    "<Configure>",
    lambda e: canvas_hourly.configure(scrollregion=canvas_hourly.bbox("all")),
)

canvas_hourly.create_window((0, 0), window=hourly_cards_frame, anchor="nw")
canvas_hourly.configure(xscrollcommand=scrollbar_hourly.set)

canvas_hourly.pack(side=TOP, fill=X, expand=True)
scrollbar_hourly.pack(side=BOTTOM, fill=X)

# ---- Weekly Forecast ----
weekly_frame = Frame(right_panel, bg=BG_MAIN)
weekly_frame.pack(fill=BOTH, expand=True, padx=30, pady=15)

Label(
    weekly_frame,
    text="7-Day Forecast",
    font=("Helvetica", 16, "bold"),
    bg=BG_MAIN,
    fg=TEXT_MAIN,
).pack(anchor="w", pady=10)

weekly_cards_frame = Frame(weekly_frame, bg=BG_MAIN)
weekly_cards_frame.pack(fill=X, pady=10)

root.mainloop()
