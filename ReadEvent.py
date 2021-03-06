import chardet

def ReadData(path):
    text = open(path, 'rb').read()
    TxtDetail = chardet.detect(text)
    if TxtDetail['encoding'] == 'GB2312':
        LoadF = open(path, 'r' , encoding = 'gb18030')
        TxtDetail['encoding'] = 'gb18030'
    else :
        LoadF = open(path, 'r' , encoding = chardet.detect(text)['encoding'])
    data =  LoadF.readlines()
    TxtDetail['data'] = data
    return TxtDetail