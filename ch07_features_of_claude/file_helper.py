from pathlib import Path

class FileHelper:

    def __init__(self, client):
        self.client = client
        

    def upload(self, file_path):
        path = Path(file_path)
        extension = path.suffix.lower()
    
        mime_type_map = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".md": "text/plain",
            ".py": "text/plain",
            ".js": "text/plain",
            ".html": "text/plain",
            ".css": "text/plain",
            ".csv": "text/csv",
            ".json": "application/json",
            ".xml": "application/xml",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
            ".jpeg": "image/jpeg",
            ".jpg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
    
        mime_type = mime_type_map.get(extension)
    
        if not mime_type:
            raise ValueError(f"Unknown mimetype for extension: {extension}")
            
        filename = path.name
    
        with open(file_path, "rb") as file:
            return self.client.beta.files.upload(file=(filename, file, mime_type))
    
    
    def list_files(self):
        return self.client.beta.files.list()
    
    
    def delete_file(self, id):
        return self.client.beta.files.delete(id)
    
    
    def download_file(self, id, filename=None):
        file_content = self.client.beta.files.download(id)
    
        if not filename:
            file_metadata = self.get_metadata(id)
            file_content.write_to_file(file_metadata.filename)
        else:
            file_content.write_to_file(filename)


    def get_metadata(self, id):
        return self.client.beta.files.retrieve_metadata(id)
