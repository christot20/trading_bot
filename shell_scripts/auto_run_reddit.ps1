# make if statement to check if the day is not saturday or sunday
$Day = (get-date).DayOfWeek
$Date = get-date -DisplayHint Date
$HolidayTable = @(
    # 2022/2023 US Federal Holidays (From Sepetmber 2022 - December 2023)
    'Monday, September 5, 2022',
    'Thursday, November 24, 2022',
    'Monday, December 26, 2023',
    'Monday, January 2, 2023',
    'Monday, January 16, 2023',
    'Monday, February 20, 2023',
    'Friday, April 7, 2023',
    'Monday, May 29, 2023',
    'Monday, June 19, 2023'
    'Tuesday, July 4, 2023',
    'Monday, September 4, 2023',
    'Thursday, November 23, 2023',
    'Monday, December 25, 2023'
);
if (($Day -ne "Saturday" -and $Day -ne "Sunday") -and ($Date -notin $HolidayTable))
{
    Start-Process "c:/trading_bot/venv/Scripts/python.exe" -ArgumentList "c:/trading_bot/src/bot.py"
    $wshell = New-Object -ComObject wscript.shell
    Start-Sleep 10
    $wshell.SendKeys('r') # make something so that it takes an input on what to choose (r, a, or m)
    $wshell.SendKeys('{ENTER}')
    Start-Sleep ((get-date "4:00pm") - (get-date)).TotalSeconds
    Stop-Process -Name "Python" # works
    # $wshell.SendKeys('^c') # just to make sure
    # might want to exit as well
}
# taskkill /pid $PID
# exit

# next things to do are try to get this working on main machine, start working on algo version
# and more tests

