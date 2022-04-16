import chardet

def ReadData(path):
    text = open(path, 'rb').read()
    if chardet.detect(text)["encoding"] == 'GB2312':
        LoadF = open(path, "r" , encoding = 'gb18030')
    else :
        LoadF = open(path, "r" , encoding = chardet.detect(text)["encoding"])
    data =  LoadF.readlines()
    return data