import tkinter as tk
import copy
import shutil
from tkinter import filedialog
from FetchData import FetchHistoryData
import os

ConditionListAll = []
ConditionList = []
OpSelected = 0
Rowr       = 0
SetCount   = 0

FindInRange=[("Lowest",40),("Higest",41),("Average",42),("Sum",43),("None",0)]

TechType=[("Open",1),("High",2),("Low",3),("Close",4),("MA",5),("RSI",6),("KD",7),("MACD",8),("Value",9),(">",20),("<",21),(">=",22),
("<=",23),("=",24),("+",25),("-",26),("*",27),("/",28),("CrossUp",29),("CrossDown",30),("And",31),("Or",32)]

TradeType = [("Buy",50),("Sell",51),("BuyNextBar",52)]


def OpToStr(Opcode):
    global TechType
    global FindInRange

    if Opcode >= 40 and Opcode <= 42:
        for Ty,In in FindInRange:
            if In == Opcode:
                return Ty        

    for Ty,In in TechType:
        if In == Opcode:
            return Ty
    return ""

def get():
    YearStart = var1.get()
    YearEnd   = var2.get()
    for IDid in IDList:
        FetchHistoryData(IDid,YearStart,YearEnd)

def AddId():
    global IDList
    NewID = var3.get()

    # Check ID format first
    try:
        if int(NewID) < 0 or int(NewID) > 10000:
            SetIdSta.set("ID number error")
            return
    except ValueError:
            SetIdSta.set("Not a vaule")
            return

    for idid in IDList:
        if idid == NewID:
            SetIdSta.set("ID already exist")
            return

    # If check pass, add it to list
    IDList.append(NewID)
    WriteIDlist()

def RemoveID():
    global IDList    
    DelID = var3.get()
    i = 0
    for idid in IDList:
        i += 1
        if DelID == idid:
            IDList.remove(idid)
            WriteIDlist()
            return
    SetIdSta.set("Not Find!")

def WriteIDlist():
    global IDList    
    f = open("IDList.txt", mode='w')
    length = len(IDList)
    i = 0
    for idid in IDList:
        f.write(idid)
        i += 1
        if i != length:
            f.write(",")
    f.close()
    RefleshIDlebal()

def RefleshIDlebal():
    global IdAll
    IdAll = ""    
    ReadIdlist()
    IDvar.set("ID List Now: "+IdAll)
    SetIdSta.set("Update success!")

def ReadIdlist():
    global IDList
    global IdAll
    for IDID in IDList:
        IdAll = IdAll+IDID+"-"

def StringForList(List):
    index = 0
    OpInt = 0
    RangeV   = ""
    Range    = 0
    str = ""

    for lis in List:
        if index % 2 == 0:
            OpInt = int(lis)
            str += OpToStr(int(lis))
        if index % 2 == 1:
            if OpInt >= 40 and OpInt <= 42:
                RangeV = lis
                Range  = 1
                str += "("
            if OpInt > 0 and OpInt < 10: # tech pointer
                if Range != 0:
                    str += "("+lis+"),"+RangeV+")"
                    Range = 0
                else:
                    str += "("+lis+")"
        str += " "
        index += 1
    return  str       

