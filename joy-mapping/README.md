# 配置参数说明
## 启动参数
```text

主程序 [-interval] [interval_value] [-wait] [wait_value] [-fps] [fps_value]

参数interval, 会直接影响启动映射后的按键体验, 不能为负数, 建议0~300之间
    1. -interval 或者 -i 后面接数字
    2. 来设置模拟键盘按下的时间间隔
    3. 默认不设置时为100, 例如:

                            主程序 -interval 300

参数wait, 会影响配置时的按键反馈, 不能为负数, 建议0~500之间
    1. -wait 或者 -w 后面接数字
    2. 来设置在进行配置时,手柄或键盘按下后进行下一项设置的等待事件
    3. 默认不设置为300, 例如:

                            主程序 -wait 500

参数fps, , 一般可不用设置, 不能为负数, 建议60~120之间
    1. -fps 或者 -f 后面接数字
    2. 使得程序在按键处理时的整体执行频率, 可用作以上两个参数的辅助设置
    3. 默认不设置为60, 例如:
                            主程序 -fps 120
```

## 绑定手柄码
> binding.ini
## 将手柄按键映射到键盘
> mapping.ini

## 基本操作指令
### 方向
```text
UP
DOWN
LEFT
RIGHT
```

### 按键
```text
A
B
X
Y
```

### 选择与开始
```text
SELECT
START
```

### 左右按键
```text
LEFT-BUTTON
RIGHT-BUTTON
```

### 左右扳机键
```text
LEFT-TRIGGER
RIGHT-TRIGGER
```

### 左摇杆
```text
LEFT-POINT-UP
LEFT-POINT-DOWN
LEFT-POINT-LEFT
LEFT-POINT-RIGHT
LEFT-POINT-CENTER
```

### 右摇杆
```text
RIGHT-POINT-UP
RIGHT-POINT-DOWN
RIGHT-POINT-LEFT
RIGHT-POINT-RIGHT
RIGHT-POINT-CENTER
```

### Home键
```text
HOME
```

