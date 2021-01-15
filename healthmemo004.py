#! python3
#coding: utf-8

# 体重等を測ったら、簡単にメモしてcsv保存
# 体重・日時・血圧・脈・体脂肪率・体温・歩数を記録する。

'''

開発履歴
20201029 Ver001 健康支援研修から体重等を記録し易くするメモアプリを作る事にした
20201031 Ver002 データ構造などをｐｃで作成し、ipadでui作成。ベータ版
20201114 Ver003 体重のグラフ表示を追加。グラフ化すると入力が面白くなる！！
20201117 Ver004 起動時loadとsaveのバックアップ作成。上書きでデータ消えた(T_T)
20201125 Ver004 グラフに歩数・体温・血圧を追加。バージョン変更無。


★日付と朝と夜＝午前午後から自動判別。csvに記録→グーグルスプレッドシートに追記＋メールでバックアップを自動送信。
★→自動追記とメール送信はしない。csvを共有してコピーするとした。
★小数点は入力しない。3桁の数で入力して、自動変換。←変換しない。小数点入力無しにする。
★メモの字数を自動カウント＋警告を出すようにする。(200文字制限？)　、
★縦横の両方で使えるようにする。キーボードに注意。できれば縦メイン。→iPad横のみ用とした。iphoneでは小さすぎた。
★保存ボタン(メールの自動送信も含む)は、必要かも。
★csvも日毎に1ファイル作って、pcでcsvを合成するファイル統合ソフト作った方がいいかな？
　→そうすると、iPad上でのcsvは1次元配列でもできるかもしれない。→csv一つに毎日のデータ追記にした。2次元配列。

'''

import ui
import datetime
import sys

import io #gazou hennkou
import csv
import os #file sousa
# import pandas 不可！pythonista3は、pandas使用不能。numpyとバージョン合わないらしい。csvで読むことにした。
import matplotlib.pyplot as plt
from PIL import Image

#global変数　一覧

nitiji_now = datetime.datetime.now() # 現在日時の取得
nitiji_on = nitiji_now.strftime('%Y/%m/%d_%H:%M:%S')
# datetime関数から日時を取り出して、表示する文字の変数に代入
nitiji_kyou = str(nitiji_now.strftime('%Y/%m/%d'))
#kyoufile = str('healthmemodata') + nitiji_now.strftime('%Y%m%d') + str('.csv')
filename = str('healthmemodata.csv')
graphname = str('healthmemograph.png')

healthlist = [['年月日','体重朝','体重夜','血圧上朝','血圧下朝','脈拍朝','血圧上夜','血圧下夜','脈拍夜','体脂肪','歩数','メモ','体温朝','体温夜']]
nitiji_asaban = 'AM'
taijyuuAM = '001'
taijyuuPM = '002'
ketuatuueAM = '003'
ketuatuuePM = '006'
ketuatusitaAM = '004'
ketuatusitaPM = '007'
myakuhakuAM = '005'
myakuhakuPM = '008'
taionAM = '012'
taionPM = '013'
taisibou = '009'
hosuu = '0010'
memo = 'memo011'
listnosaigonohi = False


###########
# グラフ作成と表示

