from flask import Flask,request
import json
import pandas as pd
import numpy as np
import datetime
from datetime import date,datetime, timedelta
import time
from sklearn import  metrics, preprocessing
import lightgbm as lgb
import pickle

def concate_data_sets(data_train, data_test):
    '''Concatenate train and test data sets '''
    data=pd.concat([data_train, data_test],axis=0)
    date_train_test_split=data_test.date.min()
    return(data,date_train_test_split)


def get_scores(data):
    ''' Get scores for validation '''
    data1=data.dropna(subset=['sales','pred'])
    rmse=np.round(np.sqrt(metrics.mean_squared_error(data1['sales'],data1['pred'])),3)
    mae=np.round(np.abs(data1['sales']-data1['pred']).mean(),3)
    rmae=np.round(mae/(data1['sales'].mean()),3)
    return (rmse,mae,rmae)


def get_features(data, categorical_features, numerical_features,
                 target_variable='sales', use_target_mean_cat_feature=True, 
                 use_count_cat_feature=True):
    ''' Create features for predictive model '''
    date_variable='date'
    data[date_variable]=pd.to_datetime(data[date_variable])
    data=data.set_index(date_variable).sort_index().reset_index()
    data.dropna(subset=[date_variable],inplace=True)
    data['weekday']=data[date_variable].dt.weekday
    data['month']=data[date_variable].dt.month
    data['monthday']=data[date_variable].dt.day
    data['week']=data[date_variable].dt.week
    data['weekday']=data['weekday'].astype(int)
    data['month']=data['month'].astype(int)
    data['monthday']=data['monthday'].astype(int)
    data['week']=data['week'].astype(int)
    features=numerical_features+['weekday','month','monthday','week']
    for i in categorical_features:
        data[i].fillna('na',inplace=True)
        enc = preprocessing.LabelEncoder()
        data[i+'_enc'] = enc.fit_transform(data[i])
        features.append(i+'_enc')
    if (use_target_mean_cat_feature):
        for i in categorical_features:
            a=data.groupby(i)[target_variable].mean().to_frame(i+'_mean').reset_index()
            data=data.copy().merge(a,how='left',on=i)
            features.append(i+'_mean')
    if (use_count_cat_feature):
        for i in categorical_features:
            a=data.groupby(i)[target_variable].count().to_frame(i+'_count').reset_index()
            data=data.merge(a,how='left',on=i) 
            features.append(i+'_count')
    data_size=data.shape[0]
    return (data,features)


def lightgbm_train(data,features,target_variable,num_boost_round,  params,
                     target_log=False, model_file='model.pkl', verbose_eval=50,  test_part=0.25):
    ''' Train predictive model'''
    data_size=data.shape[0]
    ntest=int(round(data_size*(test_part)))
    data_train=data.iloc[:-ntest,:].copy()
    data_test=data.iloc[-ntest:,:].copy()
        
    if (target_log):
        data_train['target_var']=np.log(data_train[target_variable]+1)
        data_test['target_var']=np.log(data_test[target_variable]+1)
    else:
        data_train['target_var']=data_train[target_variable] 
        data_test['target_var']=data_test[target_variable] 
        
    train_d = lgb.Dataset(data_train[features], data_train['target_var'])
    val_d = lgb.Dataset(data_test[features], data_test['target_var'])

    model = lgb.train(params, train_d, num_boost_round = num_boost_round , 
                      early_stopping_rounds = 50, valid_sets = [train_d, val_d], 
                      verbose_eval = verbose_eval)  
    
    if(target_log):
        data_test['pred']=np.exp(model.predict(data_test[features]))-1
        data_train['pred']=np.exp(model.predict(data_train[features]))-1
    else:
        data_test['pred']=model.predict(data_test[features])
        data_train['pred']=model.predict(data_train[features])
    
    err={}
    err['train_rmse'], err['train_mae'], err['train_rmae']=get_scores(data_train)
    err['test_rmse'], err['test_mae'], err['test_rmae']=get_scores(data_test)
    
    best_iteration=model.best_iteration
    
    if (target_log):
        data['target_var']=np.log(data[target_variable]+1)
    else:
        data['target_var']=data[target_variable] 
        
    train_d = lgb.Dataset(data[features], data['target_var'])

    model = lgb.train(params, train_d, num_boost_round = best_iteration, verbose_eval = 0)  
    
    pickle.dump(model, open(model_file, "wb"))
    
    print ('Done!')
    
    return (model,data_train, data_test,err, best_iteration)


def lightgbm_predict(model,data_train,data_test,categorical_features, numerical_features,target_variable,target_log):
    '''Get prediction for test data set'''
    data_train.date=pd.to_datetime(data_train.date)
    data_test.date=pd.to_datetime(data_test.date)
    data,date_train_test_split=concate_data_sets(data_train, data_test)
    data,features=get_features(data, categorical_features, numerical_features,target_variable=target_variable)
    data_test=data[data.date>=date_train_test_split].copy()
    if(target_log):
        data_test['prediction']=np.exp(model.predict(data_test[features]))-1
    else:
        data_test['prediction']=model.predict(data_test[features])
    return(data_test)

