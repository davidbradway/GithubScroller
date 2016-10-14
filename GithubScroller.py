#!/usr/bin/env python3
from subprocess import call

def main():
    call(["git", "add", "."])
    call(["git", "status"])
    call(["git", "commit", "-m", "'add file'"])
    #call(["git", "push"])
    return 0

if __name__ == '__main__':
    main()