def graphsakusei(): # グラフ画像作成
	xmin=0
	xmax=100
	dx=1
	ymax=730
	ymin=670
	dy=25
	
	if os.path.exists(graphname):# グラフ画像あれば、消す。無ければそのまま作成。
		os.remove(graphname)
	else:
		pass
	x0 = [x[0] for x in healthlist]#０列目を抽出
	del x0[0]
	x = range(len(x0))
	y = [y[1] for y in healthlist]
	y1 = [y1[2] for y1 in healthlist]
	del y[0]
	del y1[0]
	plt.figure() #matplotでグラフ描く毎に最初に宣言しないと重ね書きされる。pythonista3の癖。

	# 体重以外の項目を換算して表示
	y2b = [y2b[10] for y2b in healthlist]#歩数
	y2 = other_y(y2b)
	print(y2b)
	print(y2)
	plt.plot(x,y2,linestyle='dashed',marker='o',color='g',label='Hosuu')#緑
	
	y3b = [y3b[9] for y3b in healthlist]#体脂肪
	y3 = other_y(y3b)
	print(y3b)
	print(y3)
	plt.plot(x,y3,linestyle='dashed',marker='o',color='orchid',label='Tisibou')#紫
	
	y4b = [y4b[12] for y4b in healthlist]#体温am
	y4 = other_y(y4b)
	plt.plot(x,y4,linestyle='dashed',marker='o',color='hotpink',label='TaionAM')#ピンク
	
	y5b = [y5b[3] for y5b in healthlist]#血圧上am
	y5 = other_y(y5b)
	plt.plot(x,y5,linestyle='dashed',marker='o',color='y',label='KetuatuUeAM')#黄色
	
	y6b = [y6b[4] for y6b in healthlist]#血圧下am
	y6 = other_y(y6b)
	plt.plot(x,y6,linestyle='dashed',marker='o',color='gold',label='KetuatuSitaAM')#黄色
	'''
	y7b = [y7b[11] for y7b in healthlist]#memoの▲の日
	y7 = other_y(y7b)
	plt.plot(x,y7,linestyle='dashed',marker='o',color='goldenrod',label='Memo')#茶色
	'''
	
	#plt.figure() #matplotでグラフ描く毎に宣言しないと重ね書きされる。最初に宣言pythonista3の癖。
	plt.grid()#グリッドの表示
	plt.plot(x,y,marker='o',color='red',label='AMkg')#グラフにデータインプット
	plt.plot(x,y1,marker='v',color='blue',label='PMkg')
	#plt.plot(x,y2,linestyle='dashed',marker='o',color='g',label='Hosuu')
	plt.ylim(ymin,ymax) #グラフの表示範囲を指示 
	plt.title('taijyuu kg')
	plt.xlabel('date')
	plt.ylabel('kg')
	#plt.xlim([xmin,xmax])
	
	plt.legend(bbox_to_anchor=(1.01,1),loc='upper left',borderaxespad=0,fontsize=18)# 凡例の表示。
	plt.subplots_adjust(right=0.8) # 右側の余白を追加して凡例を切れない様にする(グラフを左から80％以内に表示)
	plt.show() #グラフ表示
	plt.savefig(graphname)#PNGでカレントに保存される
	
	pil_img = Image.open(graphname)#pilに画像読み込み
	imgg = pil2ui(pil_img)
	return imgg

# 体重以外の項目を675-725の50の範囲内に換算した値のリストを返す
def other_y(inputlist): #
	yyb = inputlist
	#其の他データを体重に合わせて表示(670-730→675−725の50で最大値最小値に換算して表示
	#yyb = [yyb[10] for yyb in healthlist]#歩数
	del yyb[0]#インデックスの先頭行を削除
	yyb = [float(x) for x in yyb]# リスト全体をstrからfloatに変換
	yymin2 = min2(yyb) #2番目に小さい値(自作関数)
	yyd=(float(max(yyb))-yymin2)/50
	# [0 if c<15 else c for c in yyb] #空白値が12までなので、15以下を0に置換
	yyout = [((i-yymin2)/yyd)+675 if i>15 else 0 for i in yyb] #yybのリストを順に15超は(i-yymin2)*yyd.15未満は0に置換
	print('yyb;',yyb,'yymin2;',yymin2,'yyd;',yyd,'yyout;',yyout)
	return yyout

# 2番目に小さい値を返す
def min2(inputlist): # 
	m1,m2=float('inf'),float('inf') # float('inf')は、無限大を示す
	for x in inputlist:
		#print(x)
		x = float(x) #引数がstrだとエラーになるのでfloatに変換。しかし、数字以外だとやっぱりエラー(^^)b
		if x == m1:#最小値が複数ある場合の除去用に必要な条件分岐
			pass
		elif x < m1:
			m1,m2=x,m1
		elif x < m2:
			m2 = x
	return m2

# pil <=> ui pilとios(ui)の使う画像データは異なるので　変換が必要。今回はpil→uiに変換してる。imgIn=pil
def pil2ui(imgIn):#from PIL import Image が必要
	with io.BytesIO() as bIO: # pilの画像データをiosのuiで使える画像データに変換する。import io必要
		imgIn.save(bIO, 'PNG')
		imgOut = ui.Image.from_data(bIO.getvalue())
	del bIO
	return imgOut

###########
# メイン処理

