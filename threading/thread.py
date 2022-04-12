# Original Code FezMaster on BSE - CC BY-SA 4.0
# https://blender.stackexchange.com/a/260369/86891
import threading
from time import sleep


def on_exit():
    print("Exiting Thread")


def loop():
    # while True:
    for i in range(10):
        sleep(0.25)
        print("Thread executing loop")
    on_exit()


if __name__ == "__main__":
    thread = threading.Thread(target=loop)
    thread.start()
