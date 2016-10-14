#!/usr/bin/env python3
import datetime as dt
from subprocess import call


def make_n_commits(n):
    for i in range(n):
        now = dt.datetime.now().strftime("%H:%M:%S.%f")
        call(["touch", "." + now + '.txt'])
        call(["git", "add", "."])
        call(["git", "commit", "-m", "'add " + now + " file'"])
    call(["git", "status"])
    call(["git", "push"])


def main():
    n = 4
    make_n_commits(n)


if __name__ == '__main__':
    main()