def AddSelect():
    global R1var
    global R2var
    global var4
    global var5
    global SelectOp
    global CList
    global ConditionList
    global OpSelected

    ListLast = 0
    Opcode1 = R1var.get() # hight low
    Opcode2 = R2var.get() # average lowest higest

    length = len(ConditionList)

    if length > 0:
        ListLast = int( ConditionList[length-2]  )
        print("listlast = ",ListLast)
    if var4.get() != "":
        Opcode1V = int(var4.get())
    else:
        Opcode1V = -1
    if var5.get() != "":
        Opcode2V = int(var5.get())
    else:
        Opcode2V = -1

    if Opcode2 != 0:   # if have average highest lowest
        if Opcode1 == 0 or Opcode1 >= 9: # avoid average(+,10) average(value(10),10)
            print("error combnation")
            return
        if ListLast > 0 and ListLast < 10:
            SelectOp.set("not allow pointer")
            return
        if Opcode2V == -1:
            SelectOp.set("please input a range")
            return
        if Opcode1V == -1:
            SelectOp.set("please input a value")
            return  
        ConditionList.append(str(Opcode2))
        ConditionList.append(str(Opcode2V))
        ConditionList.append(str(Opcode1))
        ConditionList.append(str(Opcode1V))

    elif Opcode2 == 0: # if no average highest lowest
        if Opcode1 > 0 and Opcode1 < 10:
            if ListLast > 0 and ListLast < 10:  # Not allow value follow by value
                SelectOp.set("not allow")
                return
            if Opcode1V == -1:
                SelectOp.set("Please input a vaule")
                return
            ConditionList.append(str(Opcode1))
            ConditionList.append(str(Opcode1V))
            print("List now1",ConditionList)
        elif length > 0:
            if Opcode1 >= 20 and Opcode1 <= 30:  #operater
                if  OpSelected == 1:
                    SelectOp.set("2 operter in condition")
                    return
                if  ListLast == 0 or ( ListLast >= 20 and ListLast <= 32 ): # Operation should not being the first or follow by other operater
                    SelectOp.set("not allow operater")
                    return
                ConditionList.append(str(Opcode1))
                ConditionList.append("-1")
                print("List now2",ConditionList)
                OpSelected = 1

            if Opcode1 >= 31 and Opcode1 <= 32:  #operater
                if  ListLast == 0 or ( ListLast >= 20 and ListLast <= 32 ): # Operation should not being the first or follow by other operater
                    SelectOp.set("not allow operater")
                    return
                ConditionList.append(str(Opcode1))
                ConditionList.append("-1")
                print("List now3",ConditionList)
                OpSelected = 0
        else:
            SelectOp.set("Not being the first")

    CList.set(StringForList(ConditionList))

def Backspace():
    global  CList
    global  ConditionList
    global  OpSelected

    if len(ConditionList) == 0:
        return

    ConditionList.pop()
    a = ConditionList.pop()

    if int(a) >= 20 and int(a) <= 24:
        OpSelected = 0

    CList.set(StringForList(ConditionList))
    print("List now",ConditionList)

def RemoveCurrentConditionList():
    number = int(var7.get())
    count = 0

    f = open("ConditionList.stock", mode='r')
    Lis = f.readlines()
    f.close()

    for a in Lis:
        Data = a[0:-1]  # to remove /n in last
        if Data == "end":
            count += 1

    if number > count:
        print("not find")
        return
    #print("Len No =",count)
    print(Lis)

    # find remove head and count
    I   = 1
    ind = 0
    remove_count = 0
    remove_head  = 0
    for a in Lis:
        Data = a[0:-1]
        #print("ind = ",ind,"data = ",Data)        
        if Data == "end":
            I += 1
            ind += 1
            if I == number:
                remove_head = ind
            continue

        if I == number:
            #print("find del ",Lis[ind])
            remove_count += 1
            ind += 1
            continue
        ind += 1

    ind = 0
    while ind <= remove_count:
        del Lis[remove_head]
        ind += 1
    #print(remove_count,remove_head)

    #print(Lis)

    f = open("ConditionList.stock", mode='w')
    f.writelines(Lis)
    f.close()

    f = open("ConditionList.stock", mode='r')
    ReadListToLabel(f)
    f.close()

def WriteConditonList():
    global ConditionList
    f = open("ConditionList.stock", mode='a')

    for Data in ConditionList:
        f.write(Data)
        f.write('\n')
    f.write('end\n')

    f.close()

def PrepareConditionString(trade,share,num,List):

    ListText = "No."+str(num)+" "

    if int(trade) == 50:
        ListText += ",Buy,"
    if int(trade) == 51:
        ListText += ",Sell,"
    if int(trade) == 52:
        ListText += ",BuyAtNext,"

    ListText += "Shares="+share+".   Rule ->"

    ListText += StringForList(List)

    return ListText

