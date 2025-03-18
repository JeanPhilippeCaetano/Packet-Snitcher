from enum import Enum
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

class ModelType(Enum):
    LOGISTIC_REGRESSION = LogisticRegression
    RANDOM_FOREST = RandomForestClassifier
    ISOLATION_FOREST = IsolationForest
    LOCAL_OUTLIER_FACTOR = LocalOutlierFactor