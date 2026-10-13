import os

os.environ.setdefault("AGENT_TEST_MODE", "1")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://cartnest:cartnest_pw@127.0.0.1:5432/cartnest_compare",
)
os.environ.setdefault("SNAPSHOT_FRESHNESS_SECONDS", "1800")
