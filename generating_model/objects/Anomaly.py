from enum import Enum
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks

class AnomalyType(Enum):
    NONE = None
    SMOTE = SMOTE(random_state=1)
    TOMEK = TomekLinks()