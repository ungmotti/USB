import winreg, re

varReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
varKey = winreg.OpenKey(varReg, r"SYSTEM\\CurrentControlSet\\Enum\\USB\\",0, winreg.KEY_ALL_ACCESS)


vidLst=list()
pidLst=list()
vidPat = re.compile('(^[0-9a-zA-Z]{4})  (.*)$')
pidPat = re.compile('(^\t)([0-9a-zA-Z]{4})  (.*)$')
totalDict=dict()
vidDict=dict()
pidDict=dict()
text = "0001  Fry's Electronics"
text2= "	7778  Counterfeit flash drive [Kingston]"
vidm = vidPat.search(text)
pidm = pidPat.search(text2)


try:
    i = 1
    while True:
        name = winreg.EnumKey(varKey, i)
        try:
            vidLst.append(name.split('&')[0].split('_')[1])
            pidLst.append(name.split('&')[1].split('_')[1])
        except:
            pass
        i += 1
except WindowsError:
    pass


with open('./usbids.txt', 'rt', encoding='utf-8') as f:
    lines = f.readlines()
    try:
        for i, line in enumerate(lines):

            if vidPat.search(line):                     #vid 찾기
                vidm = vidPat.search(line)
                vidDict[vidm.group(1)] = vidm.group(2)  #찾아지면 vid에 해당하는 vendor name 딕셔너리에 추가
                pidDict = dict()                        #vid 하위의 pid 딕셔너리 초기화

            elif pidPat.search(line):                   #pid 찾기
                pidm = pidPat.search(line)
                pidDict[pidm.group(2)] = pidm.group(3)  #찾아지면 pid에 해당하는 device name 딕셔너리에 추가

            if i < len(lines):
                if vidPat.search(lines[i+1]):           #pid검색이 끝나면 이때까지 찾은 vid에 해당하는 pidDict 이중딕셔너리로 추가
                    totalDict[(vidm.group(1), vidm.group(2))] = pidDict
    except IndexError:
        print("End Of File!")


for vid, pid in zip(vidLst, pidLst):
    vid = vid.lower()
    pid = pid.lower()
    try:
        print("VID : {}, Vender_name : {}\nPID : {}, Device_name : {}".format(vid, vidDict[vid], pid, totalDict[(vid,vidDict[vid])][pid]))
        print("=====================================================")
    except KeyError:
        print("Cannot Find! VID : {} PID : {}".format(vid, pid))
        print("=====================================================")

