#!/usr/bin/env python
# モジュールのインポート
import os, tkinter as tk, tkinter.filedialog, tkinter.messagebox,sys,re

REMOVE_STR_1 = '<b>どどんとふ</b>'
REMOVE_STR_2 = '<b>DodontoF-MUSERU</b>'
REMOVE_STR_3 = '：['

REPLACE_STR_1 = 'DX3rd セッションログ　『』'

# ファイル読み込み & 編集
def fileReadLines(filename,deletelevel):
    f = open(filename,'r',encoding="utf-8_sig")
    readLines1 = [s for s in f.readlines() if REMOVE_STR_1 not in s]
    readLines2 = [s for s in readLines1 if REMOVE_STR_2 not in s]
    readLinesTmp = [s for s in readLines2 if REMOVE_STR_3 not in s]
    # file1のみの場合はそのまま
    # 複数ファイルの場合の先頭
    if deletelevel == 2:
        del readLinesTmp[-4:]
    # 複数ファイルの場合の中間
    elif deletelevel == 3:
        del readLinesTmp[:23]
        del readLinesTmp[-4:]
    # 複数ファイルの場合の末尾
    elif deletelevel == 4:
        del readLinesTmp[:23]
    f.close()
    return readLinesTmp

# ファイル出力
def fileWrite(strOutputFileName,readedIF):
    if strOutputFileName == '':
        strOutputFileName = 'newDX3log.html'
    else:
        strOutputFileName = strOutputFileName + '.html'
    f = open(strOutputFileName,'w',encoding="utf-8_sig")
    f.writelines(readedIF)
    f.close()
    return
# ファイル選択ダイアログの表示
def fileSelect():
    root = tk.Tk()
    root.withdraw()
    fTyp = [("", "*.html")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filename = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    return filename

# タイトル置換
def logTitleReplace(readLines):
    strTitleName = titleName.get()
    readLinesTmp1 = re.sub('<title>.*</title>','<title>' + strTitleName + '</title>',",,,".join(readLines))
    print("1")
    print(readLinesTmp1)
    readLinesTmp2 = re.sub('<h1>.*</h1>', '<h1>' + strTitleName + '</h1>',readLinesTmp1)
    print("2")
    print(readLinesTmp2)
    return readLinesTmp2.split(",,,")
# 統合_main
def integration():
    try:
        strOutputFileName = outputFileName.get()
        strInputFileName1 = inputFileName1.get()
        strInputFileName2 = inputFileName2.get()
        strInputFileName3 = inputFileName3.get()
        # file1が未選択の場合は注意メッセージを表示
        if strInputFileName1 == '':
            tkinter.messagebox.showinfo('system', 'File1が未選択')
            return

        # file2以降が存在する場合
        if strInputFileName2 != '':
            readedIF = fileReadLines(strInputFileName1, 2)
            # file1 & fie2 & file3
            if strInputFileName3 != '':
                #print(strInputFileName3)
                readedIFtmp = fileReadLines(strInputFileName2, 3)
                readedIF.extend(readedIFtmp)
                readedIFtmp = fileReadLines(strInputFileName3, 4)
                readedIF.extend(readedIFtmp)
                #print('file1 & file2 & file3')
            # file1 & file 2
            else:
                readedIFtmp = fileReadLines(strInputFileName2, 4)
                readedIF.extend(readedIFtmp)
                #print('file1 & file2')
        # file1のみの場合
        else:
            readedIF = fileReadLines(strInputFileName1, 1)
            #print('file1')
        readedIFEnd = logTitleReplace(readedIF)
        fileWrite(strOutputFileName, readedIFEnd)

        #print("統合END")
        tkinter.messagebox.showinfo('system', 'END')
        return

    except:
        tkinter.messagebox.showinfo('system', '何か起きたからやり直してくれ')
        return

# file1選択_click
def fileSelect1():
    filename = fileSelect()
    #label1.configure(text='file1：' + str(filename))
    inputFileName1.delete(0,tk.END)
    inputFileName1.insert(0,str(filename))
    return

# file2選択_click
def fileSelect2():
    filename = fileSelect()
    #label2.configure(text='file2：' + str(filename))
    inputFileName2.delete(0, tk.END)
    inputFileName2.insert(0, str(filename))
    return

# file3選択_click
def fileSelect3():
    filename = fileSelect()
    inputFileName3.delete(0, tk.END)
    inputFileName3.insert(0, str(filename))
    return

# main
try:
    # rootウィンドウを作成
    root = tk.Tk()
    # rootウィンドウのタイトルを変える
    root.title("DX3rdHTMLLogOrder")
    # ウィンドウサイズ
    root.geometry("800x200")

    # フレームの作成（フレームをrootに配置,フレーム淵を2pt,フレームの形状をridge）
    frame1 = tk.Frame(root, bd=2, relief="ridge")
    # フレームを画面に配置し、横方向に余白を拡張する
    frame1.pack(fill="x")

    button1 = tk.Button(frame1, text='file1選択', command=fileSelect1)
    button1.pack(anchor="nw", side="left")
    label1 = tk.Label(frame1, text='file1：')
    label1.pack(anchor="nw", side="left")
    inputFileName1 = tk.Entry(frame1, font=("", 12), justify="left", width=86)
    inputFileName1.pack(anchor="nw", side="left")

    frame2 = tk.Frame(root, bd=2, relief="ridge")
    frame2.pack(fill="x")
    button2 = tk.Button(frame2, text='file2選択', command=fileSelect2)
    button2.pack(anchor="nw", side="left")
    label2 = tk.Label(frame2, text='file2：')
    label2.pack(anchor="nw", side="left")
    inputFileName2 = tk.Entry(frame2, font=("", 12), justify="left", width=86)
    inputFileName2.pack(anchor="nw", side="left")

    frame3 = tk.Frame(root, bd=3, relief="ridge")
    frame3.pack(fill="x")
    button3 = tk.Button(frame3, text='file3選択', command=fileSelect3)
    button3.pack(anchor="nw", side="left")
    label3 = tk.Label(frame3, text='file3：')
    label3.pack(anchor="nw", side="left")
    inputFileName3 = tk.Entry(frame3, font=("", 12), justify="left", width=86)
    inputFileName3.pack(anchor="nw", side="left")

    frame4 = tk.Frame(root, bd=3, relief="ridge")
    frame4.pack(fill="x")
    frame4_1 = tk.Frame(frame4, bd=1, relief="ridge")
    frame4_1.pack(fill="x")
    titleLabel = tk.Label(frame4_1, text='タイトル名：')
    titleLabel.pack(anchor="w", side="left")
    titleName = tk.Entry(frame4_1, font=("", 12), justify="left", width=50)
    titleName.pack(anchor="w", side="left")
    titleName.delete(0, tk.END)
    titleName.insert(0, REPLACE_STR_1)

    frame4_2 = tk.Frame(frame4, bd=1, relief="ridge")
    frame4_2.pack(fill="x")
    outputFileLabel = tk.Label(frame4_2, text='出力ファイル名：')
    outputFileLabel.pack(anchor="w", side="left")
    outputFileName = tk.Entry(frame4_2, font=("", 12), justify="left", width=50)
    outputFileName.pack(anchor="w", side="left")

    integrationButton = tk.Button(root, text='統合', command=integration)
    integrationButton.pack(anchor="sw", side="left")

    exitButton = tk.Button(root, text='Exit', command=sys.exit)
    exitButton.pack(anchor="se", side="right")

    root.mainloop()
except:
    #tkinter.messagebox.showinfo('system', '何か起きたから閉じます')
    sys.exit