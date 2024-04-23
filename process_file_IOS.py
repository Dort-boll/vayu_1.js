import os
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class AdvancedFileProcessor:
    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("AdvancedFileProcessor")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def load_data(self, file_path):
        self.logger.info(f"Loading data from: {file_path}")
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Only CSV, XLSX, or XLS files are supported.")
        return df

    def preprocess_data(self, df):
        self.logger.info("Preprocessing data...")
        # Example preprocessing steps: handling missing values, encoding categorical variables, etc.
        # For demonstration, we'll just drop any rows with missing values
        df.dropna(inplace=True)
        return df

    def train_model(self, df):
        self.logger.info("Training machine learning model...")
        X = df.drop(columns=['target'])
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model, X_test, y_test

    def evaluate_model(self, model, X_test, y_test):
        self.logger.info("Evaluating model performance...")
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        self.logger.info(f"Accuracy: {accuracy}")
        self.logger.info(f"Classification Report:\n{report}")

    def fine_tune_model(self, model, df):
        self.logger.info("Fine-tuning model...")
        # Example fine-tuning: hyperparameter optimization, feature selection, etc.
        # For demonstration, we'll retrain the model with more trees
        model.n_estimators = 200
        X = df.drop(columns=['target'])
        y = df['target']
        model.fit(X, y)
        self.logger.info("Model fine-tuning completed.")

if __name__ == "__main__":
    file_processor = AdvancedFileProcessor()
    file_path = "data.csv"

    df = file_processor.load_data(file_path)
    df = file_processor.preprocess_data(df)
    model, X_test, y_test = file_processor.train_model(df)
    file_processor.evaluate_model(model, X_test, y_test)

    # Fine-tune the model
    file_processor.fine_tune_model(model, df)
    file_processor.evaluate_model(model, X_test, y_test)