def ReadListToLabel(file):
    global Rowr
    global SetCount

    List    = []
    TextAll = ""
    trade = ""
    share = ""

    i = 0
    count = 1
    length = 0
    Maxlen = 0

    # find max length to pending
    for Lis in file.readlines():
        Data = Lis[0:-1]  # to remove /n in last
        if Data == "end":  # done find max length
            i = 0
            length = len( PrepareConditionString(trade,share,count,List) )
            print("len",length)
            if length  > Maxlen:
                Maxlen = length
                print("Max len",Maxlen)
            List.clear()
            count += 1
            continue
        if i == 0:
            trade = Data
        if i == 1:
            share = Data
        if i >= 2:
            List.append(Data)            
        i += 1

    file.seek(0,0)
    i      = 0
    count = 1
    List.clear()

    for Lis in file.readlines():
        Data = Lis[0:-1]  # to remove /n in last
        print("Data",Data)
        if Data == "end":  # done, make a string
            i = 0
            p = 0
            TextNow = PrepareConditionString(trade,share,count,List)
            length = len( TextNow )
            TextAll += TextNow
            if length  < Maxlen: # pending
                while p < Maxlen - length:
                    if p == (Maxlen - length -1):
                        TextAll += ""
                        break    
                    TextAll += "  " # pending space
                    p += 1
            TextAll += "\n"
            List.clear()
            count += 1
            continue
        if i == 0:
            trade = Data
        if i == 1:
            share = Data
        if i >= 2:
            List.append(Data)
        i += 1

    print(TextAll)
    ListText.set(TextAll)

    l12.grid(row=Rowr+1, column=0,columnspan=20,rowspan=12)
    Rowr += count
'''
def ReadListToConditionList(file):
    global ConditionList

    ConditionList.clear()
    for Lis in file.readlines():
        Data = Lis[0:-1]  # to remove /n in last
        if Data == "end":
            break
        ConditionList.append(Data)
'''
def CreatCondition():
    global  ConditionList
    global  CList
    global  OpSelected

    Trade = R3var.get()
    Share = var6.get()

    if Trade == 0 or int(Share) == 0:
        print("error")
        return

    length = len(ConditionList)

    # pasring list
    if length == 0:
        print("error")
        return

    Op  = 0
    i   = 0
    for Lis in ConditionList:
        #print("i=",i,"L=",Lis)
        print("Lisa,",Lis)
        if i % 2 == 0:
            if int(Lis) == 31 or int(Lis) == 32: # when and or op
                if i == 0: # and or should not being first
                    print("error1 and or not being first")
                    return
                elif Op == 0:   # need > < = in section
                    print("error2 no op")
                    return
                elif Op == 1:   # reset op = 1           
                    Op = 0
                    print("And or readed")
            if (int(Lis) >= 20 and int(Lis) <= 24) or int(Lis) == 29 or int(Lis) == 30: # when > < = cross op, set op = 1 
                if Op == 1:     # two > < = in section
                    print("two > < = cross in section")
                    return
                else:
                    Op = 1
                    #print("<>=")
        #if i % 2 == 1:
        i += 1
    
    if Op == 0: # after check op should be 1
        print("error4 no op")
        return

    OpSelected = 0
    ConditionList.insert(0,Share)
    ConditionList.insert(0,str(Trade))

    WriteConditonList()

    f = open("ConditionList.stock", mode='r')
    ReadListToLabel(f)
    f.close()

    # clear
    ConditionList.clear()
    CList.set("")

def SelectRangeOp():
    global SelectOp
    global R1var
    global R2var
    global var4
    global var5

    combo    = ""

    if var4.get() != "":
        Opcode1V = int(var4.get())
    else:
        Opcode1V = -1
    if var5.get() != "":
        Opcode2V = int(var5.get())
    else:
        Opcode2V = -1

    Opcode1 = R1var.get()
    Opcode2 = R2var.get()

    print("op1 =",Opcode1)

    if Opcode2 == 0:   # Range op = 0, using Tech op only
        if Opcode1 > 0 and Opcode1 < 10 and Opcode1V != -1 :
            combo = OpToStr(Opcode1) + "(" + str(Opcode1V) + ")"
        else:
            combo = OpToStr(Opcode1)
    elif Opcode1 == 0: # Tech op = 0, using range op only
        if Opcode2V != -1:
            combo = OpToStr(Opcode2)+"(,"+ str(Opcode2V) +")"
        else:
            combo = OpToStr(Opcode2)+"()"
    else:  # Tech + Range
        if Opcode1 > 0 and Opcode1 < 9:
            if Opcode1V != -1 and Opcode2V != -1:
                combo1 = OpToStr(Opcode1) + "(" + str(Opcode1V) + ")"               # average(10)
                combo = OpToStr(Opcode2)+ "("+ combo1 +"," + str(Opcode2V) + ")"    # average(open(10),10)
            elif Opcode1V == -1 and Opcode2V == -1:
                combo1 = OpToStr(Opcode1)                                           # open
                combo = OpToStr(Opcode2)+ "("+ combo1 +",)"                         # average(open,)
            elif Opcode1V == -1:
                combo1 = OpToStr(Opcode1)                                           # open
                combo = OpToStr(Opcode2)+ "("+ combo1 +"," + str(Opcode2V) + ")"    # average(open,10)
            elif Opcode2V == -1:
                combo1 = OpToStr(Opcode1) + "(" + str(Opcode1V) + ")"               # open(10)
                combo = OpToStr(Opcode2)+ "("+ combo1 +",)"                         # average(open(10),)
        else:
            R2var.set(0)                                                            # case for + - * / corssup crossdown value
            combo = OpToStr(Opcode1)

    SelectOp.set(combo)

