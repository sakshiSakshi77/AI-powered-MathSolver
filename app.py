import os
import cv2
import numpy as np
from read import DiagramAnalyzer
import tempfile
from math_solver import try_sympy_solve
from gemini_helper import get_gemini_explanation
from formulas import calculate_shape_property, get_supported_shapes
from PIL import Image
import pytesseract
import io
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ocr_trocr import extract_clean_math_from_image
import re


# --- OCR Preprocessing Helpers ---
# Remove pytesseract import and all pytesseract-based OCR helpers (preprocess_image_for_ocr, upscale_image, try_multiple_psm_modes, enhance_math_characters, etc.)
# Replace any call to pytesseract.image_to_string or similar with extract_math_from_image
# If there is a function or endpoint that handles OCR, update it to use extract_math_from_image

def try_easyocr_fallback(image):
    """Fallback to EasyOCR if available (requires: pip install easyocr)"""
    try:
        import easyocr
        reader = easyocr.Reader(['en'])
        results = reader.readtext(np.array(image))
        
        # Extract text from results
        text_parts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Only include high-confidence results
                text_parts.append(text)
        
        if text_parts:
            combined_text = ' '.join(text_parts)
            # Clean up common OCR mistakes for math
            cleaned = combined_text.replace('l', '1').replace('O', '0').replace('o', '0')
            print(f"EasyOCR result: {cleaned}")
            return cleaned
    except ImportError:
        print("EasyOCR not installed. Install with: pip install easyocr")
    except Exception as e:
        print(f"EasyOCR error: {e}")
    
    return None

def post_process_ocr_text(text):
    """Post-process OCR text to fix common math character misrecognitions"""
    if not text:
        return text
    
    # Common OCR mistakes for math characters
    replacements = {
        'l': '1',      # lowercase L often misread as 1
        'I': '1',      # uppercase I often misread as 1
        'O': '0',      # uppercase O often misread as 0
        'o': '0',      # lowercase o often misread as 0
        'S': '5',      # S sometimes misread as 5
        's': '5',      # s sometimes misread as 5
        'G': '6',      # G sometimes misread as 6
        'g': '9',      # g sometimes misread as 9
        'B': '8',      # B sometimes misread as 8
        'Z': '2',      # Z sometimes misread as 2
        'z': '2',      # z sometimes misread as 2
        '×': '*',      # multiplication symbol
        '÷': '/',      # division symbol
        '−': '-',      # minus sign
        '=': '=',      # equals sign
        '(': '(',      # parentheses
        ')': ')',
        '[': '(',
        ']': ')',
        '{': '(',
        '}': ')',
    }
    
    # Apply replacements
    processed = text
    for old, new in replacements.items():
        processed = processed.replace(old, new)
    
    # Remove extra spaces and normalize
    processed = ' '.join(processed.split())
    
    # Remove non-math characters (keep only allowed characters)
    allowed_chars = '0123456789+-*/=().xX '
    processed = ''.join(c for c in processed if c in allowed_chars)
    
    return processed.strip()
# --- End OCR Preprocessing Helpers ---


