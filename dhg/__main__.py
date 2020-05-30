import sys
import dhg.draw_grid as draw
import dhg.detect_grid as detect


class CommandException(BaseException):
    def __init__(self, message="CommandException"):
        super(CommandException, self).__init__(message)


HELP_STR = "dhg has 2 commands.\n" \
            "-d, --draw followed by an int x where x is greater than 1.\n" \
            "An outfile maybe specified after the x to write the hex grid, without this the file is writen " \
            "as hex_grid_size_x.png.\n" \
            "The command draws a hex grid with the side length of x.\n" \
            "Examples: \n" \
            "\t-d 8\n" \
            "\t--draw 12 hex_grid.png\n" \
            "-i, --interpret followed by an int x communicating the the size of the grid and " \
           "the path of hex grid image.\n" \
            "An outfile maybe specified after hex grid image and the outfile, without this the file is writen " \
            "as coords.txt.\n\n" \
            "The command a interpreters a hex grid where the grid has been coloured grey (#C3C3C3, (195,195,195))\n" \
            "hexes and returns a list in the outfile of cube coords of the grey hexes.\n" \
            "Examples: \n" \
            "\t-i 8 hex_grid.png\n" \
            "\t--interpret 16 hex_grid.png cube_coords.txt"


# TODO implement argparse instead of manual parsing as below.
def main():
    try:
        if 3 <= len(sys.argv) <= 5:
            _, command, *inputs = sys.argv
            if command == "-i" or command == "--interpret":
                x, *d = inputs
                detect.image_to_grid(int(x), *d)
            elif command == "-d" or command == "--draw":
                x, *d = inputs
                if isinstance(d, str):
                    draw.save_grid(int(x), d)
                elif isinstance(d, list):
                    draw.save_grid(int(x))
                else:
                    raise CommandException()
            else:
                raise CommandException()
        else:
            raise CommandException()
    except BaseException:
        print(HELP_STR)


if __name__ == '__main__':
    main()

