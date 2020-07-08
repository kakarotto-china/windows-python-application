# -*- coding: utf-8 -*- #


def reCheckJoy(pygame, autoStart: int):
    '''
    检测手柄是否连接
    :param pygame:
    :param autoStart:
    :return: 连接返回True, 并将全局变量AUTO_START设置为1 未连接返回False
    '''

    global AUTO_START

    pygame.joystick.init()  # 每次都初始化手柄, 并在业务处理完毕后卸载手柄, 才可以达到实时检测的目的
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    if len(joysticks) == 0:
        printRed("手柄已经断开, 请重新连接手柄!!!")
        AUTO_START = autoStart  # 未检测到手柄, 全局变量AUTO_STAR置为1, 返回后, 则在主菜单中开始检测, 连接后继续调用start方法
        pygame.display.quit()
        pygame.joystick.quit()
        return False
    for joystick in joysticks:
        joystick.init()  # 必须初始化来获取输入事件

    return True


def start():
    '''
    启动手柄映射程序
    读取到binding.ini和mapping.ini配置文件, 根据对应关系使用win32模拟按下键盘
    按下键盘与抬起键盘时间间隔为全局变量INTERVAL, 由程序启动时控制台传入, 未设置则为100
    :return:
    '''

    import win32api

    import pygame
    from pygame import time

    pygame.display.init()  # 按需加载模块

    from ctypes import windll
    mapVirtualKey = windll.user32.MapVirtualKeyA

    def keyPress(key_code, sleep=INTERVAL):
        '''
        模拟win32按下键盘
        :param key_code: 16进制键盘码
        :param sleep: 按下与抬起间隔时间
        :return:
        '''
        win32api.keybd_event(key_code, mapVirtualKey(key_code, 0), 0, 0)
        time.wait(sleep)
        win32api.keybd_event(key_code, mapVirtualKey(key_code, 0), 2, 0)

    transBinding = {}
    for k, v in BINDING.items("binding"):
        transBinding[v] = k

    # def move_callself(value):
    #     '''
    #     按下手柄后不松, 则需要持续按下键盘上的键, 需要递归调用
    #     :param value:
    #     :return:
    #     '''
    #     list_event = pygame.event.get(pygame.JOYHATMOTION)
    #     if len(list_event) == 0:
    #         bindValue = "hat-0-" + str(value)
    #         if transBinding.__contains__(bindValue):
    #             opt = transBinding[bindValue]
    #             if MAPPING.has_option("mapping", opt):
    #                 keyCode = MAPPING.get("mapping", opt)
    #                 if "" != keyCode:
    #                     keyPress(VK_CODE[keyCode])
    #                     move_callself(value)
    #                 else:
    #                     printRed("当前操作未设置映射: " + opt)
    #             else:
    #                 printRed("请检查配置文件 [mapping.ini] 没有: " + opt)
    #         else:
    #             printRed("当前键未绑定: " + bindValue)
    #     elif list_event[0].value == (0, 0) or list_event[0].value == value:
    #         return
    #     else:
    #         move_callself(list_event[0].value)

    def move(value):
        global TEMP_NOT_BIND_OR_MAPPING

        bindValue = "hat-0-" + str(value)
        if transBinding.__contains__(bindValue):
            opt = transBinding[bindValue]
            if MAPPING.has_option("mapping", opt):
                keyCode = MAPPING.get("mapping", opt)
                if "" != keyCode:
                    keyPress(VK_CODE[keyCode])
                else:
                    printStr = "当前操作未设置映射: " + opt
                    if TEMP_NOT_BIND_OR_MAPPING != printStr:  # 使用全局变量判断与上次是否相同, 避免连续打印
                        TEMP_NOT_BIND_OR_MAPPING = printStr
                        printRed(TEMP_NOT_BIND_OR_MAPPING)
            else:
                printStr = "请检查配置文件 [mapping.ini] 没有:" + opt
                if TEMP_NOT_BIND_OR_MAPPING != printStr:  # 使用全局变量判断与上次是否相同, 避免连续打印
                    TEMP_NOT_BIND_OR_MAPPING = printStr
                    printRed(TEMP_NOT_BIND_OR_MAPPING)
        else:
            printStr = "当前键未绑定: " + bindValue  # 使用全局变量判断与上次是否相同, 避免连续打印
            if TEMP_NOT_BIND_OR_MAPPING != printStr:
                TEMP_NOT_BIND_OR_MAPPING = printStr
                printRed(TEMP_NOT_BIND_OR_MAPPING)

    def click(button):
        global TEMP_NOT_BIND_OR_MAPPING

        key = "btn-" + str(button)
        if transBinding.__contains__(key):
            opt = transBinding[key]
            if MAPPING.has_option("mapping", opt):
                keyCode = MAPPING.get("mapping", opt)
                if "" != keyCode:
                    keyPress(VK_CODE[keyCode])
                else:
                    printStr = "当前操作未设置映射: " + opt
                    if TEMP_NOT_BIND_OR_MAPPING != printStr:  # 使用全局变量判断与上次是否相同, 避免连续打印
                        TEMP_NOT_BIND_OR_MAPPING = printStr
                        printRed(TEMP_NOT_BIND_OR_MAPPING)
            else:
                printStr = "请检查配置文件 [mapping.ini] 没有:" + opt
                if TEMP_NOT_BIND_OR_MAPPING != printStr:  # 使用全局变量判断与上次是否相同, 避免连续打印
                    TEMP_NOT_BIND_OR_MAPPING = printStr
                    printRed(TEMP_NOT_BIND_OR_MAPPING)
        else:
            printStr = "当前键未绑定: " + key
            if TEMP_NOT_BIND_OR_MAPPING != printStr:  # 使用全局变量判断与上次是否相同, 避免连续打印
                TEMP_NOT_BIND_OR_MAPPING = printStr
                printRed(TEMP_NOT_BIND_OR_MAPPING)

    printGreen("手柄映射开始执行... 按下[ctrl+c]回到主菜单")
    global AUTO_START
    while reCheckJoy(pygame, 1):  # 实时检测手柄连接状态, 自动启动变量则置为1
        pygame.time.Clock().tick(FPS)  # 通过时钟对象指定循环频率 每秒循环60次

        for event in pygame.event.get():  # 监听用户事件
            if event.type == pygame.QUIT:  # 判断用户是否点击了关闭按钮
                print("回到主菜单 [joy-mapping程序] 退出...")
                AUTO_START = -1  # 退出时AUTO_START置为-1, 用来返回到主菜单
                pygame.display.quit()  # 卸载所有pygame模块
                pygame.joystick.quit() # 返回前, 卸载手柄
                return
            if event.type == pygame.JOYBUTTONDOWN:  # event.button => A 0, B 1, X 2, Y 3, LEFT 4, RIGHT 5, SELECT 6, START 7, AXIS_LEFT 8, AXIS_RIGHT 9
                click(event.button)
            if event.type == pygame.JOYHATMOTION:  # event.value 弹起(0, 0) 上(0, 1) 下(0, -1) 左(-1, 0) 右(1, 0)
                if event.value != (0, 0):  # 过滤弹起(0, 0)按键
                    move(event.value)

        pygame.joystick.quit()  # 每次循环都卸载手柄, 用来每次都获取新的手柄状态


