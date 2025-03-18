from enum import Enum
from sklearn.preprocessing import MinMaxScaler, RobustScaler

class Scaler(Enum):
    NONE = None
    MINMAX = MinMaxScaler()
    ROBUST = RobustScaler()