import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# ── Connection settings ────────────────────────────────────────────────────────
DB_USER     = "titanic_user"
DB_PASSWORD = "titanic_pass"
DB_HOST     = "127.0.0.1"
DB_PORT     = 3306
DB_NAME     = "my_database"

CONNECTION_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

MAX_RETRIES    = 10
RETRY_INTERVAL = 10  # seconds


def get_engine(url: str):
    return create_engine(url, pool_pre_ping=True)


def load_titanic(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM titanic"))
        return pd.DataFrame(result.fetchall(), columns=result.keys())


def main() -> None:
    engine = get_engine(CONNECTION_URL)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[Attempt {attempt}/{MAX_RETRIES}] Connecting to MySQL …")
            df = load_titanic(engine)

            print(f"\n✅  Success! Loaded {len(df)} rows × {len(df.columns)} columns.\n")
            pd.set_option("display.max_columns", 12)
            pd.set_option("display.width", 200)
            print(df)
            return

        except OperationalError as exc:
            print(f"   ⚠️  Not ready yet: {exc.orig}")
            if attempt < MAX_RETRIES:
                print(f"   Retrying in {RETRY_INTERVAL} s …\n")
                time.sleep(RETRY_INTERVAL)
            else:
                print("\n❌  Max retries reached. Exiting.")
                raise SystemExit(1)


if __name__ == "__main__":
    main()