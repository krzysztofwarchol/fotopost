import os
import torch
from torch import nn
from torchvision import transforms
from torchvision import models
from PIL import Image
import numpy as np
from app.ml_model.resnext50 import Resnext50


model_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "ml_model\\cnn_model.pth"
)

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

transform = transforms.Compose(
    [
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ]
)

device = "cpu"

loaded_model = Resnext50(n_classes=27)

loaded_model.load_state_dict(torch.load(f=model_path, map_location=torch.device("cpu")))

loaded_model.to(device)


def predict_tags(image_path):
    image = Image.open(image_path)

    transform_image = transform(image)

    loaded_model.eval()

    transform_image = transform_image.to(device)

    classes = [
        "house",
        "birds",
        "sun",
        "valley",
        "nighttime",
        "boats",
        "mountain",
        "tree",
        "snow",
        "beach",
        "vehicle",
        "rocks",
        "reflection",
        "sunset",
        "road",
        "flowers",
        "ocean",
        "lake",
        "window",
        "plants",
        "buildings",
        "grass",
        "water",
        "animal",
        "person",
        "clouds",
        "sky",
    ]

    with torch.no_grad():
        raw_pred = loaded_model(transform_image.unsqueeze(0)).cpu().numpy()[0]
        raw_pred = np.array(raw_pred > 0.5, dtype=float)

    predicted_labels = np.array(classes)[np.argwhere(raw_pred > 0)[:, 0]]
    if not len(predicted_labels):
        predicted_labels = ["tag not detected"]

    return predicted_labels
