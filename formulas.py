"""
Geometric Formulas Module
Provides comprehensive calculations for various geometric shapes.
"""

import math
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class ShapeParameters:
    """Container for shape parameters with validation."""
    length: float = 0.0
    width: float = 0.0
    height: float = 0.0
    radius: float = 0.0
    base: float = 0.0
    side: float = 0.0
    apothem: float = 0.0
    vertices: int = 0
    major_axis: float = 0.0
    minor_axis: float = 0.0
    top_base: float = 0.0
    bottom_base: float = 0.0
    
    def validate(self, shape_type: str) -> bool:
        """Validate parameters for a specific shape type."""
        if shape_type in ['Rectangle', 'Square']:
            return self.length > 0 and self.width > 0
        elif shape_type == 'Circle':
            return self.radius > 0
        elif shape_type == 'Triangle':
            return self.base > 0 and self.height > 0
        elif shape_type == 'Trapezoid':
            return (self.top_base > 0 and self.bottom_base > 0 and 
                   self.height > 0)
        elif shape_type == 'Parallelogram':
            return self.base > 0 and self.height > 0
        elif shape_type == 'Ellipse':
            return self.major_axis > 0 and self.minor_axis > 0
        elif shape_type == 'RegularPolygon':
            return self.side > 0 and self.vertices >= 3
        elif shape_type == 'Cylinder':
            return self.radius > 0 and self.height > 0
        elif shape_type == 'Sphere':
            return self.radius > 0
        elif shape_type == 'Cone':
            return self.radius > 0 and self.height > 0
        elif shape_type == 'Pyramid':
            return self.base > 0 and self.height > 0
        return False

class GeometricFormulas:
    """Comprehensive geometric formula calculations."""
    
    @staticmethod
    def rectangle_area(length: float, width: float) -> float:
        """Calculate area of rectangle."""
        return length * width
    
    @staticmethod
    def rectangle_perimeter(length: float, width: float) -> float:
        """Calculate perimeter of rectangle."""
        return 2 * (length + width)
    
    @staticmethod
    def rectangle_volume(length: float, width: float, height: float) -> float:
        """Calculate volume of rectangular prism."""
        return length * width * height
    
    @staticmethod
    def square_area(side: float) -> float:
        """Calculate area of square."""
        return side ** 2
    
    @staticmethod
    def square_perimeter(side: float) -> float:
        """Calculate perimeter of square."""
        return 4 * side
    
    @staticmethod
    def square_volume(side: float, height: float) -> float:
        """Calculate volume of square prism."""
        return side ** 2 * height
    
    @staticmethod
    def circle_area(radius: float) -> float:
        """Calculate area of circle."""
        return math.pi * radius ** 2
    
    @staticmethod
    def circle_circumference(radius: float) -> float:
        """Calculate circumference of circle."""
        return 2 * math.pi * radius
    
    @staticmethod
    def circle_volume(radius: float) -> float:
        """Calculate volume of sphere."""
        return (4 / 3) * math.pi * radius ** 3
    
    @staticmethod
    def triangle_area(base: float, height: float) -> float:
        """Calculate area of triangle."""
        return 0.5 * base * height
    
    @staticmethod
    def triangle_perimeter(side1: float, side2: float, side3: float) -> float:
        """Calculate perimeter of triangle."""
        return side1 + side2 + side3
    
    @staticmethod
    def triangle_volume(base: float, height: float, depth: float) -> float:
        """Calculate volume of triangular prism."""
        return 0.5 * base * height * depth
    
    @staticmethod
    def trapezoid_area(top_base: float, bottom_base: float, height: float) -> float:
        """Calculate area of trapezoid."""
        return 0.5 * (top_base + bottom_base) * height
    
    @staticmethod
    def trapezoid_perimeter(top_base: float, bottom_base: float, 
                          left_side: float, right_side: float) -> float:
        """Calculate perimeter of trapezoid."""
        return top_base + bottom_base + left_side + right_side
    
    @staticmethod
    def parallelogram_area(base: float, height: float) -> float:
        """Calculate area of parallelogram."""
        return base * height
    
    @staticmethod
    def parallelogram_perimeter(base: float, side: float) -> float:
        """Calculate perimeter of parallelogram."""
        return 2 * (base + side)
    
    @staticmethod
    def ellipse_area(major_axis: float, minor_axis: float) -> float:
        """Calculate area of ellipse."""
        return math.pi * major_axis * minor_axis
    
    @staticmethod
    def ellipse_perimeter(major_axis: float, minor_axis: float) -> float:
        """Calculate approximate perimeter of ellipse (Ramanujan's approximation)."""
        a, b = major_axis, minor_axis
        h = ((a - b) / (a + b)) ** 2
        return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
    
    @staticmethod
    def regular_polygon_area(side: float, vertices: int) -> float:
        """Calculate area of regular polygon."""
        return (vertices * side ** 2) / (4 * math.tan(math.pi / vertices))
    
    @staticmethod
    def regular_polygon_perimeter(side: float, vertices: int) -> float:
        """Calculate perimeter of regular polygon."""
        return vertices * side
    
    @staticmethod
    def cylinder_volume(radius: float, height: float) -> float:
        """Calculate volume of cylinder."""
        return math.pi * radius ** 2 * height
    
    @staticmethod
    def cylinder_surface_area(radius: float, height: float) -> float:
        """Calculate surface area of cylinder."""
        return 2 * math.pi * radius * (radius + height)
    
    @staticmethod
    def sphere_volume(radius: float) -> float:
        """Calculate volume of sphere."""
        return (4 / 3) * math.pi * radius ** 3
    
    @staticmethod
    def sphere_surface_area(radius: float) -> float:
        """Calculate surface area of sphere."""
        return 4 * math.pi * radius ** 2
    
    @staticmethod
    def cone_volume(radius: float, height: float) -> float:
        """Calculate volume of cone."""
        return (1 / 3) * math.pi * radius ** 2 * height
    
    @staticmethod
    def cone_surface_area(radius: float, height: float) -> float:
        """Calculate surface area of cone."""
        slant_height = math.sqrt(radius ** 2 + height ** 2)
        return math.pi * radius * (radius + slant_height)
    
    @staticmethod
    def pyramid_volume(base_area: float, height: float) -> float:
        """Calculate volume of pyramid."""
        return (1 / 3) * base_area * height
    
    @staticmethod
    def pyramid_surface_area(base_area: float, base_perimeter: float, 
                           slant_height: float) -> float:
        """Calculate surface area of pyramid."""
        lateral_area = 0.5 * base_perimeter * slant_height
        return base_area + lateral_area

