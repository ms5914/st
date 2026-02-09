# accounts = [
#     {"accountId": "team_1", "parent": "wksp_1"}
#     {"accountId": "org_1", "parent": None},
#     {"accountId": "wksp_1", "parent": "org_1"},
#     {"accountId": "wksp_2", "parent": "org_1"},
#
# ]
#
# user_role_assignments = [
#     {"userId": "usr_1", "accountId": "org_1", "role": "admin"},
#     {"userId": "usr_2", "accountId": "wksp_1", "role": "editor"},
#     {"userId": "usr_3", "accountId": "wksp_1", "role": "viewer"},
#     {"userId": "usr_1", "accountId": "wksp_2", "role": "editor"}
# ]


class Org:
    def __init__(self, org_id):
        self.id  = org_id
        self.children  = set()
        self.roles_in_this_level = set()
class RBACRoleResolver:
    def __init__(self, accounts, user_role_assignments):
        self.accounts = accounts
        self.user_role_assignments = user_role_assignments
        self.orgs = dict()

        # Two pass since things might be onordered
        self.create_parent_accounts(accounts)
        self.create_parent_accounts(accounts)

    def create_parent_accounts(self, accounts):
        for account_id, parent_id in accounts:
            if account_id not in self.orgs:
                current_org = Org(account_id)
                self.orgs[account_id] = current_org
                if parent_id in self.orgs:
                    parent_elem = self.orgs[parent_id]
                    parent_elem.children.add(current_org)



rbac = RBACRoleResolver(accounts, user_role_assignments)


