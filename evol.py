import subprocess
import sys

import graffiti


default_branch = subprocess.check_output(
    "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'",
    shell=True,
    text=True,
).strip()

if len(sys.argv) == 1:
    if subprocess.run("git symbolic-ref HEAD --quiet", stdout=subprocess.DEVNULL).returncode == 0:
        n = 1
    else:
        is_headed_with_merge_commit = (
            int(subprocess.check_output("git rev-list HEAD --parents -1 | wc --word", shell=True, text=True)) > 2
        )
        if not is_headed_with_merge_commit:
            subprocess.run("git reset --hard & git del", shell=True)
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
print(graffiti.render(str(n)))
subprocess.run("git show --stat & code . --reuse-window", shell=True)
subprocess.run("git revert HEAD --no-edit & git revert HEAD --no-commit & git reset", shell=True)
