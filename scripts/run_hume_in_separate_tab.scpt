#!/usr/bin/env osascript
--
--osascript -e 'tell app "Terminal"
--  do script "cd ~/repos/hint; workon hint; ./manage.py runserver"
--  do script "cd ~/repos/hint/frontend; ng build --watch=true --outputPath=/Users/mansthornvik/repos/hint/backend/static/ang"
--end tell'

on run scriptpath
  tell application "Terminal"
    my makeTab()
    do script "cd " & scriptpath & "/../hume && workon hume && python main.py $HUME_UUID --sim" in front window
  end tell
end run

on makeTab()
  tell application "System Events" to keystroke "t" using {command down}
end makeTab
