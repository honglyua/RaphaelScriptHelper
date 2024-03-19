#!/usr/bin/python
# -*- encoding: utf-8 -*-

import RaphaelScriptHelper as rsh
import PosImageDict as pid
import time
# 需要用管理员打开cmd运行

# 宗派任务：
# 打开活动主页-->点击宗派任务-->接取任务-->执行任务-->提交任务-->完成任务
#                               ↑------------------------------↓
# 任务数共10轮，注意每轮任务过程中，需预留足够时间完成任务
# 完成任务标志：左侧任务栏没有宗派任务索引

# 前往任务点、返回宗派点坐标


def starter():
    goAndBackPos = 0
    print("开启宗派任务...")
    if not goToZongPaiMap():
        return
    print("接取第一次宗派任务...")
    if not getZongPaiTask():
        return
    while not checkIfLastZongPaiTask():
        print("执行单次宗派任务...")
        if goAndBackPos == 0:
            goAndBackPos = executeZongPaiTask()
        else:
            executeZongPaiTask(goAndBackPos)
        if not doZongPaiTask():
            break
        print("回到宗派...")
        goBackZongPai(goAndBackPos)
        print("提交单次宗派任务...")
        submitZongPaiTask()

    if not doZongPaiLastTask(goAndBackPos):
        return
    goBackZongPai(goAndBackPos)
    submitZongPaiTask()
    print("完成所有宗派任务...")

def goToZongPaiMap():
    print("打开活动主页...")
    ret = rsh.find_pic_touch_pc(pid.activity_icon)
    if not ret:
        print("【识图】识别活动失败...")
        return False
    print("点击参加宗派事务...")
    time.sleep(2)
    zpPos = rsh.find_pic_pc(pid.zongpai_icon, True)
    if zpPos is None:
        print("【识图】识别宗派失败...")
        return False
    enterPos = rsh.find_target_pic_pc(pid.zongpai_icon, pid.participate_icon, True)
    if enterPos is None:
        print("【识图】识别参加宗派失败...")
        return False
    zpx, zpy = zpPos
    etx, ety = enterPos
    rsh.touch_pc(zpx+etx/2, zpy)
    time.sleep(20)
    return True

def getZongPaiTask():
    zpPos = rsh.find_pic_pc(pid.zongpai_get_task_icon, True)
    if zpPos is None:
        print("【识图】识别接取任务失败...")
        return False
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(2)
    rsh.touch_pc(zpx, zpy)
    return True

def checkIfLastZongPaiTask():
    leftTopPos = rsh.find_pic_pc(pid.zongpai_last_task_icon)
    if leftTopPos is None:
        print("不是最后一次宗派任务...")
        return False
    else:
        print("是最后一次宗派任务...")
        return True

def executeZongPaiTask(pos = 0):
    if pos == 0:
        zpPos = rsh.find_pic_pc(pid.zongpai_task_icon, True)
        if zpPos is None:
            print("【识图】执行任务失败...")
            return 0
        zpx, zpy = zpPos
        rsh.touch_pc(zpx, zpy)
        time.sleep(20)
        return zpPos
    else:
        zpx, zpy = pos
        rsh.touch_pc(zpx, zpy)
        time.sleep(20)
        return pos

def doZongPaiTask():
    zpPos = rsh.find_pic_pc(pid.use_icon, True)
    if zpPos is None:
        buyTaskPos = checkIfBuyTask()
        if buyTaskPos != 0:
            # 是购买药材任务
            print("执行购买任务...")
            return doBuyTask(buyTaskPos)
        
        buyTaskPos = checkIfBuyFaBaoTask()
        if buyTaskPos != 0:
            # 是购买法宝任务
            print("执行购买法宝任务...")
            return doBuyFaBaoTask(buyTaskPos)
        
        buyTaskPos = checkIfDigTask()
        if buyTaskPos != 0:
            # 是购买挖掘任务
            print("执行挖掘任务...")
            return doDigTask(buyTaskPos)
    else:
        zpx, zpy = zpPos
        rsh.touch_pc(zpx, zpy)
        time.sleep(5)
        return True

def checkIfBuyTask():
    zpPos = rsh.find_pic_pc(pid.buy_icon, True)
    if zpPos is None:
        return 0
    else:
        return zpPos

def doBuyTask(zpPos):
    zpx, zpy = zpPos
    print("点击购买...")
    rsh.touch_pc(zpx, zpy)
    time.sleep(2)
    if not confirmTask():
        return False
    if not closeTask():
        return False
    return True

def confirmTask():
    # 是否需要确认
    zpPos = rsh.find_pic_pc(pid.confirm_icon, True)
    if zpPos is None:
        print("【识图】识别确认按钮失败...")
        return False
    zpx, zpy = zpPos
    print("点击确认...")
    rsh.touch_pc(zpx, zpy)
    time.sleep(2)
    return True

def closeTask():
    zpPos = rsh.find_pic_pc(pid.close_icon, True)
    if zpPos is None:
        print("【识图】识别关闭按钮失败...")
        return False
    zpx, zpy = zpPos
    print("点击关闭...")
    rsh.touch_pc(zpx, zpy)
    time.sleep(2)
    return True

def checkIfBuyFaBaoTask():
    zpPos = rsh.find_pic_pc(pid.fabao_search, True)
    if zpPos is None:
        return 0
    else:
        return zpPos

def doBuyFaBaoTask(zpPos):
    zpx, zpy = zpPos
    print("点击法宝搜索...")
    rsh.touch_pc(zpx, zpy)
    time.sleep(2)
    buyPos = checkIfBuyTask()
    if buyPos != 0:
        return doBuyTask(buyPos)
    else:
        return False

def checkIfDigTask():
    zpPos = rsh.find_pic_pc(pid.zongpai_dig_task_icon, True)
    if zpPos is None:
        return 0
    else:
        return zpPos

def doDigTask(zpPos):
    zpPos = rsh.find_pic_pc(pid.hoeing_icon, True)
    if zpPos is None:
        print("【识图】识别锄地按钮失败...")
        return False
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(4)

def goBackZongPai(zpPos):
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(20)

def submitZongPaiTask():
    zpPos = rsh.find_pic_pc(pid.zongpai_complete_task_icon, True)
    if zpPos is None:
        print("【识图】识别提交按钮失败...")
        return False
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(4)
    print("接取下一任务")
    rsh.touch_pc(zpx, zpy)
    return True

def doZongPaiLastTask(zpPos):
    zpx, zpy = zpPos
    rsh.touch_pc(zpx, zpy)
    time.sleep(20)
    if not doZongPaiTask():
        return False
    time.sleep(2)
    return clickAutoHit()

def clickAutoHit():
    zpPos = rsh.find_pic_pc(pid.auto_hit_icon, True)
    if zpPos is None:
        print("【识图】识别挂机按钮失败...")
        return False
    else:
        zpx, zpy = zpPos
        print("点击挂机...")
        rsh.touch_pc(zpx, zpy)
        time.sleep(90)
        return True

if __name__ == '__main__':
    print("3秒后启动宗派事务...")
    time.sleep(3)
    starter()