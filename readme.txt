Prediction REST API

Working with virtual environment:

Create virtualenv:
virtualenv -p python3.6 venv

Activate virtualenv:
source venv/bin/activate

Install required python packages :
pip install -r requirements/requirements.txt

Run server:
python app.py

Test rest API:
In new terminal, script directory: 
source venv/bin/activate
python test.py

Prediction REST API end points:
Model training:
 End point: 'http://server_ip:port/train/'
 Type of request : POST, json
 json keys:
 'userid' - user id;
 'categorical_features' - list of categorical features;
 'numerical_features' - list of numerical features;
 'data_train' - data frame for training predictive model, format is the list of dictionaries where  key is feature name, 
  value is the value of feature for data sample;
 'target_variable' - target variable name;
  Data frame has obvious date feature with name 'date' and format 'yyyy-mm-dd'
  
  Example of json data:
  
{'userid': 'user1',
 'categorical_features': ['dept_id',
  'cat_id',
  'store_id',
  'state_id',
  'event_name_1'],
 'numerical_features': ['snap_CA', 'snap_TX', 'snap_WI'],
 'target_variable': 'sales',
 'data_train': [{'date': '2013-01-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_1',
   'state_id': 'CA',
   'event_name_1': 'NewYear',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0,
   'sales': 386.07},
  {'date': '2013-01-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_2',
   'state_id': 'CA',
   'event_name_1': 'NewYear',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0,
   'sales': 851.83},
  {'date': '2013-01-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_3',
   'state_id': 'CA',
   'event_name_1': 'NewYear',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0,
   'sales': 581.1},
  {'date': '2013-01-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_4',
   'state_id': 'CA',
   'event_name_1': 'NewYear',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0,
   'sales': 281.2099999999999},
  {'date': '2013-01-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'TX_1',
   'state_id': 'TX',
   'event_name_1': 'NewYear',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0,
   'sales': 392.58000000000015}]}
   
 Prediction:
 End point: 'http://server_ip:port/predict/'
 Type of request : POST, json
 json keys: the same like for model training
 'data_test' - the same data frame as for model training except target variable column which should be predicted
 Result of prediction - list of predicted target variable in json format, values in the list correspond 
 to the rows of test data frame.  
 
 Example of request data:
 {'userid': 'user1',
 'categorical_features': ['dept_id',
  'cat_id',
  'store_id',
  'state_id',
  'event_name_1'],
 'numerical_features': ['snap_CA', 'snap_TX', 'snap_WI'],
 'target_variable': 'sales',
 'data_test': [{'date': '2015-05-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_1',
   'state_id': 'CA',
   'event_name_1': 'na',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0},
  {'date': '2015-05-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_2',
   'state_id': 'CA',
   'event_name_1': 'na',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0},
  {'date': '2015-05-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_3',
   'state_id': 'CA',
   'event_name_1': 'na',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0},
  {'date': '2015-05-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'CA_4',
   'state_id': 'CA',
   'event_name_1': 'na',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0},
  {'date': '2015-05-01',
   'dept_id': 'FOODS_1',
   'cat_id': 'FOODS',
   'store_id': 'TX_1',
   'state_id': 'TX',
   'event_name_1': 'na',
   'snap_CA': 1.0,
   'snap_TX': 1.0,
   'snap_WI': 0.0}]}
   
 Example of prediction results:
 {'prediction': [722.3371006983247,
  1022.643302848146,
  1000.4824859038298,
  359.436872082368,
  467.0423624171987,
  ......
  ]}
  
Docker container:

Build docker container:
cd script_dir
docker build -t demand_pred_api .

Run docker container:
cd script_dir
docker run -d -p 8080:8080 demand_pred_api

Test container demand_pred_api:
cd script_dir
source venv/bin/activate
python test.py
