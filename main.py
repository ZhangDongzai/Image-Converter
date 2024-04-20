import concurrent.futures
import os
import time

import PIL.Image


PATH = "./path.txt"
FILE_END = ".bmp"
CHANGE_END = ".png"
FORMAT = "PNG"


def get() -> list[str]:
    dirs: list[str] = []
    paths: list[str] = []
    with open(file=PATH, encoding="utf-8") as file:
        for line in file.readlines():
            dirs.append(line.rstrip("\n"))
    for dir in dirs:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if not path.endswith(FILE_END):
                continue
            paths.append(os.path.join(dir, name))
    return paths


def convert(path: str) -> None:
    destination_path = os.path.splitext(path)[0] + CHANGE_END

    with PIL.Image.open(path) as file:
        file.save(destination_path, format=FORMAT)


def timer(function: object) -> object:
    def run(*arg: object, **kwarg: object) -> None:
        start_time = time.perf_counter()
        result = function(*arg, **kwarg)
        print(f"Running time: {time.perf_counter() - start_time}")
        return result
    return run


@timer
def main() -> None:
    pool = concurrent.futures.ProcessPoolExecutor()
    paths = get()
    pool.map(convert, paths)
    pool.shutdown()


if __name__ == "__main__":
    main()
