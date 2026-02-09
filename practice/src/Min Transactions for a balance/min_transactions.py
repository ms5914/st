
#approach 1 using sorting
def redistribute_money(accounts, min_threshold):
    accounts.sort()  # Sort the accounts in ascending order
    left = 0  # Pointer for the leftmost account
    right = len(accounts) - 1  # Pointer for the rightmost account
    transactions = []  # List to store the transactions

    while left < right:
        if accounts[left] < min_threshold:
            deficit = min_threshold - accounts[left]
            if accounts[right] - deficit >= min_threshold:
                accounts[left] += deficit
                accounts[right] -= deficit
                transactions.append((right, left, deficit))
                left += 1
            else:
                accounts[left] += accounts[right] - min_threshold
                transactions.append((right, left, accounts[right] - min_threshold))
                right -= 1
        else:
            left += 1

    return len(transactions), transactions


# Example usage
accounts = [3, 5, 11, 28]
min_threshold = 10
num_transactions, transactions = redistribute_money(accounts, min_threshold)
print(f"Number of transactions: {num_transactions}")
print("Transactions:")
for transaction in transactions:
    print(f"Transfer {transaction[2]} from account {transaction[0]} to account {transaction[1]}")








#approach 2 using backtracking
def redistribute_money(accounts, min_threshold):
    def backtrack(accounts, transactions, min_transactions):
        if all(amt >= min_threshold for amt in accounts):
            min_transactions[0] = min(min_transactions[0], len(transactions))
            return

        for i in range(len(accounts)):
            if accounts[i] < min_threshold:
                deficit = min_threshold - accounts[i]
                for j in range(len(accounts)):
                    if i != j and accounts[j] > min_threshold:
                        surplus = accounts[j] - min_threshold
                        transfer = min(deficit, surplus)
                        accounts[i] += transfer
                        accounts[j] -= transfer
                        transactions.append((j, i, transfer))
                        backtrack(accounts, transactions, min_transactions)
                        accounts[i] -= transfer
                        accounts[j] += transfer
                        transactions.pop()
                return

    min_transactions = [float('inf'), []]  # [min_count, transactions]
    backtrack(accounts, [], min_transactions)
    return min_transactions[0], min_transactions[1]


# Example usage
accounts = [3, 5, 11, 28]
min_threshold = 10
min_txns = redistribute_money(accounts, min_threshold)
print(f"Minimum transactions needed: {min_txns}")