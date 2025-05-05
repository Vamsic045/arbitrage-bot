import os

ALERT_ON = os.getenv("ALERT_ON", "true").lower() == "true"
AUTO_TRADE = os.getenv("AUTO_TRADE", "false").lower() == "true"

