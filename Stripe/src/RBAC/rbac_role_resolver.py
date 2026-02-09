from collections import defaultdict


class RBACRoleResolver:
    def __init__(self, accounts: list[dict], user_role_assignments: list[dict]):
        # Map account to parent
        self.parent_map = {}
        for account in accounts:
            self.parent_map[account["accountId"]] = account["parent"]

        # Map: (userId, accountId) -> set of roles
        self.role_map = defaultdict(set)
        for assignment in user_role_assignments:
            key = (assignment["userId"], assignment["accountId"])
            self.role_map[key].add(assignment["role"])

        # Index: accountId -> set of userIds
        self.users_by_account = defaultdict(set)
        for assignment in user_role_assignments:
            self.users_by_account[assignment["accountId"]].add(assignment["userId"])

    def _getAncestors(self, accountId: str) -> list[str]:
        """Helper: Get account and all parents."""
        ancestors = []
        current = accountId
        while current is not None:
            ancestors.append(current)
            current = self.parent_map.get(current)
        return ancestors

    def getUserRoles(self, userId: str, accountId: str) -> list[str]:
        """Get all roles including inherited ones."""
        roles = set()
        for ancestor in self._getAncestors(accountId):
            key = (userId, ancestor)
            if key in self.role_map:
                roles.update(self.role_map[key])
        return list(roles)

    def getUsersForAccount(self, accountId: str) -> list[str]:
        """Get all users with any role on this account."""
        users = set()
        for ancestor in self._getAncestors(accountId):
            users.update(self.users_by_account.get(ancestor, set()))
        return list(users)

    def getUsersForAccountWithFilter(self, accountId: str, roleFilters: list[str]) -> list[str]:
        """Get users who have all specified roles."""
        all_users = self.getUsersForAccount(accountId)

        if not roleFilters:
            return all_users

        required_roles = set(roleFilters)
        return [
            user_id for user_id in all_users
            if required_roles.issubset(set(self.getUserRoles(user_id, accountId)))
        ]

    def addRoleAssignment(self, userId: str, accountId: str, role: str):
        """Add a role assignment dynamically."""
        key = (userId, accountId)
        self.role_map[key].add(role)
        self.users_by_account[accountId].add(userId)


# ─── Test Suite ───────────────────────────────────────────────────────────────

def test_phase1_direct_lookup():
    print("=" * 60)
    print("Phase 1: Direct Role Lookup")
    print("=" * 60)

    accounts = [
        {"accountId": "org_1", "parent": None},
        {"accountId": "wksp_1", "parent": "org_1"},
        {"accountId": "wksp_2", "parent": "org_1"},
        {"accountId": "team_1", "parent": "wksp_1"},
    ]
    assignments = [
        {"userId": "usr_1", "accountId": "org_1", "role": "admin"},
        {"userId": "usr_2", "accountId": "wksp_1", "role": "editor"},
        {"userId": "usr_3", "accountId": "wksp_1", "role": "viewer"},
        {"userId": "usr_1", "accountId": "wksp_2", "role": "editor"},
    ]

    # For phase 1 only, we test direct lookup by temporarily bypassing inheritance.
    # But since getUserRoles already includes inheritance, we verify direct assignments
    # by checking accounts with no parents.
    rbac = RBACRoleResolver(accounts, assignments)

    # Direct: usr_1 at org_1 -> ["admin"]
    result = rbac.role_map.get(("usr_1", "org_1"), set())
    print(f"  Direct roles usr_1 @ org_1: {sorted(result)}")
    assert result == {"admin"}, f"Expected {{'admin'}}, got {result}"

    # Direct: usr_1 at wksp_2 -> ["editor"]
    result = rbac.role_map.get(("usr_1", "wksp_2"), set())
    print(f"  Direct roles usr_1 @ wksp_2: {sorted(result)}")
    assert result == {"editor"}, f"Expected {{'editor'}}, got {result}"

    # Direct: usr_2 at wksp_1 -> ["editor"]
    result = rbac.role_map.get(("usr_2", "wksp_1"), set())
    print(f"  Direct roles usr_2 @ wksp_1: {sorted(result)}")
    assert result == {"editor"}, f"Expected {{'editor'}}, got {result}"

    # Direct: usr_3 at org_1 -> [] (no direct assignment)
    result = rbac.role_map.get(("usr_3", "org_1"), set())
    print(f"  Direct roles usr_3 @ org_1: {sorted(result)}")
    assert result == set(), f"Expected set(), got {result}"

    print("  ✅ Phase 1 passed!\n")


