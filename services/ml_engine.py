
import numpy as np 
from sklearn.linear_model import  LinearRegression 

# Example training data
# queue size -> wait time

X = np.array([[1],[2],[3],[4],[5]])
y = np.array([5,10,15,20,25])

model = LinearRegression()
model.fit(X,y)

def predict_wait_time(total_service_time,doctors=1):
    """
    Predict waiting time based on workload

    Formula:
    waiting time = total service time ahead / doctors
    """

    if doctors <= 0 :
        doctors = 1

    estimated_wait = total_service_time / doctors

    return round(estimated_wait , 2)

