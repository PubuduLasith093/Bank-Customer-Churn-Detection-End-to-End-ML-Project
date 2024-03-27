import sys
from bank_churn.exception import BankChurnException
from bank_churn.logger import logging

from bank_churn.components.data_ingestion import DataIngestion
# from bank_churn.components.data_validation import DataValidation
# from bank_churn.components.data_transformation import DataTransformation
# from bank_churn.components.model_trainer import ModelTrainer
# from bank_churn.components.model_evaluation import ModelEvaluation
# from bank_churn.components.model_pusher import ModelPusher

from bank_churn.entity.config_entity import (DataIngestionConfig,)
                                          

from bank_churn.entity.artifact_entity import (DataIngestionArtifact)



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        # self.data_validation_config = DataValidationConfig()
        # self.data_transformation_config = DataTransformationConfig()
        # self.model_trainer_config = ModelTrainerConfig()
        # self.model_evaluation_config = ModelEvaluationConfig()
        # self.model_pusher_config = ModelPusherConfig()


    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise BankChurnException(e, sys) from e
        

    def run_pipeline(self, ) -> None:
            """
            This method of TrainPipeline class is responsible for running complete pipeline
            """
            try:
                data_ingestion_artifact = self.start_data_ingestion()
            
            
            except Exception as e:
                raise BankChurnException(e, sys)
