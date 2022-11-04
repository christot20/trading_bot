$Day = (get-date).DayOfWeek
$Date = get-date -DisplayHint Date
$HolidayTable = @(
    # 2022/2023 US Federal Holidays (From September 2022 - December 2023)
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
)

$wshell = New-Object -ComObject wscript.shell # used for keyboard input
if (($Day -ne "Saturday" -and $Day -ne "Sunday") -and ($Date -notin $HolidayTable)) # if it is trading day
{
    venv\Scripts\activate # activate venv
    Start-Sleep ((get-date '04:00am') - (get-date)).TotalSeconds # wait until its 4
    Start-Process 'c:/trading_bot/venv/Scripts/python.exe' -ArgumentList 'c:/trading_bot/app/sheet_writer.py' # start sheet writer
    Start-Sleep 5
    streamlit run .\app\app.py # run app locally
}