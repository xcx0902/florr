import florr_edit_core
from pymem import Pymem
import threading

import tkinter as tk
import tkinter.messagebox

root = tk.Tk()

root.title('Florr Editor')
# root.geometry('400x300')
# root.iconbitmap('icon.ico')

rw = 2
condi_list = []
unit_list = []
inv_entry_list = [(tk.StringVar(), tk.StringVar())]

addr_var = tk.StringVar(value='-1')
pid_var = tk.StringVar(value='-1')
petalname_var = tk.StringVar()
petallev_var = tk.StringVar(value='Common')
petalnum_var = tk.StringVar()

def disable_all():
    for each in unit_list:
        each['state'] = 'disabled'

def enable_all():
    for each in unit_list:
        each['state'] = 'normal'


def find_process():
    disable_all()
    res = florr_edit_core.find_florr_pid('edge.exe')
    if res:
        pid_var.set(str(res))
    else:
        tkinter.messagebox.showwarning('错误', '未找到 florr 进程！')
        pid_var.set('-1')
    enable_all()

def scan_inv_base():
    if pid_var.get() == '-1':
        tkinter.messagebox.showwarning('错误', '请先找到 florr 进程！')
        return

    disable_all()
    pid = int(pid_var.get())
    inventory = []
    for each in inv_entry_list:
        petal_name = each[0].get()
        nw = [petal_name]
        l = each[1].get().split(',')
        for t in l:
            k = t.strip(' ')
            if k == '':
                continue
            nw.append(int(k))
        inventory.append(nw)
    
    res = florr_edit_core.scan_inventory_base(pid, inventory)
    if res > 0:
        addr_var.set(str(res))
    elif res == -1:
        tkinter.messagebox.showwarning('错误', '花瓣名称错误！')
        addr_var.set('-1')
    elif res == -2:
        tkinter.messagebox.showwarning('错误', '未找到 florr 进程！')
        addr_var.set('-1')
        
    enable_all()

def modify_inv():
    pid = int(pid_var.get())
    base = int(addr_var.get())
    petal_name = petalname_var.get()
    petal_lev = petallev_var.get()
    petal_num = int(petalnum_var.get())
    print(petal_name, petal_lev, petal_num)
    florr_edit_core.modify_inventory(pid, base, petal_name, petal_lev, petal_num)
    pass


def on_bt1_click():
    t = threading.Thread(target=find_process)
    t.setDaemon(True)
    t.start()

def on_bt4_click():
    t = threading.Thread(target=scan_inv_base)
    t.setDaemon(True)
    t.start()

def on_bt5_click():
    t = threading.Thread(target=modify_inv)
    t.setDaemon(True)
    t.start()


def addentry(rt):
    global rw, condi_list
    if rw >= 10:
        return
    
    inv_entry_list.append((tk.StringVar(), tk.StringVar()))

    t = tk.Label(rt, text='%d.'%rw)
    condi_list.append(t)
    t.grid(row=rw, column=0, padx=5, pady=5)
    t = tk.Entry(rt, textvariable=inv_entry_list[rw - 1][0])
    condi_list.append(t)
    t.grid(row=rw, column=1, padx=5)
    t = tk.Entry(rt, textvariable=inv_entry_list[rw - 1][1])
    condi_list.append(t)
    t.grid(row=rw, column=2, padx=5)
    rw += 1

def delentry():
    global rw, condi_list
    if len(condi_list) < 3:
        return
    
    rw -= 1
    condi_list[-1].destroy()
    condi_list[-2].destroy()
    condi_list[-3].destroy()
    condi_list = condi_list[:-3]
    inv_entry_list.pop()


f1 = tk.LabelFrame(root, text='加载')
f1.pack(padx=10, pady=10, side='left')

bt1 = tk.Button(f1, text='寻找 florr 进程', command=on_bt1_click)
bt1.grid(row=0, column=0, padx=5, pady=10, sticky='E')

ent0 = tk.Entry(f1, textvariable=pid_var, state='readonly', width=15)
ent0.grid(row=0, column=1, columnspan=2, padx=5, pady=10, sticky='W')

f11 = tk.LabelFrame(f1, text='条件')
f11.grid(row=3, column=0, columnspan=2)

bt2 = tk.Button(f1, text='添加条件', command=(lambda rt=f11:addentry(rt)))
bt2.grid(row=2, column=0, padx=5, pady=5, sticky='E')

bt3 = tk.Button(f1, text='删除条件', command=(delentry))
bt3.grid(row=2, column=1, padx=5, pady=5, sticky='W')

tk.Label(f11, text='花瓣名称（英文）').grid(row=0, column=1, padx=5)
tk.Label(f11, text='各等级花瓣数量（用逗号分隔）').grid(row=0, column=2, padx=5)

tk.Label(f11, text='1.').grid(row=1, column=0, padx=5, pady=5)
tk.Entry(f11, textvariable=inv_entry_list[0][0]).grid(row=1, column=1, padx=5)
tk.Entry(f11, textvariable=inv_entry_list[0][1]).grid(row=1, column=2, padx=5)

bt4 = tk.Button(f1, text='查找内存地址', command=on_bt4_click)
bt4.grid(row=4, column=0, padx=5, pady=10, sticky='E')

ent1 = tk.Entry(f1, textvariable=addr_var, state='readonly', width=15)
ent1.grid(row=4, column=1, padx=5, pady=10, sticky='W')

f2 = tk.LabelFrame(root, text='修改')
f2.pack(padx=10, pady=10, side='left', anchor='n')


tk.Label(f2, text='花瓣名称（英文）').grid(row=0, column=0, padx=5)
tk.Label(f2, text='花瓣品质').grid(row=0, column=1, padx=5)
tk.Label(f2, text='修改花瓣数量').grid(row=0, column=2, padx=5)
ent2 = tk.Entry(f2, textvariable=petalname_var)
ent2.grid(row=1, column=0, padx=5, pady=5)
opt1 = tk.OptionMenu(f2, petallev_var, *florr_edit_core.petal_levels)
opt1.grid(row=1, column=1, padx=5, pady=5)
ent3 = tk.Entry(f2, textvariable=petalnum_var)
ent3.grid(row=1, column=2, padx=5, pady=5)
bt5 = tk.Button(f2, text='修改', width='10', command=on_bt5_click)
bt5.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

unit_list.append(bt1)
unit_list.append(bt2)
unit_list.append(bt3)
unit_list.append(bt4)

root.mainloop()
