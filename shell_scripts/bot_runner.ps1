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
    $choices = 'm','a','r'
    $counter = 0
    Foreach ($choice in $choices)
    {
        Start-Process "c:/trading_bot/venv/Scripts/python.exe" -ArgumentList "c:/trading_bot/src/bot.py"
        $wshell = New-Object -ComObject wscript.shell
        Start-Sleep 30
        $wshell.SendKeys($choice) # make something so that it takes an input on what to choose (r, a, or m)
        $wshell.SendKeys('{ENTER}')
        if ($counter -eq 0)
        {
            Start-Sleep ((get-date "09:30am") - (get-date)).TotalSeconds
        }
        $counter++
    }
    Start-Sleep ((get-date "11:00am") - (get-date)).TotalSeconds
    Stop-Process -Name "Python" # works
}
exit