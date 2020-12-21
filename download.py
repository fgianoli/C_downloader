import os
import urllib.request
import sys


# config

list_file = 'list2.txt'
dest_fold = 'downloads'


def search_Data(anno=None,nome_tile=None,prodotto=None):


    #read list of files
    f = open(list_file,'r')
    data = f.readlines()
    files = [ f.rstrip() for f in data ]
    f.close()

    base_URL = 'https://s3-eu-west-1.amazonaws.com/vito.landcover.global/v3.0.1/'



    urls = []

    for file in files:
        filename = file.split('/')[2]
        year = file.split('/')[0]
        tile = file.split('/')[1]
        if prodotto is not None and prodotto in file:
            if anno is not None and anno in file:
                if nome_tile is not None and nome_tile in file:
                    urls.append(base_URL+ year+'/'+tile+'/'+filename)
                if nome_tile is None:
                    urls.append(base_URL + year + '/' + tile + '/' + filename)
            if anno is None:
                if  nome_tile is not None and nome_tile in file:
                    urls.append(base_URL+ year+'/'+tile+'/'+filename)
                if nome_tile is None:
                    urls.append(base_URL + year + '/' + tile + '/' + filename)
        if prodotto is None:
            if anno is not None and anno in file:
                if nome_tile is not None and nome_tile in file:
                    urls.append(base_URL + year + '/' + tile + '/' + filename)
                if nome_tile is None:
                    urls.append(base_URL + year + '/' + tile + '/' + filename)
            if anno is None:
                if nome_tile is not None and nome_tile in file:
                    urls.append(base_URL + year + '/' + tile + '/' + filename)
                if nome_tile is None:
                    urls.append(base_URL + year + '/' + tile + '/' + filename)

    #for u in urls:
        #print(u)

    return urls

anno= None
nome_tile= 'W180S40'
prodotto =None

download = search_Data(prodotto=prodotto, anno=anno)
print(download)

# create dest folder
abs_dfold = os.getcwd() + '/' + dest_fold
if (not os.path.exists(abs_dfold)):
    os.mkdir(abs_dfold)
else:
    # do whatever id folder exists
    print('Folder already exists.')
    pass



for d in download:
    output = "C:/Users/giano/Desktop/LC/" + os.path.basename(d)
    urllib.request.urlretrieve(d, output)

sys.exit()

