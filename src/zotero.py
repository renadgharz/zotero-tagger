from pyzotero import zotero
import yaml
import json
import os
from src.paths import CONFIG_DIR, OUTPUTS_DIR

class ZoteroConnection:
    
    """
    A class to connect to the Zotero API.
    """
    
    def __init__(self, config_dir=CONFIG_DIR + "/config.yaml", log_file='processed_items.log'):
        
        """
        Initializes the ZoteroConnection class.
        """
        
        with open(config_dir, 'r') as f:
            config = yaml.safe_load(f)
        
        self.library_id = config['library_id']
        self.api_key = config['api_key']
        self.library_type = config['library_type']
        
        self.zot = zotero.Zotero(self.library_id, self.library_type, self.api_key)
    
        self.log_file = os.path.join(OUTPUTS_DIR, log_file)
        self.processed_items = self._load_processed_items()
    
    
    def retrieve_items_with_pdf(self):
        
        """
        Retrieves items with PDFs from the Zotero library.
        """
        
        items = self.zot.items(itemType='journalArticle')
        items_with_pdf = []
        
        for item in items:
            attachments = self.zot.children(item['key'], itemType='attachment')
            has_pdf = any(attachment['data']['contentType'] == 'application/pdf' for attachment in attachments)    
        
            if has_pdf:
                items_with_pdf.append(item)
                
        return items_with_pdf

 
    def _load_processed_items(self):
        
        """
        Loads processed items from the log file.
        """
        
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("")
            return set()
        
        with open(self.log_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    
    def _save_processed_items(self):
        
        """
        Saves processed items to the log file.
        """
        
        with open(self.log_file, 'w') as f:
            for item in self.processed_items:
                f.write(f"{item}\n")
    
    def _save_items_to_json(self, items, file_dir):
        
        """
        Saves retrieved items to a JSON file.
        """
        
        with open(file_dir, 'w') as f:
            json.dump(items, f, indent=4)
            
        for item in items:
            self.processed_items.add(item['key'])
        self._save_processed_items()


# test case - will need to be moved to separate unit test eventually
# if __name__ == "__main__":
#     client = ZoteroConnection()
#     items = client.retrieve_items_with_pdf()
#     if items:
#         for item in items[:-1]:
#             print(item["key"])
#         client._save_items_to_json(items, file_dir= OUTPUTS_DIR + "/test.json")