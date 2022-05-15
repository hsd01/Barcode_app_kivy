from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
import cv2
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from pyzbar.pyzbar import decode
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel

class MainApp(MDApp):
    def build(self):
        self.con = 0
        self.text_data = "0_0"
        self.layout = MDBoxLayout(orientation = 'vertical')
        self.image = Image()
        self.layout.add_widget(self.image)
        self.save_img = MDRaisedButton(text="capture",
                                        pos_hint={'center_x':.5, 'center_y':.5},
                                        size_hint=(.2, .2))
        
        
        self.save_img.bind(on_press=self.img_cap)
        lbl = Label(text = self.text_data)
        self.layout.add_widget(self.save_img)
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        self.ret, self.frame = self.cap.read()
        
        #self.cap.release()
        #cv2.destroyAllWindows()
        return self.layout
    def load_video(self, *args):
        ret, frame = self.cap.read()
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        text = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt = 'bgr')
        text.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt='ubyte')
        self.image.texture = text
    def img_cap(self, *args):
        img = "Pick_cap.png"
        cv2.imwrite(img, self.image_frame)
        self.read_barcodes(self.image_frame)
        f = open("barcode_result.txt",'r')
        self.text_data = f.read()
        self.con += 1
        if self.con > 1:
            self.layout.remove_widget(self.l)
            
        self.l=MDLabel(text=self.text_data, size_hint =(1, .2), 
                  theme_text_color="Custom",
                  text_color=(0.5,0,0.5,1),
                  font_style='Caption')
        self.layout.add_widget(self.l)
        
    def read_barcodes(self, frame):
        #barcodes = pyzbar.decode(frame)
        self.frame = frame
        barcodes = decode(self.frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            #decoding the information from the barcode or QR code.
            #And then drawing a rectangle around it.
            #This helps us to see if our machine has detected the barcode/Qr code.
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(self.frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            #adding text on top of the rectangle that was created.
            #The text will show the decoded information.
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            #exporting the information into a text document.
            #If you are planning to test with multiple barcodes or QR codes, I recommend changing the document name otherwise it will overwrite.
            with open("barcode_result.txt", mode ='w') as file:
                file.write("Info:" + barcode_info)
        return self.frame

    
if __name__=='__main__':
    MainApp().run()
    self.cap.release()
    cv2.destroyAllWindows()
