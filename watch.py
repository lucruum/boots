import argparse
import asyncio
import csv
import itertools
import pathlib
import subprocess


def is_running(task):
    if task is None:
        return False

    status = subprocess.run(
        f'tasklist /fi "pid eq {task.result().pid}" /fo csv /nh', encoding="oem", stdout=subprocess.PIPE
    ).stdout
    _, pid, *_ = next(csv.reader([status]))
    return pid == str(task.result().pid)


def kill(task):
    if is_running(task):
        subprocess.run(f"taskkill /pid {task.result().pid} /f /t", stdout=subprocess.DEVNULL)
        task.result().kill()
        task.cancel()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("-n", "--interval", type=float, default=1)
    args = parser.parse_args()

    command = args.command
    interval = args.interval

    task = None
    while True:
        kill(task)
        task = asyncio.ensure_future(asyncio.create_subprocess_shell(command))
        await asyncio.sleep(interval)


asyncio.run(main())
