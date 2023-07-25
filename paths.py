from pathlib import Path

prjpath = Path(__file__).parent


def create_if_not_exists(func):
    def wrapper(*args):
        p = func(*args)
        p.mkdir(exist_ok=True)
        return p

    return wrapper


@create_if_not_exists
def OUTDIR():
    return prjpath.joinpath("output")


filepath = lambda filename: OUTDIR().joinpath(filename)
