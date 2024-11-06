class DataValidator:
    def validate_data(self, data):
        """Validate data structure and content"""
        return self._check_required_columns(data) and self._check_data_types(data)
        
    def _check_required_columns(self, data):
        """Check if all required columns exist"""
        required_columns = [
            "Invoice ID", "Branch", "City", "Customer type",
            "Product line", "Unit price", "Quantity", "Total", "Date"
        ]
        return all(col in data.columns for col in required_columns)
        
    def _check_data_types(self, data):
        """Check if data types are correct"""
        pass
