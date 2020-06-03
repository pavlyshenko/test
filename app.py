from predictionfunctions import *

# Set up options

# server host ip
server_host_ip='0.0.0.0'

# Set up server port
server_port=8080
#server_port=8888

# Debug mode
debug=True

# directory for data and model
data_dir='data_dir'

# LightGBM options 
lightgbm_params = {
        'boosting_type': 'gbdt',
        'metric': 'rmse',
        'objective': 'regression',
        'n_jobs': -1,
        'seed': 15,
        'num_leaves': 100,  
        'max_depth': 5,  
        'learning_rate': 0.1,
        'bagging_fraction': 1, 
        'colsample_bytree': 0.75}
num_boost_round=500

# Model file name
model_file='model.pkl'

# Use logarithmic transformation for target variable
target_log=False

####################################################

app = Flask(__name__) 


@app.route('/train/', methods = ['POST'])
def train_model():
    try:
        r_data = request.get_json()
        data_train=pd.DataFrame(r_data['data_train'])
        userid=r_data['userid']
        target_variable=r_data['target_variable']
        categorical_features=r_data['categorical_features']
        numerical_features=r_data['numerical_features']
    except:
        result={'result_code':'incorrect data load'}
        output_result = json.dumps(result)   
        return output_result
    data_train.to_csv(data_dir+'/'+userid+'_'+'train.csv',index=False)
    try:
        data_train,features=get_features(data_train, categorical_features, numerical_features,target_variable=target_variable)
    except:
        result={'result_code':'incorrect features processing'}
        output_result = json.dumps(result)   
        return output_result
    try:
        model,data_train, data_test,err, best_iteration=lightgbm_train(data_train,features,target_variable,
            num_boost_round, lightgbm_params,target_log=target_log, model_file=data_dir+'/'+userid+'_'+model_file,
            verbose_eval=300,  test_part=0.15)
        result={'train_model_scores':err}
        result['result_code']='Ok'
    except:
        result={'result_code':'error model training'}
    output_result = json.dumps(result)   
    return output_result


@app.route('/predict/', methods = ['POST'])
def predict_sales():
    try:
        r_data = request.get_json()
        userid=r_data['userid']
        data_test=pd.DataFrame(r_data['data_test'])
        target_variable=r_data['target_variable']
        categorical_features=r_data['categorical_features']
        numerical_features=r_data['numerical_features']
        target_variable=r_data['target_variable']
    except:
        result={'result_code':'incorrect data load'}
        output_result = json.dumps(result)   
        return output_result
    try:
        data_train=pd.read_csv(data_dir+'/'+userid+'_'+'train.csv')
    except:
        result={'result_code':'incorrect train file load'}
        output_result = json.dumps(result)   
        return output_result
    try:
        model=pickle.load(open(data_dir+'/'+userid+'_'+model_file, 'rb'))
    except:
        result={'result_code':'incorrect model file load'}
        output_result = json.dumps(result)   
        return output_result
    
    try:
        data_test=lightgbm_predict(model,data_train,data_test,categorical_features, 
                                   numerical_features,target_variable,target_log)  
        result={'prediction':data_test.prediction.tolist()}
        result['result_code']='Ok' 
    except:
        result={'prediction':[],'result_code':'error model prediction'}
    output_result = json.dumps(result)  
    return output_result


if __name__ == '__main__':
    app.run(debug=debug, host=server_host_ip,port=server_port)