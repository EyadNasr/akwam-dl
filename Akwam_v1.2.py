from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from sys import stdout, stdin
from re import match, findall, DOTALL
from requests import get
from numpy import unique
from msvcrt import getch
from os import mkdir,chdir, getcwd, system
from os.path import isfile, isdir
from time import sleep
from bidi.algorithm import get_display
from Arabic_Reshaper import reshape


import os
import ctypes
import msvcrt
import subprocess

from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)




def connproblem():
    print("\n\nTHERE IS A PROBLEM WITH YOUR CONNECTION, CHECK YOUR INTERNET CONNENCTION AND TRY AGAIN!")
    print('\nTry again [y] or quit [n]? Press [y] to retry or [n] to quit')
    ask = getch()
    if ask == b'y': 
        print('')
        pass
    else: raise SystemExit


def retrynow(num):
    ssss = 'CONNECTION ERROR... Retrying... (' + str(num) + ')'
    if num == 1: print('\n')
    stdout.flush()
    stdout.write('\r'+ ssss)
    sleep(10)
    if num%10 == 0: connproblem()
    return num


def consolefont():
    import ctypes
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11
    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = 'Sin Sun-ExtB'
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font))


def keyinter():
    print("\n\nPROGRAM INTERRUPT BY USER\n")
    getch()
    raise SystemExit


def getlinks(url, stwith):
    iternum = 1
    while True:
        try:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(url,headers=hdr)
            page = urlopen(req).read()
            if iternum > 1: print('\n')
            break
        except KeyboardInterrupt: keyinter()
        except Exception: iternum = retrynow(iternum)
        iternum = iternum + 1
    soup = BeautifulSoup(page, "html.parser")
# Retrieve all of the anchor tags
    tags = soup('a')
    #lst = [tag.get('href', '') for tag in tags if match(stwith, tag.get('href', ''))]
    lst = []
    epidic = {}
    for tag in tags:
        if match(stwith, tag.get('href', '')) and tag.get('class') == ['text-white']:
            lst = lst + [tag.get('href', '')]
            #print(tag.contents)
            epidic[int(findall('.+? ([0-9]+)', tag.contents[0])[0])] = tag.get('href', '')
    #print(epidic)
    #newlst = [item for item in lst if lst.count(item) == 2]
    #newlst = newlst[::-2]
    return(epidic)


