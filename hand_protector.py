from pynput import keyboard
from sys import argv
from time import sleep,time
from Modules.WindowMgr import *
from os import system

#讀入INI
ini_filename="hand_protector.ini"
if len(argv)>1 and argv[1]!="" and (argv[1]).split(".")[1]=="ini":
    ini_filename=argv[1]
#讀取 xinput.ini參數
with open(ini_filename,"r",encoding="utf-8") as f:
    tmp_content=f.read()
exec(tmp_content)
loop_flag=True
edit_flag=False
COMBINATION = {keyboard.Key.alt, keyboard.Key.ctrl,keyboard.Key.enter}
current = set()

def kb_press_eval_key(key_val):
    global edit_flag
    edit_flag=False
    kb = keyboard.Controller()
    if key_val!="": #不是空白才繼續動作
        if key_val not in ["LM","RM"]:
            if len(key_val)==1:
                kb.press(key_val)
            else:
                kb.press(eval("Key."+key_val))

def kb_release_eval_key(key_val):
    global edit_flag
    edit_flag=False
    kb = keyboard.Controller()
    if key_val!="": #不是空白才繼續動作
        if key_val not in ["LM","RM"]:
            if len(key_val)==1:
                kb.release(key_val)
            else:
                kb.release(eval("Key."+key_val))


def on_press(key):
    try:
        global edit_flag,current,loop_flag
        #print("{0} pressed".format(key))
        tmp_str=str(key.char)
        if tmp_str in KEY_ONOFF and edit_flag==True:
            if tmp_str not in current:
                current.add(tmp_str)
            else:
                current.remove(tmp_str)
        elif tmp_str==PAUSE_HOTKEY:
            if loop_flag:
                loop_flag=False
            else:
                loop_flag=True
            #print('PAUSE_SWITCH')
    except:
        pass
"""
    except AttributeError:
        if key in COMBINATION:
            current.add(key)
            if all(k in current for k in COMBINATION):
                print('All modifiers active!')
        #print('special key {0} pressed'.format(
        #    key))
"""

def on_release(key):
    try:
        global loop_flag
        #print('{0} released'.format(key))
        if key == keyboard.Key.backspace:
            return False
            #loop_flag=False
    except:
        pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

w=WindowMgr()
keyon_title='::::KEYON::::'
w.set_cmd_title(keyon_title)
w.reset()
w.set_window_on_top(keyon_title,350,150)
w.set_window_alpha(keyon_title, alpha_val=200)
#print(keyon_title)
if ADD_ALL_KEY_ONOFF_ON_START:
    for i in KEY_ONOFF: current.add(i)
print("KEY_ON 監控視窗:"+ACTIVE_WIN_TITLE+"\n按 [Backspace] 結束程式 | 按 [\\] 暫停或重啟\n"+"-"*50)
last_seconds=int(time())
while 1:
    if 'stop' in(str(listener)): exit()
    print_str=f'啟用狀態:{loop_flag} | ON:'+str([i for i in current])+" "*10
    print('\r'+print_str,end='',flush=True)
    if ACTIVE_WIN_TITLE=="" or (ACTIVE_WIN_TITLE!="" and ACTIVE_WIN_TITLE in w.active_window_title() and loop_flag):
        current_seconds=int(time())
        for i in current:
            if i=='q' and current_seconds==last_seconds: continue
            kb_press_eval_key(i)
            kb_release_eval_key(i)
        last_seconds=current_seconds
        edit_flag=True
    sleep(DELAY_SECOND)
    #system("cls")