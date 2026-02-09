import threading
import bisect
from collections import defaultdict, deque


class SlidingWindowRateLimiter:
    """
    Standard Sliding Window implementation using a Deque.
    Efficient for in-order timestamps. O(1) amortized time.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits = {}

    def _cleanup(self, key: str, timestamp: int) -> None:
        if key not in self.hits:
            return
        window_start = timestamp - self.window_seconds
        while self.hits[key] and self.hits[key][0] <= window_start:
            self.hits[key].popleft()
        if not self.hits[key]:
            del self.hits[key]

    def hit(self, key: str, timestamp: int) -> None:
        if key not in self.hits:
            self.hits[key] = deque()
        self._cleanup(key, timestamp)
        self.hits[key].append(timestamp)

    def allowed(self, key: str, timestamp: int) -> bool:
        self._cleanup(key, timestamp)
        if key not in self.hits:
            return True
        return len(self.hits[key]) < self.max_requests


class RobustRateLimiter:
    """
    Handles out-of-order timestamps using binary search (bisect).
    Also implements 'check_and_hit' to prevent race conditions.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits = defaultdict(list)
        self.lock = threading.Lock()

    def _cleanup(self, key: str, timestamp: int) -> None:
        window_start = timestamp - self.window_seconds
        # Find index of first timestamp that should remain
        idx = bisect.bisect_right(self.hits[key], window_start)
        if idx > 0:
            self.hits[key] = self.hits[key][idx:]

    def check_and_hit(self, key: str, timestamp: int) -> bool:
        """Atomic check-and-record operation."""
        with self.lock:
            self._cleanup(key, timestamp)
            if len(self.hits[key]) < self.max_requests:
                # Use insort to handle out-of-order timestamps
                bisect.insort(self.hits[key], timestamp)
                return True
            return False


class ThreadSafeRateLimiter:
    """
    Thread-safe implementation using per-key locking for high concurrency.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits = {}
        self.locks = {}
        self.global_lock = threading.Lock()

    def _get_lock(self, key: str) -> threading.Lock:
        with self.global_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            return self.locks[key]

    def check_and_hit(self, key: str, timestamp: int) -> bool:
        lock = self._get_lock(key)
        with lock:
            # Re-check key existence under lock
            if key not in self.hits:
                self.hits[key] = deque()

            # Cleanup
            window_start = timestamp - self.window_seconds
            while self.hits[key] and self.hits[key][0] <= window_start:
                self.hits[key].popleft()

            # Logic
            if len(self.hits[key]) < self.max_requests:
                self.hits[key].append(timestamp)
                return True
            return False


# --- Testing Script ---
if __name__ == "__main__":
    print("--- Testing Basic Sliding Window ---")
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=10)
    limiter.hit("user_1", 1)
    limiter.hit("user_1", 2)
    print(f"Allowed at t=3: {limiter.allowed('user_1', 3)}")  # True
    limiter.hit("user_1", 3)
    print(f"Allowed at t=4: {limiter.allowed('user_1', 4)}")  # False (Limit 3 reached)
    print(f"Allowed at t=12: {limiter.allowed('user_1', 12)}")  # True (t=1 expired)

    print("\n--- Testing Out-of-Order Timestamps ---")
    robust = RobustRateLimiter(max_requests=2, window_seconds=10)
    robust.check_and_hit("user_2", 10)
    robust.check_and_hit("user_2", 5)  # Arrived late
    print(f"Hits for user_2: {robust.hits['user_2']}")  # [5, 10]
    print(f"Allowed at t=11: {robust.check_and_hit('user_2', 11)}")  # False