def getJoyKey():
    '''
    pygame监测手柄按键为全局, 所以不需要激活窗口
    在控制台按下Ctrl+C会被pygame监测到为QUIT事件, 将变量设置为False退出循环, 代表跳过
    :return: 跳过返回空字符串 按下按键返回对应的键盘按键拼接字符串
    '''

    # 解决卡顿问题，原因是每次都获取手柄，并初始化， 且每次都在卸载

    import pygame

    # 只加载需要的模块
    pygame.display.init()

    global AUTO_START
    while reCheckJoy(pygame, 2):
        pygame.time.Clock().tick(FPS)  # 通过时钟对象指定循环频率 每秒循环60次
        for event in pygame.event.get():  # 监听用户事件
            if event.type == pygame.QUIT:  # 判断用户是否点击了关闭按钮
                AUTO_START = -1  # 退出时AUTO_START置为-1, 用来返回到主菜单
                pygame.display.quit()
                pygame.joystick.quit() # 返回前, 卸载手柄
                return ""
            if event.type == pygame.JOYBUTTONDOWN:  # event.button => A 0, B 1, X 2, Y 3, LEFT 4, RIGHT 5, SELECT 6, START 7, AXIS_LEFT 8, AXIS_RIGHT 9
                print("btn", event.button, sep="-")
                pygame.joystick.quit()
                pygame.display.quit()
                pygame.time.wait(WAIT)
                return "btn-" + str(event.button)
            if event.type == pygame.JOYHATMOTION:  # event.value 弹起(0, 0) 上(0, 1) 下(0, -1) 左(-1, 0) 右(1, 0)
                if event.value == (0, 1):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.joystick.quit()
                    pygame.display.quit()
                    pygame.time.wait(WAIT)
                    return "hat-" + str(event.hat) + "-" + str(event.value)
                if event.value == (0, -1):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.joystick.quit()
                    pygame.display.quit()
                    pygame.time.wait(WAIT)
                    return "hat-" + str(event.hat) + "-" + str(event.value)
                if event.value == (1, 0):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.joystick.quit()
                    pygame.display.quit()
                    pygame.time.wait(WAIT)
                    return "hat-" + str(event.hat) + "-" + str(event.value)
                if event.value == (-1, 0):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.joystick.quit()
                    pygame.display.quit()
                    pygame.time.wait(WAIT)
                    return "hat-" + str(event.hat) + "-" + str(event.value)
        pygame.joystick.quit() # 每次循环都卸载来获得手柄最新状态
    return "DISCONNECT"


