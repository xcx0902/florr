from tkinter import*
from random import*
from tkinter.ttk import*
from tkinter.messagebox import*
import tkinter as tk
import ctypes
import threading
import webbrowser
import time
import threading
from time import strftime
import winsound
from tkinter.scrolledtext import ScrolledText
#from pynput.keyboard import Key, Controller
import pyautogui
#---------------------------------------------------- WINDOW
root = Tk()
winWidth = 630
winHeight = 400
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
root.geometry(f"{winWidth}x{winHeight}+{x}+{y}")
root.title("Florr.io Tool")
root.resizable(0,0)
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)
#-----------------------------------------------------
global setting
setting = 1

#----------------------------------------------------
class mine(threading.Thread):
    
    def __init__(self, *args, **kwargs):
        super(mine, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()    
        self.__flag.set()       
        self.__running = threading.Event()      
        self.__running.set()      

    def run(self):
        while self.__running.is_set():
            self.__flag.wait()
            if setting == 1:
                pyautogui.keyDown("shift")
            if setting == 2:
                pyautogui.keyDown("space")             
            if setting == 3:
                pyautogui.keyDown("w")
    def pause(self):
        self.__flag.clear()    

    def resume(self):
        self.__flag.set()    
    def stop(self):
        self.__flag.set()      
        self.__running.clear()        
threads = []
t1 = mine()
threads.append(t1)
t1.pause()
if __name__ == '__main__':
    for t in threads:
        t.daemon=True
        t.start()

#-----------------------------------------------------
def minimize():
    root.iconify()
def showPopupMenu(event):
    rightmenu.post(event.x_root,event.y_root)

def t_close_handler():
    root.attributes("-disabled", 0)
    window.destroy()
def status():
    def apply():
        alpha = scale.get()
        alpha = alpha / 100
        root.attributes('-alpha',alpha)
        acc = round(alpha,2)
        viewa = f"当前设定值:{str(acc)}"
    if demoStatus.get():
        global window
        window = Toplevel(root)
        window.geometry("620x300+200+250")
        window.title("透明效果设置")
        root.attributes('-alpha',0.85)
        tip2_window = Label(window,
                    text='透明效果设置\n',
                    font=("Microsoft YaHei UI", 12),
                    foreground="black")
        tip2_window.pack()
        scale = Scale(window, from_=1, to_=100,orient=HORIZONTAL,length=220)
        scale.set(85)
        scale.pack()

        root.attributes('-disabled', 1)#Top=window
        tip_window = Label(window,
                    text='提示：\n'
                    '通过拖动或点击滑动条设置主窗口透明度。\n'
                            '数值越小，透明程度越高；数值越大，则反之\n'
                            '建议的值为85-98之间，默认值为85',
                    font=("Microsoft YaHei UI", 8),
                    foreground="black")
        tip_window.pack()
        apply = Button(window,
                    text='应用',
                    command=apply)
        apply.place(relx=0.4, y=260, relwidth=0.2, height=35)
        window.resizable(0,0)
        window.attributes('-toolwindow', True)
        window.protocol("WM_DELETE_WINDOW", t_close_handler)
    else:
        root.attributes('-alpha',1)
def topview():
    if homoStatus.get():
        root.attributes('-topmost', -1)
    else:
       root.attributes('-topmost', 0)    
       
       
def t_close_handler_about():
    root.attributes('-disabled', 0)
    window_about.destroy()
def about():
    def update():
        webbrowser.open('https://github.com/12sdj/Florr.io-Tool')
    global window_about
    window_about = Toplevel(root)
    window_about.geometry("510x280+200+250")
    window_about.resizable(0,0)
    window_about.attributes('-toolwindow', True)
    window_about.title("关于")
    window_about.protocol("WM_DELETE_WINDOW", t_close_handler_about)
    root.attributes('-disabled', 1)
    label_a = Label(window_about,
                   text='关于本程序',
                   font=("Microsoft YaHei UI", 12))
    label_a.pack()
    tip_window = Label(window_about,
                    text='Florr.io Tool \n'
                            'Version 1.0.0 Update 01\n'
                            'Copyright (c) 2022 12sdj',
                    font=("Microsoft YaHei UI", 10),
                    foreground="black")
    tip_window.pack()
    control2 = Button(window_about, text ="查看源代码", command = update)
    control2.place(relx=0.35, y=235, relwidth=0.3, height=40)
def t_close_handler_licence():
    root.attributes('-disabled', 0)
    window_licence.destroy()
def license():
    global window_licence
    window_licence = Toplevel(root)
    window_licence.geometry("780x590+200+250")
    window_licence.resizable(0,0)
    window_licence.attributes('-toolwindow', True)
    window_licence.protocol("WM_DELETE_WINDOW", t_close_handler_licence)
    window_licence.title("开源协议【契约】")
    root.attributes('-disabled', 1)
    #Unint
    label_b = Label(window_licence,
                   text='开源协议',
                   font=("Microsoft YaHei UI", 12))
    label_b.pack()
    state = ScrolledText(window_licence, relief="flat", font=("Microsoft YaHei UI", 10))
    state.place(relx=0.02, y=40, relwidth=0.96, height=530)
    state.insert(INSERT, "注意：\n")
    state.insert(INSERT, "本软件不含有任何旨在破坏用户计算机数据和获取用户隐私信息的恶意代码，不含有任何跟踪、监视用户计算机的功能代码，不会监控用户网上、网下的行为，不会收集用户使用其它软件、文档等个人信息，不会泄漏用户隐私。\n")
    state.insert(INSERT, "\n")
    state.insert(INSERT, "以下为开源协议内容：\n")
    state.insert(INSERT, "MIT License\n")
    state.insert(INSERT, "\n")
    state.insert(INSERT, "Copyright (c) 2022 12sdj\n")
    state.insert(INSERT, "\n")
    state.insert(INSERT, "Permission is hereby granted, free of charge, to any person obtaining a copy\n")
    state.insert(INSERT, "of this software and associated documentation files (the 'Software'), to deal\n")
    state.insert(INSERT, "in the Software without restriction, including without limitation the rights\n")
    state.insert(INSERT, "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n")
    state.insert(INSERT, "copies of the Software, and to permit persons to whom the Software is\n")
    state.insert(INSERT, "furnished to do so, subject to the following conditions:\n")
    state.insert(INSERT, "\n")
    state.insert(INSERT, "The above copyright notice and this permission notice shall be included in all\n")
    state.insert(INSERT, "copies or substantial portions of the Software.\n")
    state.insert(INSERT, "\n")
    state.insert(INSERT, "THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n")
    state.insert(INSERT, "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n")
    state.insert(INSERT, "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n")
    state.insert(INSERT, "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n")
    state.insert(INSERT, "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n")
    state.insert(INSERT, "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n")
    state.insert(INSERT, "SOFTWARE.\n")
    state.configure(state='disabled')
    
#------------------------------------------------------
def control():
    control['state'] = DISABLED
    end['state'] = NORMAL
    state.configure(state='normal')
    state.delete('0.0', END)
    state.insert(INSERT, "当前状态：正在运行\n")
    state.insert(INSERT, "程序正在以您对程序的配置做出相应操作\n")
    state.insert(INSERT, "\n")
    state.insert(INSERT, "健康游戏忠告\n")
    state.insert(INSERT, "抵制不良游戏，拒绝盗版游戏。\n")
    state.insert(INSERT, "注意自我保护，谨防受骗上当。\n")
    state.insert(INSERT, "适度游戏益脑，沉迷游戏伤身。\n")
    state.insert(INSERT, "合理安排时间，享受健康生活。")
    state.configure(state='disabled')
    global setting
    setting = var3.get()
    b['state'] = DISABLED
    b2['state'] = DISABLED
    b3['state'] = DISABLED
    t1.resume()
def end():
    control['state'] = NORMAL
    end['state'] = DISABLED
    state.configure(state='normal')
    state.delete('0.0', END)
    state.insert(INSERT, "当前状态：空闲\n")
    state.insert(INSERT, "您可以在控制中心右侧选择一个您倾向的配置，设置后点击“开始运行”从而运行程序")
    state.configure(state='disabled')
    b['state'] = NORMAL
    b2['state'] = NORMAL
    b3['state'] = NORMAL
    t1.pause()
    pyautogui.keyUp("space")  
    pyautogui.keyUp("shift")  
    pyautogui.keyUp("w")   
def chosen():
    global setting
    setting = var3.get()


#-----------------------------------------------------
label_1 = Label(root,
                   text='Florr.io Tool',
                   font=("Microsoft YaHei UI", 12))
label_1.pack()
label_2 = Label(root,
                   text='运行情况和提示',
                   font=("Microsoft YaHei UI", 8))
label_2.place(relx=0.03, y=40, relwidth=0.45, height=25)
label_3 = Label(root,
                   text='控制中心',
                   font=("Microsoft YaHei UI", 8))
label_3.place(relx=0.03, y=240, relwidth=0.45, height=25)
state = ScrolledText(root, relief="flat", font=("Microsoft YaHei UI", 10))
state.place(relx=0.03, y=70, relwidth=0.94, height=170)
state.insert(INSERT, "当前状态：空闲\n")
state.insert(INSERT, "您可以在控制中心右侧选择一个您倾向的配置，设置后点击“开始运行”从而运行程序\n")
state.insert(INSERT, "\n")
state.insert(INSERT, "值得注意的是，程序会模拟按住特定键盘上按键。因此，建议您不要在程序运行时，打开其他带有输入框的软件。\n")
state.configure(state='disabled')
#state.delete('0.0', END)
control = Button(root, text = "开始运行", command = control)
control.place(relx=0.03, y=265, relwidth=0.4, height=40)
end = Button(root, text = "停止运行", command = end)
end.place(relx=0.03, y=305, relwidth=0.4, height=40)
end['state'] = DISABLED


var3 = IntVar()
var3.set(setting)
b = Radiobutton(root,text="Defend(SHIFT)",variable = var3 ,value =1,command=chosen)
b.place(relx=0.46, y=265, relwidth=0.3, height=40)
b2 = Radiobutton(root,text="Attack(SPACE)",variable = var3 ,value =2,command=chosen)
b2.place(relx=0.46, y=305, relwidth=0.3, height=40)
b3 = Radiobutton(root,text="AFK",variable = var3 ,value =3,command=chosen)
b3.place(relx=0.76, y=265, relwidth=0.24, height=40)
#-----------------------------------------------------ToolBar
menubar = Menu(root)
menubar.add_cascade(label='关于本程序', command=about) 
menubar.add_cascade(label='开源协议', command=license)
winmenu = Menu(menubar, tearoff=0) 
menubar.add_cascade(label='窗口选项', menu=winmenu)
demoStatus = BooleanVar()
demoStatus.set(False)
homoStatus = BooleanVar()
homoStatus.set(False)
winmenu.add_checkbutton(label = "透明效果",command=status,variable=demoStatus)
winmenu.add_checkbutton(label = "窗口前置",command=topview,variable=homoStatus)
root.config(menu=menubar)
winmenu.add_separator()
winmenu.add_command(label='退出程序', command=root.quit)
root.config(menu=menubar) 

rightmenu = Menu(root,tearoff=False)
rightmenu.add_command(label="窗口最小化",command=minimize)
rightmenu.add_command(label="退出程序",command=root.destroy)
root.bind("<Button-3>",showPopupMenu)
#-----------------------------------------------------------
root.mainloop()