def Entry1callback():
    global var1

    Stri = var1.get()

    if str.isdigit(Stri) != 1:
        var1.set(Stri[0:-1])
        return

    if len(Stri) == 1:
        if Stri[-1] != '2':
            var1.set(Stri[0:-1])
            return

    if len(Stri) == 2:
        if Stri[-1] != '0':
            var1.set(Stri[0:-1])
            return

    if len(Stri) == 5:
        if Stri[-1] != '0' and Stri[-1] != '1':
            var1.set(Stri[0:-1])
            return

    if len(Stri) == 6:
        if Stri[-2] == '1' and Stri[-1] > '2':
            var1.set(Stri[0:-1])
            return
        if Stri[-2] == '0' and Stri[-1] == '0':
            var1.set(Stri[0:-1])
            return

    if len(Stri) > 6:
        var1.set(Stri[0:-1])
        return

def Entry2callback():
    global var2

    Stri = var2.get()

    if str.isdigit(Stri) != 1:
        var2.set(Stri[0:-1])
        return

    if len(Stri) == 1:
        if Stri[-1] != '2':
            var2.set(Stri[0:-1])
            return

    if len(Stri) == 2:
        if Stri[-1] != '0':
            var2.set(Stri[0:-1])
            return

    if len(Stri) == 5:
        if Stri[-1] != '0' and Stri[-1] != '1':
            var2.set(Stri[0:-1])
            return

    if len(Stri) == 6:
        if Stri[-2] == '1' and Stri[-1] > '2':
            var2.set(Stri[0:-1])
            return
        if Stri[-2] == '0' and Stri[-1] == '0':
            var2.set(Stri[0:-1])
            return

    if len(Stri) > 6:
        var2.set(Stri[0:-1])
        return

def Entry3callback():
    global var3

    Stri = var3.get()

    if str.isdigit(Stri) != 1:
        var3.set(Stri[0:-1])
        return

    value = int(var3.get())
    if value > 9999:
        var3.set(Stri[0:-1])
        return

def Entry4callback():
    global var4
    global SelectOp

    Stri = var4.get()

    if Stri == "":
        var4.set("0")
        SelectRangeOp()
        return

    if str.isdigit(Stri) != 1:
        var4.set(Stri[0:-1])
        SelectRangeOp()
        return

    value = int(var4.get())

    if value >=240:
        var4.set("240")

    SelectRangeOp()

def Entry5callback():
    global var5
    global SelectOp

    Stri = var5.get()

    if Stri == "":
        var5.set("0")
        SelectRangeOp()
        return

    if str.isdigit(Stri) != 1:
        var5.set(Stri[0:-1])
        SelectRangeOp()
        return

    value = int(var5.get())
    if value < 0 or value >=240:
        var5.set("240")

    SelectRangeOp()

def Entry6callback():
    global var6
    Stri = var6.get()

    if str.isdigit(Stri) != 1:
        var6.set(Stri[0:-1])
        return

def Entry7callback():
    global var7
    Stri = var7.get()

    if str.isdigit(Stri) != 1:
        var7.set(Stri[0:-1])
        return

