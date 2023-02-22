import pickle
import numpy as np
import dill
from .preprocess import preprocess_text

def logistic_regression_best(text: str):
    model = pickle.load(open("models/best_logistic_model.pickle", "rb"))
    tfidf_fit = dill.load(open("models/tfidf_trans.dill", "rb"))
    process_text = tfidf_fit.transform([text])
    predicted = model.predict_proba(process_text)
    print(predicted)
    predicted_class = np.argmax(predicted)
    print(predicted_class)
    confident = predicted[0][predicted_class] * 100
    return {"class": predicted_class, "confident": confident}
