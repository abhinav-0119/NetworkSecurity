from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact

from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score
import sys

def get_classification_metric(y_true,y_pred):
    try:
        f1score=f1_score(y_true,y_pred)
        recallscore=recall_score(y_true,y_pred)
        precisionscore=precision_score(y_true,y_pred)
        accuracyscore=accuracy_score(y_true,y_pred)

        classification_metric_artifact=ClassificationMetricArtifact(
            f1=f1score,
            accuracy=accuracyscore,
            precision=precisionscore,
            recall=recallscore,
        )
        return classification_metric_artifact
    except Exception as e:
        raise CustomException(e,sys)