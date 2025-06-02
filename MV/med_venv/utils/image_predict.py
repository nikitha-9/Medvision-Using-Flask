import torch
import torchxrayvision as xrv
from PIL import Image
import torchvision.transforms as transforms

# Load model globally once
model = xrv.models.DenseNet(weights="densenet121-res224-chex")

model.eval()

# Define image transform pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485], std=[0.229])
])

def predict_image(image_path):
    img = Image.open(image_path).convert('L')  # convert to grayscale
    img_tensor = transform(img).unsqueeze(0)  # add batch dim
    
    with torch.no_grad():
        results = model(img_tensor)[0]  # get prediction tensor
        
    # Map predictions to labels
    labels = model.pathologies  # ['Atelectasis', 'Cardiomegaly', ...]
    probs = torch.sigmoid(results)
    
    # Prepare output string of top predictions with probability > threshold (e.g., 0.5)
    threshold = 0.5
    detected = [(label, prob.item()) for label, prob in zip(labels, probs) if prob > threshold]
    
    if not detected:
        return "No significant abnormalities detected (Healthy)."
    
    output = "Detected conditions:\n"
    for label, prob in detected:
        output += f"{label}: {prob:.2f}\n"
    
    return output
