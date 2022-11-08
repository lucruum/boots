PYTHON_SITE_PACKAGES_PATH=`python -m site --user-site`

find -name "*.py" -exec cp {} "$PYTHON_SITE_PACKAGES_PATH" --force \;
