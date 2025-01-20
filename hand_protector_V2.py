from pynput import keyboard
from sys import argv
from time import sleep,time
from Modules.WindowMgr import *
from os import system

VERSION = "250120a"

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
        # if tmp_str in KEY_ONOFF and edit_flag==True:
        #     if tmp_str not in current:
        #         current.add(tmp_str)
        #     else:
        #         current.remove(tmp_str)
        if tmp_str==PAUSE_HOTKEY:
            if loop_flag:
                loop_flag=False
                on_off_key(False)
            else:
                loop_flag=True
                on_off_key(True)
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
        if key == keyboard.Key.delete:
            return False
            #loop_flag=False
    except:
        pass

def press_and_release(arg):
    kb_press_eval_key(arg)
    kb_release_eval_key(arg)


def on_off_key(arg):
    global current,KEY_ONOFF
    if arg==True:
        for i in KEY_ONOFF:
            current.add(i)
    else:
        if len(current)>0:
            for i in KEY_ONOFF:
                current.remove(i)

def switch_ON():
    global current,KEY_ONOFF,onoff_stat
    pass


if __name__=="__main__":
    #讀入INI
    ini_filename="hand_protector_V2.ini"
    if len(argv)>1 and argv[1]!="" and (argv[1]).split(".")[1]=="ini":
        ini_filename=argv[1]
    #讀取 xinput.ini參數
    with open(ini_filename,"r",encoding="utf-8") as f:
        tmp_content=f.read()
    exec(tmp_content)
    loop_flag=AUTO_START_ON
    edit_flag=False
    COMBINATION = {keyboard.Key.alt, keyboard.Key.ctrl,keyboard.Key.enter}
    current = set()
    onoff_stat=AUTO_START_ON
    on_off_key(onoff_stat)

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    
    w=WindowMgr()
    keyon_title='::::HAND-PROTECTOR::::'
    w.set_cmd_title(keyon_title)
    w.reset()
    w.set_window_on_top(keyon_title,350,150)
    w.set_window_alpha(keyon_title, alpha_val=190)

    print(f"版本:v.{VERSION} 監控視窗:{ACTIVE_WIN_TITLE}\n"+"-"*50+f"\n按 [Delete] 結束程式 | 按 [{PAUSE_HOTKEY}] 暫停或重啟\n"+"-"*50)
    last_seconds=int(time())
    tmp = set()
    while 1:
        PRINT_VAR=""
        for i in current:PRINT_VAR=PRINT_VAR+" "+i
        if HEAL_ON and loop_flag: PRINT_VAR+=" 補"
        if FORCE_MOVE and loop_flag: PRINT_VAR+=" 移"
        if 'stop' in(str(listener)): exit()
        print_str=f'啟用狀態:{loop_flag} | ON:{PRINT_VAR}'+" "*10
        print('\r'+print_str,end='',flush=True)
        if ACTIVE_WIN_TITLE=="" or (ACTIVE_WIN_TITLE!="" and ACTIVE_WIN_TITLE in w.active_window_title() and loop_flag):
            current_seconds=int(time())
            if HEAL_ON and current_seconds!=last_seconds:
                press_and_release(KEY_HEAL)
            for i in current:
                if i not in tmp:
                    press_and_release(i)
                    tmp.add(i)
                    break
            if FORCE_MOVE:
                press_and_release(KEY_FORCE_MOVE)
            last_seconds=current_seconds
            edit_flag=True
            if tmp == current:
                for i in current: tmp.remove(i)
        #system("cls")
        sleep(DELAY_SECOND)