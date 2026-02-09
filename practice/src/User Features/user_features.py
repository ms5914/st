
####################PART 1
def get_user_features(user, features):
    """
    Returns a set of feature IDs that apply to the given user.

    Rules:
    - If feature has 'locations', user's location must match
    - If feature has 'abTest' = True, user ID must be even
    """
    user_id = user["id"]
    user_location = user["location"]
    active_features = set()

    for feature in features:
        feature_id = feature["id"]

        # Check location restriction
        locations = feature.get("locations", [])
        if locations and user_location not in locations:
            continue  # User's location doesn't match

        # Check A/B test requirement
        ab_test = feature.get("abTest", False)
        if ab_test and user_id % 2 != 0:
            continue  # Odd user ID, not in A/B test

        # Feature applies to this user
        active_features.add(feature_id)

    return active_features


# Test Data for Part 1
users_part1 = [
    {"id": 0, "name": "eva", "location": "US"},
    {"id": 1, "name": "tess", "location": "US"},
    {"id": 2, "name": "rahool", "location": "CA"},
    {"id": 3, "name": "amanda", "location": "CA"}
]

features_part1 = [
    {
        "id": "annual_sale",
        "locations": ["US"],
        "abTest": True,
    },
    {
        "id": "enhanced_comments",
        "abTest": True,
    },
    {
        "id": "canada_promotion",
        "locations": ["CA"],
    }
]

print("\nPART1\n")
for user in users_part1:
    active = get_user_features(user, features_part1)
    features_str = ", ".join(sorted(active)) if active else "N/A"
    print(f"{user['name']:<10} | {features_str}")




###########################PART 2############################################
def get_user_features_v2(user, features):
    """
    Returns a set of feature IDs that apply to the given user.

    Rules:
    - If feature has 'locations', user's location must match (cannot opt-in to wrong location)
    - If feature has 'abTest' = True, user ID must be even OR user opted in
    - User can opt-out of any feature
    """
    user_id = user["id"]
    user_location = user["location"]
    opt_in = set(user.get("optIn", []))
    opt_out = set(user.get("optOut", []))
    active_features = set()

    for feature in features:
        feature_id = feature["id"]

        # Skip if user opted out
        if feature_id in opt_out:
            continue

        # Check location restriction (cannot be overridden by opt-in)
        locations = feature.get("locations", [])
        if locations and user_location not in locations:
            continue  # User's location doesn't match

        # Check A/B test requirement (can be overridden by opt-in)
        ab_test = feature.get("abTest", False)
        if ab_test:
            # Need even ID OR opt-in
            if user_id % 2 == 0 or feature_id in opt_in:
                active_features.add(feature_id)
        else:
            # Not an A/B test, feature applies
            active_features.add(feature_id)

    return active_features


# Test Data for Part 2
users_part2 = [
    {"id": 0, "name": "eva", "location": "US", "optIn": ["annual_sale"]},
    {"id": 1, "name": "tess", "location": "US", "optIn": ["annual_sale"]},
    {"id": 2, "name": "rahool", "location": "CA", "optOut": ["enhanced_comments", "canada_promotion"]},
    {"id": 3, "name": "amanda", "location": "CA", "optIn": ["annual_sale"]}
]

features_part2 = [
    {
        "id": "annual_sale",
        "locations": ["US"],
        "abTest": True,
    },
    {
        "id": "enhanced_comments",
        "abTest": True,
    },
    {
        "id": "canada_promotion",
        "locations": ["CA"],
    }
]

print("\nPART2\n")
for user in users_part2:
    active = get_user_features_v2(user, features_part2)
    features_str = ", ".join(sorted(active)) if active else "N/A"
    print(f"{user['name']:<10} | {features_str}")


######################Part 3 ########################

def get_user_features_v3(user, features):
    """
    Returns a set of feature IDs that apply to the given user.

    Rules:
    - If feature has 'locations', user's location must match (cannot opt-in to wrong location)
    - If feature has 'abTest' = True, user ID must be even OR user opted in
    - User can opt-out of any feature
    - Features with conflicts are resolved by priority (higher priority wins)
    """
    user_id = user["id"]
    user_location = user["location"]
    opt_in = set(user.get("optIn", []))
    opt_out = set(user.get("optOut", []))

    # Step 1: Determine eligible features (before conflict resolution)
    eligible_features = {}

    for feature in features:
        feature_id = feature["id"]

        # Skip if user opted out
        if feature_id in opt_out:
            continue

        # Check location restriction
        locations = feature.get("locations", [])
        if locations and user_location not in locations:
            continue

        # Check A/B test requirement
        ab_test = feature.get("abTest", False)
        if ab_test:
            if user_id % 2 == 0 or feature_id in opt_in:
                eligible_features[feature_id] = feature
        else:
            eligible_features[feature_id] = feature

    # Step 2: Resolve conflicts based on priority
    active_features = set(eligible_features.keys())

    for feature_id in list(active_features):
        if feature_id not in active_features:
            continue  # Already removed

        feature = eligible_features[feature_id]
        conflicts = set(feature.get("conflicts", []))
        priority = feature.get("priority", 0)

        for conflict_id in conflicts:
            if conflict_id in active_features:
                conflict_feature = eligible_features[conflict_id]
                conflict_priority = conflict_feature.get("priority", 0)

                # Remove the lower priority feature
                if priority > conflict_priority:
                    active_features.remove(conflict_id)
                elif priority < conflict_priority:
                    active_features.remove(feature_id)
                    break
                # If equal priority, keep both (or you could use ID as tie-breaker)

    return active_features


# Test Data for Part 3
users_part3 = [
    {"id": 0, "name": "eva", "location": "US", "optIn": ["annual_sale"]},
    {"id": 1, "name": "tess", "location": "US", "optIn": ["annual_sale"]},
    {"id": 2, "name": "rahool", "location": "CA", "optOut": ["enhanced_comments", "canada_promotion"]},
    {"id": 3, "name": "amanda", "location": "CA", "optIn": ["annual_sale"]}
]

features_part3 = [
    {
        "id": "annual_sale",
        "locations": ["US"],
        "abTest": True,
        "conflicts": ["enhanced_comments"],
        "priority": 10
    },
    {
        "id": "enhanced_comments",
        "abTest": True,
        "conflicts": ["annual_sale"],
        "priority": 5
    },
    {
        "id": "canada_promotion",
        "locations": ["CA"],
        "conflicts": [],
        "priority": 8
    }
]

print("\nPART3\n")
for user in users_part3:
    active = get_user_features_v3(user, features_part3)
    features_str = ", ".join(sorted(active)) if active else "N/A"
    print(f"{user['name']:<10} | {features_str}")

