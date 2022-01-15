#!/usr/bin/env osascript

on run scriptpath
    tell application "Terminal"
        my makeTab()
        do script "workon hume && python " & scriptpath & "/../hume/main.py $HUME_UUID sim" in front window
    end tell
end run

on makeTab()
    tell application "System Events" to keystroke "t" using {command down}
end makeTab