def getKeyboard(msg):
    '''
    pygame显示界面并开启主循环进行依次绑定键盘按键
    关闭窗口或在控制台按下Ctrl+C会被pygame监测到为QUIT事件, 将变量设置为False退出循环, 代表跳过
    :param msg: 界面提示语
    :return: 跳过返回空字符串 按下按键返回对应的手柄按键拼接字符串
    '''

    import pygame
    import os
    os.environ["SDL_VIDEO_CENTERED"] = "1"  # 此环境变量可以让pygame窗口在屏幕居中

    pygame.display.init()
    pygame.font.init()

    WIDTH, HEIGHT = 500, 200
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("绑定键盘-活动窗口")
    pygame.display.set_icon(pygame.image.load(PATH_JOY_PNG).convert_alpha())

    font20 = pygame.font.SysFont("SimHei", 20)
    font30 = pygame.font.SysFont("SimHei", 30)

    fontMsg = font20.render(msg, True, (0, 0, 0))
    posMsg = ((WIDTH - fontMsg.get_width()) / 2, HEIGHT / 10)

    doWhile = True
    keyStr = " "
    while doWhile:
        pygame.time.Clock().tick(FPS)  # 通过时钟对象指定循环频率 每秒循环60次
        screen.fill((255, 255, 255))
        for event in pygame.event.get():  # 监听用户事件
            if event.type == pygame.QUIT:  # 判断用户是否点击了关闭按钮
                doWhile = False
            if event.type == pygame.KEYDOWN:
                keyStr = VK_CODE_PYGAME[str(event.key)]
                print(keyStr, event.key)

                fontKeyStr = font30.render(keyStr, True, (0, 0, 0))
                posKeyStr = ((WIDTH - fontKeyStr.get_width()) / 2, HEIGHT / 2)
                screen.blit(fontMsg, posMsg)
                screen.blit(fontKeyStr, posKeyStr)
                pygame.display.update()
                pygame.time.wait(WAIT)
                doWhile = False

        screen.blit(fontMsg, posMsg)
        fontKeyStr = font30.render(keyStr, True, (0, 0, 0))
        posKeyStr = ((WIDTH - fontKeyStr.get_width()) / 2, HEIGHT / 2)
        screen.blit(fontKeyStr, posKeyStr)
        pygame.display.update()

    pygame.display.quit()
    pygame.font.quit()
    return keyStr


