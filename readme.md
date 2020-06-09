Prediction REST API
====

Working with virtual environment:
---

Create virtualenv:

```
virtualenv -p python3.6 venv 
```

Activate virtualenv:

```
source venv/bin/activate
```

Install required python packages:

```
pip install -r requirements/requirements.txt
```

### Run server:

```
python app.py
```

### Test rest API:

In new terminal, script directory: 

```
source venv/bin/activate
python test.py
```

Prediction REST API end points:
---

### Model training:

End point: 'http://server_ip:port/train/'

Type of request : POST, json

#### Json keys:

 'userid' - user id;

 'categorical_features' - list of categorical features;

 'numerical_features' - list of numerical features;

 'data_train' - data frame for training predictive model, format is the list of dictionaries where  key is feature name, value is the value of feature for data sample;
 
'target_variable' - target variable name;
 
 Data frame has obvious date feature with name 'date' and format 'yyyy-mm-dd'
  
####  Example of json data for model training request:
  
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

#### Response for model training request:

Json keys: 'train_model_scores', 'result_code'.

'train_model_scores' - training model scores, 
e.g., important score: train_model_scores['test_rmae'] - relative mean of absolute error

'result_code':    'Ok' - successful result, 
in the case of error there are the following 
codes: 'incorrect data load', 'incorrect features processing', 'error model training'. 

### Prediction:

 End point: 'http://server_ip:port/predict/'

 Type of request : POST, json

#### Json keys:

 'userid' - user id;

 'categorical_features' - list of categorical features;

 'numerical_features' - list of numerical features;

 'data_test' - the same data frame as for model training except target variable column which should be predicted
 
#### Example of request data:

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

#### Response for prediction request:

Result of prediction - list of predicted target variable in json format, values in the list correspond to the rows of test data frame.  

Json  keys: 'result_code', 'prediction'

'result_code' - result of request processing:  'Ok' - successful result, 
in the case of error there are the following 
codes: 'incorrect data load', 'incorrect train file load', 'incorrect model file load' 

#### Example of list for Json key 'prediction':

 {'prediction': [722.3371006983247,
  1022.643302848146,
  1000.4824859038298,
  359.436872082368,
  467.0423624171987,
  ......
  ]}
  
Docker container:
---

Build docker container:
```
cd script_dir
docker build -t prediction_rest_api .
```

Run docker container:
```
cd script_dir
docker run -d -p 8080:8888 prediction_rest_api
```
Test container prediction_rest_api:

```
cd script_dir
source venv/bin/activate
python test.py
```
Create GitHub packages:
---

Create access tocken according to:
https://github.com/vallkor/DemandForecaster/blob/develop/README.md#what-is-github-packages

Set up environment variable:

```
export DOCKER_PASS=...
export DOCKER_USER=...
```

Log in into GitHub and push docker package:

```
docker login docker.pkg.github.com -u $DOCKER_USER -p $DOCKER_PASS
```
Push docker images
```
docker tag $(docker images -q prediction_rest_api) docker.pkg.github.com/vallkor/demandforecaster/prediction_rest_api
docker push docker.pkg.github.com/vallkor/demandforecaster/prediction_rest_api
```

