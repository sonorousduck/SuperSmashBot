from multiprocessing import Process, Pipe
from agent import Agent


def update_agent(agent):
    return agent.model.load_weights('recentweights.hdf5')

def function_main(receive_pipe, send_pipe, func):
    agent = Agent()

    while True:
        data = receive_pipe.recv()
        if data == 'exit':
            return
        if data == 'updateAgent':
            agent = update_agent(agent)
            continue
        result = func(data, agent)
        send_pipe.send(result)





class ProcessCore:
    """
    Creates a subprocess that will run the passed in function_to_run when supplied data through sendData
    Retrieves output from getData, which will block until there is something to get from the resulting sendData
    If you try getData before ever sending data, you may end in infinite loop
    """
    def __init__(self, function_to_run):
        self.__child_to_parent_recv, self.__child_to_parent_send = Pipe()
        self.__parent_to_child_recv, self.__parent_to_child_send = Pipe()
        self.process = Process(target=function_main, args=(self.__parent_to_child_recv, self.__child_to_parent_send, function_to_run))
        self.process.start()


    """
    Sends data to the subprocess. Can use almost like as if you started the function
    """
    def sendData(self, data):
        self.__parent_to_child_send.send(data)

    """
    Get the result from the sendData call. Will block until the data is ready
    """
    def getData(self):
        data = self.__child_to_parent_recv.recv()
        return data

    def closeConnection(self):
        self.sendData('exit')
        self.process.join()

def f(data):
    return data['Howdy']

if __name__ == '__main__':
    myProcess = ProcessCore(f)
    myProcess2 = ProcessCore(f)
    data = {}
    data['Howdy'] = 2
    data['Test'] = 10
    myProcess.sendData(data)
    myProcess2.sendData({'Howdy': 10})
    value = myProcess2.getData()
    print(f"Value returned {value}")
    value = myProcess.getData()
    print(f"Value returned {value}")
    myProcess.closeConnection()
    myProcess2.closeConnection()
