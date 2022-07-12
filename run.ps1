#cd "%USERPROFILE%\Desktop\Data Report"
$old = Read-Host "Please enter the date to replace in the following format: 'YYYY-MM-DD' (CHECK date of queries in the python file!) "
$monthago = Read-Host "Please enter the date exactly one month ago in the following format: 'YYYY-MM-DD' "
(gc page.py) -replace $old, $monthago | Out-File -encoding ASCII page.py
python page.py
#PAUSE