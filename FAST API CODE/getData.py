from sys import excepthook
import wget


Filelist = [
     'Farmgate 21.01.2023.pdf',
     'Farmgate 14.01.2023.pdf',
     'Farmgate 07.01.2023.pdf',
     'Farmgate 31.12.2022.pdf',
     'Farmgate 24.12.2022.pdf',
     'Farmgate 17.12.2022.pdf',
     'Farmgate 10.12.2022.pdf',
     'Farmgate 03.12.2022.pdf',
     'Farmgate 26.11.2022.pdf',
     'Farmgate 19.11.2022.pdf',
     'Farmgate 12.11.2022.pdf',
     'Farmgate 05.11.2022.pdf',
     'Farmgate 29.10.2022.pdf',
     'Farmgate 22.10.2022.pdf',
     'Farmgate 15.10.2022.pdf',
     'Farmgate 08.10.2022.pdf',
     'Farmgate 01.10.2022.pdf',
     'Farmgate 24.09.2022.pdf',
     'Farmgate 17.09.2022.pdf',
     'Farmgate 10.09.2022.pdf',
     'Farmgate 03.09.2022.pdf',
     'Farmgate 27.08.2022.pdf',
     'Farmgate 20.08.2022.pdf',
     'Farmgate 13.08.2022.pdf',
     'Farmgate 06.08.2022.pdf',
     'Farmgate 30.07.2022.pdf',
     'Farmgate 23.07.2022.pdf',
     'Farmgate 16.07.2022.pdf',
     'Farmgate 09.07.2022.pdf',
     'Farmgate 02.07.2022.pdf',
     'Farmgate 25.06.2022.pdf',
     'Farmgate 18.06.2022.pdf',
     'Farmgate 11.06.2022.pdf',
     'Farmgate 04.06.2022.pdf',
     'Farmgate 28.05.2022.pdf',
     'Farmgate 21.05.2022.pdf',
     'Farmgate 14.05.2022.pdf',
     'Farmgate 07.05.2022.pdf',
     'Farmgate 30.04.2022.pdf',
     'Farmgate 23.04.2022.pdf',
     'Farmgate 16.04.2022.pdf',
     'Farmgate 09.04.2022.pdf',
     'Farmgate 02.04.2022.pdf',
     'Farmgate 26.03.2022.pdf',
     'Farmgate 19.03.2022.pdf',
     'Farmgate 12.03.2022.pdf',
     'Farmgate 05.03.2022.pdf',
     'Farmgate 26.02.2022.pdf',
     'Farmgate 19.02.2022.pdf',
     'Farmgate 12.02.2022.pdf',
     'Farmgate 05.02.2022.pdf'    
]

for file in Filelist:
    url = 'http://ja-mis.com/Reports/' + file
    print('Downloading ' + file + '...', end='')
    try:
        wget.download(url, './data')
        # print(url)
    except:
        print('FAILED!')
    else:
        print('done!')
