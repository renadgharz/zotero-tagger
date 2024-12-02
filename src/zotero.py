from pyzotero import zotero
import yaml
import json
from paths import CONFIG_DIR, OUTPUTS_DIR

class ZoteroConnection:
    
    """
    A class to connect to the Zotero API.
    """
    
    def __init__(self, config_path=CONFIG_DIR + "/config.yaml"):
        
        """
        Initializes the ZoteroConnection class.
        """
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.library_id = config['library_id']
        self.api_key = config['api_key']
        self.library_type = config['library_type']
        
        self.zot = zotero.Zotero(self.library_id, self.library_type, self.api_key)
    
    def retrieve_items(self):
        
        """
        Retrieves items from the Zotero library.
        """
        
        items = self.zot.items(itemType='journalArticle')    
        return items
    
    def save_items_to_json(self, items, file_path=OUTPUTS_DIR):
        
        """
        Saves retrieved items to a JSON file.
        """
        
        with open(file_path, 'w') as f:
            json.dump(items, f, indent=4)


# test class - will need to be moved to separate unit test eventually
if __name__ == "__main__":
    client = ZoteroConnection()
    items = client.retrieve_items()
    if items:
        client.save_items_to_json(items, file_path= OUTPUTS_DIR + "/test.json")