def calculate_shape_property(shape_type: str, calc_type: str, 
                           params: Dict[str, Any]) -> Optional[float]:
    """
    Calculate geometric property for any supported shape.
    
    Args:
        shape_type: Type of shape (Rectangle, Circle, Triangle, etc.)
        calc_type: Type of calculation (area, perimeter, volume, surface_area)
        params: Dictionary of shape parameters
    
    Returns:
        Calculated value or None if calculation fails
    """
    try:
        # Create parameter object
        shape_params = ShapeParameters(
            length=float(params.get('l', 0) or 0),
            width=float(params.get('w', 0) or 0),
            height=float(params.get('h', 0) or 0),
            radius=float(params.get('r', 0) or 0),
            base=float(params.get('b', 0) or 0),
            side=float(params.get('s', 0) or 0),
            apothem=float(params.get('a', 0) or 0),
            vertices=int(params.get('vertices', 0) or 0),
            major_axis=float(params.get('major', 0) or 0),
            minor_axis=float(params.get('minor', 0) or 0),
            top_base=float(params.get('top_base', 0) or 0),
            bottom_base=float(params.get('bottom_base', 0) or 0)
        )
        
        # Validate parameters
        if not shape_params.validate(shape_type):
            return None
        
        # Calculate based on shape type and calculation type
        if shape_type in ['Rectangle', 'Square']:
            if calc_type == 'area':
                if shape_type == 'Square':
                    return GeometricFormulas.square_area(shape_params.side)
                else:
                    return GeometricFormulas.rectangle_area(shape_params.length, shape_params.width)
            elif calc_type == 'perimeter':
                if shape_type == 'Square':
                    return GeometricFormulas.square_perimeter(shape_params.side)
                else:
                    return GeometricFormulas.rectangle_perimeter(shape_params.length, shape_params.width)
            elif calc_type == 'volume':
                if shape_type == 'Square':
                    return GeometricFormulas.square_volume(shape_params.side, shape_params.height)
                else:
                    return GeometricFormulas.rectangle_volume(shape_params.length, shape_params.width, shape_params.height)
        
        elif shape_type == 'Circle':
            if calc_type == 'area':
                return GeometricFormulas.circle_area(shape_params.radius)
            elif calc_type == 'perimeter':
                return GeometricFormulas.circle_circumference(shape_params.radius)
            elif calc_type == 'volume':
                return GeometricFormulas.sphere_volume(shape_params.radius)
            elif calc_type == 'surface_area':
                return GeometricFormulas.sphere_surface_area(shape_params.radius)
        
        elif shape_type == 'Triangle':
            if calc_type == 'area':
                return GeometricFormulas.triangle_area(shape_params.base, shape_params.height)
            elif calc_type == 'perimeter':
                # For perimeter, we need all three sides
                side1 = shape_params.base
                side2 = shape_params.side
                side3 = float(params.get('side3', 0) or 0)
                return GeometricFormulas.triangle_perimeter(side1, side2, side3)
            elif calc_type == 'volume':
                depth = float(params.get('depth', 0) or 0)
                return GeometricFormulas.triangle_volume(shape_params.base, shape_params.height, depth)
        
        elif shape_type == 'Trapezoid':
            if calc_type == 'area':
                return GeometricFormulas.trapezoid_area(shape_params.top_base, shape_params.bottom_base, shape_params.height)
            elif calc_type == 'perimeter':
                left_side = float(params.get('left_side', 0) or 0)
                right_side = float(params.get('right_side', 0) or 0)
                return GeometricFormulas.trapezoid_perimeter(shape_params.top_base, shape_params.bottom_base, left_side, right_side)
        
        elif shape_type == 'Parallelogram':
            if calc_type == 'area':
                return GeometricFormulas.parallelogram_area(shape_params.base, shape_params.height)
            elif calc_type == 'perimeter':
                return GeometricFormulas.parallelogram_perimeter(shape_params.base, shape_params.side)
        
        elif shape_type == 'Ellipse':
            if calc_type == 'area':
                return GeometricFormulas.ellipse_area(shape_params.major_axis, shape_params.minor_axis)
            elif calc_type == 'perimeter':
                return GeometricFormulas.ellipse_perimeter(shape_params.major_axis, shape_params.minor_axis)
        
        elif shape_type == 'RegularPolygon':
            if calc_type == 'area':
                return GeometricFormulas.regular_polygon_area(shape_params.side, shape_params.vertices)
            elif calc_type == 'perimeter':
                return GeometricFormulas.regular_polygon_perimeter(shape_params.side, shape_params.vertices)
        
        elif shape_type == 'Cylinder':
            if calc_type == 'volume':
                return GeometricFormulas.cylinder_volume(shape_params.radius, shape_params.height)
            elif calc_type == 'surface_area':
                return GeometricFormulas.cylinder_surface_area(shape_params.radius, shape_params.height)
        
        elif shape_type == 'Sphere':
            if calc_type == 'volume':
                return GeometricFormulas.sphere_volume(shape_params.radius)
            elif calc_type == 'surface_area':
                return GeometricFormulas.sphere_surface_area(shape_params.radius)
        
        elif shape_type == 'Cone':
            if calc_type == 'volume':
                return GeometricFormulas.cone_volume(shape_params.radius, shape_params.height)
            elif calc_type == 'surface_area':
                return GeometricFormulas.cone_surface_area(shape_params.radius, shape_params.height)
        
        elif shape_type == 'Pyramid':
            if calc_type == 'volume':
                base_area = float(params.get('base_area', 0) or 0)
                return GeometricFormulas.pyramid_volume(base_area, shape_params.height)
            elif calc_type == 'surface_area':
                base_area = float(params.get('base_area', 0) or 0)
                base_perimeter = float(params.get('base_perimeter', 0) or 0)
                slant_height = float(params.get('slant_height', 0) or 0)
                return GeometricFormulas.pyramid_surface_area(base_area, base_perimeter, slant_height)
        
        return None
        
    except (ValueError, TypeError, ZeroDivisionError) as e:
        print(f"Calculation error for {shape_type} {calc_type}: {e}")
        return None

