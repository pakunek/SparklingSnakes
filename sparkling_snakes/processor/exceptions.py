class InvalidFile(FileNotFoundError):
    def __init__(self, *, file_path: str = '<unknown>'):
        self.message = f'Invalid file provided for processing: {file_path}'
        super().__init__(self.message)
