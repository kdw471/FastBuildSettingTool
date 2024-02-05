import xml.etree.ElementTree as ET
import getpass
import sys

# 실행 파라미터로 FastBuild 키고 끄는 방식
bAllowFastBuild = 'true'

# 파라미터 0일시 fastbuild 비활성화, 파라미터 없거나 다른 값일시 활성화
if len(sys.argv) > 1 and sys.argv[1]=='0':
    bAllowFastBuild = 'false'
else:
    bAllowFastBuild = 'true'

# 태그 탐색시 전역 namespace를 찾고자하는 태그네임 앞에 붙여서 탐색해야함
buildConfigNamespace =  "{https://www.unrealengine.com/BuildConfiguration}"
registerNamespace = "https://www.unrealengine.com/BuildConfiguration"

# 전역 namespace를 앞에 붙인 풀태그네임 반환
def GetTag(TagName):
    return buildConfigNamespace + TagName

# 태그네임 변수로 저장해둠
allowFastBuildTagName =  GetTag("bAllowFASTBuild")
buildConfigTagName = GetTag("BuildConfiguration")

fastBuildTagName = GetTag("FASTBuild")
enableDistributionTagName = GetTag("bEnableDistribution")
enableCacheTagName = GetTag("bEnableCaching")
cacheModeTagName = GetTag("CacheMode")

# namespace가 태그마다 표시되는 것을 방지, 전역으로 등록(using namespace std; 랑 비슷한듯, 하지만 보이는 것만 변경되고 탐색시는 여전히 namespace를 포함한 태그네임으로 해야함)
ET.register_namespace('', registerNamespace)

# 정확한 경로 산출을 위한 현재 유저명 가져오기
username = getpass.getuser()
buildConfigurationPath = "C:\\Users\\" + username + "\\AppData\\Roaming\\Unreal Engine\\UnrealBuildTool\\BuildConfiguration.xml"

# 산출된 경로의 xml 파일 불러옴
xmlTree = ET.parse(buildConfigurationPath)

# 경로를 못찾을시 종료
if xmlTree is None:
    print("BuildConfiguration.xml not found..Check C:\\Users\CurrentUserName Exists?")
    exit()

# xmlTree의 루트 태그 가져옴
xmlRoot = xmlTree.getroot()

# allowFastBuild 태그를 탐색
foundAllowFBTag = xmlRoot.find(".//" + allowFastBuildTagName)

# 탐색 성공시 값을 true로 설정해주고
# 탐색 실패시 태그 생성후 값을 true로 설정.
if foundAllowFBTag is not None:
    foundAllowFBTag.text = bAllowFastBuild
    print("Set bAllowFASTBuild to",str(bAllowFastBuild))
else:
    # 상위 태그인 BuildConfiguration 태그를 탐색
    buildConfigTag = xmlRoot.find(".//" + buildConfigTagName)

    # 탐색 성공시 하위에 bAllowFASTBuild 태그를 추가해주고
    # 탐색 실패시 BuildConfiguration 태그를 생성한 뒤에 bAllowFASTBuild 태그를 생성 및 추가
    if buildConfigTag is None:
        print("BuildConfiguration Tag Not Found, so create one")
        buildConfigTag = ET.SubElement(xmlRoot, buildConfigTagName)
    
    foundAllowFBTag = ET.SubElement(buildConfigTag, allowFastBuildTagName)
    foundAllowFBTag.text = bAllowFastBuild
    print("Set bAllowFASTBuild to",str(bAllowFastBuild))
    
# FastBuild 설정과 관련된 태그 FASTBuild와
# 그 하위 태그 bEnableDistribution, bEnableCaching을 없으면 추가해준다
# 위와 동일하게 진행

# fastBuildTag를 탐색
fastBuildTag = xmlRoot.find(".//" + fastBuildTagName)

# 탐색 성공시
if fastBuildTag is not None:
    # enableCacheTag, enableDistributionTag를 탐색 및 없을시 생성과 값true 세팅
    enableCacheTag = fastBuildTag.find(enableCacheTagName)
    if enableCacheTag is None:
        ET.SubElement(fastBuildTag, enableCacheTagName)
    enableCacheTag.text = str('true')
    print("Set enableCacheTag to true")

    cacheModeTag = fastBuildTag.find(cacheModeTagName)
    if cacheModeTag is None:
        ET.SubElement(fastBuildTag, cacheModeTagName)
    cacheModeTag.text = str('ReadWrite')
    print("Set cacheMode to ReadWrite")

    enableDistributionTag = fastBuildTag.find(enableDistributionTagName)
    if enableDistributionTag is None:
        ET.SubElement(fastBuildTag, enableDistributionTagName)
    enableDistributionTag.text = str('true')       
    print("Set enableDistributionTag to true")   
else:
    # 탐색 실패시
    # fastBuildTag를 xmlTree루트 하위태그로 생성해줌과 동시에 
    # enableCacheTag, enableDistributionTag를 생성과 값true 세팅
    fastBuildTag = ET.SubElement(xmlRoot, fastBuildTagName)
    ET.SubElement(fastBuildTag, enableCacheTagName).text = str('true')
    ET.SubElement(fastBuildTag, enableDistributionTagName).text = str('true')
    ET.SubElement(fastBuildTag, cacheModeTagName).text = str('ReadWrite')
    print("Set enableCacheTag to true")
    print("Set enableDistributionTag to true")   
    print("Set cacheMode to ReadWrite")

# 세팅한 사항들을 다시 파일에 쓰기
xmlTree.write(buildConfigurationPath)
print(buildConfigurationPath + " Setting Succeed")


