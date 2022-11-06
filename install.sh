SITE_PACKAGES_PATH=`python -m site --user-site`

cp "evol.py" "$SITE_PACKAGES_PATH" --force
cp "notify.py" "$SITE_PACKAGES_PATH" --force