import  random
import numpy as np
import math
class OpponentPool:
    def __init__(self,model,envs):
        self.n_envs=envs
        # self.policy_now= random.randrange(3)
        self.policy_list=[random.randint(0, 2) for _ in range(self.n_envs)]
        self.model=model

    def refresh_policy(self,i):
        self.policy_list[i]=random.randint(0, 2)
    def predict(self,obs,deterministic):
        obs_list = obs["obs"]
        actions=[]
        for i in range(self.n_envs):
            match self.policy_list[i]:
                case 0:
                    # print("现在使用模型推理")
                    single_obs={"obs":obs_list[i]}
                    action, _state = self.model.predict(single_obs, deterministic)
                    actions.append(action)
                case 1:
                    # print("现在使用简单脚本")
                    actions.append(self.simple_policy(obs_list[i]))
                case 2:
                    # print("使用高级脚本")
                    actions.append(self.advanced_policy(obs_list[i]))
        return np.vstack(actions)

    def simple_policy(self,obs):
        return [1 if obs[0]>obs[6] else 0,
                1 if obs[0]<obs[6] else 0,
                1 if obs[9]<0 else 0]
    def advanced_policy(self,obs):
        if obs[9]>0:
            target = self.calculate_target(obs[6], obs[7], obs[8], obs[9])

            return [1 if obs[0] > target else 0,
                    1 if obs[0] < target else 0,
                    1 if obs[9] < 0 else 0]
        else:
            return [0,0,random.choice([0,1])]
    def calculate_target(self,x0, y0, vx, vy):
        # 计算到达y=1所需的时间
        t = (1.0 - y0) / vy
        # 处理x方向速度为零的情况
        if vx == 0:
            x = x0
        else:
            # 计算等效的总位移
            x_total = x0 + vx * t
            # 计算整数部分和余数
            n = math.floor(x_total)
            r = x_total - n
            # 根据奇偶性确定最终位置
            if n % 2 == 0:
                x = r
            else:
                x = 1 - r
        return x
