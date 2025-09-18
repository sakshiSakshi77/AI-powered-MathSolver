import sympy as sp
import re
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_math_expression(expr):
    """
    Clean and normalize math expression for better parsing.
    """
    if not expr:
        return ""
    
    # Remove extra whitespace
    expr = re.sub(r'\s+', ' ', expr.strip())
    
    # Remove trailing dots/periods that cause syntax errors
    expr = expr.rstrip('.')
    
    # Fix common OCR mistakes that might have been missed
    replacements = {
        'l': '1',      # lowercase L
        'I': '1',      # uppercase I
        'O': '0',      # uppercase O
        'o': '0',      # lowercase o
        '×': '*',      # multiplication symbol
        '÷': '/',      # division symbol
        '−': '-',      # minus sign
        '²': '^2',     # squared
        '³': '^3',     # cubed
        '√': 'sqrt',   # square root
        'π': 'pi',     # pi
        '∞': 'oo',     # infinity
    }
    
    for old, new in replacements.items():
        expr = expr.replace(old, new)
    
    # Fix spacing around operators
    expr = re.sub(r'(\d+)([+\-*/^=])', r'\1 \2', expr)
    expr = re.sub(r'([+\-*/^=])(\d+)', r'\1 \2', expr)
    
    # Fix function calls
    expr = re.sub(r'(\w+)\(', r'\1(', expr)
    
    return expr

def degrees_to_radians(expr):
    """
    Convert degree-based trigonometric functions to radians.
    """
    if not expr:
        return expr
    
    # More robust pattern matching for trig functions
    patterns = [
        (r'sin\(([^)]+)\)', r'sin((\1)*pi/180)'),
        (r'cos\(([^)]+)\)', r'cos((\1)*pi/180)'),
        (r'tan\(([^)]+)\)', r'tan((\1)*pi/180)'),
        (r'asin\(([^)]+)\)', r'asin((\1)*pi/180)'),
        (r'acos\(([^)]+)\)', r'acos((\1)*pi/180)'),
        (r'atan\(([^)]+)\)', r'atan((\1)*pi/180)'),
    ]
    
    for pattern, replacement in patterns:
        expr = re.sub(pattern, replacement, expr)
    
    return expr

def extract_variables_from_expression(expr):
    """
    Extract variable names from a mathematical expression.
    """
    if not expr:
        return set()
    
    # Pattern to match variable names (letters, possibly with subscripts)
    var_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    variables = set(re.findall(var_pattern, expr))
    
    # Remove common function names and constants
    excluded = {
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
        'sqrt', 'log', 'ln', 'exp', 'abs',
        'pi', 'e', 'oo', 'inf', 'nan'
    }
    
    return variables - excluded

def substitute_labels(expr, labels):
    """
    Substitute label values into expression, ignoring irrelevant labels.
    """
    if not expr or not labels:
        return expr
    
    # Extract variables from the expression
    expr_variables = extract_variables_from_expression(expr)
    logger.info(f"Variables found in expression: {expr_variables}")
    
    # Build substitution dictionary
    subs = {}
    for lab in labels:
        if not isinstance(lab, dict):
            continue
            
        if 'value' in lab and 'text' in lab:
            var_name = str(lab['text']).strip()
            if var_name in expr_variables:
                try:
                    subs[var_name] = float(lab['value'])
                    logger.info(f"Substituting {var_name} = {lab['value']}")
                except (ValueError, TypeError):
                    logger.warning(f"Invalid value for {var_name}: {lab['value']}")
                    
        elif 'text' in lab and '=' in str(lab['text']):
            try:
                var, val = str(lab['text']).split('=', 1)
                var_name = var.strip()
                if var_name in expr_variables:
                    subs[var_name] = float(val.strip())
                    logger.info(f"Substituting {var_name} = {val.strip()}")
            except (ValueError, TypeError):
                logger.warning(f"Invalid label format: {lab['text']}")
    
    # Apply substitutions
    for var, val in subs.items():
        # Use word boundaries to avoid partial matches
        pattern = rf'\b{re.escape(var)}\b'
        expr = re.sub(pattern, str(val), expr)
    
    return expr

