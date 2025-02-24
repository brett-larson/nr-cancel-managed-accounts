import time
from collections import deque
from datetime import datetime, timedelta
from cancel_managed_accounts.utils import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

class RateLimiter:
    """
    Rate limiter to limit the number of calls per specified time window
    """
    def __init__(self, calls_per_minute: int, time_window: timedelta = timedelta(minutes=1)):
        self.calls_per_minute = calls_per_minute
        self.time_window = time_window
        self.calls = deque()

    def wait_if_needed(self):
        """
        Wait if the rate limit is reached
        :return: None
        """
        now = datetime.now()

        # Remove calls older than the time window
        if self.calls:
            start_time = self.calls[0].strftime("%H:%M:%S")
            end_time = self.calls[-1].strftime("%H:%M:%S")
            logger.info(f"Checking calls: {len(self.calls)} calls from {start_time} to {end_time}")
        else:
            logger.info("Checking calls: 0 calls")

        while self.calls and (now - self.calls[0]) > self.time_window:
            self.calls.popleft()

        # If at limit, wait until oldest call is more than the time window old
        if len(self.calls) >= self.calls_per_minute:
            wait_time = (self.calls[0] + self.time_window - now).total_seconds()
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting for {wait_time} seconds.")
                try:
                    time.sleep(wait_time)
                except Exception as e:
                    logger.error(f"Error during sleep: {e}")

        self.calls.append(now)
