def solve_user_linking(rows, weights, threshold, target_user_id):
    # Helper to calculate similarity between two records
    def get_score(u1, u2):
        score = 0
        for field, weight in weights.items():
            if u1[field] == u2[field]:
                score += weight
        return score

    # 1. Build the Adjacency List (The Graph)
    adj = {row['id']: [] for row in rows}
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if get_score(rows[i], rows[j]) >= threshold:
                adj[rows[i]['id']].append(rows[j]['id'])
                adj[rows[j]['id']].append(rows[i]['id'])

    # --- PART 1: Direct Matches ---
    # Just the target and those directly connected to it
    direct_matches = {target_user_id} | set(adj[target_user_id])

    # --- PART 2: Follow-up 1 (1-Hop) ---
    # Direct matches + their immediate neighbors
    one_hop_matches = set(direct_matches)
    for neighbor in adj[target_user_id]:
        one_hop_matches.update(adj[neighbor])

    # --- PART 3: Follow-up 2 (All Indirect / Full Component) ---
    full_component = set()
    queue = [target_user_id]
    visited = {target_user_id}

    while queue:
        curr = queue.pop(0)
        full_component.add(curr)
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return {
        "direct": sorted(list(direct_matches)),
        "one_hop": sorted(list(one_hop_matches)),
        "full_component": sorted(list(full_component))
    }


# --- Example Execution ---
rows = [
    {"id": 1, "name": "Alice", "email": "alice@gmail.com", "company": "Stripe"},
    {"id": 2, "name": "Alicia", "email": "alice@gmail.com", "company": "Stripe"},
    {"id": 3, "name": "Alice", "email": "alice@yahoo.com", "company": "Google"},
    {"id": 4, "name": "Bob", "email": "bob@gmail.com", "company": "Stripe"}
]
weights = {"name": 0.2, "email": 0.5, "company": 0.3}
threshold = 0.5

results = solve_user_linking(rows, weights, threshold, 1)
print(results)