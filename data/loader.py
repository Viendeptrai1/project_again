import pandas as pd
from utils.validators import DataValidator
from utils.helpers import handle_error

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.validator = DataValidator()
        
    def load_data(self):
        """Load data from CSV file"""
        try:
            data = pd.read_csv(self.file_path)
            if self.validator.validate_data(data):
                return data
        except Exception as e:
            handle_error(f"Error loading data: {str(e)}")
        return None