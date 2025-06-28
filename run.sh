#!/bin/bash

# Check if script was executed using bash and not sh!
isBashNotSh ()
{
    if [ -n "$BASH_VERSION" ]; then
        echo "Running under Bash (version: $BASH_VERSION)"
    else
        echo "Not running under Bash! Run script under bash and not sh!!!"
        exit
    fi
}

# Automatically setup Python3 venv for XnorDuinoDesktop, using the requirements.txt file.
runVenvSetup ()
{
    REPO_DIR=$1"requirements.txt"

    echo "Installing packages from requirements.txt..."

    set -e  # Exit on any error
    # Create a virtual environment
    if [ ! -d "venv" ]; then
      echo "Creating virtual environment..."
      python3 -m venv venv
    fi

    echo "Activating virtual environment..."
    source venv/bin/activate

    echo "Upgrading pip..."
    pip install --upgrade pip

    echo "Installing dependencies from requirements.txt..."
    pip install -r $REPO_DIR
    echo "✅ Done installing XnorDuinoDesktop..."
}


# Fetch the application from git using clone command:
runGitClone ()
{
    URL=$1

    echo "Cloning latest XnorDuinoDesktop version from: $URL"
    rm -Rf XnorDuinoDesktop/
    rm -Rf venv/
    git clone --depth=1 --branch $(git ls-remote --tags --sort="v:refname" $URL | tail -n1 | sed 's/.*\///') $URL

    # command to fetch one release older, for testing:
    # git clone --depth=1 --branch $(git ls-remote --tags --sort="v:refname" $URL | tail -n2 | head -n1 | sed 's/.*\///') $URL
}

# Run update of application after previous installations:
runUpdate ()
{
    REPO_DIR=$1
    URL=$2

    cd $REPO_DIR
    local_tag=$(git describe --tags --abbrev=0)
    remote_tag=$(git ls-remote --tags --sort="v:refname" $URL | tail -n1 | sed 's/.*\///')
    if [ "$local_tag" != "$remote_tag" ]; then
        echo "Newer release detected: $remote_tag (local: $local_tag). Updating..."

        # Fetch latest tags and checkout new release
        git fetch --tags --depth=1
        git checkout $remote_tag

        # check if additional dependencies require updates:
        cd ..
        runVenvSetup $REPO_DIR
    else
        cd ..
        echo "Local repo is already up-to-date: $local_tag"
    fi


}

killRunningInstances ()
{
    # kill existing opened screens
    echo "Closing running instances..."
    screen -ls | awk '/\t[0-9]+\.main_flask/{print $1}' | xargs -r -n 1  -I {} screen -S {} -X quit
    screen -ls | awk '/\t[0-9]+\.main_serialServer/{print $1}' | xargs -r -n 1  -I {} screen -S {} -X quit
    screen -ls | awk '/\t[0-9]+\.xbeeServer/{print $1}' | xargs -r -n 1  -I {} screen -S {} -X quit
}

executeInstances ()
{
    # Execute python code:
    echo "Launching XnorDuinoDesktop..."
    screen -dmS main_flask venv/bin/python XnorDuinoDesktop/FlaskGUI/main_flask.py
    screen -dmS main_serialServer venv/bin/python XnorDuinoDesktop/SerialServer/main.py
    screen -dmS xbeeServer venv/bin/python XnorDuinoDesktop/XbeeServer/main.py
}


# ============= Main Functions ==================
# ===============================================
_REPO_DIR_="XnorDuinoDesktop/"
_URL_="https://github.com/timdv91/XnorDuinoDesktop.git"

# check if ran as bash and not sh:
isBashNotSh

# check if install or update is needed:
if [ ! -d $_REPO_DIR_ ]; then
    runGitClone $_URL_
    runVenvSetup $_REPO_DIR_
else
    killRunningInstances
    runUpdate $_REPO_DIR_ $_URL_
fi

# update the run file:
cp $_REPO_DIR_"/run.sh" run.sh

executeInstances

