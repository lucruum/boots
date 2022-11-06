import subprocess
import sys


if len(sys.argv) == 2 and sys.argv[1] == "rollback":
    subprocess.run(
        "git reset --hard &"
        "git clean --force -dx &"
        "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@' | xargs git checkout",
        shell=True,
    )
    exit()


if len(sys.argv) == 1:
    if subprocess.check_output("git status --porcelain", shell=True):
        n = int(subprocess.check_output("git rev-list HEAD | wc --lines", shell=True)) + 2
    else:
        n = 2
else:
    n = int(sys.argv[1])

subprocess.run(
    "cls &"
    "git reset --hard &"
    "git clean --force -dx &"
    "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@' | xargs git checkout",
    shell=True,
)

subprocess.run(f"git rev-list HEAD --reverse | sed '{n}q;d' | xargs git checkout", shell=True)

subprocess.run(
    "cls & git show --stat & git reset HEAD~1 --quiet --soft & git reset & code . --reuse-window",
    shell=True,
)
