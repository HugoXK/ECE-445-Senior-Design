import numpy as np
from sklearn.linear_model import LinearRegression

def Position_Mapper(X,Y):
    # Normalization
    X[:,0] = X[:,0]/640
    X[:,1] = X[:,1]/480 
    # Model Setup
    model = LinearRegression(fit_intercept=True)
    result = model.fit(X,Y)
    return result.coef_,result.intercept_,result.score(X,Y),result

def Position_Predictor(X,Y,Pred_X):
    _,_,_,result = Position_Mapper(X,Y)
    print(result)
    predict_coordinate = result.predict(Pred_X)
    return predict_coordinate


if __name__ == "__main__":
    X = np.array([[351,254],
                  [343,211],
                  [342,171],
                  [362,165],
                  [313,174],
                  [313,217],
                  [312,267],
                  [372,201]],dtype= float)
    Y = np.array([[0.35,0.2],
                  [0.35,0.05],
                  [0.33,-0.1],
                  [0.25,-0.12],
                  [0.43,-0.12],
                  [0.45,0.05],
                  [0.47,0.22],
                  [0.25,0.04]],dtype=float)


    print(Position_Mapper(X,Y))