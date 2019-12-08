import numpy as np 
import pandas as pd

import seaborn as sns

def predictor(data_dict):

    # Load Data
    trainData = pd.read_csv('input/train.csv')
    testData = pd.read_csv('input/test.csv')

    # Drop Id Coulmn
    trainData = trainData.drop('Id', axis=1)
    testData = testData.drop('Id', axis=1)

    # Find no. of days from Date
    trainData['Open Date'] = pd.to_datetime(trainData['Open Date'], format='%m/%d/%Y')   
    testData['Open Date'] = pd.to_datetime(testData['Open Date'], format='%m/%d/%Y')

    trainData['OpenDays']=""
    testData['OpenDays']=""

    dateLastTrain = pd.DataFrame({'Date':np.repeat(['12/09/2019'],[len(trainData)]) })
    dateLastTrain['Date'] = pd.to_datetime(dateLastTrain['Date'], format='%m/%d/%Y')  
    dateLastTest = pd.DataFrame({'Date':np.repeat(['12/09/2019'],[len(testData)]) })
    dateLastTest['Date'] = pd.to_datetime(dateLastTest['Date'], format='%m/%d/%Y')  

    trainData['OpenDays'] = dateLastTrain['Date'] - trainData['Open Date']
    testData['OpenDays'] = dateLastTest['Date'] - testData['Open Date']

    trainData['OpenDays'] = trainData['OpenDays'].astype('timedelta64[D]').astype(int)
    testData['OpenDays'] = testData['OpenDays'].astype('timedelta64[D]').astype(int)

    trainData = trainData.drop('Open Date', axis=1)
    testData = testData.drop('Open Date', axis=1)

    # Convert Categorical variables to dummy variables
    citygroupDummy = pd.get_dummies(trainData['City Group'])
    trainData = trainData.join(citygroupDummy)

    citygroupDummyTest = pd.get_dummies(testData['City Group'])
    testData = testData.join(citygroupDummyTest)

    trainData = trainData.drop('City Group', axis=1)
    testData = testData.drop('City Group', axis=1)

    typeDummy = pd.get_dummies(trainData['Type'])
    trainData = trainData.join(typeDummy)

    typeDummyTest = pd.get_dummies(testData['Type'])
    testData = testData.join(typeDummyTest)

    trainData = trainData.drop('Type', axis=1)
    testData = testData.drop('Type', axis=1)


    #Regression on relevant columns
    from sklearn.ensemble import RandomForestRegressor

    sns.set_context("notebook", font_scale=1.1)
    sns.set_style("ticks")

    import numpy
    '''
    List of Variables:

    OpenDays
    CityGroup -- BigCities/Other
    RestuarntType -- DT/FC/IL
    Population -- P2 (Normalized range - 1:10)
    Percentage Population below 30 - P3 (Normalized range - 1:10)
    Gender Ratio - P22 (Normalized range - 1:5)
    Development index - P24 (Normalized range - 0:5)
    Area (Size) - P20 (Normalized range - 1:15)
    Car Park Area - P26 (Normalized range - 1:10)
    No. of points of interest nearby - P28 ((Normalized range - 1:10)
    '''

    xTrain = pd.DataFrame({'OpenDays':trainData['OpenDays'].apply(numpy.log),
                        'Big Cities':trainData['Big Cities'], 'Other':trainData['Other'], 
                        'DT':trainData['DT'], 'FC':trainData['FC'], 'IL':trainData['IL'],
                        'P2':trainData['P2'], 'P3':trainData['P3'], 'P22':trainData['P22'], 'P24':trainData['P24'],
                        'P20':trainData['P20'], 'P28':trainData['P28'], 'P26':trainData['P26']})

    yTrain = trainData['revenue'].apply(numpy.log)
    xTest = pd.DataFrame({'OpenDays':[data_dict['OpenDays']],
                        'Big Cities':[data_dict['Big Cities']], 'Other':[data_dict['Other']],
                        'DT':[data_dict['DT']], 'FC':[data_dict['FC']], 'IL':[data_dict['IL']],
                        'P2':[data_dict['P2']], 'P3':[data_dict['P3']], 'P22':[data_dict['P22']], 'P24':[data_dict['P24']],
                        'P20':[data_dict['P20']], 'P28':[data_dict['P28']], 'P26':[data_dict['P26']]})

    # xTest = pd.DataFrame(data_dict)

    from sklearn import linear_model

    cls = RandomForestRegressor(n_estimators=150)
    cls.fit(xTrain, yTrain)
    pred = cls.predict(xTest)
    pred = numpy.exp(pred)
    cls.score(xTrain, yTrain)

    pred = cls.predict(xTest)
    pred = numpy.exp(pred)

    pred2 = []
    for i in range(len(pred)):
        if pred[i] != float('Inf'):
            pred2.append(pred[i])

    m = sum(pred2) / float(len(pred2))

    for i in range(len(pred)):
        if pred[i] == float('Inf'):
            print("haha")
            pred[i] = m

    # testData = pd.read_csv("input/test.csv")
    # # submission = pd.DataFrame({
    # #         "Id": testData["Id"],
    # #         "Prediction": pred
    # #     })
    return pred[0]
    # submission.to_csv('Output.csv',header=True, index=False)

