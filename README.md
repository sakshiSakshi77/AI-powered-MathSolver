# Canvas Math Project

A comprehensive web application for drawing math problems, performing OCR on handwritten expressions, solving mathematical problems with SymPy, and calculating geometric properties.

## Overview

This project provides a complete solution for:
- **Drawing Interface**: Interactive canvas for drawing math problems and geometric shapes
- **OCR Processing**: Advanced OCR with multiple preprocessing techniques for handwritten math
- **Math Solving**: Robust SymPy-based solver with error handling and validation
- **Geometric Calculations**: Comprehensive formulas for 2D and 3D shapes
- **AI Integration**: Optional Gemini API for step-by-step explanations

## Features

### 🎨 Drawing Interface
- Interactive HTML5 canvas for drawing math expressions
- Multi-step UI with drawing, labeling, and question input
- Support for labeling points, angles, and sides on geometric diagrams
- Automatic canvas persistence across steps

### 🔍 Advanced OCR System
- **Multiple Preprocessing Techniques**:
  - Gaussian blur for noise reduction
  - Adaptive thresholding for better binarization
  - Morphological operations (erosion and dilation)
  - Connected components analysis for noise removal
  - 3x image upscaling for better recognition

- **Multiple PSM Mode Testing**:
  - PSM 6: Uniform block of text
  - PSM 7: Single text line
  - PSM 8: Single word
  - PSM 13: Raw line (no specific orientation)

- **Math-Specific Character Enhancement**:
  - CLAHE (Contrast Limited Adaptive Histogram Equalization)
  - Bilateral filtering to preserve edges
  - Otsu's thresholding for automatic threshold selection

- **Post-Processing Corrections**:
  - `l` → `1` (lowercase L)
  - `I` → `1` (uppercase I)
  - `O` → `0` (uppercase O)
  - `o` → `0` (lowercase o)
  - `×` → `*` (multiplication symbol)
  - `÷` → `/` (division symbol)
  - `−` → `-` (minus sign)

- **EasyOCR Fallback**: Optional fallback to EasyOCR for better handwritten text recognition

### 🧮 Enhanced Math Solver
- **Robust Expression Cleaning**:
  - OCR mistake correction
  - Whitespace normalization
  - Symbol standardization

- **Intelligent Label Substitution**:
  - Variable extraction from expressions
  - Smart matching with word boundaries
  - Validation of label values

- **Expression Validation**:
  - Syntax checking
  - Balanced parentheses validation
  - Operator validation
  - Content validation

- **Enhanced Parsing**:
  - Controlled parsing with `sp.parse_expr(..., evaluate=False)`
  - Graceful error handling
  - Comprehensive logging

- **Question Preprocessing**:
  - Natural language processing ("what is", "calculate", "solve", "find")
  - Punctuation cleanup
  - Format normalization

### 📐 Geometric Formulas System
- **2D Shapes**: Rectangle, Square, Circle, Triangle, Trapezoid, Parallelogram, Ellipse, Regular Polygon
- **3D Shapes**: Cylinder, Sphere, Cone, Pyramid
- **Calculations**: Area, Perimeter, Volume, Surface Area
- **Parameter Validation**: Automatic validation of input parameters
- **Modular Design**: Easy to extend with new shapes and formulas

## Installation

### Prerequisites
- Python 3.7+
- Tesseract OCR

### Required Dependencies
```bash
pip install -r requirements.txt
```

### Optional Dependencies
For EasyOCR fallback:
```bash
pip install easyocr
```

For AI explanations (Gemini API):
```bash
pip install google-generativeai
```

### Tesseract Installation
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## Usage

### Running the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### API Endpoints

#### OCR Processing
```http
POST /ocr
Content-Type: multipart/form-data

Form data: image (file)
```

#### Math Problem Solving
```http
POST /solve
Content-Type: application/json

{
    "question": "2+3",
    "labels": [{"text": "a", "value": 5}],
    "strokes": []
}
```

#### Geometric Calculations
```http
POST /calculate
Content-Type: application/json

{
    "shape_type": "Rectangle",
    "calc_type": "area",
    "l": 5,
    "w": 3
}
```

#### Get Supported Shapes
```http
GET /shapes
```

#### Shape Analysis
```http
POST /analyze
Content-Type: multipart/form-data

Form data: image (file)
```

## Testing

### OCR Testing
```bash
python test_ocr.py path/to/your/image.png
```

### Math Solver Testing
```bash
python test_math_solver.py
```

### Geometric Formulas Testing
```bash
python test_formulas.py
```

## Configuration

### OCR Configuration
Modify parameters in `app.py`:
- **Upscaling factor**: Change `scale=3` in `upscale_image()`
- **PSM modes**: Modify the list in `try_multiple_psm_modes()`
- **Character whitelist**: Update the whitelist in the OCR endpoint
- **Post-processing rules**: Add more replacements in `post_process_ocr_text()`

