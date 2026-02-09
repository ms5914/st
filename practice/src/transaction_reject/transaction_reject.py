from collections import defaultdict

# ============ PART 1 ============
def part1(transactions):
    balances = defaultdict(int)
    for txn in transactions:
        name, ts, currency, amount = txn
        balances[name] += amount
    result = {name: bal for name, bal in balances.items() if bal != 0}
    return result

# ============ PART 2 ============
def part2(transactions):
    balances = defaultdict(int)
    rejected = []
    for txn in transactions:
        name, ts, currency, amount = txn
        if balances[name] + amount < 0:
            rejected.append(txn)
        else:
            balances[name] += amount
    result = {name: bal for name, bal in balances.items() if bal != 0}
    return result, rejected

# ============ PART 3(a) ============
def part3a(transactions, platform_id):
    balances = defaultdict(int)
    rejected = []
    current_reserve = 0
    max_reserve = 0

    for txn in transactions:
        name, ts, currency, amount = txn
        if name == platform_id:
            balances[name] += amount
            # Platform deposit might reduce current reserve usage
        else:
            new_balance = balances[name] + amount
            if new_balance < 0:
                deficit = -new_balance
                # Check if platform can cover the deficit
                if balances[platform_id] >= deficit:
                    balances[platform_id] -= deficit
                    balances[name] = 0
                    current_reserve += deficit
                    max_reserve = max(max_reserve, current_reserve)
                else:
                    # Platform can't cover it — reject
                    rejected.append(txn)
            else:
                balances[name] = new_balance

    result = {name: bal for name, bal in balances.items() if bal != 0}
    return max_reserve, rejected, result


# --- Test ---
print("=== Part 1 ===")
txns1 = [
    ("acct_123", 1, "usd", 1000),
    ("acct_123", 2, "usd", 500),
    ("acct_321", 3, "usd", 400),
    ("acct_321", 4, "usd", -400),
]
print(part1(txns1))

print("\n=== Part 2 ===")
txns2 = [
    ("acct_123", 1, "usd", 1000),
    ("acct_123", 2, "usd", 500),
    ("acct_321", 3, "usd", 400),
    ("acct_321", 4, "usd", -500),
]
balances, rejected = part2(txns2)
print("Balances:", balances)
print("Rejected:", rejected)

print("\n=== Part 3(a) ===")
txns3 = [
    ("acct_123", 1, "usd", 1000),
    ("acct_321", 3, "usd", 400),
    ("acct_321", 4, "usd", -500),
]
max_res, rej, bals = part3a(txns3, "acct_123")
print("Max reserve:", max_res)
print("Rejected:", rej)
print("Balances:", bals)