def doBind():
    '''
    手柄码绑定
    pygame对手柄按键的检测为全局
    :return:
    '''

    printYellow("格式: hat-hat的id-按键元组 或者 btn-按钮id 建议使用菜单 [4] 查看按键码后, 直接编辑 [binding.ini] 配置文件")
    for k, v in BINDING.items("binding"):
        print("按下手柄, 绑定到 [" + k + "] 操作 (按[Ctrl+C]跳过)")
        joyKey = getJoyKey()
        if "" == joyKey:
            continue
        elif "DISCONNECT" == joyKey:
            return # 返回到主菜单 以重新执行检测方法
        else:
            BINDING.set("binding", k, joyKey)

    # 设置完, 保存到配置文件
    with open(PATH_BINDING, "w") as fp:
        BINDING.write(fp)


def doMap():
    '''
    键盘映射
    pygame对键盘按键的检测必须在活动窗口内, 所以这里通过显示一个pygame窗口来进行设置
    :return:
    '''

    print("支持的按键命名: ", )
    for k, v in VK_CODE_PYGAME.items():
        print("[" + k + "->" + v + "]", end=" ")
    print()
    printYellow("建议直接编辑 [mapping.ini] 配置文件")
    for k, v in MAPPING.items("mapping"):
        print("在新打开的活动窗口按下键盘, 映射到 [" + k + "] 操作 (按[Ctrl+C]/关闭窗口跳过当前)")
        keyboard = getKeyboard("按下键盘绑定到 [" + k + "]")
        if "" == keyboard:
            continue
        else:
            MAPPING.set("mapping", k, keyboard)
    # 设置完, 保存到配置文件
    with open(PATH_MAPPING, "w") as fp:
        MAPPING.write(fp)


def showConfig():
    '''
    显示当前未见mapping.ini和binding.ini配置关系
    :return:
    '''

    try:
        printGreen("当前绑定与映射关系: 操作 -> [手柄码] => [键名]")
        for k, v in BINDING.items("binding"):
            print(k + " -> [" + v + "]" + " => [" + MAPPING.get("mapping", k) + "]")
    except:
        printRed("配置文件 [binding.ini] 与 [mapping.ini] 的操作键不一致, 请检查!!!")
        print("配置文件 [binding.ini] :", end=" ")
        for k, v in BINDING.items("binding"):
            print(k, end=" ")
        print()
        print("配置文件 [mapping.ini] :", end=" ")
        for k, v in MAPPING.items("mapping"):
            print(k, end=" ")
        print()


def joyCode():
    '''
    循环测试手柄码, 在控制台按下Ctrl+C会被pygame监测到为QUIT事件, 将变量置为False退出循环
    :return:
    '''

    import pygame

    printYellow("*** 按下手柄按键, 显示对应的手柄码, 可手动修改 [binding.ini] 配置文件, 例: UP = btn-1 (按下组合键[Ctrl+C]回到主菜单) ***")

    pygame.display.init()

    global AUTO_START
    while reCheckJoy(pygame, 3): # 循环检测手柄连接, 重启变量置为3
        pygame.time.Clock().tick(FPS)  # 通过时钟对象指定循环频率 每秒循环60次
        for event in pygame.event.get():  # 监听用户事件
            if event.type == pygame.QUIT:  # 判断用户是否点击了关闭按钮, Ctrl+C 退出后卸载模块
                print("回到主菜单 [按键检测] 退出...")
                AUTO_START = -1  # 退出时AUTO_START置为-1, 用来返回到主菜单
                pygame.display.quit()
                pygame.joystick.quit()
                return
            if event.type == pygame.JOYAXISMOTION:  # joy 0 type ... hat/axis/button
                # event.axis    LEFT_左右 0, LEFT_上下 1, 扳机键左右 2, RIGHT_上下 3,  RIGHT_左右 4
                # event.value   左-1 右1     上-1 下1      左1 右-1       上-1 下1          左-1 右1
                print("摇杆", event.axis, "值", event.value)
                pygame.time.wait(WAIT)
            if event.type == pygame.JOYBALLMOTION:  # 追踪球, 没有设备无法测试
                print(event)
                pygame.time.wait(WAIT)
            if event.type == pygame.JOYBUTTONDOWN:  # event.button => A 0, B 1, X 2, Y 3, LEFT 4, RIGHT 5, SELECT 6, START 7, AXIS_LEFT 8, AXIS_RIGHT 9
                print("btn", event.button, sep="-")
                pygame.time.wait(WAIT)
            # if event.type == pygame.JOYBUTTONUP: # 不做按键抬起检测
            #     pass
            if event.type == pygame.JOYHATMOTION:  # event.value 弹起(0, 0) 上(0, 1) 下(0, -1) 左(-1, 0) 右(1, 0)
                if event.value == (0, 0):
                    continue
                if event.value == (0, 1):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.time.wait(WAIT)
                if event.value == (0, -1):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.time.wait(WAIT)
                if event.value == (1, 0):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.time.wait(WAIT)
                if event.value == (-1, 0):
                    print("hat", event.hat, event.value, sep="-")
                    pygame.time.wait(WAIT)
        pygame.joystick.quit() # 每次循环都卸载来获得手柄最新状态

