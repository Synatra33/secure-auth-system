from getpass import getpass



def login_flow(auth_service, user_service):
    print("=== LOGIN ===")

    username = input("Username: ").strip().lower()
    password = getpass("Password: ").strip()

    result = auth_service.authenticate(username, password)

    if not result:
        print("Login failed.")
        return

    identity, refresh_token = result

    from interfaces.cli.router import route_user
    route_user(identity, refresh_token, auth_service, user_service)
