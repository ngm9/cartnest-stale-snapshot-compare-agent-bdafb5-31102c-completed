import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    return os.environ.get(
        "DATABASE_URL",
        "postgresql://cartnest:cartnest_pw@127.0.0.1:5432/cartnest_compare",
    )


def get_model() -> str:
    return os.environ.get("AGENT_MODEL", "gpt-4o-mini")


def test_mode_enabled() -> bool:
    return os.environ.get("AGENT_TEST_MODE", "0") == "1"


def freshness_seconds() -> int:
    return int(os.environ.get("SNAPSHOT_FRESHNESS_SECONDS", "1800"))
