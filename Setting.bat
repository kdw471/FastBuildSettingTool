@echo off

::ip 구하기
for /f "tokens=2 delims=:" %%f in ('ipconfig ^| findstr /C:"IPv4"') do set IP=%%f

::공유 폴더가 속한 PC의 IP를 설정(사용자 지정)
set SharedPathIP=192.168.1.200

::공유 IP와 현재 PC IP가 같으면 로컬호스트 IP로 설정
if %IP%==%SharedPathIP% set SharedPathIP=127.0.0.1

set ExePath=C:\FastBuild
set BrokeragePath=\\%SharedPathIP%\FastBuildBrokeragePath
set FastBuildFilesCopyPath=%BrokeragePath%\FastBuildSetting
set CachePath= %BrokeragePath%\Cache
set CacheMode=rw
::최신 FastBuild 실행파일을 로컬 FastBuild 폴더에 복사
mkdir %ExePath%
copy /Y %FastBuildFilesCopyPath% %ExePath%\

::Path 환경변수에 FastBuild 실행파일 경로추가
::setx Path "%Path%;%ExePath%"
setx FASTBUILD_EXECUTABLE_PATH %ExePath%\FBuild.exe

::공유폴더 IP 경로
setx FASTBUILD_BROKERAGE_PATH %BrokeragePath%
setx FASTBUILD_CACHE_PATH %CachePath%
setx FASTBUILD_CACHE_MODE %CacheMode%

::BuildConfiguration.xml 태그 관련 수정 사항 적용(allowFASTBuild->true 등)
python %ExePath%\FastBuildConfigurationUpdate.py
timeout 5