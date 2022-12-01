import pathlib
import shutil
import site
import subprocess


git_global_config_path = pathlib.Path(
    subprocess.check_output("git -c core.editor=echo config --global --edit", text=True).strip()
)

python_site_packages_path = pathlib.Path(site.getusersitepackages())


python_site_packages_path.mkdir(exist_ok=True, parents=True)


shutil.copy(".gitconfig", git_global_config_path)

for it in pathlib.Path.cwd().glob("*.py"):
    if it.name != "x.py":
        shutil.copy(it, python_site_packages_path)
