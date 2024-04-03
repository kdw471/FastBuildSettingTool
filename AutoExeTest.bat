@echo off
::총실행횟수를 외부 파라미터로 받음
set /a exeTimes=%1

::실행 시작후와 실행 종료후 대기시간을 지정(단위:초)
set /a waitTime=5

::읽을 Log파일의 위치를 명시적 지정
set logPath=C:\Users\%username%\AppData\Local\TheStrangeCity\Saved\Logs\TheStrangeCity.log

::실행 파일의 상대적 위치 설정
set exePath=..\Windows

::현재 실행 횟수 카운팅 변수
set /a counter=0

::현재 실행 성공 횟수 카운팅
set /a succeddTimes=0

::실행 루프 구문
:BeginPoint

::실행 성공문자 카운팅 변수
set /a foundCnt=0

::실행 시작
start %exePath%\TheStrangeCity.exe

::대기
timeout %waitTime%

::실행 종료
taskkill /IM TheStrangeCity.exe /f /t

::로그 파일에서 성공문자 읽어서 결과 반환
for /F "delims=" %%x in ('findstr /C:"PathManager" %logPath%') do set /a foundCnt=%foundCnt%+1

::성공문자 계수가 1이상이라면 성공
if %foundCnt% GTR 0 (
	set /a succeddTimes=%succeddTimes%+1
	set succeddTimes
	echo Execute Successfully!
)

::실행 횟수 증가
set /a counter=%counter%+1
set counter

::현실행 횟수가 총실행 횟수에 다다르면 종료
if %counter% GEQ %exeTimes% (
	echo %succeddTimes%:%exeTimes%>ExeLog.txt
	timeout 1000
) else ( 
timeout %waitTime%
goto BeginPoint
 )