def getlistOfSeasons(parent, findit, fff, episodesFlag):
    if findit == '"(https://.*?akwam.+?/(movie|series)/.+?)"':
        findit1 = '"(https://.*?akwam.+?/series/.+?)"'
        findit2 = '"(https://.*?akwam.+?/movie/.+?)"'
        finditboth = [findit1, findit2]
        parentboth = [parent+'series', parent+'movie']
    else:
        finditboth = [findit]
        parentboth = [parent]
    bothdict = {}
    extracted_websub = ''
    for both1, both2 in zip(parentboth, finditboth):
        parent = both1
        iternum = 1
        while True:
            try:
                r = get(parent)
                x = r.content.decode("utf-8")
                findit = both2
                r = get(parent)
                x = r.content.decode("utf-8")
                if iternum > 1: print('\n')
                break
            except KeyboardInterrupt: keyinter()
            except Exception: iternum = retrynow(iternum)
            iternum = iternum + 1
        if fff:
            morePages = findall('page=([1-9]+)', x)
            Pages = unique(morePages).tolist()
            Pages = [1] + [int(i) for i in Pages]
            Pages = list(range(1, max(Pages)+1))
            all_X = ''
            for i in Pages:
                if i == 1: all_X = all_X + ' ' + x
                else:
                    parent_i = parent + '&page=' + str(i)
                    iternum = 1
                    while True:
                        try:
                            r = get(parent_i)
                            x = r.content.decode("utf-8")
                            if iternum > 1: print('\n')
                            break
                        except KeyboardInterrupt: keyinter()
                        except Exception: iternum = retrynow(iternum)
                        iternum = iternum + 1
                    all_X = all_X + ' ' + x
            aka = r'<h3 class="entry-title font-size-14 m-0"><a href="(https://.*?akwam.+?/(movie|series)/[^" \t\n\r\f\v]+)".+\n.+\n.+"badge badge-pill badge-secondary ml-1">([0-9][0-9][0-9][0-9])</span>'
            uniq = findall(aka, all_X)
            try: 
                if len(uniq) > 0: 
                    extracted_websub = findall('(https://.+?)/[^ \t\n\r\f\v]+', uniq[0][0])[0]
                    #uniq.remove(parent)
            except: 
                pass
            unsrt = [int(i[0].split('/')[-2]) for i in uniq]
            dicto = {}
            
            for i in range(0, len(uniq)): dicto[unsrt[i]] = uniq[i][0] + ' ' + uniq[i][2]
        else:
            uniq = findall(findit, x)
            extracted_websub = findall('(https://.*?akwam.+?)/[^ \t\n\r\f\v]+', uniq[0])[0]
            uniq = unique(uniq).tolist()
            unsrt = [int(i.split('/')[-2]) for i in uniq]
            dicto = {}
            for i in range(0, len(uniq)): dicto[unsrt[i]] = uniq[i]
        bothdict.update(dicto)
    dicto = bothdict
    lsts = []
    if len(dicto) == 1: sstr = ' Link found'
    else: sstr = ' Links found'
    print('\n' + str(len(dicto)) + sstr)
    count = 1
    for j in sorted(dicto):
        reshaped_text = reshape(dicto[j])
        bidi_text = get_display(reshaped_text)
        s = str(dicto[j].encode())
        links = []
        TYPE = '" [' + bidi_text.split('/')[-3] + ']'
        print('\n', count, 'Do you want to download "' + bidi_text.split('/')[-1].replace('-s-', "'s ").replace('-', ' ') + TYPE + ' ?')
        flag = True
        ending = getch()
        if ending == b'y':
            if bidi_text.find('series') != -1:
                if fff: linksdic = getlinks(findall("'(.+)'", s)[0][:-5], extracted_websub + '/episode/')
                else: linksdic = getlinks(findall("'(.+)'", s)[0], extracted_websub + '/episode/')
                episodessorted = sorted(linksdic)
                links = [linksdic[i] for i in episodessorted]
                if episodesFlag:
                    print('\n' + '"' + bidi_text.split('/')[-1].replace('-', ' ') + '" has', max(episodessorted), 'episodes.')
                    episodeslst = input('Enter the desired episodes: ')
                    cond = 0
                    numset = '0123456789:,'
                    while cond == 0:
                        episodeslst = episodeslst.replace(' ', '').replace('\t', '').split(',')
                        for e in episodeslst:
                            #if all(x in numset for x in episodeslst): pass
                            if len(findall('^[1-9]+[0]*$', e)) > 0 and int(e) <= max(episodessorted): pass
                            elif len(findall('^[1-9]+[0]*:[1-9]+[0]*$', e)) > 0 and int(e.split(':')[0]) < int(e.split(':')[1]) and int(e.split(':')[1]) <=max(episodessorted): pass
                            else:
                                episodeslst = input('Invalid input, Enter the desired episodes: ')
                                cond = cond + 1
                        if cond > 0: cond = 0
                        else: break
                    
                    candlist = []
                    for i in episodeslst:
                        if ':' not in i: candlist.append(int(i))
                        else: candlist = candlist + list(range(int(i.split(':')[0]), int(i.split(':')[1])+1))
                    pro = sorted(unique(candlist).tolist())
                    links = []
                    missing = []
                    for i in pro:
                        if i not in linksdic: missing = missing + [i]
                        else: links = links + [linksdic[i]]
                    if len(missing) > 0:
                        print('\nThe following episodes are missing from the website: ', end='')
                        for q in missing: print(q, '', end='')
                        print('')
            elif bidi_text.find('movie') != -1:
                if fff: links = [bidi_text[:-5]]
                else: links = [bidi_text]
        lsts = lsts + links
        if ending == b'q':
            print('\n[q] is pressed')
            break
        count = count + 1
    links = lsts
    return links


