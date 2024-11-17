from pyzotero import zotero
import yaml
import json

class ZoteroConnection:
    def __init__(self, config_path="../config/config.yaml"):
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.library_id = config['library_id']
        self.api_key = config['api_key']
        self.library_type = config['library_type']
        
        self.zot = zotero.Zotero(self.library_id, self.library_type, self.api_key)
    
    def fetch_items(self):
        items = self.zot.items(itemType='journalArticle')    
        return items
    
    def save_items_to_json(self, items, file_path="../items.json"):
        with open(file_path, 'w') as f:
            json.dump(items, f, indent=4)

if __name__ == "__main__":
    client = ZoteroConnection()
    items = client.fetch_items()
    if items:
        client.save_items_to_json(items, file_path="test.json")