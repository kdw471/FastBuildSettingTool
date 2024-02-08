@echo off
set /a exeTimes=%1
set /a waitTime=3
set logPath=C:\Users\%username%\AppData\Local\TheStrangeCity\Saved\Logs\TheStrangeCity.log
set exePath=..\Windows
set /a counter=0
set /a succeddTimes=0

:BeginPoint
start %exePath%\TheStrangeCity.exe
timeout %waitTime%
taskkill /IM TheStrangeCity.exe /f /t

for /F "delims=" %%x in ('findstr /C:"PathManager" %logPath%') do set result=%%x

if %ERRORLEVEL% ==0 (
	set /a succeddTimes=%succeddTimes%+1
	set succeddTimes
	echo Execute Successfully!
)

set /a counter=%counter%+1
set counter

if %counter% GEQ %exeTimes% (
	echo %succeddTimes%:%exeTimes%>ExeLog.txt
	timeout 1000
) else ( goto BeginPoint )