def test_phase2_inheritance():
    print("=" * 60)
    print("Phase 2: Inheritance")
    print("=" * 60)

    accounts = [
        {"accountId": "org_1", "parent": None},
        {"accountId": "wksp_1", "parent": "org_1"},
        {"accountId": "team_1", "parent": "wksp_1"},
    ]
    assignments = [
        {"userId": "usr_1", "accountId": "org_1", "role": "admin"},
        {"userId": "usr_1", "accountId": "wksp_1", "role": "editor"},
        {"userId": "usr_2", "accountId": "wksp_1", "role": "viewer"},
    ]

    rbac = RBACRoleResolver(accounts, assignments)

    result = sorted(rbac.getUserRoles("usr_1", "org_1"))
    print(f"  usr_1 @ org_1: {result}")
    assert result == ["admin"], f"Expected ['admin'], got {result}"

    result = sorted(rbac.getUserRoles("usr_1", "wksp_1"))
    print(f"  usr_1 @ wksp_1: {result}")
    assert result == ["admin", "editor"], f"Expected ['admin', 'editor'], got {result}"

    result = sorted(rbac.getUserRoles("usr_1", "team_1"))
    print(f"  usr_1 @ team_1: {result}")
    assert result == ["admin", "editor"], f"Expected ['admin', 'editor'], got {result}"

    result = sorted(rbac.getUserRoles("usr_2", "team_1"))
    print(f"  usr_2 @ team_1: {result}")
    assert result == ["viewer"], f"Expected ['viewer'], got {result}"

    result = sorted(rbac.getUserRoles("usr_2", "org_1"))
    print(f"  usr_2 @ org_1: {result}")
    assert result == [], f"Expected [], got {result}"

    print("  ✅ Phase 2 passed!\n")


def test_phase3_users_for_account():
    print("=" * 60)
    print("Phase 3: Finding Users with Access")
    print("=" * 60)

    accounts = [
        {"accountId": "org_1", "parent": None},
        {"accountId": "wksp_1", "parent": "org_1"},
        {"accountId": "wksp_2", "parent": "org_1"},
    ]
    assignments = [
        {"userId": "usr_1", "accountId": "org_1", "role": "admin"},
        {"userId": "usr_2", "accountId": "wksp_1", "role": "editor"},
        {"userId": "usr_3", "accountId": "wksp_1", "role": "viewer"},
    ]

    rbac = RBACRoleResolver(accounts, assignments)

    result = sorted(rbac.getUsersForAccount("org_1"))
    print(f"  Users @ org_1: {result}")
    assert result == ["usr_1"], f"Expected ['usr_1'], got {result}"

    result = sorted(rbac.getUsersForAccount("wksp_1"))
    print(f"  Users @ wksp_1: {result}")
    assert result == ["usr_1", "usr_2", "usr_3"], f"Expected ['usr_1', 'usr_2', 'usr_3'], got {result}"

    result = sorted(rbac.getUsersForAccount("wksp_2"))
    print(f"  Users @ wksp_2: {result}")
    assert result == ["usr_1"], f"Expected ['usr_1'], got {result}"

    print("  ✅ Phase 3 passed!\n")


def test_phase4_filter_by_role():
    print("=" * 60)
    print("Phase 4: Filtering Users by Role")
    print("=" * 60)

    accounts = [
        {"accountId": "org_1", "parent": None},
        {"accountId": "wksp_1", "parent": "org_1"},
    ]
    assignments = [
        {"userId": "usr_1", "accountId": "org_1", "role": "admin"},
        {"userId": "usr_1", "accountId": "wksp_1", "role": "editor"},
        {"userId": "usr_2", "accountId": "wksp_1", "role": "editor"},
        {"userId": "usr_3", "accountId": "wksp_1", "role": "viewer"},
    ]

    rbac = RBACRoleResolver(accounts, assignments)

    # No filter
    result = sorted(rbac.getUsersForAccountWithFilter("wksp_1", []))
    print(f"  Filter [] @ wksp_1: {result}")
    assert result == ["usr_1", "usr_2", "usr_3"]

    # admin filter
    result = sorted(rbac.getUsersForAccountWithFilter("wksp_1", ["admin"]))
    print(f"  Filter ['admin'] @ wksp_1: {result}")
    assert result == ["usr_1"]

    # editor filter
    result = sorted(rbac.getUsersForAccountWithFilter("wksp_1", ["editor"]))
    print(f"  Filter ['editor'] @ wksp_1: {result}")
    assert result == ["usr_1", "usr_2"]

    # admin AND editor filter
    result = sorted(rbac.getUsersForAccountWithFilter("wksp_1", ["admin", "editor"]))
    print(f"  Filter ['admin', 'editor'] @ wksp_1: {result}")
    assert result == ["usr_1"]

    # nonexistent role
    result = sorted(rbac.getUsersForAccountWithFilter("wksp_1", ["superadmin"]))
    print(f"  Filter ['superadmin'] @ wksp_1: {result}")
    assert result == []

    print("  ✅ Phase 4 passed!\n")


if __name__ == "__main__":
    test_phase1_direct_lookup()
    test_phase2_inheritance()
    test_phase3_users_for_account()
    test_phase4_filter_by_role()
    print("🎉 All phases passed!")