def main():
    try:
        websub = 'https://.*?akwam.+?'
        flag = False
        episodesFlag = False
        while True:
            allLinks1 = []
            sizes = []
            quals = []
            quals_dict = {'5': '1080', '4': '720', '3': '480', '2': '360', '1': '240'}
            quals_dict_rev = {'1080': '5', '720': '4', '480': '3', '360': '2', '240': '1'}
            parent = input('Paste Movie or Series link, (or write what you want to search for): ')
            system('cls')
            texxxt = 'Paste Movie or Series link, (or write what you want to search for): ' + parent
            reshaped_text = reshape(texxxt)
            bidi_text = get_display(reshaped_text)
            print(bidi_text)
            name = parent.split('/')[-1].split('%')[0].replace('-', ' ').strip()
            if parent.find('https:') == -1:
                parent = 'https://akwam.cc/search?q=' + parent
            if parent.find('series') != -1:
                fff = False
                print("\nPress [q] to end questions, [y] to download or [n] to skip:")
                websub1 = 'https://' + parent[8:].split('/')[0]
                links = getlistOfSeasons(parent, '"(' + websub1 + '/series/.+?)"', fff, episodesFlag)
            elif parent.find('search') != -1:
                fff = True
                print('\nIs it a Movie or a Series or both?\n(Press [m] for Movie, [s] for Series , [e] for specific Episodes of a series or any other key for both Movies and Series)\n')
                ending = getch()
                print(ending.decode('utf-8'), 'is pressed', end = '')
                if ending == b'm': 
                    Type = '&section=movie'
                    Typo = '&section=movie'
                elif ending == b's': 
                    Type = '&section=series'
                    Typo = '&section=series'
                elif ending == b'e':
                    Type = '&section=series'
                    Typo = '&section=series'
                    episodesFlag = True
                else: 
                    Type = '&section=(movie|series)'
                    Typo = '&section='
                if episodesFlag: print(', to specify episodes: type the range of episodes or episode numbers separated by commas\nfor example: 1,4,7,9:12,15')
                else: print('')
                print("\nPress [q] to end questions, [y] to download or [n] to skip:")
                links = getlistOfSeasons(parent+Typo, '"(' + websub + '/' + Type[9:] + '/.+?)"', fff, episodesFlag)
                name = parent.split('/')[-1].split('%')[0].replace('-', ' ').split('&')[0].split('?q=')[1].replace('+', ' ')
                if len(links) == 0 and not flag:
                    print('\nDid not find what you were searching for!')
            elif parent.find('movie') != -1:
                links = [parent]
            else: links = []
            if len(links) == 0:
                print('\nZero links extracted!')
            else:
                print('')
                for i in links:
                    sss = "Gathering download pages... ( " + str(links.index(i)+1) + " out of " + str(len(links)) + " )"
                    stdout.flush()
                    stdout.write('\r'+ sss)
                    iternum = 1
                    while True:
                        try:
                            r = get(i)
                            z = r.content.decode("utf-8")
                            if iternum > 1: print('\n')
                            break
                        except KeyboardInterrupt: keyinter()
                        except Exception: iternum = retrynow(iternum)
                        iternum = iternum + 1
                    #downlink1 = findall('"(http://go.akwam' + websuper + '/link/.+?)".+?([0-9.,]+ [MG]B)', z)
                    #downlink1 = findall('data-quality="([1-5])">.+?"(http://re.two.re/link/.+?)".+?([0-9.,]+ [MG]B)', z, DOTALL)
                    downlink1 = findall('data-quality="([1-5])">.+?<a href="(http://[^" \t\n\r\f\v]+/link/[^" \t\n\r\f\v]+?)".+?([0-9.,]+ [MG]B)</span>', z, DOTALL)
                    #downlink1 = findall('"(' + websub + '/download/.+?)".+?([0-9.,]+ [MG]B)', z)
                    tempo = ''
                    for (u, m, k) in downlink1:
                        if tempo == k: continue
                        iternum = 1
                        while True:
                            try:
                                rr = get(m)
                                zz = rr.content.decode("utf-8")
                                if iternum > 1: print('\n')
                                break
                            except KeyboardInterrupt: keyinter()
                            except Exception: iternum = retrynow(iternum)
                            iternum = iternum + 1
                        downlink2 = findall('"(https://[^" \t\n\r\f\v]*?akwam[^" \t\n\r\f\v]+?/download/.+?)"', zz)
                        if len(downlink2) > 1: downlink2 = [downlink2[0]]
                        sizes.append(k)
                        quals.append(u)
                        for ii in downlink2: allLinks1.append(ii)
                        tempo = k
                print('\n')
                allLinks2 = []
                avail_quals = unique(quals).tolist()
                avail_quals.sort()
                print('Available Qualities are: ', end='')
                for i in avail_quals: print(quals_dict[i], end=' ')
                quals_real = [quals_dict[i] for i in sorted(avail_quals)][::-1]
                if len(avail_quals) != 1:
                    print('\nChoose the desired quality (or press Enter for all qualities): ')
                    nummm = 1
                    numlist = []
                    quals_real_dic = {}
                    for i in quals_real:
                        print('Press [' + str(nummm) + '] for', i + 'p')
                        numlist = numlist + [str(nummm)]
                        quals_real_dic[str(nummm)] = i
                        nummm = nummm + 1
                        if i == quals_real[-1]: print('')
                    Qual = getch()
                    while True:
                        try: Qual = Qual.decode()
                        except:
                            print('Invalid input! Choose the desired quality (or press Enter for all qualities): ')
                            Qual = getch()
                            continue
                        if Qual in numlist or Qual == '\r': break
                        elif Qual.encode() == b'\x03': keyinter()
                        else: 
                            print('Invalid input! Choose the desired quality (or press Enter for all qualities): ')
                            Qual = getch()
                    if Qual in quals_dict: Qual = quals_real_dic[Qual]
                else:
                    Qual = quals_dict[avail_quals[0]]
                if Qual == '\r': print('All available qualities are added!')
                else: print('\n' + Qual + 'p is chosen')
                print('')
                chosensizes = []
                savedsizes = sizes
                for URL,size, qual in zip(allLinks1, sizes, quals):
                    if Qual == '\r': pass
                    elif qual != quals_dict_rev[Qual]: continue
                    chosensizes = chosensizes + [size]
                    iternum = 1
                    while True:
                        try:
                            r = get(URL)
                            s = r.content.decode("utf-8")
                            if iternum > 1: print('\n')
                            break
                        except KeyboardInterrupt: keyinter()
                        except Exception: iternum = retrynow(iternum)
                        iternum = iternum + 1
                    final = findall('<a href="(https://s.+?[.]akwam.link/download.+?)"', s)[0]
                    allLinks2.append(final)
                    kkk = "Saving download links... ( " + str(round(100* (allLinks1.index(URL)+1)/len(allLinks1))) + ' %' + " )"
                    stdout.flush()
                    stdout.write('\r'+ kkk)
                kkk = "Saving download links... ( 100 % )"
                stdout.flush()
                stdout.write('\r'+ kkk)
                print('\n')
                sizesorted1 = [str(i) + '   ' + ii + '\n' for i, ii in zip(allLinks2, chosensizes) if i.lower().find('1080p') != -1]

                sizesorted2 = ['\n\n'] + [str(k) + '   ' + kk + '\n' for k, kk in zip(allLinks2, chosensizes) if k.lower().find('720p') != -1]
                if len(sizesorted1) == 0: sizesorted2.remove(sizesorted2[0])

                sizesorted3 = ['\n\n'] + [str(j) + '   ' + jj + '\n' for j, jj in zip(allLinks2, chosensizes) if j.lower().find('480p') != -1]
                if len(sizesorted2) == 1: sizesorted3.remove(sizesorted3[0])

                sizesorted4 = ['\n\n'] + [str(m) + '   ' + mm + '\n' for m, mm in zip(allLinks2, chosensizes) if m.lower().find('360p') != -1]
                if len(sizesorted3) == 1: sizesorted4.remove(sizesorted4[0])

                sizesorted5 = ['\n\n'] + [str(m) + '   ' + mm + '\n' for m, mm in zip(allLinks2, chosensizes) if m.lower().find('360p') == -1 and m.lower().find('480p') == -1 and m.lower().find('720p') == -1 and m.lower().find('1080p') == -1]
                if len(sizesorted4) == 1: sizesorted5.remove(sizesorted5[0])

                sizesorted = sizesorted1 + sizesorted2 + sizesorted3 + sizesorted4 + sizesorted5
                directory = name + '.txt'
            if len(links) != 0:
                pathx = getcwd() + '\\Akwam-links'
                if not isdir(pathx):
                    mkdir(pathx)
                directory = pathx + '\\' + directory
                c = 1
                reshaped_text = reshape(directory)
                bidi_text = get_display(reshaped_text)
                print("Download links saved to -->> ", bidi_text)
                text = ' '.join(chosensizes)
                try: gigas = sum([float(dig.replace(',', '')) for dig in findall("([0-9.,]+) GB", text)])
                except ValueError: gigas = 0.0
                try: megas = sum([float(dig.replace(',', '')) for dig in findall("([0-9.,]+) MB", text)])
                except ValueError: megas = 0.0
                total = gigas + megas / 1024
                print("\nTotal size is", round(total, 3), 'GB')
                if isfile(directory):
                    txts = '\nFile ' + directory.split('\\')[-1] +' already Exists, do you want to overwrite [y] or rename [n]? Press [y] to overwrite or [n] to rename: '
                    reshaped_text = reshape(txts)
                    bidi_text = get_display(reshaped_text)
                    print(bidi_text)
                    ends = getch()
                    if ends != b'y':
                        print("Renamed")
                        while isfile(directory):
                            rep = findall('[0-9]*[.]txt', directory)[0]
                            directory = directory.replace(rep, str(c) + '.txt')
                            c = c + 1
                    else:
                        print("Overwritten")
                with open(directory, 'wb') as fhand:
                    tots = '""" Total Size is ' + str(round(total, 3)) + ' GB """'
                    tExt = tots.center(len(max(sizesorted, key=len))) + '\n\n'
                    fhand.write(tExt.encode("utf-8"))
                    for i in range(0, len(sizesorted)):
                        row = sizesorted[i]
                        fhand.write(row.encode("utf8"))
                    texT = '\n\n\n' + '"""Download Links with no sizes (for jdownloader batch download)"""'.center(len(max(sizesorted, key=len).split('   ')[0])) + '\n\n\n'
                    fhand.write(texT.encode("utf8"))
                    copyall = ''
                    for i in range(0, len(sizesorted)):
                        copyall = copyall + row
                        row = sizesorted[i].split('   ')[0]+'\n'
                        fhand.write(row.encode("utf8"))
                    from pyperclip import copy
                    copy(copyall)
                    print('\nAll Download links copied to clipboard!')
                printtext = '\nOpen the text file that contains the download links "' + directory.split('\\')[-1] + '"? Press [y] for "yes" or [n] for "no" '
                reshaped_text = reshape(printtext)
                bidi_text = get_display(reshaped_text)
                print(bidi_text)
                ending = getch()
                if ending == b'y':
                    print("Opening saved links... ")
                    from os import startfile
                    startfile(directory)
                else: print("No...")
            print('\nRun script again? [y/n]: ')
            end = getch()
            if end != b'y': 
                print("Exiting...")
                raise SystemExit
            print('\n')
    except KeyboardInterrupt: 
        print("\n\nPROGRAM INTERRUPT BY USER\n")
        getch()
        raise SystemExit


consolefont()
#maximize_console()
main()
