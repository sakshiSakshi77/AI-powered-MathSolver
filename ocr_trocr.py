import re
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import ImageOps,Image 
import torch
import numpy as np
import cv2
from typing import Union, Tuple

# Load both models for comparison
processor_handwritten = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model_handwritten = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

processor_printed = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
model_printed = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')

def preprocess_image_for_trocr(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    image = image.resize((384, 384), resample=Image.BICUBIC)
    image = ImageOps.invert(image)
    image = image.convert("L").point(lambda x: 0 if x < 128 else 255)
    image = image.convert("RGB")
    return image

def clean_math_ocr_output(text: str) -> str:
    text = text.lower().strip()
    
    # Fix common OCR mistakes
    text = text.replace("t", "+")  # 't' often misread as '+'
    text = text.replace("l", "1")  # 'l' often misread as '1'
    text = text.replace("o", "0")  # 'o' often misread as '0'
    text = text.replace("s", "5")  # 's' often misread as '5'
    
    # Remove trailing dots/periods that cause syntax errors
    text = text.rstrip('.')
    
    # More aggressive operator detection and replacement
    # If we have two numbers separated by a single character, it's likely an operator
    text = re.sub(r'(\d)\s*\.\s*(\d)', r'\1-\2', text)  # period between numbers → minus
    text = re.sub(r'(\d)\s*,\s*(\d)', r'\1-\2', text)  # comma between numbers → minus
    text = re.sub(r'(\d)\s*:\s*(\d)', r'\1-\2', text)  # colon between numbers → minus
    
    # If still no operator and two numbers separated by space, add plus
    '''
    if not re.search(r'[+\-*/^=]', text):
        text = re.sub(r'(\d)\s+(\d)', r'\1+\2', text)
    '''
    if not re.search(r'[+\-*/^=]', text):
        nums = re.findall(r'\d+', text)
        if len(nums) == 2 and len(text.split()) == 2:
            text = f"{nums[0]}+{nums[1]}"
    
    # Remove any remaining non-math characters
    text = re.sub(r'[^0-9a-z+\-*/^=(). ]', '', text)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_clean_math_from_image(image_input: Union[str, Image.Image], use_printed_model: bool = False) -> Tuple[str, str]:
    if isinstance(image_input, str):
        image = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        image = image_input
    else:
        raise ValueError("image_input must be a file path or PIL Image")

    try:
        preprocessed = preprocess_image_for_trocr(image)
        preprocessed.save("debug_preprocessed.png")
        print("🔍 Saved preprocessed image as debug_preprocessed.png")
        
        # Choose model based on parameter
        if use_printed_model:
            processor = processor_printed
            model = model_printed
            print("📝 Using printed model")
        else:
            processor = processor_handwritten
            model = model_handwritten
            print("✍️ Using handwritten model")
        
        inputs = processor(images=preprocessed, return_tensors="pt").pixel_values.to("cpu")
        model.to("cpu")
        with torch.no_grad():
            generated_ids = model.generate(inputs)
        raw_ocr_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        cleaned = clean_math_ocr_output(raw_ocr_text)
        print("🧠 OCR raw output:", repr(raw_ocr_text))
        print("🧠 Cleaned math output:", repr(cleaned))
        if not raw_ocr_text:
            print("❌ TrOCR returned empty string.")
        return raw_ocr_text, cleaned
    except Exception as e:
        print(f"❌ ERROR during TrOCR inference: {e}")
        return "", "" 