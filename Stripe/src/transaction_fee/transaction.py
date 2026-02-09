# Transaction Fee Calculator
# stripe · anonymous user · 2mon
# Transaction Fee Calculator
# The Challenge
# You need to build a system that calculates fees for a payment platform. You will get transaction data as a long CSV string. You need to read this data and calculate the fee for each payment based on specific rules.

# There are three parts to this problem. We start with simple math and add harder rules later.

# Basic Fees: Read the data and calculate cost based on the payment method.
# New Rules: Only charge fees for successful payments. Use different rates for different countries.
# Discounts: Give discounts to merchants who process a lot of payments.
# Input Data
# The input is a single string in CSV format. The first row lists the column names. The rows after that are the actual transaction records.

# id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
# What the columns mean:

# id: The unique ID for the transaction.
# reference: Reference number.
# amount: Money involved in cents (e.g., 1000 = $10.00).
# currency: The money type (e.g., "eur", "usd").
# date: When it happened (YYYY-MM-DD).
# merchant_id: ID for the seller.
# buyer_country: Country code of the buyer.
# transaction_type: What kind of action it is (e.g., "payment").
# payment_provider: How they paid (e.g., "card", "klarna").
# status: Did it work? (e.g., "payment_completed", "payment_failed").



# Part 1: Basic Fee Calculation
# The Task
# Write a function to read the CSV string. Calculate the fee for each transaction based on the payment_provider. Each provider charges a percentage of the amount plus a fixed fee.

# Fee Table:

# Payment Provider

# Fee Rate

# card

# 2.9% + 30 cents

# klarna

# 3.5% + 50 cents

# bank_transfer

# 0.8% flat

# You must round the final fee down to the nearest whole number (integer).

# Example Data
# Input:

# id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
# py_1,1,1000,eur,2024-12-24,acct_1,ie,payment,card,payment_completed
# py_2,2,2500,eur,2024-12-24,acct_2,de,payment,card,payment_failed
# py_3,3,3400,eur,2024-12-25,acct_2,ie,payment,klarna,payment_completed
# py_4,4,5000,eur,2024-12-25,acct_1,fr,payment,bank_transfer,payment_completed
# Output:

# id,transaction_type,payment_provider,fee
# py_1,payment,card,59
# py_2,payment,card,102
# py_3,payment,klarna,169
# py_4,payment,bank_transfer,40
# How we got these numbers:

# py_1: 1000 × 0.029 + 30 = 59
# py_2: 2500 × 0.029 + 30 = 102.5. Round down to 102.
# py_3: 3400 × 0.035 + 50 = 169
# py_4: 5000 × 0.008 = 40
# What You Need To Do
# Read the CSV string properly (ignore the header row after reading it).
# Use the right math formula for each provider.
# Return the result as a CSV string.
# Round fees down (use integer conversion).

# How to Solve It
# Part 1 Solution
# Plan:

# Split the CSV string by lines (\n) and commas (,).
# Ignore the first line (headers).
# Look at the payment_provider column.
# Do the math and save the result.
# Complexity: O(n) (linear time). We look at each line once.

# Code:

def calculate_fees(csv_data):
    lines = csv_data.strip().split('\n')
    header = lines[0].split(',')

    # Map column names to indices
    col_idx = {name: i for i, name in enumerate(header)}

    fee_config = {
        'card': (0.029, 30),
        'klarna': (0.035, 50),
        'bank_transfer': (0.008, 0)
    }

    results = ['id,transaction_type,payment_provider,fee']

    for line in lines[1:]:
        fields = line.split(',')
        tx_id = fields[col_idx['id']]
        tx_type = fields[col_idx['transaction_type']]
        provider = fields[col_idx['payment_provider']]
        amount = int(fields[col_idx['amount']])

        rate, fixed = fee_config[provider]
        fee = int(amount * rate + fixed)  # floor by int conversion

        results.append(f'{tx_id},{tx_type},{provider},{fee}')

    return '\n'.join(results)


# Watch Out For:
# Empty inputs.
# Providers that are not in your list.
# Bad data in the CSV.












# Part 2: Conditional Fee Rules
# New Rules
# Now, update your code to handle status checks and countries.

# Check Status: Only calculate a fee if status is "payment_completed".
# Failed Payments: If the status is failed or pending, the fee is 0.
# Regional Rates: Ireland ("ie") has special, cheaper rates.
# Special Rates for Ireland (ie):

# Payment Provider

# Fee Rate

# card

# 1.9% + 20 cents

# klarna

# 2.5% + 40 cents

# All other countries use the standard rates from Part 1.

# Example Data
# Input:

# id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
# py_1,1,1000,eur,2024-12-24,acct_1,ie,payment,card,payment_completed
# py_2,2,2500,eur,2024-12-24,acct_2,de,payment,card,payment_failed
# py_3,3,3400,eur,2024-12-25,acct_2,ie,payment,klarna,payment_completed
# py_4,4,5000,eur,2024-12-25,acct_1,fr,payment,bank_transfer,payment_completed
# py_5,5,2000,eur,2024-12-26,acct_1,ie,payment,card,payment_pending
# Output:

# id,transaction_type,payment_provider,fee
# py_1,payment,card,39
# py_2,payment,card,0
# py_3,payment,klarna,125
# py_4,payment,bank_transfer,40
# py_5,payment,card,0
# How we got these numbers:

# py_1: Ireland rate used. (Cheaper than standard).
# py_2: Failed, so fee is 0.
# py_3: Ireland rate used.
# py_4: France uses standard rate.
# py_5: Pending, so fee is 0.
# What You Need To Do
# Look at the status column before doing math.
# Check the buyer_country. If it is "ie", use the special rates.
# Keep your code clean. Separate the logic for checking status and calculating fees.

