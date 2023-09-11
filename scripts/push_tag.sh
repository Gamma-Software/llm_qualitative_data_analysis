# Get the version in args
version=$1

# Check if the version is in the right format (v1.0.0)
echo $version | grep -qP "^v[0-9]+\.[0-9]+\.[0-9]+$"

# If the version is not in the right format, exit with an error
if [ $? -ne 0 ]; then
    echo "Version $version is not in the right format (v1.0.0)"
    exit 1
fi

# Check if the version is not already tagged
git tag | grep -q $version

# If the version is already tagged, exit with an error
if [ $? -eq 0 ]; then
    echo "Version $version is already tagged"
    exit 1
fi

# Verify we are on main branch
git branch --show-current | grep -q "main"

# If the branch is not main, exit with an error
if [ $? -ne 0 ]; then
    echo "You are not on the main branch"
    exit 1
fi

# Apply the version number
sed -i "s/VERSION=\".*\"/VERSION=\"$version\"/" source/version.py
git add version.py
git commit -m "Bump version to $version"
git push origin main

# Tag the version
git tag "$version"
git push origin "$version"