# Q1: Minimum cost with no distances (all distances are 0)
def min_cost_no_distance(factories):
    """
    Simply pick the minimum cost option for each factory.
    Time: O(N*M) where N=factories, M=avg options per factory
    """
    total_cost = 0
    for factory_options in factories:
        min_cost = min(option[0] for option in factory_options)
        total_cost += min_cost
    return total_cost





# Q2: Minimum cost with distances (3 factories)
def min_cost_3_factories(factories):
    """
    Try all combinations of options for 3 factories.
    Time: O(M^3) where M=avg options per factory
    """
    min_total = float('inf')

    for opt1 in factories[0]:
        for opt2 in factories[1]:
            for opt3 in factories[2]:
                construction_cost = opt1[0] + opt2[0] + opt3[0]
                distance_penalty = abs(opt1[1] - opt2[1]) + abs(opt2[1] - opt3[1])
                total_cost = construction_cost + distance_penalty
                min_total = min(min_total, total_cost)

    return min_total







# Q3: Minimum cost with N factories (backtracking approach)
def min_cost_n_factories(factories):
    """
    Use backtracking to try all combinations.
    Time: O(M^N) - exponential
    """
    n = len(factories)
    min_cost = [float('inf')]

    def backtrack(factory_idx, chosen_options):
        if factory_idx == n:
            # Calculate total cost
            cost = calculate_cost(chosen_options)
            min_cost[0] = min(min_cost[0], cost)
            return

        # Try each option for current factory
        for option in factories[factory_idx]:
            chosen_options.append(option)
            backtrack(factory_idx + 1, chosen_options)
            chosen_options.pop()

    def calculate_cost(chosen_options):
        construction_cost = sum(opt[0] for opt in chosen_options)
        distance_penalty = sum(abs(chosen_options[i][1] - chosen_options[i + 1][1])
                               for i in range(len(chosen_options) - 1))
        return construction_cost + distance_penalty

    backtrack(0, [])
    return min_cost[0]






# Q4: Skip exactly one factory - NAIVE APPROACH
def min_cost_skip_one_naive(factories):
    """
    Try skipping each factory once, solve for remaining N-1 factories.
    Time: O(N * M^(N-1))
    """
    n = len(factories)
    min_total = float('inf')

    # Try skipping each factory
    for skip_idx in range(n):
        # Create list without the skipped factory
        remaining = [factories[i] for i in range(n) if i != skip_idx]
        cost = min_cost_n_factories(remaining)
        min_total = min(min_total, cost)

    return min_total


# Q4: Skip exactly one factory - OPTIMAL DP APPROACH
def min_cost_skip_one_optimal(factories):
    """
    Dynamic Programming approach.
    State: dp[i][j][skip_used] where:
      - i: number of factories processed (0 to N)
      - j: which option was chosen for last built factory (tuple of factory_idx, option_idx)
      - skip_used: boolean, whether we've used our skip

    Time: O(N^2 * M^2) where N=factories, M=avg options
    Space: O(N^2 * M)
    """
    n = len(factories)
    INF = float('inf')

    # dp[i][(last_factory_idx, last_option_idx)][skip_used] = min construction cost
    from collections import defaultdict

    # Current states
    dp = defaultdict(lambda: INF)
    dp[(None, None, False)] = 0  # No factory built yet, no skip used

    for i in range(n):
        new_dp = defaultdict(lambda: INF)

        for (last_factory_idx, last_option_idx, skip_used), cost in dp.items():
            # Option 1: Skip factory i (only if we haven't skipped before)
            if not skip_used:
                new_dp[(last_factory_idx, last_option_idx, True)] = min(
                    new_dp[(last_factory_idx, last_option_idx, True)],
                    cost
                )

            # Option 2: Build factory i with each available option
            for opt_idx, (build_cost, distance) in enumerate(factories[i]):
                new_cost = cost + build_cost

                # Add distance penalty if there was a previous factory
                if last_factory_idx is not None:
                    prev_distance = factories[last_factory_idx][last_option_idx][1]
                    new_cost += abs(distance - prev_distance)

                new_dp[(i, opt_idx, skip_used)] = min(
                    new_dp[(i, opt_idx, skip_used)],
                    new_cost
                )

        dp = new_dp

    # Find minimum among states where exactly one factory was skipped
    result = min(cost for (_, _, skip_used), cost in dp.items() if skip_used)
    return result


# Test with your example
array = [
    [[10, 0], [20, 0], [35, 0]],
    [[35, 0], [50, 0], [25, 0]],
    [[30, 0], [5, 0], [40, 0]]
]

print("Q1 - No distances:", min_cost_no_distance(array))
print("Q2 - 3 factories with distances:", min_cost_3_factories(array))
print("Q3 - N factories with distances:", min_cost_n_factories(array))
print("Q4 - Skip one (naive):", min_cost_skip_one_naive(array))
print("Q4 - Skip one (optimal DP):", min_cost_skip_one_optimal(array))

# Test with actual distances
array_with_distance = [
    [[10, 0], [20, 5], [35, 10]],
    [[35, 3], [50, 8], [25, 15]],
    [[30, 2], [5, 12], [40, 20]]
]

print("\n--- With actual distances ---")
print("Q3 - N factories:", min_cost_n_factories(array_with_distance))
print("Q4 - Skip one (optimal DP):", min_cost_skip_one_optimal(array_with_distance))