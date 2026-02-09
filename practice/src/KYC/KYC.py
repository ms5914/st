csv_data = """col1,col2,col3,col4,col5,col6
BIZ001,land water,landwater.com,land,land water LLC,Environmental services
BIZ002,Acme Global Trading,acme.com,Acme,XYZ ENTERPRISES,Import export services
BIZ003,Maple     Ridge               Bakery,maplebakery.com,Maple,MAPLE RIDGE BAKERY LLC,Artisan baked goods
BIZ004,Innovation Labs Inc,innovlabs.com,Labs,INNOVATION RESEARCH,R&D services"""


#part 1 just checking that all fields are present and are not zero length or empty spaces.
def print_verification(stripped_elements, is_verified):
    if is_verified:
        return f"VERIFIED: {stripped_elements[1]}"
    else:
        return f"NOT VERIFIED: {stripped_elements[1] if len(stripped_elements) > 1 else ''}"



def validate_businesses(csv_data):
    results = []
    for line in csv_data.split("\n")[1:]:
        elements = line.split(",")
        stripped_elements = [elem.strip() for elem in elements]
        if len(stripped_elements) != 6:
            results.append(print_verification(stripped_elements, False))
            continue
        if not all(len(elem) for elem in stripped_elements):
            results.append(print_verification(stripped_elements, False))
            continue
        results.append(print_verification(stripped_elements, True))
    return "\n".join(results)

# print(validate_businesses(csv_data))

# part 2 check the length of the Full Description (col5). It must follow Stripe's rules. The length must be between 5 and 31 characters (inclusive).
def validate_businesses(csv_data):
    results = []
    for line in csv_data.split("\n")[1:]:
        elements = line.split(",")
        stripped_elements = [elem.strip() for elem in elements]
        if len(stripped_elements) != 6:
            results.append(print_verification(stripped_elements, False))
            continue
        if not all(len(elem) for elem in stripped_elements):
            results.append(print_verification(stripped_elements, False))
            continue
        if not (len(stripped_elements[4]) >= 5 and len(stripped_elements[4])<=31):
            results.append(print_verification(stripped_elements, False))
            continue
        results.append(print_verification(stripped_elements, True))
    return "\n".join(results)

# print(validate_businesses(csv_data))


#part 3
#Part 3: Block Bad Words
# What You Need To Do
# To stop fraud, we must block generic business names in the Full Description (col5). If col5 contains any of these words, mark the account NOT VERIFIED:
#
# Blocked Words (Case-Insensitive):
#
# ONLINE STORE
# ECOMMERCE
# RETAIL
# SHOP
# GENERAL MERCHANDISE
# Case-insensitive means "Shop", "SHOP", and "shop" are all blocked.

BLOCKED_WORDS = ["online store", "ecommerce", "retail", "shop", "general merchandise"]
def validate_businesses(csv_data):
    results = []
    for line in csv_data.split("\n")[1:]:
        elements = line.split(",")
        stripped_elements = [elem.strip() for elem in elements]
        if len(stripped_elements) != 6:
            results.append(print_verification(stripped_elements, False))
            continue
        if not all(len(elem) for elem in stripped_elements):
            results.append(print_verification(stripped_elements, False))
            continue
        if not (len(stripped_elements[4]) >= 5 and len(stripped_elements[4])<=31):
            results.append(print_verification(stripped_elements, False))
            continue
        if not all( word not in stripped_elements[4].lower() for word in BLOCKED_WORDS):
            results.append(print_verification(stripped_elements, False))
            continue
        results.append(print_verification(stripped_elements, True))
    return "\n".join(results)

# print(validate_businesses(csv_data))
# Part 4: Match Business Names
# What You Need To Do
# Make sure the Business Name (col2) matches the descriptions (col4 or col5). At least 50% of the words in the Business Name must appear in either the Short Description (col4) or Full Description (col5).
#
# How to Match Words:
#
# Split col2, col4, and col5 into words using spaces.
# Remove "LLC" and "Inc" from the lists.
# Ignore upper/lower case.
# Check if half of the name's words exist in the description fields.
# Example
# Input:
#
# csv_data = """col1,col2,col3,col4,col5,col6
# BIZ001,land water,landwater.com,land,land water LLC,Environmental services
# BIZ002,Acme Global Trading,acme.com,Acme,XYZ ENTERPRISES,Import export services
# BIZ003,Maple Ridge Bakery,maplebakery.com,Maple,MAPLE RIDGE BAKERY LLC,Artisan baked goods
# BIZ004,Innovation Labs Inc,innovlabs.com,Labs,INNOVATION RESEARCH,R&D services"""
# Output:
#
# VERIFIED: land water
# NOT VERIFIED: Acme Global Trading
# VERIFIED: Maple Ridge Bakery
# VERIFIED: Innovation Labs Inc
# Explanation:
#
# BIZ001: "land water" (2 words). Both are in col5. Match: 100%. -> VERIFIED
# BIZ002: "Acme Global Trading" (3 words). Only "Acme" is found. Match: 33% (less than 50%). -> NOT VERIFIED
# BIZ003: "Maple Ridge Bakery" (3 words). All 3 match. Match: 100%. -> VERIFIED
# BIZ004: "Innovation Labs Inc" (2 words, ignoring Inc). Both match. Match: 100%. -> VERIFIED
# Rules
# Split text by whitespace.
# Ignore "LLC" and "Inc".
# Comparison is case-insensitive.
# You need >= 50% match.
# Questions to Ask the Interviewer
# Can I combine col4 and col5 for the check?
# How do I handle punctuation (like "Ben & Jerry's")?
# What if the name becomes empty after removing "LLC"?
def remove_generic_business_names(words):

    words.discard("llc")
    words.discard("inc")
    words.discard("")
    return words

def validate_businesses(csv_data):
    results = []
    for line in csv_data.split("\n")[1:]:
        elements = line.split(",")
        stripped_elements = [elem.strip() for elem in elements]
        if len(stripped_elements) != 6:
            results.append(print_verification(stripped_elements, False))
            continue
        if not all(len(elem) for elem in stripped_elements):
            results.append(print_verification(stripped_elements, False))
            continue
        if not (len(stripped_elements[4]) >= 5 and len(stripped_elements[4])<=31):
            results.append(print_verification(stripped_elements, False))
            continue
        if not all( word not in stripped_elements[4].lower() for word in BLOCKED_WORDS):
            results.append(print_verification(stripped_elements, False))
            continue

        business_name = remove_generic_business_names(set(stripped_elements[1].lower().split(" ")))
        print(business_name)
        short_desc = remove_generic_business_names(set(stripped_elements[3].lower().split(" ")))
        long_desc = remove_generic_business_names(set(stripped_elements[4].lower().split(" ")))
        combined_desc = short_desc.union(long_desc)
        matches = business_name.intersection(combined_desc)

        if (1.0*len(matches))/len(business_name) < 0.5:
            results.append(print_verification(stripped_elements, False))

        results.append(print_verification(stripped_elements, True))
    return "\n".join(results)
print(validate_businesses(csv_data))
