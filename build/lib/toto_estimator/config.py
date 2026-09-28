"""Central, replaceable configuration for the MVP predictor."""

from pathlib import Path

POINTS_WEIGHT = 0.70
GOAL_DIFFERENCE_WEIGHT = 0.30
OVERALL_WEIGHT = 0.50
VENUE_WEIGHT = 0.50
DRAW_THRESHOLD = 0.10

MIN_TOTAL_MATCHES = 10
MIN_VENUE_MATCHES = 5
TICKET_SIZE = 14

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
HISTORICAL_DATA_PATH = DATA_DIR / "historical_matches.csv"
SAMPLE_TICKET_PATH = DATA_DIR / "sample_ticket.csv"

