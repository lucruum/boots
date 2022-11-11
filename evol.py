import subprocess
import sys


glyph_width = 10
glyph_height = 6
glyphs = [
    ["_______   ", "\\   _  \\  ", "/  /_\\  \\ ", "\\  \\_/   \\", " \\_____  /", "       \\/ "],
    [" ____     ", "/_   |    ", " |   |    ", " |   |    ", " |___|    ", "          "],
    ["________  ", "\\_____  \\ ", " /  ____/ ", "/       \\ ", "\\_______ \\", "        \\/"],
    ["________  ", "\\_____  \\ ", "  _(__  < ", " /       \\", "/______  /", "       \\/ "],
    ["   _____  ", "  /  |  | ", " /   |  |_", "/    ^   /", "\\____   | ", "     |__| "],
    [" .________", " |   ____/", " |____  \\ ", " /       \\", "/______  /", "       \\/ "],
    ["  ________", " /  _____/", "/   __  \\ ", "\\  |__\\  \\", " \\_____  /", "       \\/ "],
    ["_________ ", "\\______  \\", "    /    /", "   /    / ", "  /____/  ", "          "],
    ["  ______  ", " /  __  \\ ", " >      < ", "/   --   \\", "\\______  /", "       \\/ "],
    [" ________ ", "/   __   \\", "\\____    /", "   /    / ", "  /____/  ", "          "],
]

offsets = [
    [1, 2, 0, 1, 0, 1, 1, 3, 0, 2],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [2, 1, 1, 0, 1, 0, 2, 2, 1, 1],
    [1, 1, 0, 1, 0, 1, 1, 2, 0, 1],
    [0, 2, 1, 2, 1, 2, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 2, 2, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 2, 0, 1],
    [1, 0, 1, 1, 2, 2, 1, 1, 1, 0],
]


def render(x):
    digits = [int(it) for it in str(x)]

    positions = [0]
    for i in range(len(digits) - 1):
        positions.append(positions[-1] + glyph_width - offsets[digits[i]][digits[i + 1]])

    art = [[" " for _ in range(positions[-1] + glyph_width)] for _ in range(glyph_height)]

    for i, it in enumerate(digits):
        for y in range(glyph_height):
            for x in range(glyph_width):
                if glyphs[it][y][x] != " " and art[y][positions[i] + x] in (" ", "|", "_"):
                    art[y][positions[i] + x] = glyphs[it][y][x]

    return "\n".join("".join(it) for it in art)


default_branch = subprocess.check_output(
    "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'",
    shell=True,
    text=True,
).strip()

if len(sys.argv) == 1:
    if subprocess.run("git symbolic-ref HEAD --quiet", stdout=subprocess.DEVNULL).returncode == 0:
        n = 1
    else:
        head_hash = subprocess.check_output("git rev-parse HEAD", shell=True, text=True).strip()
        n = (
            int(
                subprocess.check_output(
                    f"git rev-list {default_branch} --reverse | grep {head_hash} --line-number | cut --fields=1 --delimiter=':'",
                    shell=True,
                )
            )
            + 1
        )
else:
    n = int(sys.argv[1])

subprocess.run("cls & git rollback", shell=True)
subprocess.run(f"git rev-list {default_branch} --reverse | sed '{n}q;d' | xargs git checkout", shell=True)
subprocess.run("cls", shell=True)
print(render(n))
subprocess.run("git show --stat & code . --reuse-window", shell=True)
