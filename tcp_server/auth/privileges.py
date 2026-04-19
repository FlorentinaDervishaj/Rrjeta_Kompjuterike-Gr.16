from config import PRIVILEGES, ADMIN_PASSWORD
from core.state import server_state


def get_privilege(client_name: str) -> str:
    priv = PRIVILEGES.get(client_name, "read-only")
    return "admin" if priv == "admin" else "read-only"


def get_privilege_by_addr(addr_str: str) -> str:
    with server_state["lock"]:
        client = server_state["active_clients"].get(addr_str)
        if client:
            return client.get("priv", "read-only")
    return "read-only"


def set_privilege_by_addr(addr_str: str, priv: str) -> None:
    with server_state["lock"]:
        client = server_state["active_clients"].get(addr_str)
        if client:
            client["priv"]      = priv
            client["privilege"] = priv


def check_privilege(client_name: str, required: str) -> bool:
    priv = get_privilege(client_name)
    if required == "admin" and priv != "admin":
        return False
    return True


def check_privilege_by_addr(addr_str: str, required: str) -> bool:
    priv = get_privilege_by_addr(addr_str)
    if required == "admin" and priv != "admin":
        return False
    return True


def try_elevate_to_admin(addr_str: str, password: str) -> bool:
    if password == ADMIN_PASSWORD:
        set_privilege_by_addr(addr_str, "admin")
        return True
    return False