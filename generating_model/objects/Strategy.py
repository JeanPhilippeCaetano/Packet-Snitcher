from objects.Anomaly import AnomalyType
from objects.Model import ModelType

class Strategy:
    def __init__(self, name, model_type: ModelType, anomaly_type: AnomalyType, X_train, y_train, X_test, params={'random_state':1}):
        self.name = name
        self.model = model_type.value(**params)
        self.anomaly_type = anomaly_type
        self.X_test = X_test
        if anomaly_type != AnomalyType.NONE:
            self.X_train, self.y_train = anomaly_type.value.fit_resample(X_train, y_train)
        else:
            self.X_train, self.y_train = X_train, y_train
        
    def __str__(self):
        return (
            f"Strategy(name={self.name}, "
            f"model={self.model.__class__.__name__}, "
            f"anomaly_type={self.anomaly_type.name}, "
            f"X_train_shape={self.X_train.shape}, "
            f"y_train_shape={self.y_train.shape}, "
            f"X_test_shape={self.X_test.shape})"
        )