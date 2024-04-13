import os
import sys

import numpy as np
import pandas as pd
from bank_churn.entity.config_entity import BankChurnPredictorConfig
from bank_churn.entity.s3_estimator import bankchurnEstimator
from bank_churn.exception import BankChurnException
from bank_churn.logger import logging
from bank_churn.utils.main_utils import read_yaml_file
from pandas import DataFrame


class BankChurnData:
    def __init__(self,
                credit_score,
                country,
                gender,
                age,
                tenure,
                balance,
                products_number,
                credit_card,
                active_member,
                estimated_salary
                ):
        """
        Usvisa Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.credit_score = credit_score
            self.country = country
            self.gender = gender
            self.age = age
            self.tenure = tenure
            self.balance = balance
            self.products_number = products_number
            self.credit_card = credit_card
            self.active_member = active_member
            self.estimated_salary = estimated_salary


        except Exception as e:
            raise BankChurnException(e, sys) from e

    def get_bankchurn_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            
            bankchurn_input_dict = self.get_bankchurn_data_as_dict()
            return DataFrame(bankchurn_input_dict)
        
        except Exception as e:
            raise BankChurnException(e, sys) from e


    def get_bankchurn_data_as_dict(self):
        """
        This function returns a dictionary from USvisaData class input 
        """
        logging.info("Entered get_usvisa_data_as_dict method as USvisaData class")

        try:
            input_data = {
                "credit_score": [self.credit_score],
                "country": [self.country],
                "gender": [self.gender],
                "age": [self.age],
                "tenure": [self.tenure],
                "balance": [self.balance],
                "products_number": [self.products_number],
                "credit_card": [self.credit_card],
                "active_member": [self.active_member],
                "estimated_salary": [self.estimated_salary],
            }

            logging.info("Created bank churn data dict")

            logging.info("Exited get_bank_churn_data_as_dict method as BankChurn class")

            return input_data

        except Exception as e:
            raise BankChurnException(e, sys) from e

class BankChurnClassifier:
    def __init__(self,prediction_pipeline_config: BankChurnPredictorConfig = BankChurnPredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise BankChurnException(e, sys)

    def predict(self, dataframe) -> str:
        """
        This is the method of USvisaClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of USvisaClassifier class")
            model = bankchurnEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise BankChurnException(e, sys)