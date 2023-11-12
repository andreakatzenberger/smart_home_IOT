import getpass

def run_dms_simulator(callback, stop_event, print_lock):
    dms_keys = ["A", "B", "C", "D",
                "1", "2", "3", "4",
                "5", "6", "7", "8",
                "9", "0", "*", "#" ]
    while True:
        key = str(getpass.getpass("").capitalize().strip())
        if key in dms_keys:
            with print_lock:
                callback(key)

        if stop_event.is_set():
            break