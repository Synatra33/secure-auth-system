from domain.role import Role
from getpass import getpass
from interfaces.cli.admin_logs import view_audit_logs
from interfaces.cli.admin_users import view_users





def admin_menu(identity, refresh_token, auth_service, user_service):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. View users")
        print("2. Create user")
        print("3. Change role")
        print("4. Suspend user")
        print("5. Unlock user")
        print("6. View audit logs")
        print("7. Logout")

        choice = input("Select: ").strip()

        try:
            if choice == "1":
                view_users(user_service)

            if choice == "2":
                username = input("Username: ").strip().lower()
                password = getpass("Password: ").strip()
                role = Role(input("Role (admin/aux_admin/user): ").strip().lower())
                user_service.create_user(username, password, role)
                print("User created.")

            elif choice == "3":
                target = input("Target username: ").strip().lower()
                role = Role(input("New role: ").strip().lower())
                user_service.change_role(target, role, identity)
                print("Role updated.")

            elif choice == "4":
                target = input("Target username: ").strip().lower()
                user_service.suspend_user(target, identity)
                print("User suspended.")

            elif choice == "5":
                target = input("Target username: ").strip().lower()
                user_service.unlock_user(target, identity)
                print("User unlocked.")

            elif choice == "6":
                view_audit_logs(identity)

            elif choice == "7":
                auth_service.invalidate_all_sessions(identity.username)
                print("Logged out.")
                break

            else:
                print("Invalid option.")

        except Exception as e:
            print(f"Error: {e}")
