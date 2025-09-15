LOGO_PATH = "assets/logo.txt"

COLORS = {
    -1: '\33[0m',   # WHITE
    0: '\33[90m',   # GRAY
    1: '\33[92m',   # GREEN
    2: '\33[93m',   # YELLOW
    3: '\33[91m',   # RED
    4: '\33[94m',   # BLUE
}


def draw_logo(logo_path: str = LOGO_PATH) -> None:
    color_end = COLORS.get(-1)
    with open(logo_path, "r") as file:
        for i, line in enumerate(file):
            color_i = COLORS.get(i)
            print(f"{color_i}{line}{color_end}", end='')


if __name__ == "__main__":
    draw_logo()