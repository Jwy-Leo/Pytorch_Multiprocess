import torch.multiprocessing as mp
def main():
    global_ep, global_ep_r = MP_Value(int,0), MP_Value(float,0)

    print(global_ep)
    print(global_ep._getvalue())

    global_ep(10)                               # Assign value
    print(global_ep)
    print(global_ep._getvalue())

    output = global_ep + 3                      # add method , return integer
    print(output)

    global_ep += 3                              # self add method , value change
    print(global_ep)

    if not global_ep >=1:                       # Boolean function 
        print("global valuable bigger than 1")

    try:                                        # Only implemented same data type method 
        output = global_ep + global_ep_r
    except Exception as e:
        print(e)
# global_ep, global_ep_r, res_queue = MP_Value(int,0), MP_Value(float,0), mp.Queue()
    # print("Create maximum cpu numbers process: {}".format(mp.cpu_count()))
    # workers, working_table = [], []
    # for index in range(mp.cpu_count()):
    #     name = index
    #     workers.append(worker(global_ep, global_ep_r, res_queue,name))
    #     working_table.append(1)

    # for worker_item in workers:
    #     worker_item.start()
    # res = []
    # while True:
        
    #     r = res_queue.get()
    #     if isinstance(r,tuple):
    #         signal = r[0]
    #         name = r[1]
    #         working_table[int(name)] = 0
    #     elif isinstance(r,float) or isinstance(r,int):
    #         res.append(r)
    #     else:
    #         raise ValueError("Unknown message bug type: {}, value: {}".format(type(r),r))
    #     if any(working_table)==False:
    #         break
    # for worker_item in workers:
    #     worker_item.join()
    
    # import matplotlib.pyplot as plt 
    # # print(res)
    # plt.plot(res)
    # plt.ylabel('Moving average ep reward')
    # plt.xlabel('Step')
    # plt.show(block=False)
class MP_Value(object):
    def __init__(self,data_type,initial_value):
        self.data_type = data_type
        self.typecode_to_type = {long:'l',int:'i',float:'d'}
        self.valuable = mp.Value(self.typecode_to_type[self.data_type],initial_value)
        
        # self.value = lambda : self.valuable.value

        # self.typecode_to_type = {
        # 'c': ctypes.c_char,  'u': ctypes.c_wchar,
        # 'b': ctypes.c_byte,  'B': ctypes.c_ubyte,
        # 'h': ctypes.c_short, 'H': ctypes.c_ushort,
        # 'i': ctypes.c_int,   'I': ctypes.c_uint,
        # 'l': ctypes.c_long,  'L': ctypes.c_ulong,
        # 'f': ctypes.c_float, 'd': ctypes.c_double
        # }
          
    def _check_input_type(self,input_info):
        assert (isinstance(input_info,type(self.valuable)) or isinstance(input_info,self.data_type) or isinstance(input_info,type(self))), \
                "cannot do the different type operation input type : {} is different from {},{},{}".format(type(input_info),type(self.valuable),self.data_type,type(self))
        if isinstance(input_info,type(self.valuable)):
            assert isinstance(input_info.value,self.data_type), "cannot do the different type operation"
        if isinstance(input_info,type(self)):
            assert input_info.data_type==self.data_type, "cannot do the different type operation"
    
    def __str__(self):
        # return "Type: {}  Value: {}".format(str(self.valuable),self.valuable.value)
        return str(self.valuable.value)+", Type:{}".format(self.data_type.__name__)
    def __format__(self):
        return self.__str__()
    def __call__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            self.valuable.value = other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            self.valuable.value = other_input.value
        if isinstance(other_input,self.data_type):
            self.valuable.value = other_input
    def __add__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = self.valuable.value + other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            output = self.valuable.value + other_input.value
        if isinstance(other_input,self.data_type):
            output = self.valuable.value + other_input
        return output
    def __sub__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = self.valuable.value - other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            output = self.valuable.value - other_input.value
        if isinstance(other_input,self.data_type):
            output = self.valuable.value - other_input
        return output  
    def __mul__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = self.valuable.value * other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            output = self.valuable.value * other_input.value
        if isinstance(other_input,self.data_type):
            output = self.valuable.value * other_input
        return output
    def __truediv__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = self.valuable.value / other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            output = self.valuable.value / other_input.value
        if isinstance(other_input,self.data_type):
            output = self.valuable.value / other_input
        return output
    def __eq__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = (self.valuable.value == other_input.valuable.value)
        if isinstance(other_input,type(self.valuable)):
            output = (self.valuable.value == other_input.value)
        if isinstance(other_input,self.data_type):
            output = (self.valuable.value == other_input)
        return output
    def __ne__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = (self.valuable.value != other_input.valuable.value)
        if isinstance(other_input,type(self.valuable)):
            output = (self.valuable.value != other_input.value)
        if isinstance(other_input,self.data_type):
            output = (self.valuable.value != other_input)
        return output
    def __lt__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = (self.valuable.value < other_input.valuable.value)
        if isinstance(other_input,type(self.valuable)):
            output = (self.valuable.value < other_input.value)
        if isinstance(other_input,self.data_type):
            output = (self.valuable.value < other_input)
        return output
    def __le__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = (self.valuable.value <= other_input.valuable.value)
        if isinstance(other_input,type(self.valuable)):
            output = (self.valuable.value <= other_input.value)
        if isinstance(other_input,self.data_type):
            output = (self.valuable.value <= other_input)
        return output
    def __gt__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = (self.valuable.value > other_input.valuable.value)
        if isinstance(other_input,type(self.valuable)):
            output = (self.valuable.value > other_input.value)
        if isinstance(other_input,self.data_type):
            output = (self.valuable.value > other_input)
        return output
    def __ge__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            output = (self.valuable.value >= other_input.valuable.value)
        if isinstance(other_input,type(self.valuable)):
            output = (self.valuable.value >= other_input.value)
        if isinstance(other_input,self.data_type):
            output = (self.valuable.value >= other_input)
        return output
    def __iadd__(self,other_input):
        self._check_input_type(other_input)
        with self.valuable.get_lock():
            if isinstance(other_input,type(self)):
                self.valuable.value += other_input.valuable.value
            if isinstance(other_input,type(self.valuable)):
                self.valuable.value += other_input.value
            if isinstance(other_input,self.data_type):
                self.valuable.value += other_input
        return self
    def __isub__(self,other_input):
        self._check_input_type(other_input)
        with self.valuable.get_lock():
            if isinstance(other_input,type(self)):
                self.valuable.value -= other_input.valuable.value
            if isinstance(other_input,type(self.valuable)):
                self.valuable.value -= other_input.value
            if isinstance(other_input,self.data_type):
                self.valuable.value -= other_input
        return self
    def __imul__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            self.valuable.value *= other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            self.valuable.value *= other_input.value
        if isinstance(other_input,self.data_type):
            self.valuable.value *= other_input
        return self
    def __itruediv__(self,other_input):
        self._check_input_type(other_input)
        if isinstance(other_input,type(self)):
            self.valuable.value /= other_input.valuable.value
        if isinstance(other_input,type(self.valuable)):
            self.valuable.value /= other_input.value
        if isinstance(other_input,self.data_type):
            self.valuable.value /= other_input
        return self
    def __neg__(self):
        with self.valuable.get_lock():
            self.valuable.value = self.valuable.value * -1
        return self
    def _getvalue(self):
        return self.valuable.value
    

if __name__=="__main__":
    main()