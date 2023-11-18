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