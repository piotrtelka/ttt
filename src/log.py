from datetime import datetime


def log(*args):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: ", end="")
    print(*args)