def LoadConditionFromFile():
    file_path = filedialog.askopenfilename(filetypes =[("stock files", "*.stock")])
    print(file_path)

    f = open(file_path, mode='r')

    #ReadListToConditionList(f)
    #f.seek(0,0)
    ReadListToLabel(f)
    f.close()
    try:
        os.remove("ConditionList.stock")
    except:
        print("no file to remove")

    shutil.copyfile(file_path,"ConditionList.stock")

def SaveConditionToFile():
    try:
        open("ConditionList.stock", mode='r')
    except FileNotFoundError:
        print("No Rule Created")
        SelectOp.set("Save fail,No Rule")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".stock",filetypes =[("stock files", "*.stock")] )
    #print("copy ConditionList.txt "+file_path)
    shutil.copyfile("ConditionList.stock",file_path)
    #f = open(file_path, mode='w')

    #f.close()
try:
    os.remove("ConditionList.stock")
except:
    print("no file to remove")

f = open("IDList.txt", mode='r')
IDList = []
while 1:
    ID = f.read(4)
    IDList.append(ID)
    ID = f.read(1)
    if ID != ",":
        break
f.close()

IdAll = "--"

ReadIdlist()

window = tk.Tk()
window.title('Stock')
window.geometry('840x950')
window.resizable(0,0)
'''
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
#window.rowconfigure(3, weight=1)
'''

IDvar    = tk.StringVar()
mainvar  = tk.StringVar()
SetIdSta = tk.StringVar()
SelectOp = tk.StringVar()
CList    = tk.StringVar()
ListText = tk.StringVar()
var1     = tk.StringVar()
var2     = tk.StringVar()
var3     = tk.StringVar()
var4     = tk.StringVar()
var5     = tk.StringVar()
var6     = tk.StringVar()
var7     = tk.StringVar()
R1var    = tk.IntVar() # TechType,OperationType
R2var    = tk.IntVar() # FindInRange
R3var    = tk.IntVar() # Trade

var1.trace("w", lambda name, index,mode, var=var1: Entry1callback())
var2.trace("w", lambda name, index,mode, var=var2: Entry2callback())
var3.trace("w", lambda name, index,mode, var=var3: Entry3callback())
var4.trace("w", lambda name, index,mode, var=var4: Entry4callback())
var5.trace("w", lambda name, index,mode, var=var5: Entry5callback())
var6.trace("w", lambda name, index,mode, var=var5: Entry6callback())
var7.trace("w", lambda name, index,mode, var=var5: Entry7callback())

# lebal
l1 = tk.Label(window,textvariable= IDvar, bg='yellow') 
l2 = tk.Label(window,text='Get stock history data(date format: yyyymm)', font=('Comic Sans MS', 20))
l3 = tk.Label(window,text='Start Year:', font=('Arial' ) )
l4 = tk.Label(window,text='End year:', font=('Arial' ) ) 
l5 = tk.Label(window,text='Add or Remove ID', font=('Comic Sans MS', 20))
l6 = tk.Label(window,textvariable= SetIdSta)
l7 = tk.Label(window,text='Stock ID:', font=('Arial' ) ) 
l8 = tk.Label(window,text='Select Now:', font=('Arial' ) )  # Select Now
l9 = tk.Label(window,textvariable=SelectOp, font=('Arial' ) )  
l10 = tk.Label(window,text='Rule Now:', font=('Arial' ) )  
l11 = tk.Label(window,textvariable=CList, font=('Arial' ) )  
l12 = tk.Label(window,textvariable=ListText, font=('Arial' ) )
l13 = tk.Label(window,text="Save/Load rule from file", font=('Comic Sans MS', 20) )
l14 = tk.Label(window,text="Rule editor", font=('Comic Sans MS', 20) )
l15 = tk.Label(window,text="Days Interval:", font=('Arial' ) )
l16 = tk.Label(window,text="Function:", font=('Arial' ) )
l17 = tk.Label(window,text="Trade Type:", font=('Arial' ) )
l18 = tk.Label(window,text="Shares:", font=('Arial' ) )
l19 = tk.Label(window,text="Rules:", font=('Comic Sans MS', 20) )
l20 = tk.Label(window,text="No:", font=('Arial' ) )

