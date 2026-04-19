import threading

server_state: dict = {
    # { "ip:port": { "name", "conn", "privilege", "messages", "connected_at", "last_seen" } }
    "active_clients": {},

    # [ { "from", "addr", "privilege", "text", "time" } ]
    "all_messages": [],

    "total_connections":    0,
    "rejected_connections": 0,
    "total_messages": 0,
    # Mutex — parandalon race conditions mes thread-ave
    "lock": threading.Lock()
}
