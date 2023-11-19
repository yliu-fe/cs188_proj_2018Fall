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

参照note 3进行，注意我们并不清楚一共有几个agent，但我们能知道的是agent 0必然是pacman，而剩余的agent 1+ 都是幽灵。

### 筛选动作`getAction()`

底层的逻辑是不动的，遍历所有的合法action，对每个action所带来的新状态进行评分，并选取其中评分最高者作为本期的动作。

唯一要注意的是，此处调用`value()`时要明确`agentIndex = 1`。因为这里评估各个action的评分相当于minimax中pacman agent已经做出了选择。

### 状态评分`value()`

这一部分是minimax的根节点。

```python
def value(self, gameState, depth=0, agentIndex=0):
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
        return self.evaluationFunction(gameState)

    if agentIndex == 0:
        return self.max_value(gameState, depth)
    else:
        return self.min_value(gameState, depth, agentIndex)
```

这一部分会和`max_value`, `min_value`函数互相嵌套。引入的三个参数分别是`gameState`（当前状态）、`depth`（当前深度）、`agentIndex`（当前agent的编号）。

首先，如果当前状态是终止状态（游戏赢了`isWin()`或输了`isLose()`），要么搜索已经到达了最大深度`self.depth`（一层“深度”代表pacman和所有ghost都打了一圈行为模拟，即完成了一圈`max_value`和`min_value`的过程）。

如果没有终止，也没有达到最大深度，就继续进行，轮到谁（传入的`agentIndex`）就评估从谁那评估，如果是pacman就最大化，如果是ghost就最小化。我们始终站在pacman的角度讨论评分问题。

### pacman行动：最大化评分`max_value()`

对于pacman来说，他的任务是选出最好的action，和`getActions()`函数非常像，这里唯一的区别在于输出的是评分`v`，要么是当前的最优评分，要么是在当前节点下，执行这一动作所带来的次生状态的`value()`函数，从而向下搜索，但这里的`value`函数仍然是`depth`而非`depth + 1`，是因为要等待所有agent都执行完一遍后再向下层探索——届时pacman将作为agent 0，第一个作出动作。

### ghost行动：最小化评分`min_value()`

类似的，这里要用到`gameState.getNumAgents()`方法，确认现在还有多少agent没有做出决策。如果所有agent都做出了决策，那么就要进入下一层搜索，即`depth + 1`。

## Question 3: Alpha-Beta Pruning

alpha-beta剪枝法，在minimax的基础上降低计算复杂度。

可以参照note 3的示例，如果左侧分支的min value = 3, 而中间分支的子节点中出现了一个2，那显然中间节点min value <= 2，因此max agent不需要考虑中间分支的任何情形了，因此，我们可以剪掉这个分支而不用担心出现精度问题。

这里唯一要注意的是，在`min_value`和`max_value`函数中，比较并更新alpha、beta时不要带等号，一定是`value > beta`或`value < alpha`。Note的流程图在这里出现了问题。

## Question 4: Expectimax