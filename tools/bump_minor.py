#!/usr/bin/env python3
import sys

def main():
    """ This function increases the minor version number """

    if len(sys.argv) < 2:
        print(f"Use: {sys.argv[0]} CURRENT_VERSION")
        sys.exit()

    ver_list = sys.argv[1].split('.')
    ver_list[-1] = str(int(ver_list[-1])+1)
    new_ver = '.'.join(ver_list)
    print(new_ver)

if __name__ == "__main__":
    main()
