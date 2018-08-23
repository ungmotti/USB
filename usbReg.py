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

            if vidPat.search(line):
                vidm = vidPat.search(line)
                vidDict[vidm.group(1)] = vidm.group(2)
                pidDict = dict()

            elif pidPat.search(line):
                pidm = pidPat.search(line)
                pidDict[pidm.group(2)] = pidm.group(3)

            if i < len(lines):
                if vidPat.search(lines[i+1]):
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

'''
with open('./usbids.txt', 'rt', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line:
            break
        vidm = vidPat.search(line)
        if vidm:
            pidDict = dict()
            vidDict[vidm.group(1)] = vidm.group(2)
            count = 0
            while True:
                line = f.readline()
                pidm = pidPat.search(line)

                if not pidm:
                    break
                else:
                    count += 1
                    pidDict[pidm.group(2)] = pidm.group(3)
            totalDict[(vidm.group(1), vidm.group(2))] = pidDict
'''
