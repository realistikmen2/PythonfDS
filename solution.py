"""МКР з Python for Data Science — наскрізний кейс «Метеослужба».

ШАБЛОН ДЛЯ СТУДЕНТА. Заповніть кожен пункт у блоках 1–4 та допишіть
ВИСНОВКИ у docstring наприкінці файлу.

Перед запуском скрипта підніміть СВІЙ Docker-контейнер з MySQL:

    docker pull <DOCKER_USER>/pfds-mkr-g<N>-<NN>
    docker run -d -p 3306:3306 --name mkr <DOCKER_USER>/pfds-mkr-g<N>-<NN>

(g<N>-<NN> — ваші група і номер у журналі, видається викладачем)

Потім чекайте ~30 секунд на ініціалізацію MySQL і запускайте:

    python solution.py

Графіки зберігаються в підпапку `plots/` поряд зі скриптом.
"""

# ====================================================================
# Прізвище, ім'я, по батькові: Глущенко Д.С
# Група:                       ЗК-33
# Дата виконання:              12.05.26
# ====================================================================

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# =========================
# DB
# =========================
DB_USER = "student"
DB_PASSWORD = "student"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "meteo"

PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

# =========================
def section(title):
    print("\n" + "="*60)
    print(title)
    print("="*60)

# =========================
def load_observations(retries=15, delay=3):
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)

    for i in range(retries):
        try:
            df = pd.read_sql("SELECT * FROM observations", engine)
            print(f"✅ Підключено. Рядків: {len(df)}")
            return df
        except OperationalError:
            print("⏳ Чекаємо MySQL...")
            time.sleep(delay)

    raise RuntimeError("DB not ready")

# =========================
# БЛОК 1
# =========================
def block_1_numpy(df):
    section("БЛОК 1 NumPy")

    T = df["temperature_c"].to_numpy(dtype=float)
    RH = df["humidity_pct"].to_numpy(dtype=float)
    WS = df["wind_speed_ms"].to_numpy(dtype=float)

    obs_id = df["obs_id"].to_numpy()
    dt = df["datetime"].to_numpy()

    # 1
    T_app = T - (100 - RH) / 5
    print("T_app example:", T_app[:5])

    # 2
    T_clean = np.where((T > 60) | (T < -60), np.nan, T)
    WS_clean = np.where(WS > 100, np.nan, WS)

    print("Outliers T:", np.sum((T > 60) | (T < -60)))
    print("Outliers WS:", np.sum(WS > 100))

    # 3
    mean = np.nanmean(T_clean)
    median = np.nanmedian(T_clean)
    std = np.sqrt(np.nanmean((T_clean - mean) ** 2))

    print("mean:", mean, "median:", median, "std:", std)

    # 4
    frost = np.sum(T_clean < 0)
    hot = np.sum(T_clean > 30)
    print("frost:", frost, "hot:", hot)

    # 5
    i_max = np.nanargmax(T_clean)
    i_min = np.nanargmin(T_clean)

    print("MAX:", T_clean[i_max], obs_id[i_max], dt[i_max])
    print("MIN:", T_clean[i_min], obs_id[i_min], dt[i_min])

# =========================
# БЛОК 2
# =========================
def block_2_cleaning(df):
    section("БЛОК 2 Cleaning")

    rows_before = len(df)

    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime")

    # duplicates
    before = len(df)
    df = df.drop_duplicates()
    print("Removed duplicates:", before - len(df))

    # humidity fill
    df["month"] = df.index.month
    before_nan = df["humidity_pct"].isna().sum()

    df["humidity_pct"] = df.groupby(["city", "month"])["humidity_pct"] \
        .transform(lambda s: s.fillna(s.median()))

    after_nan = df["humidity_pct"].isna().sum()
    print("Filled NaN:", before_nan - after_nan)

    # outliers
    before = len(df)

    df = df[(df["temperature_c"] >= -60) & (df["temperature_c"] <= 60)]
    df = df[
        df["wind_speed_ms"].isna() |
        ((df["wind_speed_ms"] >= 0) & (df["wind_speed_ms"] <= 60))
    ]

    print("Removed outliers:", before - len(df))

    print(f"Rows: {rows_before} -> {len(df)}")

    return df

# =========================
# БЛОК 3
# =========================
def block_3_analytics(df):
    section("БЛОК 3 Analytics")

    # 1
    by_city = df.groupby("city")["temperature_c"].mean().sort_values()
    print(by_city)

    # 2
    precip = df.groupby("city")["precipitation_mm"].sum()
    print(precip)

    # 3
    monthly = df["temperature_c"].resample("ME").mean()

    # 4
    pivot = df.pivot_table(values="temperature_c", index="city", columns="month")

    # 5
    rainy = (
        df.assign(date=df.index.date)
        .query("precipitation_mm > 5")
        .groupby("city")["date"]
        .nunique()
    )

    print(rainy)

    # 6 anomaly
    df["year"] = df.index.year
    monthly2 = df.groupby(["year", "month"])["temperature_c"].mean()
    norm = monthly2.groupby(level=1).mean()

    dev = monthly2 - norm
    anomaly = dev.abs().idxmax()

    print("Anomaly:", anomaly, dev[anomaly])

    return {
        "pivot": pivot,
        "monthly": monthly,
        "precip": precip
    }

# =========================
# БЛОК 4
# =========================
def block_4_plots(df, data):
    section("БЛОК 4 Plots")

    # 1 line
    fig, ax = plt.subplots()
    for city in df["city"].unique()[:3]:
        subset = df[df["city"] == city]["temperature_c"].resample("ME").mean()
        ax.plot(subset.index, subset.values, label=city)

    ax.legend()
    ax.set_title("Temperature")
    fig.savefig(PLOTS_DIR / "line.png")
    plt.close()

    # 2 bar
    fig, ax = plt.subplots()
    data["precip"].plot(kind="bar", ax=ax)
    fig.savefig(PLOTS_DIR / "bar.png")
    plt.close()

    # 3 hist
    fig, ax = plt.subplots()
    t = df["temperature_c"].dropna()
    ax.hist(t)

    ax.axvline(t.mean())
    ax.axvline(t.median())

    fig.savefig(PLOTS_DIR / "hist.png")
    plt.close()

    # 4 heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(data["pivot"].values)
    plt.colorbar(im)

    fig.savefig(PLOTS_DIR / "heatmap.png")
    plt.close()

# =========================
def main():
    df_raw = load_observations()

    block_1_numpy(df_raw)
    df_clean = block_2_cleaning(df_raw)
    analytics = block_3_analytics(df_clean)
    block_4_plots(df_clean, analytics)

# =========================
if __name__ == "__main__":
    main()