### Math Solver Configuration
Modify behavior in `math_solver.py`:
- **Character Replacements**: Add more OCR corrections in `clean_math_expression()`
- **Validation Rules**: Modify validation logic in `validate_expression()`
- **Question Preprocessing**: Add more question patterns in `preprocess_question()`
- **Variable Extraction**: Customize variable detection in `extract_variables_from_expression()`

### Logging
Enable debug logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Supported Mathematical Operations

### Basic Arithmetic
- Addition, subtraction, multiplication, division
- Exponentiation (^)
- Parentheses and order of operations

### Functions
- Trigonometric: sin, cos, tan, asin, acos, atan
- Logarithmic: log, ln
- Other: sqrt, exp, abs

### Equations
- Linear equations
- Quadratic equations
- Systems of equations

### Geometric Calculations
- **Rectangle**: Area, Perimeter, Volume (prism)
- **Square**: Area, Perimeter, Volume (prism)
- **Circle**: Area, Perimeter, Volume (sphere), Surface Area
- **Triangle**: Area, Perimeter, Volume (prism)
- **Trapezoid**: Area, Perimeter
- **Parallelogram**: Area, Perimeter
- **Ellipse**: Area, Perimeter
- **Regular Polygon**: Area, Perimeter
- **Cylinder**: Volume, Surface Area
- **Sphere**: Volume, Surface Area
- **Cone**: Volume, Surface Area
- **Pyramid**: Volume, Surface Area

## Best Practices

### Drawing Math Expressions
1. **Use thick lines**: Draw numbers and symbols with clear, thick strokes
2. **White background**: Draw on a clean white canvas
3. **Good spacing**: Leave adequate space between characters
4. **Clear symbols**: Make sure +, -, *, /, = are clearly distinguishable
5. **Avoid cursive**: Use block/print style writing

### Writing Questions
1. **Be specific**: Clearly state what you want to calculate
2. **Use proper notation**: Use standard mathematical symbols
3. **Include units**: Specify units when relevant
4. **Label variables**: Use labels for geometric problems

## Troubleshooting

### OCR Issues
1. **Low accuracy**: Try drawing larger and clearer
2. **Installation problems**: Verify Tesseract installation with `tesseract --version`
3. **Performance**: Reduce PSM modes tested if speed is critical
4. **Fallback**: Install EasyOCR for better handwritten text recognition

### Math Solver Issues
1. **Parsing errors**: Check input format and use validation
2. **Label problems**: Verify label format and variable names
3. **Performance**: Monitor for complex expressions
4. **Import errors**: Ensure SymPy is installed

### Geometric Calculation Issues
1. **Invalid parameters**: Check parameter names and ensure positive values
2. **Missing parameters**: Provide all required parameters for the shape
3. **Unknown shapes**: Check supported shapes with `/shapes` endpoint

### General Issues
1. **Import errors**: Install all required dependencies
2. **API errors**: Check endpoint URLs and request format
3. **Performance**: Monitor for complex operations

## File Structure

```
canvas_project/
├── app.py                 # Main Flask application
├── math_solver.py         # Enhanced SymPy solver
├── formulas.py           # Geometric formulas system
├── gemini_helper.py      # AI explanation integration
├── read.py               # Shape analysis
├── requirements.txt      # Python dependencies
├── test_math_solver.py   # Math solver tests
├── test_formulas.py      # Geometric formulas tests
├── test_ocr.py          # OCR testing script
├── templates/
│   └── canvas.html      # Frontend interface
└── venv/                # Virtual environment
```

## Contributing

### Adding New Shapes
1. Add shape validation in `ShapeParameters.validate()`
2. Add calculation methods in `GeometricFormulas`
3. Add calculation logic in `calculate_shape_property()`
4. Update `get_supported_shapes()` with new shape info
5. Add tests in `test_formulas.py`

### Adding New OCR Corrections
1. Add character replacements in `clean_math_expression()`
2. Add post-processing rules in `post_process_ocr_text()`
3. Update test cases in `test_math_solver.py`

### Adding New Math Functions
1. Add function handling in `try_sympy_solve()`
2. Update validation in `validate_expression()`
3. Add test cases in `test_math_solver.py`

## Performance Considerations

### Optimization Tips
1. **Caching**: Consider caching results for repeated calculations
2. **Validation**: Use validation before expensive operations
3. **Logging**: Disable logging in production for better performance
4. **Error Handling**: Fail fast on obvious errors

### Memory Usage
- OCR preprocessing may use significant memory for large images
- Math solver is memory-efficient for typical expressions
- Geometric calculations use minimal memory

## License

This project is open source and available under the MIT License. 