def readdata(): # データファイルの読み込みリスト変数に代入 不使用
	global healthlist # グローバル変数でないと各関数で読めない。ここで変更するのでglobal宣言必要
	if os.path.exists(filename):
		healthlist =[]
		faile1 = open(filename,"r",encoding='utf-8') # ファイルを読み込む＝ｒ属性でオープンする。
		healthlist = list(csv.reader(faile1)) # すべて読み込んでcsvオブジェクト→リストデータにする。
		#for n in range(len(memocamdata)): # 一行づつ全部表示。rangeで数のカウント lenで要素数
		#	memocamdata[n] = memocamdata[n].strip("\n") # stripで指定文字消去。要素1づつに入てる、改行を消す
		faile1.close() # ファイルをクローズする。メモリ節約
	else:
		healthlist = ['not data file']
	return healthlist

def writedata(healthlist): # グローバル変数のリストをデータファイルに書込み
	with open(filename,'w', newline='',encoding='utf-8') as f:# テキストファイルを作成。winはnweline='' を入れると安全？
		writer = csv.writer(f) # 二次元配列を一気に書込み
		writer.writerows(healthlist) #　二次元配列を一気に書込み

def listgousei():#入力数値を二次元配列の最後列に追加。
	global healthlist # グローバル変数でないと各関数で読めない。ここで変更するのでglobal宣言必要
	healthlist0 = [nitiji_kyou,taijyuuAM,taijyuuPM,ketuatuueAM,ketuatusitaAM,myakuhakuAM,ketuatuuePM,ketuatusitaPM,myakuhakuPM,taisibou,hosuu,memo,taionAM,taionPM]
	healthlist.append(healthlist0)
	return healthlist

def tail_csv(list0,n):#ｃｓｖの最後からｎ行目までをリストで返す。文字列のまま。
	#with open(file0) as f: #def ni file0 wo hikisuu de ireru
	#reader = csv.reader(f)#ファイルをＣＳＶリーダーに変換
	#next(reader)#ヘッダーを捨てる
	#rows = [row for row in reader]#全部行読んでリスト化
	#tail = [list(map(float,row)) for row in rows[-n:]]#文字列なのでmap()でfloatに変換して、最後ｎ行目まで抜き出す。（全部数字の場合のみ）
	tail = [list0[-n:]]
	return tail

