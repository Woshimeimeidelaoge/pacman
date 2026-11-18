# pacman

第一阶段是《灯火迷宫》（Lantern Maze），一个用 Python 和 Pygame 制作的迷宫吃豆小游戏。目标是吃完一张原创地图里的豆子，同时躲开巡逻的幽灵。

## 键盘试玩

在仓库根目录用 Python 3.12 创建虚拟环境。

```bash
python -m venv .venv
```

激活环境。macOS 或 Linux 使用 `source .venv/bin/activate`，Windows PowerShell 使用 `.\.venv\Scripts\Activate.ps1`。

```bash
python -m pip install -r requirements.txt
python main.py
```

## 玩法

- 按方向键开始。角色会沿当前方向前进，也可以提前按方向键，在下一个可转向的位置转弯。
- 幽灵每隔两个行动回合沿固定路线移动一格。角色撞墙时会停在原地，幽灵仍会巡逻。
- 每吃一颗豆子得 10 分。吃完全部豆子就通关，碰到幽灵就失败。
- `R` 重开，`Esc` 退出。

## 自动模拟

在包含 `simulate.py` 的文件夹里打开终端。批量模拟只用 Python 标准库，直接运行下面的命令即可比较两种策略。

```bash
python simulate.py --episodes 30 --max-steps 500 --seed 42
```

- `random` 从没被墙挡住的方向里等概率选一个。
- `heuristic` 用广度优先搜索寻找最近的可达豆子，每一步重新规划。搜索会避开幽灵当前和下一回合的位置。

两种策略都从同一张地图的初始状态开始，用相同的种子序列（上例为 42 到 71）。每局最多 500 步，到达上限时若仍在进行就记为超时。终端显示平均得分、胜负和超时局数、通关率、平均步数和总耗时。相同参数可以复现游戏结果，总耗时随设备和运行环境而变化。

可用 `--strategy random` 或 `--strategy heuristic` 单独跑一种策略。

## 代码

- `game.py` 管理地图、角色移动、得分和胜负。`Game.step()` 推进一个行动回合，可直接从 Python 调用。
- `main.py` 用 Pygame 读取方向键、定时推进游戏并绘制窗口。
- `strategies.py` 定义两种基线策略。策略读取 `Game` 并返回一个方向，或返回 `None` 等待一回合。
- `simulate.py` 提供命令行入口和 `run_episode()`，后续可用同一个函数评估遗传编程生成的策略。
