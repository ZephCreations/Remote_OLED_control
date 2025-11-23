# Update Project from git
#   Initialisation commands for reference:
#   git init
#   git remote add origin https://github.com/ZephCreations/Remote_OLED_control.git

git fetch origin
git reset --hard origin/master
git pull origin master

# Activate venv
source venv/bin/activate

# Start file
while true; do
    python src/main.py
    echo "main.py exited with code $? — restarting in 2 seconds"
    sleep 2
done

# Deactivate venv
deactivate

exit