ll0 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll1 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll2 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll3 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll4 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll5 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll6 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll7 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll8 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll9 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll10 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll11 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll12 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll13 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll14 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll15 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll16 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll17 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')
ll18 = tk.Label(window,text="         ", font=('Arial' ) , bg='green')
ll19 = tk.Label(window,text="         ", font=('Arial' ) , bg='red')

# entry
e1 = tk.Entry(window,textvariable=var1, width = 8, show=None)  #, width=9, font=('Arial', 14))  Start date
e2 = tk.Entry(window,textvariable=var2, width = 8, show=None)  #, width=9, font=('Arial', 14))  End date
e3 = tk.Entry(window,textvariable=var3, width = 5, show=None)  #, width=9, font=('Arial', 14))  # add or remove ID
e4 = tk.Entry(window,textvariable=var4,width = 4, show=None)  #, width=9, font=('Arial', 14))  # tech value
e5 = tk.Entry(window,textvariable=var5,width = 4, show=None)  #, width=9, font=('Arial', 14))  # range
e6 = tk.Entry(window,textvariable=var6,width = 6, show=None)  #, width=9, font=('Arial', 14))  # shares
e7 = tk.Entry(window,textvariable=var7,width = 4, show=None)  #, width=9, font=('Arial', 14))  # remove number

# button
b1 = tk.Button(window, text='Get data', font=('Arial', 9), width=8, height=1, command=get)
b2 = tk.Button(window, text='Add ID', font=('Arial', 9), command=AddId)
b3 = tk.Button(window, text='Remove ID', font=('Arial', 9), command=RemoveID)
b4 = tk.Button(window, text='Add select to rule', font=('Arial', 9), command=AddSelect)
b5 = tk.Button(window, text='Backspace', font=('Arial', 9), command=Backspace)
b6 = tk.Button(window, text='Create a Rule', font=('Arial', 13), command=CreatCondition)
b7 = tk.Button(window, text='Remove rule by number', font=('Arial', 9), command=RemoveCurrentConditionList)
b8 = tk.Button(window, text='Save Rule', font=('Arial', 9), command=SaveConditionToFile)
b9 = tk.Button(window, text='Load Rule', font=('Arial', 9), command=LoadConditionFromFile)

Rowr += 1

# grid
l1.grid(row=Rowr, column=0,columnspan=20)
Rowr += 1

l2.grid(row=Rowr, column=0,columnspan=20)  #Get stock history data(date format: yyyymm)
Rowr += 1

l3.grid(row=Rowr, column=1,columnspan=2,sticky ="E")  # Start date
e1.grid(row=Rowr, column=3,columnspan=3,sticky ="W")  # entry
l4.grid(row=Rowr, column=5,columnspan=2,sticky ="E")  # end date
e2.grid(row=Rowr, column=7,columnspan=3,sticky ="W")  # entry
b1.grid(row=Rowr, column=9,columnspan=3,sticky ="W")  # get data button
Rowr += 1

l5.grid(row=Rowr, column=0,columnspan=20)    # Add or Remove ID lebal
l6.grid(row=Rowr, column=5,sticky ="W")      # Add or Remove ID status lebal
Rowr += 1

l7.grid(row=Rowr, column=1,columnspan=2,sticky ="E")   # stock id
e3.grid(row=Rowr, column=3,columnspan=3,sticky ="W")   # add id entry
b2.grid(row=Rowr, column=7,columnspan=3,sticky ="W")   # add id button
b3.grid(row=Rowr, column=9,columnspan=3,sticky ="W")   # remove id button
Rowr += 1

l13.grid(row=Rowr, column=0,columnspan=20) # Save/Load rule from file label
Rowr += 1

b8.grid(row=Rowr, column=8,columnspan=3,sticky ="W") # Save rule button
b9.grid(row=Rowr, column=10,columnspan=3,sticky ="W") # Load rule button
Rowr += 1

l14.grid(row=Rowr, column=0,columnspan=20)  # rule editor lebal
Rowr += 1

I = 1
for Type,Index in TechType:
    r1 = tk.Radiobutton(window, text=Type, variable=R1var, value=Index, font=('Arial',8 ), command=SelectRangeOp)
    if I > 17:
        I = 1
        Rowr += 1
    r1.grid(row=Rowr, column=I ,columnspan=3,sticky ="W")
    I += 2
Rowr += 1

