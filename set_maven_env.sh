#!/bin/bash

# Set Maven environment variables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &>/dev/null && pwd )"
MAVEN_BASEDIR="$SCRIPT_DIR"

# Export environment variables
export MAVEN_BASEDIR
echo "MAVEN_BASEDIR set to $MAVEN_BASEDIR"

# Check for JAVA_HOME
if [ -z "$JAVA_HOME" ]; then
    echo "WARNING: JAVA_HOME not set. Maven might not work properly."
    echo "Please set JAVA_HOME environment variable to the location of your Java installation."
fi

echo "Maven environment variables set successfully."
echo "You can now run ./mvnw from any directory."
