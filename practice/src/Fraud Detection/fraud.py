"""

timestamp_seconds,unique_id,amount,card_number,merchant
"""
from cachetools.func import lru_cache

input_str = """5,R1,5.60,4242424242424242,bobs_burgers
10,R2,500.00,4242111111111111,a_corp"""

rules="""1,merchant,bobs_burgers
20,card_number,4242111111111111"""

## 1 part.
def parse_all_input(input_str):
    results = []
    for line in input_str.split("\n"):
        timestamp, id, amount, card_number, merchant = line.split(",")
        results.append((int(timestamp), id, float(amount), card_number, merchant))

    results.sort(key=lambda v: v[0])
    return results

def parse_input(input_str):
    results = []
    for line in input_str.split("\n"):
        timestamp, id, amount, card_number, merchant = line.split(",")
        results.append((int(timestamp), id, float(amount), "APPROVE"))

    results.sort(key=lambda v: v[0])
    return results


def get_output_in_required_format(input_str):
    "timestamp, unique ID, amount, and outcome "
    results = parse_input(input_str)
    return " ".join([f"{res[0]} {res[1]} {res[2]} {res[3]}" for res in results])



### 2 part
@lru_cache(maxsize=None)
def parse_rules(rules):
    mapp_merchants = {}
    mapp_cards = {}
    for rule in rules.split("\n"):
        time_curr, type, value = rule.split(",")
        time_curr = int(time_curr)
        if type == "merchant":
            mapp_merchants[value] = min(mapp_merchants.get(value, float('inf')), time_curr)
        if type == "card_number":
            mapp_cards[value] = min(mapp_cards.get(value, float('inf')), time_curr)

    return (mapp_merchants, mapp_cards)



def get_output_with_rules(input_str, rules):
    parsed_rules = parse_rules(rules)
    mapp_merchants, mapp_cards = parsed_rules[0], parsed_rules[1]
    results = parse_all_input(input_str)
    final_results = []
    for timestamp, id, amount, card_number, merchant in results:
        if card_number in mapp_cards and timestamp>= mapp_cards[card_number]:
            final_results.append(f"{timestamp} {id} {amount} REJECT")
        elif merchant in mapp_merchants and timestamp >= mapp_merchants[merchant]:
            final_results.append(f"{timestamp} {id} {amount} REJECT")
        else:

            final_results.append(f"{timestamp} {id} {amount} APPROVE")

    return " ".join(final_results)


print(get_output_with_rules(input_str, rules))


def amount_lost_to_fraud(input_str, rules):
    parsed_rules = parse_rules(rules)
    mapp_merchants, mapp_cards = parsed_rules[0], parsed_rules[1]
    results = parse_all_input(input_str)
    amount_lost = 0
    for timestamp, id, amount, card_number, merchant in results:
        if merchant in mapp_merchants and timestamp < mapp_merchants[merchant]:
            amount_lost = amount_lost + amount
        elif card_number in mapp_cards and timestamp< mapp_cards[card_number]:
            amount_lost = amount_lost + amount
        else:
            continue
    return amount