l15.grid(row=Rowr, column=1,columnspan=3,sticky ="W")  # Input days interval for Price/MA/KD/RSI/MACD :
e4.grid(row=Rowr, column=4,columnspan=2,sticky ="W")   # entry for days interval
Rowr += 1

I = 1
l16.grid(row=Rowr, column=I,columnspan=3,sticky ="W")    # function for Price/MA/KD/RSI/MACD :
I += 3
e5.grid(row=Rowr, column=I,columnspan=2,sticky ="W")
I += 1

for Type,Index in FindInRange:   # average lowest highest sum
    r1 = tk.Radiobutton(window, text=Type, variable=R2var, value=Index, font=('Arial',8 ), command=SelectRangeOp)
    r1.grid(row=Rowr, column=I,columnspan=3,sticky ="W")
    I += 2
Rowr += 1


l8.grid(row=Rowr, column=1,columnspan=3,sticky ="W")   # select now
l9.grid(row=Rowr, column=3,columnspan=5,sticky ="W")   # select now text
b4.grid(row=Rowr, column=13,columnspan=3,sticky ="W")  # add select
b5.grid(row=Rowr, column=16,columnspan=3,sticky ="W")  # backspace
Rowr += 1

l10.grid(row=Rowr, column=1,columnspan=3,sticky ="W")     # comdition now
l11.grid(row=Rowr, column=3,columnspan=17,sticky ="W")    # comdition now text
Rowr += 1


l17.grid(row=Rowr, column=1,columnspan=5,sticky ="W")  # trade type
I = 4
for Type,Index in TradeType:
    r1 = tk.Radiobutton(window, text=Type, variable=R3var, font=('Arial',8 ), value=Index)
    r1.grid(row=Rowr, column=I,columnspan=5,sticky ="W")
    I += 2
I += 2
l18.grid(row=Rowr, column=I,columnspan=2,sticky ="E")  # Shares
e6.grid(row=Rowr, column=I+2,columnspan=3,sticky ="W") # Shares entry
Rowr += 1


b6.grid(row=Rowr, column=8,columnspan=4)  # save this rule button
#Rowr += 1
I = 11
l20.grid(row=Rowr, column=I,columnspan=3,sticky ="E") # remove rule No.
e7.grid(row=Rowr, column=I+3,columnspan=3,sticky ="W")  # remove rule
b7.grid(row=Rowr, column=I+4,columnspan=4,sticky ="W")  # remove rule button
Rowr += 1

l19.grid(row=Rowr, column=0,columnspan=20)              # Rules
Rowr += 1

ll0.grid(row=0, column=0,sticky ="W")
ll1.grid(row=0, column=1,sticky ="W")
ll2.grid(row=0, column=2,sticky ="W")
ll3.grid(row=0, column=3,sticky ="W")
ll4.grid(row=0, column=4,sticky ="W")
ll5.grid(row=0, column=5,sticky ="W")
ll6.grid(row=0, column=6,sticky ="W")
ll7.grid(row=0, column=7,sticky ="W")
ll8.grid(row=0, column=8,sticky ="W")
ll9.grid(row=0, column=9,sticky ="W")
ll10.grid(row=0, column=10,sticky ="W")
ll11.grid(row=0, column=11,sticky ="W")
ll12.grid(row=0, column=12,sticky ="W")
ll13.grid(row=0, column=13,sticky ="W")
ll14.grid(row=0, column=14,sticky ="W")
ll15.grid(row=0, column=15,sticky ="W")
ll16.grid(row=0, column=16,sticky ="W")
ll17.grid(row=0, column=17,sticky ="W")
ll18.grid(row=0, column=18,sticky ="W")
ll19.grid(row=0, column=19,sticky ="W")

IDvar.set("ID List Now: "+IdAll)

window.mainloop()


'''
def Sim():
    Dates = var111.get()
    Y = Dates[0:4]
    M = Dates[4:]
    OutStr = "Year ="+Y+" Month ="+M
    Error = 0
    try:
        intY = int(Y)
        intM = int(M)
    except ValueError:
        Error = 1

    if Error == 1:
        mainvar.set("No a value")
    else:
        if intY < 1980 or ( intM < 0 or intM > 12 ):
            OutStr = "Date format error" 
        mainvar.set(OutStr)
'''