def cleanAll():
    '''
    分别清空binding.ini和mapping.inimapping.ini配置文件的值
    :return:
    '''
    for k, v in BINDING.items("binding"):
        BINDING.set("binding", k, "")
    # 设置完, 保存到配置文件
    with open(PATH_BINDING, "w") as fp:
        BINDING.write(fp)
        print("配置文件 [binding.ini] 值已清空")
    for k, v in MAPPING.items("mapping"):
        MAPPING.set("mapping", k, "")
    # 设置完, 保存到配置文件
    with open(PATH_MAPPING, "w") as fp:
        MAPPING.write(fp)
        print("配置文件 [mapping.ini] 值已清空")


def main_menu():
    '''
    主循环菜单
    :return:
    '''

    from sys import exit

    while True:
        if 1 == AUTO_START:  # 启动菜单0后手柄断开则会将AUTO_START设置为1
            test_joy_connect()  # 检测手柄连接
            start()

        if 2 == AUTO_START:  # 启动菜单1后手柄断开则会将AUTO_START设置为2
            test_joy_connect()  # 检测手柄连接
            print("已经重新连接, 需要从头开始设置...")
            doBind()

        if 3 == AUTO_START:
            test_joy_connect()  # 检测手柄连接
            joyCode()

        while 0 == AUTO_START or -1 == AUTO_START:
            print()
            print("★ " * 15)
            print("★ " + "\t" * 4 + "\t  ★ ")
            print("★ " + "\t" + "      请输入菜单项  " + "\t" + "\t  ★ ")
            print("★ " + "\t" * 4 + "\t  ★ ")
            print("★\t* [0]\t启动\t\t\t  ★ ")
            print("★\t* [1]\t绑定手柄码\t\t  ★ ")
            print("★\t* [2]\t映射按键设置\t\t  ★ ")
            print("★\t* [3]\t显示当前设置\t\t  ★ ")
            print("★\t* [4]\t手柄按键测试\t\t  ★ ")
            print("★\t* [C]\t清空所有配置文件\t  ★ ")
            print("★\t* [5/Q]\t退出\t\t\t  ★ ")
            print("★ " + "\t" * 4 + "\t  ★ ")
            print("★ " * 15)
            print()
            select = input(">>>")
            print("进入菜单项 [" + select + "]")
            print()
            if select == "0":
                start()  # 启动
            elif select == "1":
                doBind()  # 进行绑定设置
            elif select == "2":
                doMap()  # 手柄映射到键盘
            elif select == "3":
                showConfig()  # 显示当前配置
            elif select == "4":
                joyCode()  # 测试手柄按键码
            elif select == "C":
                cleanAll()  # 清空所有配置文件值
            elif select == "5" or select == "Q":
                print("[joy-mapping程序] 退出...")
                exit()  # 退出
            else:
                printRed("错误, 请输入正确的菜单序号...")


