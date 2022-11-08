GIT_GLOBAL_CONFIG_PATH=`git -c core.editor=echo config --global --edit | sed "s/hint: Waiting for your editor to close the file... //"`
PYTHON_SITE_PACKAGES_PATH=`python -m site --user-site`

cp ".gitconfig" "$GIT_GLOBAL_CONFIG_PATH" --force
find -name "*.py" -exec cp {} "$PYTHON_SITE_PACKAGES_PATH" --force \;