def preprocess_question(question):
    """
    Preprocess the question to extract the mathematical expression.
    """
    if not question:
        return ""
    
    # Remove question words and punctuation
    question = re.sub(r'what\s+is\s+', '', question, flags=re.IGNORECASE)
    question = re.sub(r'calculate\s+', '', question, flags=re.IGNORECASE)
    question = re.sub(r'solve\s+', '', question, flags=re.IGNORECASE)
    question = re.sub(r'find\s+', '', question, flags=re.IGNORECASE)
    question = re.sub(r'=\s*\?$', '', question)
    question = re.sub(r'\?$', '', question)
    
    return question.strip()

def validate_expression(expr):
    """
    Validate if an expression is likely to be a valid mathematical expression.
    """
    if not expr:
        return False, "Empty expression"
    
    # Check for basic mathematical structure
    has_numbers = bool(re.search(r'\d', expr))
    has_operators = bool(re.search(r'[+\-*/^=]', expr))
    has_functions = bool(re.search(r'\b(sin|cos|tan|sqrt|log|ln|exp)\b', expr, re.IGNORECASE))
    
    if not (has_numbers or has_functions):
        return False, "No numbers or functions found"
    
    # Check for balanced parentheses
    if expr.count('(') != expr.count(')'):
        return False, "Unbalanced parentheses"
    
    # Check for consecutive operators (except for negative numbers)
    if re.search(r'[+\-*/^]{2,}', expr):
        return False, "Consecutive operators"
    
    return True, "Valid expression"

def try_sympy_solve(question, labels=None):
    """
    Try to solve a math problem using SymPy with robust error handling.
    Returns (result, steps, error). If cannot solve, result is None and error is set.
    """
    result = None
    steps = None
    error = None
    
    try:
        if not question:
            return None, None, "No question provided"
        
        logger.info(f"Original question: '{question}'")
        
        # Step 1: Preprocess the question
        question = preprocess_question(question)
        logger.info(f"After preprocessing: '{question}'")
        
        # Step 2: Clean the expression
        question = clean_math_expression(question)
        logger.info(f"After cleaning: '{question}'")
        
        # Step 3: Substitute labels
        question_sub = substitute_labels(question, labels)
        logger.info(f"After label substitution: '{question_sub}'")
        
        # Step 4: Validate the expression
        is_valid, validation_msg = validate_expression(question_sub)
        if not is_valid:
            return None, None, f"Invalid expression: {validation_msg}"
        
        # Step 5: Convert degrees to radians
        question_sub = degrees_to_radians(question_sub)
        logger.info(f"After degree conversion: '{question_sub}'")
        
        # Step 6: Try to parse and solve
        if '=' in question_sub:
            # Handle equations
            left, right = question_sub.split('=', 1)
            left = left.strip()
            right = right.strip()
            
            logger.info(f"Parsing equation: {left} = {right}")
            
            # Parse with evaluate=False for more control
            left_expr = sp.parse_expr(left, evaluate=False)
            right_expr = sp.parse_expr(right, evaluate=False)
            
            eq = sp.Eq(left_expr, right_expr)
            sol = sp.solve(eq)
            
            result = sol
            steps = f"Equation: {eq}\nSolution: {sol}"
            
        else:
            # Handle expressions
            logger.info(f"Parsing expression: {question_sub}")
            
            # Parse with evaluate=False for more control
            expr = sp.parse_expr(question_sub, evaluate=False)
            
            # Try to evaluate
            if hasattr(expr, 'evalf'):
                val = expr.evalf()
            else:
                val = str(expr)
            
            result = val
            steps = f"Expression: {expr}\nValue: {val}"
        
        logger.info(f"Successfully solved: {result}")
        
    except sp.SympifyError as e:
        error = f"SymPy parsing error: {str(e)}"
        logger.error(f"SymPy parsing failed: {error}")
    except Exception as e:
        error = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error: {error}")
    
    return result, steps, error

def format_solution(result, steps):
    """
    Format the solution for display.
    """
    if result is None:
        return "Could not solve the problem."
    
    if isinstance(result, list):
        if len(result) == 1:
            return f"Solution: {result[0]}\n\nSteps:\n{steps}"
        else:
            return f"Solutions: {result}\n\nSteps:\n{steps}"
    else:
        return f"Result: {result}\n\nSteps:\n{steps}" 