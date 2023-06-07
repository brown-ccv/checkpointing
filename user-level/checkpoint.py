import pickle
import os
import numpy as np
import time

total_steps=1000
checkpoint_interval=10

def calculation():
    vector_size=20000
    #Generate a random vector of size vector_size.
    vec1=np.random.randint(1000,size=vector_size)
    vec2=np.random.randint(1000,size=vector_size)
    product=np.zeros(vector_size)
    for i in range(vector_size):
        product[i]=vec1[i]*vec2[i]
    time.sleep(0.1)
    return np.sum(product)
     
#Check if checkpoint file exists   
if os.path.isfile('checkpoint.pkl'):
    with open('checkpoint.pkl','rb') as f:
        step,data=pickle.load(f)
        
    
else:
    #No checkpoint file. Start calculation
    step=0
    data=[]

print(f"Starting calculation from iteration: {step}")
while(step<total_steps):
    print(f"Calculating step: {step}")
    #Run calculation
    step_result=calculation()
    data.append(step_result)
    if ( step % checkpoint_interval == 0):
        #Open or overwrite previous checkpoint
        with open("checkpoint.pkl","wb") as f:
            pickle.dump((step,data),f)
        print(f"Finished Checkpointing step: {step}")
    step+=1

print(f"Program complete.")
    