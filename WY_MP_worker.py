import torch.multiprocessing as mp
import gym
import numpy as np
import matplotlib.pyplot as plt 
from WY_MP_Value import MP_Value
MAX_EP = 20000
GAMMA = 0.9

def main():
    global_ep, global_ep_r, res_queue = MP_Value(int,0), MP_Value(float,0), mp.Queue()
    print("Create maximum cpu numbers process: {}".format(mp.cpu_count()))
    workers, working_table = [], []
    for index in range(mp.cpu_count()):
        name = index
        workers.append(worker(global_ep, global_ep_r, res_queue,name))
        working_table.append(1)

    for worker_item in workers:
        worker_item.start()
    res = []
    while any(working_table):
        
        data = res_queue.get()
        if isinstance(data,tuple):
            (infomation, id_process) = data
            if not isinstance(infomation,str):
                res.append(infomation)
            else:
                if infomation=="done":
                    working_table[int(id_process)] = 0
                else:
                    raise "Error state {}".format(information)
        else:
            raise ValueError("Unknown message bug type: {}, value: {}".format(type(data),data))
    for worker_item in workers:
        worker_item.join()
    
    
    # print(res)
    plt.plot(res)
    plt.ylabel('Moving average ep reward')
    plt.xlabel('Step')
    plt.show()
class worker(mp.Process):
    def __init__(self,global_ep,global_ep_r,res_queue,name,_end_message_func=None):
        super(worker,self).__init__()
        self.name = "{}".format(name)
        self.g_ep, self.g_ep_r, self.res_queue = global_ep, global_ep_r, res_queue
        self.env = gym.make('CartPole-v0')#.unwrapped
        self.action_n = self.env.action_space.n
        self.gepr = 0.0
        if _end_message_func is not None:
            self._end_message_operator = _end_message_func  # given (state,name)
        else:
            self._end_message_operator = self._default_end_message  # given (state,name)
    def run(self):
        
        total_step = 1
        while self.g_ep._getvalue() < MAX_EP:
            s = self.env.reset()
            buf_s, buf_a, buf_r = [], [], []
            ep_r = 0.0
            while True:
                action = np.random.choice(self.action_n)
                _next_s, r, done, other_info = self.env.step(action)
                if done: r=-1
                ep_r += r
                buf_s.append(s)
                buf_a.append(action)
                buf_r.append(r)

                s = _next_s
                if done:
                    self.g_ep+=1
                    # if self.g_ep_r==0.0:
                    #     self.g_ep_r(ep_r)
                    # else:
                    #     self.g_ep_r *= 0.99 
                    #     self.g_ep_r += (ep_r * 0.01)
                    # self.res_queue.put(self.g_ep_r._getvalue())
                    if self.gepr==0.0:
                        self.gepr = ep_r
                    else:
                        self.gepr *= 0.99 
                        self.gepr += (ep_r * 0.01)
                    self.res_queue.put(self._pass_message(self.gepr))
                    break
                # record(self.g_ep, self.g_ep_r, ep_r, self.res_queue, self.name)
                # if self.name == 'w0'
                # a = env.
                # if total_step% 
                #     buf_s, buf_a, buf_r = [], [], []
                # if total_step % UPDATE_GLOBAL_ITER == 0 or done:  # update global and assign to local net
                #     # sync
                #     push_and_pull(self.opt, self.lnet, self.gnet, done, s_, buffer_s, buffer_a, buffer_r, GAMMA)
                #     buffer_s, buffer_a, buffer_r = [], [], []

                #     if done:  # done and print information
                #         record(self.g_ep, self.g_ep_r, ep_r, self.res_queue, self.name)
                #         break
                # s = s_
                # total_step += 1
        self.res_queue.put(self._end_message_operator(self.name))
    def _pass_message(self,message):
        return (message,self.name)
    def _default_end_message(self,name):
        return ('done',self.name)

if __name__=="__main__":
    main()