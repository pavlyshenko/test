import sys
import json
import requests
import pandas as pd

# Test data directory
test_data_dir='test_data'

# File names for training and testing model
data_train_file_name='data_a_train.csv'
data_test_file_name='data_a_test.csv'

# Lists of categorical and numerical features 
categorical_features=['dept_id', 'cat_id', 'store_id', 'state_id', 'event_name_1']
numerical_features=['snap_CA', 'snap_TX', 'snap_WI']

# IP address and port for RESTAPI
#server_ip_port='195.160.232.177:8888'
server_ip_port='127.0.0.1:8080'

###########################################

data_train=pd.read_csv(test_data_dir+'/'+data_train_file_name)
data_test=pd.read_csv(test_data_dir+'/'+data_test_file_name)

request_data={
'userid':'user1',
'categorical_features':['dept_id', 'cat_id', 'store_id', 'state_id', 'event_name_1'],
'numerical_features':['snap_CA', 'snap_TX', 'snap_WI'],
'target_variable':'sales',
'data_train':data_train.to_dict(orient='records'),
}

print ('Send request for model training')
results = requests.post('http://'+server_ip_port+'/train/', json=request_data).json()
try:
    results = requests.post('http://'+server_ip_port+'/train/', json=request_data).json()
    print ('Results')
    print (results)
except:
    print ('Error in training model endpoint')
    exit()
    
print ('\nSending request for prediction')
request_data={
    'userid':'user1',
'categorical_features':['dept_id', 'cat_id', 'store_id', 'state_id', 'event_name_1'],
'numerical_features':['snap_CA', 'snap_TX', 'snap_WI'],
'target_variable':'sales',
'data_test':data_test.to_dict(orient='records'),
}
try:
    results = requests.post('http://'+server_ip_port+'/predict/', json=request_data).json()
    print (results['result_code'])
    print (f"Prediction results have been received successfully ({len(results['prediction'])} result samples).")
except:
    print ('Error in receiving prediction requests')
    exit()
print ('\nDone')

