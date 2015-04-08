#!/usr/bin/env sh

# Run virtualenv if env/ doesn't exist
if [ ! -d "./env" ]; then
    virtualenv env
else
    echo "Virtual env already found..."
fi

# Parse command line arguments
print_usage() {
	cat <<_EOF_

Usage: $ [source] ./bootstrap.sh [OPTIONS]

Optionally source this script to activate virtual env in your shell.

    -d             use dev requirements
    -f             force reinstall of packages
    -h             show help
_EOF_
}

get_args() {
    local OPTIND
    dash_d=0
    dash_f=0
    while getopts "dfh" opt; do
      case $opt in
        h)
          print_usage
          return 0
          ;;
        d)
          dash_d=1
          ;;
        f)
          dash_f=1
          ;;
        \?)
          ;;
      esac
    done
}

get_args $@

# Activate virtualenv
. ./env/bin/activate

# Build install command string
install_dependencies() {
    IFS="%"  # Preserve whitespace in variables by changing inter field separator
    install_cmd="./env/bin/pip install -i http://pypi.digi.com/simple"
    if [ $dash_f -eq 1 ]; then
        # reinstall packages
	echo "Force reinstalling packages..."
        install_cmd=$(printf "%s --force-reinstall" $install_cmd )
    fi

    if [ $dash_d -eq 1 ]; then
        # use dev-requirements.txt
        install_cmd=$(printf " %s -r dev-requirements.txt" $install_cmd)
    else
        # use requirements.txt
        install_cmd=$(printf "%s -r requirements.txt" $install_cmd)
    fi

    eval $install_cmd
    unset IFS
}

if [ $dash_d -eq 1 ] && [ -f "dev-requirements.txt" ]; then
    echo "Installing development requirements..."
    install_dependencies
elif [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    install_dependencies
else
    echo "No requirements found..."
fi

