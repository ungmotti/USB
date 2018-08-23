import os, sys, winreg, re


varReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
varKey = winreg.OpenKey(varReg, r"SYSTEM\\CurrentControlSet\\Enum\\USB\\",0, winreg.KEY_ALL_ACCESS)

vidLst=list()
pidLst=list()

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


vidPat = re.compile('(^[0-9a-zA-Z]{4})  (.*)$')
pidPat = re.compile('(^\t)([0-9a-zA-Z]{4})  (.*)$')
totalDict=dict()
vidDict=dict()
pidDict=dict()

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

print(vidLst)
print(pidLst)
print(vidDict)

for vid, pid in zip(vidLst, pidLst):
    vid = vid.lower()
    pid = pid.lower()
    try:
        #print("Vender : {}, Vender_name  : {}\nDevice : {}, Device _name : {}".format(vid, vidDict[vid], pid, totalDict[(vid,vidDict[vid])][pid]))
        print("Vender : {}, Vender_name  : {}".format(vid, vidDict[vid]))
    except KeyError:
        print("Cannot Find! VID : {} PID : {}".format(vid, pid))
