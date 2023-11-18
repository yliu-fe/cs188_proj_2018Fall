# Notes for Project 2 "Multi-agent"

## Question 1: Reflex Agent

### 要求

这一部分要求完成`ReflexAgent`类。目标是彻底解决下面这种吃豆人游戏：

```shell
python pacman.py -p ReflexAgent -l testClassic
```

### 内容

这一个类中包含了2个方法：

1. getAction，即在当前游戏状态下，在评估函数选出的最优合法决策中随机选取一种作为本期的操作，可改可不改。
2. valuationFunction。每种动作的评估函数，输入当前状态和一种动作，返回动作的价值。==修改项==

思路：构造两部分得分：（1）最近食物距离；（2）最近幽灵距离；前者越大则分数越低，后者越大则分数越高

在基本分数的基础上，减去最近幽灵距离的倒数，再减去最近食物距离的倍数。两个距离中的系数可以根据情况自行调试设置。


### 额外问题：关于如何展示`multiAgents.py`中各个类型中出现变量的数据结构
print不好使，还得是debug。

断点打在`multiagent.py`中想看的地方，如果使用pycharm，在debug的设置中输入如下内容：

- script: 设置为`pacman.py`
- script parameters: 设置包括：
  - `-p ReflexAgent`（如果调试的class是`ReflexAgent`的话，其他情况也可以改）
  - `-l testClassic`（如果调试的layout是`testClassic`的话，其他情况也可以改）
  - `-t` 这一项设置代表运行中不会出现pacman的图形界面，因为debug过程中图形界面的出现直接把python编译器干崩了。
  - 以上合在一起，填进去：`-p ReflexAgent -l testClassic -t`.
- Working directory：设置为项目的根目录，例如我的是`~/cs188_proj_2018Fall/proj2-multiagent-python3`，否则会出现pacman识别不了地图文件的情况。
这种情况下会报出`Exception: The layout xxxxxx cannot be found`的错误，参见`pacman.py`Line 570。

在VS code中，将debug设置文件`launch.json`改为：

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Python: Pacman Data Structure",
            "type": "python",
            "request": "launch",
            "program": "pacman.py",
            "console": "integratedTerminal",
            "args": ["-p","ReflexAgent", "-l","testClassic", "-t",],
            "justMyCode": true
        }
    ]
```
此时需要手动设置vscode打开的文件夹为`proj2-multiagent-python3`。
——————

如果进入了debug模式且没有报任何的Extension，就可以步进（Step Over）来查看各个变量的数据结构了。在Pycharm的Debug底边栏中的“Threads & Variables”标签。

- 课程代码中的`newFood`实际上是一个`Grid`类型的数据结构，`newFood[x][y]`是一个布尔值，代表坐标为`(x,y)`的位置是否有食物。并利用`grid`类下
的`asList()`方法，将这组布尔值列表转化为所有值为True的坐标的列表。

- `newGhostStates`是GhostState的列表，其中每个GhostState列表有两个元素：当前位置和动作。

- `newPos`是一个二维元胞，即pacman的位置。

- `newScaredTimes`是一个列表，表示每个幽灵因pacman吃了能量豆而变害怕的剩余时间。

## Question 2: Minimax Agent
实现基于Minimax搜索方法的agent。