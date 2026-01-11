from domain.role import Role
from interfaces.cli.admin_menu import admin_menu


def route_user(identity, refresh_token, auth_service, user_service):
    if identity.role == Role.ADMIN:
        admin_menu(identity, refresh_token, auth_service, user_service)
    else:
        print(f"Welcome, {identity.username}.")
