# pacman

第一阶段是《灯火迷宫》（Lantern Maze），一个用 Python 和 Pygame 制作的迷宫吃豆小游戏。目标是吃完一张原创地图里的豆子，同时躲开巡逻的幽灵。

## 运行

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

## 代码

- `game.py` 管理地图、角色移动、得分和胜负。`Game.step()` 推进一个行动回合，可直接从 Python 调用。
- `main.py` 用 Pygame 读取方向键、定时推进游戏并绘制窗口。
