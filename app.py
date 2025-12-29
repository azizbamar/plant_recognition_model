from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from torchvision import transforms, models
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import json
import io

app = FastAPI()

# --------------------------
#  Load PyTorch Model
# --------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

num_classes = 480

# Load labels
with open("labels.json", "r", encoding="utf-8") as f:
    labels = list(json.load(f).values())

model = models.efficientnet_b3(pretrained=False)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

state_dict = torch.load("best_model_gpu.pth", map_location=device)
model.load_state_dict(state_dict, strict=False)

model.to(device)
model.eval()

# --------------------------
#  Preprocessing
# --------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# --------------------------
#  Prediction Endpoint
# --------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    img_bytes = await file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img_tensor = transform(image).unsqueeze(0).to(device)
    print(f"Image tensor shape: {img_tensor.shape}")  # Should be [1, 3, 224, 224]

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        print(f"Softmax output: {probs}")
        conf, pred_idx = torch.max(probs, 1)

    pred_idx = pred_idx.item()
    confidence = float(conf.item())
    label = labels[pred_idx] if pred_idx < len(labels) else "Unknown"
    return {"label" : label,
    	     "confidence" : confidence*100
    	     }
    

