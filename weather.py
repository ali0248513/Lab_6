import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates = pd.date_range("2026-03-01", periods=15).strftime("%Y-%m-%d").tolist()
city = ["Islamabad", " islamabad", "ISLAMABAD "] * 5
temp = ["32C", "30C", "27C", "33C", "31C", "26C", "34C", "29C",
        "25C", "35C", "28C", "24C", "33C", "30C", "36C"]
hum = [45, 55, 80, 40, 50, 85, 38, np.nan, 88, 35, np.nan, 90, 42, np.nan, 33]
cond = [" sunny", "CLOUDY ", " Rainy", "Sunny", "sunny", "RAINY", "Sunny ", "cloudy",
        "Rainy", "SUNNY", "Cloudy", "cloudy ", "sunny", "Cloudy", "Sunny"]

df = pd.DataFrame({"Date": dates, "City": city, "Temperature": temp,
                   "Humidity": hum, "Condition": cond})
df = pd.concat([df, df.iloc[[-1]]], ignore_index=True)  # add one duplicated row

# (a) cleaning
df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()
df["Temperature"] = df["Temperature"].str.replace("C", "", regex=False).astype(float)
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates()
print("Rows after dropping duplicates:", len(df))
med = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(med)
print("Missing Humidity filled with median:", med)

# (b) one-hot encoding
encoded = pd.get_dummies(df, columns=["Condition"], dtype=int)
print(encoded.filter(like="Condition_"))

# (d) correlation
corr = df["Temperature"].corr(df["Humidity"])
print("Correlation (Temperature, Humidity):", round(corr, 2))

# (e) condition counts
counts = df["Condition"].value_counts()
print("Condition counts:")
print(counts)

# (c)-(f) 2x2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(df["Date"], df["Temperature"], marker="o", color="tomato")
axes[0, 0].set_title("Temperature over Date")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (°C)")
axes[0, 0].tick_params(axis="x", rotation=45)

axes[0, 1].scatter(df["Temperature"], df["Humidity"], color="darkorange")
axes[0, 1].set_title("Temperature vs. Humidity")
axes[0, 1].set_xlabel("Temperature (°C)")
axes[0, 1].set_ylabel("Humidity (%)")

axes[1, 0].pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("Days per Condition")

axes[1, 1].hist(df["Temperature"], bins=5, color="seagreen", edgecolor="white")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (°C)")
axes[1, 1].set_ylabel("Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()
print("Saved weather_dashboard.png")
