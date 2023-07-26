from pandas.core.frame import DataFrame
import numpy as np
import os

if not os.path.exists('output'):
    os.makedirs('output')

with open('./1_result/dev_kit_standard_s_calibration_table.pb.txt', 'r') as f:
    pb_str = f.read()

pb_list = pb_str.split('\n')

speed = []
acc = []
cmd = []

length = int(len(pb_list)/5)
speed = [float(pb_list[i*5+1].split(':')[1]) for i in range(length)]
acc = [float(pb_list[i*5+2].split(':')[1]) for i in range(length)]
cmd = [float(pb_list[i*5+3].split(':')[1])/100 for i in range(length)]

speed_front = []
acc_front = []
cmd_front = []

speed_back = []
acc_back = []
cmd_back = []

for i in range(length):
    if cmd[i] < 0:
        speed_back.append(speed[i])
        acc_back.append(acc[i])
        cmd_back.append(-cmd[i])
    else:
        speed_front.append(speed[i])
        acc_front.append(acc[i])
        cmd_front.append(cmd[i])


speed_front_set = sorted(list(set(speed_front)))
cmd_front_set = cmd_front[:20]
acc_front_np = np.array(acc_front).reshape(20,20).T
pd_front = DataFrame(acc_front_np, index=cmd_front_set, columns=speed_front_set)
pd_front = pd_front.sort_index(axis=0, ascending=True)
pd_front.to_csv('output/throttle.csv')

speed_back_set = sorted(list(set(speed_back)))
cmd_back_set = cmd_back[:20]
acc_back_np = np.array(acc_back).reshape(20,20).T
pd_back = DataFrame(acc_back_np, index=cmd_back_set, columns=speed_back_set)
pd_back = pd_back.sort_index(axis=0, ascending=True)
pd_back.to_csv('output/brake.csv')

with open('output/throttle.csv', 'r') as f:
    throttle = f.read()
    throttle = 'pix' + throttle

with open('output/brake.csv', 'r') as f:
    brake = f.read()
    brake = 'pix' + brake

throttle_file = open('output/throttle.csv','w')
throttle_file.write(throttle)
brake_file = open('output/brake.csv','w')
brake_file.write(brake)

