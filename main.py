import argparse

import easy_scale


def main():
    parser = argparse.ArgumentParser(description="Easily scale your windows evenly across monitors in X11")
    parser.add_argument("-d", "--dpi", type=float,
                        help="Which dpi should be used before scaling. Defaults to 2x the lowest res monitor after "
                             "being scaled.")
    parser.add_argument("-s", "--scale", type=float, default=100,
                        help="How much to scale scale the monitors as a percent (100 is not scaled).")
    parser.add_argument("-p", "--primary", required=True,
                        help="Which monitor you want to use as the primary monitor.")
    parser.add_argument("monitors", nargs='+',
                        help="List of monitors you want to use moving left to right including the resolution, rate, "
                             "and diagonal inch size. For example: DisplayPort-1,1920x1080@144,27")

    args = parser.parse_args()
    easy_scale.run(args)


if __name__ == '__main__':
    main()
