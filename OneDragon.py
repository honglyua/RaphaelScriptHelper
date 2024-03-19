#!/usr/bin/python
# -*- encoding: utf-8 -*-

import RaphaelScriptHelper as rsh
import PosImageDict as pid
import time

# 一条龙主线任务：
# 1. 5人组队，由队长去【金陵】【龙三太子】接取任务
# 2. 接取后，点击左侧任务栏前往，各队友拉跟随，进去后，队长点右侧挂机
# 3. 5次任务结束后，重新回到【金陵】【龙三太子】接取任务，或者根据系统弹出对话框，点确定前往。
# 4. 总共30次任务，5次一轮，共6轮

def starter():
    task_count = 0
    while task_count < 4:
        print("开启一条龙任务...")
        ret = goToJinLingMap()
        if not ret:
            break
        ret = getDragonTask()
        if not ret:
            break
        time.sleep(2)
        ret = executeDragonTask()
        if not ret:
            break
        ret = enterDragonTask()
        if not ret:
            break
        # 估计10分钟后，每隔3分钟检测一次是否完成当前轮任务
        # 打完一轮后，会有弹框，弹框会存在5分钟
        time.sleep(13 * 60)
        checkFinish = 0
        while checkFinish < 3:
            # 判断是否有弹窗提示完成5次任务，继续接取一条龙任务
            ret = checkIfNeedConfirm()
            if not ret:
                checkFinish += 1
                time.sleep(3 * 60)
            else:
                break
        task_count += 1

def goToJinLingMap():
    print("打开活动主页...")
    # 打开之前确认是否已经完成一轮任务
    ret = checkIfAlreadyOpenGetTask()
    if ret:
        # 不需要打开活动页进行接取任务
        print("接取新一轮任务...")
        return True
    ret = rsh.find_pic_touch_pc(pid.activity_icon)
    if not ret:
        print("【识图】识别活动失败...")
        return False
    print("点击参加一条龙...")
    time.sleep(1)
    zpPos = rsh.find_pic_pc(pid.dragon_icon, True)
    if not zpPos:
        print("【识图】识别一条龙失败...")
        return False
    enterPos = rsh.find_target_pic_pc(pid.dragon_icon, pid.participate_icon, True)
    if not zpPos:
        print("【识图】识别参加一条龙失败...")
        return False
    zpx, zpy = zpPos
    etx, ety = enterPos
    rsh.touch_pc(zpx+etx/2, zpy)
    print("前往接取一条龙任务...")
    time.sleep(30)
    return True

def getDragonTask():
    zpPos = rsh.find_pic_pc(pid.dragon_get_task_icon, True)
    if not zpPos:
        print("【识图】识别接取一条龙任务失败...")
        return False
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(2)
    rsh.touch_pc(zpx, zpy)
    return True

def executeDragonTask(pos = 0):
    if pos == 0:
        zpPos = rsh.find_pic_pc(pid.dragon_task_icon, True)
        if not zpPos:
            print("【识图】识别执行一条龙失败...")
            return False
        zpx, zpy = zpPos
        rsh.touch_pc(zpx, zpy)
        time.sleep(30)
        return zpPos
    else:
        zpx, zpy = pos
        rsh.touch_pc(zpx, zpy)
        time.sleep(30)
        return pos

def enterDragonTask():
    zpPos = rsh.find_pic_pc(pid.dragon_enter_icon, True)
    if not zpPos:
        print("【识图】识别进入一条龙失败...")
        return False
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(3)
    return touchAutoHit()

def touchAutoHit():
    print("开启挂机...")
    zpPos = rsh.find_pic_pc(pid.auto_hit_icon, True)
    if not zpPos:
        print("【识图】识别挂机失败...")
        return False
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    return True

def checkIfNeedConfirm():
    zpPos = rsh.find_pic_pc(pid.sure_icon, True)
    if not zpPos:
        print("【识图】未发现确定完成按钮...")
        return False
    print("【识图】发现确定完成按钮，前往接取新一轮任务...")
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(15)
    return True

def checkIfAlreadyOpenGetTask():
    zpPos = rsh.find_pic_pc(pid.dragon_get_task_icon, True)
    print(zpPos)
    if not zpPos:
        print("【识图】不是新一轮任务...")
        return False
    return True

def checkAndClosePopWindow():
    i = 0
    while i < 2:
        zpPos = rsh.find_pic_pc(pid.close_icon_1, True)
        if zpPos:
            print("【识图】发现关闭按钮...")
            zpx, zpy = zpPos
            rsh.touch_pc(zpx, zpy)
            time.sleep(2)
        zpPos = rsh.find_pic_pc(pid.close_icon_2, True)
        if zpPos:
            print("【识图】发现关闭按钮...")
            zpx, zpy = zpPos
            rsh.touch_pc(zpx, zpy)
            time.sleep(2)
        i += 1
    
if __name__ == '__main__':
    print("1.5h后启动一条龙...")
    # 每日转点后，会有多个领取福利弹窗，需要手动关闭，不然找不到活动入口
    checkAndClosePopWindow()
    # time.sleep(60 * 60 * 1.5)
    starter()