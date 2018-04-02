#!/bin/bash

# Reference github gist: https://gist.github.com/ltfschoen/efaf16dd469ede2ef5283fc0e5d09232

function new_tab() {
  TAB_NAME=$1
  DELAY=$2
  COMMAND=$3
  osascript \
    -e "tell application \"Terminal\"" \
    -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
    -e "do script \"$DELAY; printf '\\\e]1;$TAB_NAME\\\a'; $COMMAND\" in front window" \
    -e "end tell" > /dev/null
}

new_tab "SEALS" \
			  "echo 'Loading SEALS...'"