def test_joy_connect():
    '''
    循环检测手柄连接
    :return:
    '''

    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"  # 隐藏欢迎语打印: 查看源码发现欢迎语是否打印,与环境变量有关, 存在此环境变量则不打印
    import pygame

    testting = ""
    while True:  # 循环检测
        pygame.joystick.init()  # 单独初始化手柄
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]  # 检测手柄放到数组中

        if len(joysticks) == 0:
            if len(testting) >= 6:
                testting = ""
            testting += " ."
            printRed("\r请连接手柄" + testting, end="")
        else:
            print("\r", end="")
            for joystick in joysticks:
                printGreen(str(joystick.get_name()))
                print("手柄已连接", "设备id:", str(joystick.get_id()))
            break  # 检测到则退出循环
        pygame.joystick.quit()
        pygame.time.wait(500)  # 检测间隔500ms


def init():
    '''
    定义一些全局变量
        VK_CODE: 键盘码表
        VK_CODE_PYGAME: pygame里键盘码表
        MAPPING: 配置文件mapping.ini内容
        BINDING: 配置文件binding.ini内容
        PATH_MAPPING: 配置文件mapping.ini路径
        PATH_BINDING: 配置文件binding.ini路径
        PATH_JOY_PNG: pygame窗口图标路径
        INTERVAL: 控制台参数, 模拟按下键盘的时间间隔默认设置为100,
        WAIT: pygame手柄与键盘事件识别到对应按键处理时的等待事件间隔, 默认为300
        FPS: pygame程序事件循环每秒的执行频率
        AUTO_START: 自动启动, 初始值为0
                    在启动菜单0后, 手柄断开则会将值置为1, 再次连接手柄后, 则会自动启动, 退出菜单0后则会置为-1, 继续显示主菜单页面
                    在启动菜单1后，手柄断开则会将值置为2, 再次连接手柄后, 则会自动启动, 退出菜单0后则会置为-1, 继续显示主菜单页面
        TEMP_NOT_BIND_OR_MAPPING: 用于提示是否绑定或映射的全局临时变量
    :return:
    '''

    import os
    import configparser

    global VK_CODE, VK_CODE_PYGAME, MAPPING, BINDING, PATH_MAPPING, PATH_BINDING, PATH_JOY_PNG, INTERVAL, WAIT, FPS, AUTO_START, TEMP_NOT_BIND_OR_MAPPING

    # 重写 防止读取配置文件自动将key转小写
    def optionxform(self, optionstr):
        return optionstr

    configparser.ConfigParser.optionxform = optionxform

    # 用os模块来读取
    curpath = os.path.dirname(os.path.realpath(__file__))
    PATH_BINDING = os.path.join(curpath, "binding.ini")  # 读取到本机的配置文件binding.ini
    PATH_MAPPING = os.path.join(curpath, "mapping.ini")  # 读取到本机的配置文件mapping.ini
    PATH_JOY_PNG = os.path.join(curpath, "joy.png")  # pygame窗口图标路径

    # 调用读取配置模块中的类
    BINDING = configparser.ConfigParser(allow_no_value=True)
    BINDING.read(PATH_BINDING, 'utf-8')
    MAPPING = configparser.ConfigParser(allow_no_value=True)
    MAPPING.read(PATH_MAPPING, 'utf-8')

    # 获取控制台参数
    from sys import argv
    if "-interval" in argv or "-i" in argv:
        try:
            for i, v in enumerate(argv):
                if v == "-interval" or v == "-i":
                    INTERVAL = int(argv[i + 1])
                    break
        except:
            INTERVAL = 100
    else:
        INTERVAL = 100
    if "-wait" in argv or "-w" in argv:
        try:
            for i, v in enumerate(argv):
                if v == "-wait" or v == "-w":
                    WAIT = int(argv[i + 1])
                    break
        except:
            WAIT = 300
    else:
        WAIT = 300
    if "-fps" in argv or "-f" in argv:
        try:
            for i, v in enumerate(argv):
                if v == "-fps" or v == "-f":
                    FPS = int(argv[i + 1])
                    break
        except:
            FPS = 60
    else:
        FPS = 60

    AUTO_START = 0
    TEMP_NOT_BIND_OR_MAPPING = ""

    # pygame按键码
    VK_CODE_PYGAME = {"8": "backspace", "9": "tab", "13": "enter", "304": "shift", "306": "ctrl", "308": "alt",
                      "301": "caps_lock", "27": "esc", "32": "spacebar", "280": "page_up", "281": "page_down",
                      "279": "end", "278": "home", "276": "left_arrow", "273": "up_arrow", "275": "right_arrow",
                      "274": "down_arrow", "316": "print_screen", "277": "ins", "127": "del", "48": "0", "49": "1",
                      "50": "2", "51": "3", "52": "4", "53": "5", "54": "6", "55": "7", "56": "8", "57": "9", "97": "A",
                      "98": "B", "99": "C", "100": "D", "101": "E", "102": "F", "103": "G", "104": "H", "105": "I",
                      "106": "J", "107": "K", "108": "L", "109": "M", "110": "N", "111": "O", "112": "P", "113": "Q",
                      "114": "R", "115": "S", "116": "T", "117": "U", "118": "V", "119": "W", "120": "X", "121": "Y",
                      "122": "Z", "256": "num0", "257": "num1", "258": "num2", "259": "num3", "260": "num4",
                      "261": "num5", "262": "num6", "263": "num7", "264": "num8", "265": "num9", "268": "multiply_key",
                      "270": "add_key", "267": "separator_key", "269": "subtract_key", "266": "decimal_key",
                      "271": "divide_key", "282": "F1", "283": "F2", "284": "F3", "285": "F4", "286": "F5", "287": "F6",
                      "288": "F7", "289": "F8", "290": "F9", "291": "F10", "292": "F11", "293": "F12",
                      "300": "num_lock", "302": "scroll_lock", "303": "right_shift ", "305": "right_control",
                      "307": "right_menu", "61": "+", "44": ",", "45": "-", "46": ".", "47": "/", "59": ";", "91": "[",
                      "92": "\\", "93": "]", "39": "'", "96": "`"}
    # windows按键码
    VK_CODE = {'backspace': 0x08, 'tab': 0x09, 'clear': 0x0C, 'enter': 0x0D, 'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
               'pause': 0x13, 'caps_lock': 0x14, 'esc': 0x1B, 'spacebar': 0x20, 'page_up': 0x21, 'page_down': 0x22,
               'end': 0x23, 'home': 0x24, 'left_arrow': 0x25, 'up_arrow': 0x26, 'right_arrow': 0x27, 'down_arrow': 0x28,
               'select': 0x29, 'print': 0x2A, 'execute': 0x2B, 'print_screen': 0x2C, 'ins': 0x2D, 'del': 0x2E,
               'help': 0x2F, '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37,
               '8': 0x38, '9': 0x39, 'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46, 'G': 0x47,
               'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F, 'P': 0x50,
               'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54, 'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
               'Z': 0x5A, 'num0': 0x60, 'num1': 0x61, 'num2': 0x62, 'num3': 0x63, 'num4': 0x64, 'num5': 0x65,
               'num6': 0x66, 'num7': 0x67, 'num8': 0x68, 'num9': 0x69, 'multiply_key': 0x6A, 'add_key': 0x6B,
               'separator_key': 0x6C, 'subtract_key': 0x6D, 'decimal_key': 0x6E, 'divide_key': 0x6F, 'F1': 0x70,
               'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78,
               'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B, 'F13': 0x7C, 'F14': 0x7D, 'F15': 0x7E, 'F16': 0x7F, 'F17': 0x80,
               'F18': 0x81, 'F19': 0x82, 'F20': 0x83, 'F21': 0x84, 'F22': 0x85, 'F23': 0x86, 'F24': 0x87,
               'num_lock': 0x90, 'scroll_lock': 0x91, 'left_shift': 0xA0, 'right_shift': 0xA1, 'left_control': 0xA2,
               'right_control': 0xA3, 'left_menu': 0xA4, 'right_menu': 0xA5, 'browser_back': 0xA6,
               'browser_forward': 0xA7, 'browser_refresh': 0xA8, 'browser_stop': 0xA9, 'browser_search': 0xAA,
               'browser_favorites': 0xAB, 'browser_start_and_home': 0xAC, 'volume_mute': 0xAD, 'volume_Down': 0xAE,
               'volume_up': 0xAF, 'next_track': 0xB0, 'previous_track': 0xB1, 'stop_media': 0xB2,
               'play/pause_media': 0xB3, 'start_mail': 0xB4, 'select_media': 0xB5, 'start_application_1': 0xB6,
               'start_application_2': 0xB7, 'attn_key': 0xF6, 'crsel_key': 0xF7, 'exsel_key': 0xF8, 'play_key': 0xFA,
               'zoom_key': 0xFB, 'clear_key': 0xFE, '+': 0xBB, ',': 0xBC, '-': 0xBD, '.': 0xBE, '/': 0xBF, ';': 0xBA,
               '[': 0xDB, '\\': 0xDC, ']': 0xDD, "'": 0xDE, '`': 0xC0}


