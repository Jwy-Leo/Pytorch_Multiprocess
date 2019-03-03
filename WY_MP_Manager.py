import torch.multiprocessing as mp
import gym
gym.logger.set_level(40)    # ignore the warning 
import numpy as np
import sys
from tqdm import tqdm

from WY_MP_Value import MP_Value
from WY_MP_worker import worker

MAX_EP = 70000
GAMMA = 0.9
def main():
    import time 
    print("multi process about 3 seconds")
    begin = time.time()
    multiprocess_example()
    print("multi process example time cost: {}".format(time.time()-begin))

    print("single process about 12 seconds")
    begin = time.time()
    single_process_example()
    print("single process example time cost: {}".format(time.time()-begin))

def single_process_example():
    env = gym.make('CartPole-v0')
    state_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    print("(State space, Action space) = ({},{})".format(state_space,action_space))
    epr = []
    epoch = 0
    while epoch < MAX_EP:
        s = env.reset()
        buf_s, buf_a, buf_r = [], [], []
        ep_r = 0.0
        while True:
            action = np.random.choice(action_space)
            _next_s, r, done, other_info = env.step(action)
            if done: r=-1
            ep_r += r
            buf_s.append(s)
            buf_a.append(action)
            buf_r.append(r)

            s = _next_s
            if done:
                epoch += 1
                break
def multiprocess_example():
    mymp = MP_Manager(0,0,128)
    mymp.run()

class MP_Manager(object):
    def __init__(self,worker_object,worker_input,n_workers = mp.cpu_count()):
        # Global parameters
        self.worker_object = worker_object
        self.worker_input = worker_input

        self.global_ep, self.global_ep_r, self.res_queue = MP_Value(int,0), MP_Value(float,0), mp.Queue()

        # print("Create maximum cpu numbers process: {}".format())
        self.workers, self.working_table,self.res = [], [], []

        for index in range(n_workers):
            name = index
            self.workers.append(worker(self.global_ep, self.global_ep_r, self.res_queue,name,self._end_message))
            self.working_table.append(1)
    def run(self):
        self.start()
        self.monitor()
        self.collect_process()
    def start(self):
        for worker_item in self.workers:
            worker_item.start()
    def monitor(self):
        previous = sum(self.working_table)
        t = tqdm(total=previous)
        
        while any(self.working_table):
            deal_num = previous - sum(self.working_table)
            previous = sum(self.working_table)
            t.update(deal_num)

            responce = self.res_queue.get()
            # print(responce)
            self.datagram_process(responce)
            
            
            # sys.stdout.write("\r{:3d}/{:3d}".format(sum(self.working_table),len(self.working_table)))
            
            
        # sys.stdout.write("\n")
        t.close()
        return self.res
    def collect_process(self):
        for worker_item in self.workers:
            worker_item.join()
    def _end_message(self,name):
        return ('done',name)
    def datagram_process(self,data):
        if isinstance(data,tuple):
            (infomation, id_process) = data
            if not isinstance(infomation,str):
                self.res.append(infomation)
            else:
                if infomation=="done":
                    self.working_table[int(id_process)] = 0
                else:
                    raise "Error state {}".format(information)
        else:
            raise ValueError("Unknown message bug type: {}, value: {}".format(type(data),data))

if __name__=="__main__":
    main()
    