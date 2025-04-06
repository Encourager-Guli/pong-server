# pong-server

本项目用于为基于 [Godot](https://godotengine.org/) 引擎的游戏训练强化学习智能体，灵感来源并基于 [edbeeching/godot_rl_agents](https://github.com/edbeeching/godot_rl_agents)。  
代码运行于服务器端，用于控制智能体，接收来自客户端（游戏）传输的数据，并执行训练或推理任务。  

## 🎮 客户端项目

你可以在此处找到对应的游戏客户端项目（基于 Godot 引擎）：  
👉 [Encourager-Guli/Panthom-Pong-Online](https://github.com/Encourager-Guli/Panthom-Pong-Online)

该客户端将作为环境模拟器，通过 socket 与本项目通信，实现训练或对抗模式。

## ✨ 功能特点

- 支持多进程并行训练
- 可加载预训练模型继续训练
- 支持与已有模型对抗
- 与 Godot 客户端实时通信，实现训练/推理过程

## 📦 安装依赖

请确保已安装 Python 环境，然后执行以下命令安装所需依赖项：

```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 启动训练

使用以下命令启动训练：

```bash
python servers/stable_baselines3_example.py   --opponent_mpath servers/models/01.zip  --resume_model_path servers/models/01.zip     --env_path servers/Pong_60FPS_selfplay.exe    --experiment_name experiment01     --save_checkpoint_frequency 10000     --n_parallel 4     --linear_lr_schedule     --speedup 4
```

### 启动推理（对战模式）

使用以下命令启动推理服务器，加载已训练模型与客户端进行对战：

```bash
python servers/server.py --opponent_path servers/models/01.zip
```

## 🕹️ 启动游戏

最后，运行客户端游戏，连接服务器即可开始训练或对抗。

---

