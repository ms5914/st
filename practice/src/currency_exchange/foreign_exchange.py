#part 1
class CurrencyConverter:
    def __init__(self, rate_string):
        self.rates = {}
        self._parse_rates(rate_string)

    def _parse_rates(self, rate_string):
        if not rate_string:
            return

        for entry in rate_string.split(","):
            parts = entry.split(":")
            from_curr, to_curr, rate = parts[0], parts[1], float(parts[2])

            if from_curr not in self.rates:
                self.rates[from_curr] = {}
            self.rates[from_curr][to_curr] = rate

    def getRate(self, from_curr, to_curr):
        # Same currency
        if from_curr == to_curr:
            return 1.0

        # Direct lookup
        if from_curr in self.rates and to_curr in self.rates[from_curr]:
            return self.rates[from_curr][to_curr]

        # Reverse lookup
        if to_curr in self.rates and from_curr in self.rates[to_curr]:
            return 1.0 / self.rates[to_curr][from_curr]

        return None






#part 2

def getRate(self, from_curr, to_curr):
    # Direct or reverse lookup first
    direct = self._get_direct_rate(from_curr, to_curr)
    if direct is not None:
        return direct

    # Try single intermediate
    all_currencies = set(self.rates.keys())
    for curr_list in self.rates.values():
        all_currencies.update(curr_list.keys())

    for intermediate in all_currencies:
        rate1 = self._get_direct_rate(from_curr, intermediate)
        rate2 = self._get_direct_rate(intermediate, to_curr)

        if rate1 is not None and rate2 is not None:
            return rate1 * rate2

    return None

def _get_direct_rate(self, from_curr, to_curr):
    """Get direct or reverse rate, returns None if not found."""
    if from_curr == to_curr:
        return 1.0
    if from_curr in self.rates and to_curr in self.rates[from_curr]:
        return self.rates[from_curr][to_curr]
    if to_curr in self.rates and from_curr in self.rates[to_curr]:
        return 1.0 / self.rates[to_curr][from_curr]
    return None


#part 3

from collections import defaultdict

def __init__(self, rate_string):
    self.graph = defaultdict(list)  # currency -> [(neighbor, rate), ...]
    self._parse_rates(rate_string)

def _parse_rates(self, rate_string):
    if not rate_string:
        return

    for entry in rate_string.split(","):
        parts = entry.split(":")
        from_curr, to_curr, rate = parts[0], parts[1], float(parts[2])

        # Store both directions
        self.graph[from_curr].append((to_curr, rate))
        self.graph[to_curr].append((from_curr, 1.0 / rate))

def getRate(self, from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0

    best_rate = None
    # BFS with (current_currency, accumulated_rate, visited_set)
    queue = [(from_curr, 1.0, {from_curr})]

    while queue:
        current, rate, visited = queue.pop(0)

        for neighbor, edge_rate in self.graph[current]:
            if neighbor == to_curr:
                new_rate = rate * edge_rate
                if best_rate is None or new_rate > best_rate:
                    best_rate = new_rate
            elif neighbor not in visited:
                new_visited = visited | {neighbor}
                queue.append((neighbor, rate * edge_rate, new_visited))

    return best_rate

#part 4

def getRate(self, from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0

    if from_curr not in self.graph:
        return None

    best_rate = [None]  # Use list to allow modification in nested function

    def dfs(current, accumulated_rate, visited):
        if current == to_curr:
            if best_rate[0] is None or accumulated_rate > best_rate[0]:
                best_rate[0] = accumulated_rate
            return

        for neighbor, edge_rate in self.graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, accumulated_rate * edge_rate, visited)
                visited.remove(neighbor)  # Backtrack

    dfs(from_curr, 1.0, {from_curr})
    return best_rate[0]

