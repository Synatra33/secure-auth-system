# interfaces/cli/admin_users.py

def view_users(user_service):
    """
    Admin-only read-only view of all users and their roles.
    """

    users = user_service.list_users()

    if not users:
        print("No users found.")
        return

    print("\n--- USERS ---")
    print(f"{'USERNAME':<15} {'ROLE':<10} STATUS")
    print("-" * 35)

    for user in users:
        status = user.status.name
        role = user.role.value
        print(f"{user.username:<15} {role:<10} {status}")