# Remove pytesseract.pytesseract.tesseract_cmd line


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('canvas.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400
    analyzer = DiagramAnalyzer(image_array=img)
    analyzer.load_image()
    thresh = analyzer.preprocess_image()
    edges = analyzer.detect_edges()
    contours = analyzer.find_contours(edges)
    analyzer.analyze_all_shapes(contours)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
        vis_path = tmpfile.name
    analyzer.create_visualization(contours, vis_path)
    with open(vis_path, 'rb') as f:
        vis_bytes = f.read()
    
    import base64
    vis_b64 = base64.b64encode(vis_bytes).decode('utf-8')
    os.remove(vis_path)
    return jsonify({
        'results': analyzer.results,
        'visualization': vis_b64
    })

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    try:
        pil_img = Image.open(file.stream)
        
        # Try multiple preprocessing approaches
        results = []
        
        # Approach 1: Enhanced preprocessing
        # preprocessed = preprocess_image_for_ocr(pil_img) # Removed
        # upscaled = upscale_image(preprocessed, scale=3) # Removed
        whitelist = '0123456789+-*/=().xX'
        raw_ocr, clean_math = extract_clean_math_from_image(pil_img) # Replaced
        if raw_ocr:
            results.append(raw_ocr)
        
        # Approach 2: Math character enhancement
        # enhanced = enhance_math_characters(pil_img) # Removed
        # upscaled_enhanced = upscale_image(enhanced, scale=3) # Removed
        if clean_math:
            results.append(clean_math)
        
        # Approach 3: Original image with different preprocessing
        if len(results) < 2:
            # Simple thresholding approach
            img_array = np.array(pil_img)
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = img_array
            
            # Apply different thresholding
            _, simple_thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            simple_img = Image.fromarray(simple_thresh)
            # upscaled_simple = upscale_image(simple_img, scale=3) # Removed
            text3 = extract_clean_math_from_image(simple_img) # Replaced
            if text3 and text3 not in results:
                results.append(text3)
        
        # Choose the best result (most characters, or most math-like)
        if results:
            # Prefer results with more math symbols
            math_symbols = '+-*/=()'
            best_result = max(results, key=lambda x: sum(1 for c in x if c in math_symbols) + len(x))
            # Post-process the result
            processed_result = post_process_ocr_text(best_result)
            print(f"OCR OUTPUT (best of {len(results)} attempts): {best_result}")
            print(f"Post-processed result: {processed_result}")
            
            if not re.search(r'[+\-*/^=]', processed_result):
                return jsonify({'error': 'No math operator detected in OCR output.', 'ocr_output': best_result, 'postprocessed': processed_result})
            else:
                clean_math = processed_result.strip()
                print("🧮 Sending to SymPy:", clean_math)
                result, steps, error = try_sympy_solve(clean_math)
                # Convert result to string for JSON serialization
                result_str = str(result) if result is not None else None
                return jsonify({'ocr_output': best_result, 'postprocessed': processed_result, 'result': result_str, 'steps': steps, 'error': error})
        else:
            # Try EasyOCR as fallback
            print("Tesseract failed, trying EasyOCR fallback...")
            easyocr_result = try_easyocr_fallback(pil_img)
            if easyocr_result:
                processed_easyocr = post_process_ocr_text(easyocr_result)
                return jsonify({'text': processed_easyocr})
            else:
                print("All OCR methods failed to extract any text")
                return jsonify({'text': ''})
            
    except Exception as e:
        print(f"OCR error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    """Enhanced calculate endpoint with support for all geometric shapes."""
    data = request.get_json() or {}
    shape_type = data.get('shape_type')
    calc_type = data.get('calc_type')
    
    print(f"Calculating {calc_type} for {shape_type}")
    print(f"Parameters: {data}")
    
    if not shape_type or not calc_type:
        return jsonify({'error': 'Missing shape_type or calc_type'}), 400
    
    try:
        # Use the new formulas module
        result = calculate_shape_property(shape_type, calc_type, data)
        
        if result is not None:
            print(f"Calculation result: {result}")
            return jsonify({
                'result': result,
                'shape_type': shape_type,
                'calc_type': calc_type,
                'success': True
            })
        else:
            print(f"Calculation failed for {shape_type} {calc_type}")
            return jsonify({
                'error': f'Invalid parameters for {shape_type} {calc_type} calculation',
                'shape_type': shape_type,
                'calc_type': calc_type,
                'success': False
            }), 400
            
    except Exception as e:
        print(f"Calculation error: {e}")
        return jsonify({
            'error': f'Calculation error: {str(e)}',
            'shape_type': shape_type,
            'calc_type': calc_type,
            'success': False
        }), 400

@app.route('/shapes', methods=['GET'])
def get_shapes():
    """Get list of supported shapes and their required parameters."""
    try:
        supported_shapes = get_supported_shapes()
        return jsonify({
            'shapes': supported_shapes,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving shapes: {str(e)}',
            'success': False
        }), 500

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json() or {}
    labels = data.get('labels', [])
    question = data.get('question', '')
    strokes = data.get('strokes', [])

    print(f"Solving question: '{question}'")
    print(f"Labels: {labels}")

    # Try SymPy with improved error handling
    sympy_result, sympy_steps, sympy_error = try_sympy_solve(question, labels)

    if sympy_error:
        print(f"SymPy error: {sympy_error}")
        return jsonify({
            'sympy_result': None,
            'sympy_steps': f"Error: {sympy_error}",
            'error': sympy_error
        })
    
    if sympy_result is not None:
        print(f"SymPy result: {sympy_result}")
        return jsonify({
            'sympy_result': str(sympy_result),
            'sympy_steps': sympy_steps,
            'success': True
        })
    else:
        print("No result from SymPy")
        return jsonify({
            'sympy_result': None,
            'sympy_steps': "Could not solve the problem with the given input.",
            'error': "No solution found"
        })

if __name__ == '__main__':
    app.run(debug=True) 