def dateck(sender):#リストの最下行が、今日か判別して代入
	#tail = [] #1次元配列を宣言
	global healthlist,taijyuuAM,taijyuuPM,ketuatuueAM,ketuatusitaAM,myakuhakuAM,ketuatuuePM,ketuatusitaPM,myakuhakuPM,taisibou,hosuu,memo,taionAM,taionPM,listnosaigonohi # グローバル変数でないと各関数で読めない。ここで変更するのでglobal宣言必要
	tail = healthlist[-1:] # リストの最後行を抽出
	if tail[0][0] == nitiji_kyou:
		listnosaigonohi = True
		taijyuuAM = tail[0][1]
		taijyuuPM = tail[0][2]
		ketuatuueAM = tail[0][3]
		ketuatusitaAM = tail[0][4]
		myakuhakuAM = tail[0][5]
		ketuatuuePM = tail[0][6]
		ketuatusitaPM = tail[0][7]
		myakuhakuPM = tail[0][8]
		taisibou = tail[0][9]
		hosuu =tail[0][10]
		memo = tail[0][11]
		taionAM = tail[0][12]
		taionPM = tail[0][13]
		
		g_name = str('体重AM； ') + str(float(taijyuuAM)/10) + str('kg') # 後ろに言葉を足す。
		sender.superview['ttaijyuuAM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('体重PM； ') + str(float(taijyuuPM)/10) + str('kg') # 後ろに言葉を足す。
		sender.superview['ttaijyuuPM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('血圧上AM； ') + ketuatuueAM + str('mmHg(135)') # 後ろに言葉を足す。
		sender.superview['tketuatuueAM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('血圧下AM； ') + ketuatusitaAM + str('mmHg(85)') # 後ろに言葉を足す。
		sender.superview['tketuatusitaAM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('脈拍AM； ') + myakuhakuAM + str('回／分(60-90)') # 後ろに言葉を足す。
		sender.superview['tmyakuhakuAM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('血圧上PM； ') + ketuatuuePM + str('mmHg(135)') # 後ろに言葉を足す。
		sender.superview['tketuatuuePM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('血圧下PM； ') + ketuatusitaPM + str('mmHg(85)') # 後ろに言葉を足す。
		sender.superview['tketuatusitaPM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('脈拍PM； ') + myakuhakuPM + str('回／分（60−90）') # 後ろに言葉を足す。
		sender.superview['tmyakuhakuPM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('体脂肪率； ') + str(float(taisibou)/10) + str('％(10−19)') # 後ろに言葉を足す。
		sender.superview['ttaisibou'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('歩数； ') + hosuu + str('歩(1万)') # 後ろに言葉を足す。
		sender.superview['thosuu'].title = g_name # テキストビューに反映する。左右重要。
		g_name = memo # 後ろに言葉を足す。
		sender.superview['tmemo'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('体温AM； ') + str(float(taionAM)/10) + str('度') # 後ろに言葉を足す。
		sender.superview['ttaionAM'].title = g_name # テキストビューに反映する。左右重要。
		g_name = str('体温PM； ') + str(float(taionPM)/10) + str('度') # 後ろに言葉を足す。
		sender.superview['ttaionPM'].title = g_name # テキストビューに反映する。左右重要。		
	else:
		pass
		
	return



###########
# load save create ボタン

def loadinput(sender):
	global healthlist,taijyuuAM,taijyuuPM,ketuatuueAM,ketuatusitaAM,myakuhakuAM,ketuatuuePM,ketuatusitaPM,myakuhakuPM,taisibou,hosuu,memo,taionAM,taionPM # グローバル
	
	if os.path.exists(filename):
		readdata()
		dateck(sender)
		
	else:
		sender.superview['lasttext'].title = str('データファイルがありません。データを作成しました。') # テキストビューに反映する。左右重要。	
		createinput(sender)
		
	img = graphsakusei()
	sender.superview['graphview'].image = img
	
	sender.superview['txtcsv'].text = str(healthlist)



def saveinput(sender):
	global healthlist
	backfilename = filename[:-4] + '_bk.csv'
	if os.path.exists(backfilename):#バックアップがあるか確認して、有れば消す
		os.remove(backfilename)
	else:
		pass
		
	if os.path.exists(filename):
		os.rename(filename,backfilename)#バックアップファイルにリネーム
		
		if listnosaigonohi:
			#print(backfilename)
			healthlist.pop(-1) #pop;リストの最後の要素を取得するメソッドだけど、結果として最後の要素を抜く
			#print(healthlist)
			listgousei()
			#print(healthlist)
			writedata(healthlist)
			sender.superview['lasttext'].title = str('healthlistdata保存完了') # テキストビューに反映
		else:
			listgousei()
			writedata(healthlist)
			sender.superview['lasttext'].title = str('healthlistdata保存完了') # テキストビューに反映
	else:
		sender.superview['lasttext'].title = str('データファイルがありません。') # テキストビューに反映する。左右重要。


def createinput(sender):
	if os.path.exists(filename):
		sender.superview['lasttext'].title = str('データファイルが既に有ります。') # テキストビューに反映する。左右重要。	
	else:
		#listgousei()
		writedata(healthlist)
	sender.superview['lasttext'].title = str('healthlistdata新規作成完了') # テキストビューに反映

def deleteinput(sender):
	if os.path.exists(filename):
		os.remove(filename)
		sender.superview['lasttext'].title = str('healthlistdata削除完了') # テキストビューに反映
	else:
		sender.superview['lasttext'].title = str('データファイルがありません。') # テキストビューに反映する。左右重要。

###########
# 体重等の入力ボタン

def taijyuuAMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('体重AM； ') + str(float(f_name)/10) + str('kg') # 後ろに言葉を足す。
	sender.superview['ttaijyuuAM'].title = g_name # テキストビューに反映する。左右重要。
	global taijyuuAM
	taijyuuAM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
	
def taijyuuPMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('体重PM； ') + str(float(f_name)/10) + str('kg') # 後ろに言葉を足す。
	sender.superview['ttaijyuuPM'].title = g_name # テキストビューに反映する。左右重要。
	global taijyuuPM
	taijyuuPM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def ketuatuueAMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('血圧上AM； ') + f_name + str('mmHg(135)') # 後ろに言葉を足す。
	sender.superview['tketuatuueAM'].title = g_name # テキストビューに反映する。左右重要。
	global ketuatuueAM
	ketuatuueAM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def ketuatusitaAMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('血圧下AM； ') + f_name + str('mmHg(85)') # 後ろに言葉を足す。
	sender.superview['tketuatusitaAM'].title = g_name # テキストビューに反映する。左右重要。
	global ketuatusitaAM
	ketuatusitaAM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def myakuhakuAMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('脈拍AM； ') + f_name + str('回／分(60-90)') # 後ろに言葉を足す。
	sender.superview['tmyakuhakuAM'].title = g_name # テキストビューに反映する。左右重要。
	global myakuhakuAM
	myakuhakuAM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def ketuatuuePMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('血圧上PM； ') + f_name + str('mmHg(135)') # 後ろに言葉を足す。
	sender.superview['tketuatuuePM'].title = g_name # テキストビューに反映する。左右重要。
	global ketuatuuePM
	ketuatuuePM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def ketuatusitaPMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('血圧下PM； ') + f_name + str('mmHg(85)') # 後ろに言葉を足す。
	sender.superview['tketuatusitaPM'].title = g_name # テキストビューに反映する。左右重要。
	global ketuatusitaPM
	ketuatusitaPM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def myakuhakuPMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('脈拍PM； ') + f_name + str('回／分（60−90）') # 後ろに言葉を足す。
	sender.superview['tmyakuhakuPM'].title = g_name # テキストビューに反映する。左右重要。
	global myakuhakuPM
	myakuhakuPM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def taisibouinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('体脂肪率； ') + str(float(f_name)/10) + str('％(10−19)') # 後ろに言葉を足す。
	sender.superview['ttaisibou'].title = g_name # テキストビューに反映する。左右重要。
	global taisibou
	taisibou = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def hosuuinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('歩数； ') + f_name + str('歩(1万)') # 後ろに言葉を足す。
	sender.superview['thosuu'].title = g_name # テキストビューに反映する。左右重要。
	global hosuu
	hosuu = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def memoinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name # 後ろに言葉を足す。
	sender.superview['tmemo'].title = g_name # テキストビューに反映する。左右重要。
	global memo
	memo = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
	
def taionAMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('体温AM； ') + str(float(f_name)/10) + str('度') # 後ろに言葉を足す。
	sender.superview['ttaionAM'].title = g_name # テキストビューに反映する。左右重要。
	global taionAM
	taionAM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
		
def taionPMinput(sender): # 数値を入れて標準するボタン
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = str('体温PM； ') + str(float(f_name)/10) + str('度') # 後ろに言葉を足す。
	sender.superview['ttaionPM'].title = g_name # テキストビューに反映する。左右重要。
	global taionPM
	taionPM = f_name
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
	
###########
# 数字入力ボタン	

def b01_click(sender):	
	text00 = "1"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b02_click(sender):	
	text00 = "2"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b03_click(sender):	
	text00 = "3"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b04_click(sender):	
	text00 = "4"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b05_click(sender):	
	text00 = "5"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b06_click(sender):	
	text00 = "6"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b07_click(sender):	
	text00 = "7"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b08_click(sender):	
	text00 = "8"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b09_click(sender):	
	text00 = "9"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b0_click(sender):	
	text00 = "0"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。

def b00_click(sender):	
	text00 = "00"
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	g_name = f_name + text00 # 後ろに言葉を足す。
	sender.superview['text1'].text = g_name # テキストビューに反映する。左右重要。
	
def bclear_click(sender):	
	f_name = sender.superview['text1'].text # textfieldのnameが['']
	sender.superview['text1'].text = str("") # テキストビューに反映する。左右重要。
	
def bmemoread_click(sender):
	sender.superview['text1'].text = memo # テキストビューに反映する。左右重要。
	

###########
# 

if os.path.exists(filename):
	readdata()
	tail = healthlist[-1:] # リストの最後行を抽出
	if tail[0][0] == nitiji_kyou:
		listnosaigonohi = True
		taijyuuAM = tail[0][1]
		taijyuuPM = tail[0][2]
		ketuatuueAM = tail[0][3]
		ketuatusitaAM = tail[0][4]
		myakuhakuAM = tail[0][5]
		ketuatuuePM = tail[0][6]
		ketuatusitaPM = tail[0][7]
		myakuhakuPM = tail[0][8]
		taisibou = tail[0][9]
		hosuu =tail[0][10]
		memo = tail[0][11]
		taionAM = tail[0][12]
		taionPM = tail[0][13]
	else:
		writedata(healthlist)

v = ui.load_view()
v.present('fullscreen')

