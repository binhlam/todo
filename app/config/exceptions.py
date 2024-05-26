class RecordNotFound(Exception):
    def __init__(self, record_type: str, record_name: str, record_val: str):
        self.record_type = record_type
        self.record_name = record_name
        self.record_val = record_val
        super().__init__(f"{record_type} with {record_name} {record_val} not found")

class CreateRecordError(Exception):
    def __init__(self, record_type: str):
        self.record_type = record_type
        super().__init__(f"Cannot create {record_type}")

class UpdateRecordError(Exception):
    def __init__(self, record_type: str, record_id: int):
        self.record_type = record_type
        self.record_id = record_id
        super().__init__(f"Cannot update {record_type} with ID {record_id}")

class DeleteRecordError(Exception):
    def __init__(self, record_type: str, record_id: int):
        self.record_type = record_type
        self.record_id = record_id
        super().__init__(f"Cannot delete {record_type} with ID {record_id}")

class PermissionDenied(Exception):
    def __init__(self, error_message: str = 'Permission Denied'):
        self.error_message = error_message
        super().__init__(self.error_message)

class Error(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message
        super().__init__(self.error_message)
