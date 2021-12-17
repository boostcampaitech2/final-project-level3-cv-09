import torch
from typing import Optional
from PIL import Image
from io import BytesIO
import base64

def load_detection_model(model_path):
    print("load model in package")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = torch.hub.load("ultralytics/yolov5", 'custom', path=model_path, force_reload=True)
    
    return model

model = load_detection_model("best_v1.pt")

class Prediction():
    def __init__(
        self,
        img: str,
        model_path :Optional[str] = None
    ):
        if model_path:
            self.model_path = model_path
        else:
            self.model_path = "best_v1.pt"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.img = Image.open(BytesIO(base64.b64decode(img)))
        print("input image size", self.img.size)
        self.img.save("images/temp.jpg")

        if model is None:
            self.model = self.load_model()
        else:
            self.model = model

    def load_model(self):
        """[summary]
        """
        print("load model in class")
        model = torch.hub.load("ultralytics/yolov5", 'custom', path=self.model_path, force_reload=True)
        return model
    
    def validate_input(self):
        """[summary]
        """
        # get size from input
        return True

    def augmentation(self):
        """[summary]
        """
        # apply augmentation
        return

    def resize(self, img):
        """[summary]
        """

        return img

    def result_to_json(self, output):
        return [
            [
                {
                    "class": int(pred[5]),
                    "name": self.model.model.names[int(pred[5])],
                    "bbox": pred[:4].tolist(),
                    "confidence": float(pred[4]),
                }
                for pred in result
            ]
            #switch this to results.xyxy to get bbox pixels
            for result in output.xyxyn 
        ]

    def inference(self):
        """[summary]
        """
        self.model.eval()
        output = self.model(self.img)

        result = self.result_to_json(output)
        return result[0]