# Part 2 Solution
# Plan:

# Check if status is "payment_completed". If not, fee is 0.
# Create a function to pick the right fees. It checks the country first.
# If the country is missing, use default fees.
# Code:

def calculate_fees(csv_data):
    lines = csv_data.strip().split('\n')
    header = lines[0].split(',')
    col_idx = {name: i for i, name in enumerate(header)}

    # Default fees
    default_fees = {
        'card': (0.029, 30),
        'klarna': (0.035, 50),
        'bank_transfer': (0.008, 0)
    }

    # Regional overrides
    regional_fees = {
        'ie': {
            'card': (0.019, 20),
            'klarna': (0.025, 40)
        }
    }

    def get_fee_config(country, provider):
        if country in regional_fees and provider in regional_fees[country]:
            return regional_fees[country][provider]
        return default_fees[provider]

    results = ['id,transaction_type,payment_provider,fee']

    for line in lines[1:]:
        fields = line.split(',')
        tx_id = fields[col_idx['id']]
        tx_type = fields[col_idx['transaction_type']]
        provider = fields[col_idx['payment_provider']]
        amount = int(fields[col_idx['amount']])
        status = fields[col_idx['status']]
        country = fields[col_idx['buyer_country']]

        if status != 'payment_completed':
            fee = 0
        else:
            rate, fixed = get_fee_config(country, provider)
            fee = int(amount * rate + fixed)

        results.append(f'{tx_id},{tx_type},{provider},{fee}')

    return '\n'.join(results)



# Part 3: Volume-Based Discounts
# Adding Discounts
# Now we add volume discounts. Merchants who sell more get cheaper fees. You need to count how many successful transactions a merchant has made.

# Discount Table:

# Total Transactions so far

# Discount

# 1-10

# 0% (Normal price)

# 11-50

# 10% off

# 51-100

# 15% off

# 101+

# 20% off

# Configuration Data:

# You will get a dictionary with fees for many countries. It looks like this:

# country_fees = {
#     "ie": {"card": (0.019, 20), "klarna": (0.025, 40), "bank_transfer": (0.006, 0)},
#     "de": {"card": (0.025, 25), "klarna": (0.030, 45), "bank_transfer": (0.007, 0)},
#     "fr": {"card": (0.027, 28), "klarna": (0.032, 48), "bank_transfer": (0.008, 0)},
#     "default": {"card": (0.029, 30), "klarna": (0.035, 50), "bank_transfer": (0.008, 0)}
# }
# Example Data
# Input:

# Imagine acct_1 has done 10 transactions already. The 11th transaction (py_11) happens. The 12th transaction (py_12) happens.

# Output:

# Transaction 11: Base fee is calculated. Then, apply a 10% discount.
# Transaction 12: Base fee is calculated. Apply a 10% discount.
# Math Detail: For py_11 (Ireland Card): Base = 1500 × 0.019 + 20 = 48.5. Discount = 10%. New Fee = 48.5 × 0.9 = 43.65. Round down -> 43.

# What You Need To Do
# Keep a count of transactions for every merchant.
# Check the merchant's count before the current transaction to find the discount.
# Only increase the count if the transaction is "payment_completed".
# Process rows in order. The order in the CSV matters.
# Use the provided dictionary for country fees. If the country isn't there, use "default".
# Questions to Ask the Interviewer
# Do I apply the discount before rounding or after?
# What if a merchant sells in different countries? Does that count towards the same volume total?
# Does the volume count ever reset (like every month)?



# Part 3 Solution
# Plan:

# Use a dictionary (defaultdict) to count how many times each merchant appears.
# Before doing math for a row, check the merchant's current count.
# Find the discount percent based on that count.
# Calculate the fee, apply the discount, then round.
# If the transaction was successful, add 1 to the merchant's count.
# Code:

from collections import defaultdict

def calculate_fees(csv_data, country_fees):
    lines = csv_data.strip().split('\n')
    header = lines[0].split(',')
    col_idx = {name: i for i, name in enumerate(header)}

    # Volume discount tiers: (min_transactions, discount_rate)
    discount_tiers = [
        (101, 0.20),
        (51, 0.15),
        (11, 0.10),
        (1, 0.00)
    ]

    def get_discount(tx_count):
        for threshold, discount in discount_tiers:
            if tx_count >= threshold:
                return discount
        return 0.0

    def get_fee_config(country, provider):
        if country in country_fees:
            return country_fees[country].get(provider, country_fees['default'][provider])
        return country_fees['default'][provider]

    merchant_volume = defaultdict(int)
    results = ['id,transaction_type,payment_provider,fee']

    for line in lines[1:]:
        fields = line.split(',')
        tx_id = fields[col_idx['id']]
        tx_type = fields[col_idx['transaction_type']]
        provider = fields[col_idx['payment_provider']]
        amount = int(fields[col_idx['amount']])
        status = fields[col_idx['status']]
        country = fields[col_idx['buyer_country']]
        merchant_id = fields[col_idx['merchant_id']]

        if status != 'payment_completed':
            fee = 0
        else:
            # Get current volume (before incrementing)
            current_volume = merchant_volume[merchant_id] + 1
            discount = get_discount(current_volume)

            rate, fixed = get_fee_config(country, provider)
            base_fee = amount * rate + fixed
            fee = int(base_fee * (1 - discount))

            # Increment volume count for completed transactions
            merchant_volume[merchant_id] += 1

        results.append(f'{tx_id},{tx_type},{provider},{fee}')

    return '\n'.join(results)





# Performance:

# Time Complexity: O(n). We still process each line once.
# Space Complexity: O(n + m). We store the output string (n) and the count for each merchant (m).