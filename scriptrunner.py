import solver
import time
import os

thread_num = 4
start = time.time()
os.system("mpiexec -n " + str(thread_num) + " python .\solver.py")
total_time = time.time()-start
print("Total time: " + str(round(total_time, 2)))
print("Average time per thread: " + str(round(total_time/thread_num, 2)))