def get_supported_shapes() -> Dict[str, Dict[str, list]]:
    """Get dictionary of supported shapes and their calculations."""
    return {
        'Rectangle': {
            'area': ['l', 'w'],
            'perimeter': ['l', 'w'],
            'volume': ['l', 'w', 'h']
        },
        'Square': {
            'area': ['s'],
            'perimeter': ['s'],
            'volume': ['s', 'h']
        },
        'Circle': {
            'area': ['r'],
            'perimeter': ['r'],
            'volume': ['r'],
            'surface_area': ['r']
        },
        'Triangle': {
            'area': ['b', 'h'],
            'perimeter': ['b', 's', 'side3'],
            'volume': ['b', 'h', 'depth']
        },
        'Trapezoid': {
            'area': ['top_base', 'bottom_base', 'h'],
            'perimeter': ['top_base', 'bottom_base', 'left_side', 'right_side']
        },
        'Parallelogram': {
            'area': ['b', 'h'],
            'perimeter': ['b', 's']
        },
        'Ellipse': {
            'area': ['major', 'minor'],
            'perimeter': ['major', 'minor']
        },
        'RegularPolygon': {
            'area': ['s', 'vertices'],
            'perimeter': ['s', 'vertices']
        },
        'Cylinder': {
            'volume': ['r', 'h'],
            'surface_area': ['r', 'h']
        },
        'Sphere': {
            'volume': ['r'],
            'surface_area': ['r']
        },
        'Cone': {
            'volume': ['r', 'h'],
            'surface_area': ['r', 'h']
        },
        'Pyramid': {
            'volume': ['base_area', 'h'],
            'surface_area': ['base_area', 'base_perimeter', 'slant_height']
        }
    } 
    