from graph_db import Vrat_fotku
from base64 import b64decode

#načte zakodovanou fotku z databáze
class Read_image:
    def load(self, node_id):
        return Vrat_fotku(node_id)

#decoduje fotku 
class Decode_image:
    def decode(self, encoded_data):
        return b64decode(str(encoded_data))

#zjistí formát obrázku
class Get_image_format:
    def return_image_format(self,decoded_data):
        if decoded_data.startswith(b'\xFF\xD8\xFF'): 
            return 'image/jpeg'
        elif decoded_data.startswith(b'\x89PNG\r\n\x1A\n'): 
            return 'image/png'
        elif decoded_data.startswith(b'GIF8'): 
            return 'image/gif'
        else: 
            return None

#vrátí data o obrázku ve správném formátu
class Return_image_data:
    def pack_img_html_data(self, image_type, encoded_photo):
        return {
            "image_format": image_type,
            "image_data": encoded_photo
        }

#Facade
class Image_decoder():
    def __init__(self, node_id):
        self.read_image = Read_image()
        self.decode_image = Decode_image()
        self.get_image_format = Get_image_format()
        self.return_image_data = Return_image_data()
        self.node_id = node_id
    
    #celá operace
    def commit(self):
        encoded_data = self.read_image.load(self.node_id)
        if not encoded_data: 
            return None
        decoded_data = self.decode_image.decode(encoded_data)
        image_type =  self.get_image_format.return_image_format(decoded_data)
        compressed_format = self.return_image_data.pack_img_html_data(image_type,encoded_data)
        return compressed_format
    
    #operace vrací pouze typ fotky
    def commit_format(self,encoded_photo_data):
        decoded_data = self.decode_image.decode(encoded_photo_data)
        image_type =  self.get_image_format.return_image_format(decoded_data)
        return image_type
        

#testing
#if __name__ == "__main__":
#    image_decoder = Image_decoder(node_id=1)
#    image_decoder.commit()