def init_console():
    '''
    定义一些控制台打印颜色字体的方法, 声明为全局
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        参数handle: 指定控制台为输入流/输出流/错误流
        参数color: 16进制数, 多个颜色用 | 连接
    :return:
    '''

    import ctypes, sys

    global printGreen, printRed, printYellow, printBlue, printYwlloRed, printYellowBG, printGreenBG, printRedBG, printBlueBG

    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    # 字体颜色定义 text colors
    FOREGROUND_BLUE = 0x09  # blue.
    FOREGROUND_GREEN = 0x0a  # green.
    FOREGROUND_RED = 0x0c  # red.
    FOREGROUND_YELLOW = 0x0e  # yellow.
    FOREGROUND_INTENSITY = 0x08  # text color is intensified.
    # 背景颜色定义 background colors
    BACKGROUND_YELLOW = 0xe0  # background color yellow.
    BACKGROUND_BLUE = 0x10  # background color contains blue.
    BACKGROUND_GREEN = 0x20  # background color contains green.
    BACKGROUND_RED = 0x40  # background color contains red.
    BACKGROUND_INTENSITY = 0x80  # background color is intensified.

    # get handle
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool

    # reset white
    def resetColor():
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    # green
    def printGreen(mess, end="\n"):
        set_cmd_text_color(FOREGROUND_GREEN)
        sys.stdout.write(mess + end)
        resetColor()

    # red
    def printRed(mess, end="\n"):
        set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(mess + end)
        resetColor()

    # blue
    def printBlue(mess, end="\n"):
        set_cmd_text_color(FOREGROUND_BLUE)
        sys.stdout.write(mess + end)
        resetColor()

    # yellow
    def printYellow(mess, end="\n"):
        set_cmd_text_color(FOREGROUND_YELLOW)
        sys.stdout.write(mess + end)
        resetColor()

    # white bkground and black text
    def printYellowRed(mess, end="\n"):
        set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
        sys.stdout.write(mess + end)
        resetColor()

    # def printYellowBG(mess, end="\n"):
    #     set_cmd_text_color(BACKGROUND_YELLOW)
    #     sys.stdout.write(mess + end)
    #     resetColor()
    # def printRedBG(mess, end="\n"):
    #     set_cmd_text_color(BACKGROUND_RED)
    #     sys.stdout.write(mess + end)
    #     resetColor()
    #
    # def printGreenBG(mess, end="\n"):
    #     set_cmd_text_color(BACKGROUND_GREEN)
    #     sys.stdout.write(mess + end)
    #     resetColor()
    #
    # def printBlueBG(mess, end="\n"):
    #     set_cmd_text_color(BACKGROUND_BLUE)
    #     sys.stdout.write(mess + end)
    #     resetColor()


def main():
    init() # 初始化一些全局变量
    init_console() # 初始化一些控制台打印颜色字体的方法
    test_joy_connect()  # 检测手柄连接
    main_menu() # 主菜单


if __name__ == "__main__":
    main()
