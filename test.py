import multiprocessing
import telebot

task_queue = multiprocessing.Queue()

def worker(input_task):
    # for i in input_task.get():
    while True:
        i = input_task.get()
        proc_name = multiprocessing.current_process().name
        print(f"имя процесса - {proc_name} значение задачи  - {i}\n")

def putter1():
        for i in ['test1', 'test2', 'test3']:
            task_queue.put(i)
def putter2():
        for i in ['test4', 'test6', 'test7']:
            task_queue.put(i)
        for i in ['test22', 'test22', 'test33']:
            task_queue.put(i)    
def start():
    NUMBER_OF_PROCESSES = 5
    
    #
    # task1 = ['zadacha1', 'zadacha2', 'zadacha3', 'zadacha4', 'zadacha5']
    # task2 = ['zadacha10', 'zadacha11', 'zadacha12', 'zadacha13', 'zadacha14']
    #
    #
    #
    # print('task1')
    # for i in task1:
    #     task_queue.put(i)
    #     time.sleep(3)
    
    #
    # for i in range(NUMBER_OF_PROCESSES):
    multiprocessing.Process(target=worker, args = (task_queue,)).start()
        
        
    
if __name__ == "__main__":
    start()
    
    multiprocessing.Process(target=putter2, args = ()).start()
    