import numpy as np
from objects.Model import ModelType
np.set_printoptions(threshold=10000, suppress = True) 
import pandas as pd 
import warnings 
import matplotlib.pyplot as plt 
warnings.filterwarnings('ignore')
import seaborn as sns
from sklearn.metrics import roc_curve, auc

from sklearn.model_selection import train_test_split

from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score, f1_score, average_precision_score


def find_best_supervized_threshold(y_true, y_prob, thresholds=np.linspace(0, 1, 100)):
    best_threshold = 0.5
    best_f1 = 0
    
    for threshold in thresholds:
        y_pred = y_prob >= threshold
        f1 = f1_score(y_true, y_pred)
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    return best_threshold

def find_best_threshold_anomaly(y_true, scores):
    thresholds=np.linspace(min(scores), max(scores), 100)
    best_threshold = thresholds[0]
    best_f1 = 0
    
    for threshold in thresholds:
        y_pred = scores < threshold
        f1 = f1_score(y_true, y_pred)
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    return best_threshold

def test_strategies(strategies, y_test, results):
    for key, strategy in strategies.items():
        scores = None
        y_pred = None
        best_threshold = None
        print(strategy)
        if (type(strategy.model) == ModelType.ISOLATION_FOREST.value) or (type(strategy.model) == ModelType.LOCAL_OUTLIER_FACTOR.value):
            print('if, lof')
            scores = strategy.model.fit(strategy.X_train[strategy.y_train==0])
            scores = strategy.model.decision_function(strategy.X_test)
            best_threshold = find_best_threshold_anomaly(y_test, scores)
            y_pred = scores < best_threshold
            scores = -scores
        else:
            print('les autres')
            strategy.model.fit(strategy.X_train,strategy.y_train)
            y_pred = strategy.model.predict(strategy.X_test)
            scores = strategy.model.predict_proba(strategy.X_test)[:,1]
            best_threshold = find_best_supervized_threshold(y_test, scores)
            y_pred = scores >= best_threshold
        
        results[key] = {
                'best_strategy': strategy,
                'name': strategy.name,
                'best_threshold': abs(best_threshold.item()),
                'confusion_matrix': confusion_matrix(y_test, y_pred),
                'balanced_accuracy_score': balanced_accuracy_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
                'average_precision_score': average_precision_score(y_test, scores),
                'y_prob': scores
        }
    return results

def get_best_strategy_by_score(results):
    best_key = max(results, key=lambda k: results[k]['average_precision_score'])
    return best_key, results[best_key]

def display_metrics(results):
    for key, result in results.items():
        # Print key metrics in a formatted way
        print(f"🔹 **Model {key} {result['name']} Performance Metrics** 🔹")
        print(f"📊 Best threshold {result['best_threshold']:.4f}")
        print(f"✅ Balanced Accuracy Score: {result['balanced_accuracy_score']:.4f}")
        print(f"🎯 F1 Score: {result['f1_score']:.4f}")
        print(f"📊 Average Precision Score: {result['average_precision_score']:.4f}")
        
        cm = result["confusion_matrix"]
        
        # Convert confusion matrix to DataFrame for a clear display
        cm_df = pd.DataFrame(cm, index=["Actual Negative", "Actual Positive"], 
                                columns=["Predicted Negative", "Predicted Positive"])
        
        # Plot Confusion Matrix
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title("Confusion Matrix")
        plt.ylabel("Actual Label")
        plt.xlabel("Predicted Label")
        plt.show()

def plot_roc_curve(results, y_test):
    plt.figure(figsize=(10, 7))

    for key, result in results.items():
        # Get the predicted probabilities
        y_prob = result['y_prob']
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        # Plot ROC curve
        plt.plot(fpr, tpr, label=f"{result['name']} (AUC = {roc_auc:.3f})")

    # Plot reference line
    plt.plot([0, 1], [0, 1], 'k--', label="Random Classifier")

    # Labels and legend
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve for Different Models")
    plt.legend(loc="lower right")
    plt.grid(True)

    # Show the plot
    plt.show()
    
