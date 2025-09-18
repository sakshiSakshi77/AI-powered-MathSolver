#!/usr/bin/env python3
"""
OpenCV Image Analyzer
Analyzes drawings and diagrams using computer vision techniques
"""

import cv2
import numpy as np
import os
import sys
import argparse
from pathlib import Path
import json
from datetime import datetime

class DiagramAnalyzer:
    def __init__(self, image_path=None, image_array=None):
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'image_path': image_path,
            'image_size': None,
            'shapes': [],
            'statistics': {},
            'processing_steps': []
        }
        if image_array is not None:
            self.image = image_array
            self.results['image_size'] = {
                'width': self.image.shape[1],
                'height': self.image.shape[0],
                'channels': self.image.shape[2]
            }
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.results['processing_steps'].append("Image loaded from array and converted to grayscale")

    def load_image(self):
        """Load and validate the input image"""
        if self.image is not None:
            # Already loaded from array
            return True
        try:
            self.image = cv2.imread(self.image_path)
            if self.image is None:
                raise ValueError(f"Could not load image from {self.image_path}")
            
            self.results['image_size'] = {
                'width': self.image.shape[1],
                'height': self.image.shape[0],
                'channels': self.image.shape[2]
            }
            
            # Convert to grayscale
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.results['processing_steps'].append("Image loaded and converted to grayscale")
            
            print(f"✓ Image loaded successfully: {self.image.shape[1]}x{self.image.shape[0]}")
            return True
            
        except Exception as e:
            print(f"✗ Error loading image: {e}")
            return False
    
    def preprocess_image(self):
        """Apply preprocessing steps to enhance the image"""
        try:
            # Apply Gaussian blur to reduce noise
            self.gray = cv2.GaussianBlur(self.gray, (5, 5), 0)
            self.results['processing_steps'].append("Applied Gaussian blur (5x5)")
            
            # Apply adaptive thresholding for better edge detection
            _, thresh = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY_INV)
            self.results['processing_steps'].append("Applied binary thresholding")
            
            print("✓ Image preprocessing completed")
            return thresh
            
        except Exception as e:
            print(f"✗ Error in preprocessing: {e}")
            return None
    
    def detect_edges(self):
        """Detect edges using Canny edge detection"""
        try:
            # Canny edge detection
            edges = cv2.Canny(self.gray, 50, 150, apertureSize=3)
            self.results['processing_steps'].append("Applied Canny edge detection (50, 150)")
            
            print("✓ Edge detection completed")
            return edges
            
        except Exception as e:
            print(f"✗ Error in edge detection: {e}")
            return None
    
    def find_contours(self, edges):
        """Find contours in the edge-detected image"""
        try:
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.results['processing_steps'].append(f"Found {len(contours)} contours")
            
            print(f"✓ Found {len(contours)} contours")
            return contours
            
        except Exception as e:
            print(f"✗ Error finding contours: {e}")
            return []
    
    def analyze_shape(self, contour):
        """Analyze a single contour to determine shape properties"""
        try:
            # Calculate basic properties
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            if area < 100:  # Filter out very small shapes
                return None
            
            # Approximate contour to polygon
            epsilon = 0.02 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            vertices = len(approx)
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            # Calculate circularity
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # Determine shape type
            shape_type = "Unknown"
            confidence = 0.5
            
            if vertices == 3:
                shape_type = "Triangle"
                confidence = 0.9
            elif vertices == 4:
                if 0.95 <= aspect_ratio <= 1.05:
                    shape_type = "Square"
                    confidence = 0.9
                else:
                    shape_type = "Rectangle"
                    confidence = 0.85
            elif vertices > 4:
                if circularity > 0.7:
                    shape_type = "Circle"
                    confidence = 0.8
                else:
                    shape_type = f"Polygon ({vertices} sides)"
                    confidence = 0.7
            
            return {
                'type': shape_type,
                'confidence': confidence,
                'area': float(area),
                'perimeter': float(perimeter),
                'vertices': int(vertices),
                'aspect_ratio': float(aspect_ratio),
                'circularity': float(circularity),
                'bounding_box': {
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h)
                },
                'centroid': {
                    'x': int(x + w/2),
                    'y': int(y + h/2)
                }
            }
            
        except Exception as e:
            print(f"✗ Error analyzing shape: {e}")
            return None
    
    def analyze_all_shapes(self, contours):
        """Analyze all detected contours"""
        print(f"\n📊 Analyzing {len(contours)} contours...")
        
        shapes = []
        total_area = 0
        shape_counts = {}
        
        for i, contour in enumerate(contours):
            shape_info = self.analyze_shape(contour)
            if shape_info:
                shapes.append(shape_info)
                total_area += shape_info['area']
                
                # Count shape types
                shape_type = shape_info['type']
                shape_counts[shape_type] = shape_counts.get(shape_type, 0) + 1
                
                print(f"  Shape {i+1}: {shape_type} (Area: {shape_info['area']:.0f}px²)")
        
        # Calculate statistics
        self.results['shapes'] = shapes
        self.results['statistics'] = {
            'total_shapes': len(shapes),
            'total_area': float(total_area),
            'shape_counts': shape_counts,
            'average_area': float(total_area / len(shapes)) if shapes else 0
        }
        
        print(f"\n📈 Analysis Summary:")
        print(f"  Total shapes detected: {len(shapes)}")
        print(f"  Total area: {total_area:.0f}px²")
        print(f"  Shape distribution: {shape_counts}")
        
        return shapes
    
    def create_visualization(self, contours, output_path):
        """Create a visualization of the detected shapes"""
        try:
            # Create a copy of the original image
            vis_image = self.image.copy()
            
            # Draw contours with different colors
            colors = [
                (255, 0, 0),    # Red
                (0, 255, 0),    # Green
                (0, 0, 255),    # Blue
                (255, 255, 0),  # Cyan
                (255, 0, 255),  # Magenta
                (0, 255, 255),  # Yellow
            ]
            
            for i, contour in enumerate(contours):
                if cv2.contourArea(contour) > 100:  # Only draw significant contours
                    color = colors[i % len(colors)]
                    cv2.drawContours(vis_image, [contour], -1, color, 2)
                    
                    # Add shape label
                    shape_info = self.analyze_shape(contour)
                    if shape_info:
                        x, y = shape_info['centroid']['x'], shape_info['centroid']['y']
                        cv2.putText(vis_image, shape_info['type'], (x-30, y), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Save visualization
            cv2.imwrite(output_path, vis_image)
            print(f"✓ Visualization saved to: {output_path}")
            
        except Exception as e:
            print(f"✗ Error creating visualization: {e}")
    
    def save_results(self, output_path):
        """Save analysis results to JSON file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"✓ Results saved to: {output_path}")
            
        except Exception as e:
            print(f"✗ Error saving results: {e}")
    
    def run_analysis(self, save_visualization=True, save_json=True):
        """Run the complete analysis pipeline"""
        print(f"🔍 Starting analysis of: {self.image_path}")
        print("=" * 50)
        
        # Load image
        if not self.load_image():
            return False
        
        # Preprocess image
        thresh = self.preprocess_image()
        if thresh is None:
            return False
        
        # Detect edges
        edges = self.detect_edges()
        if edges is None:
            return False
        
        # Find contours
        contours = self.find_contours(edges)
        if not contours:
            print("✗ No contours found")
            return False
        
        # Analyze shapes
        shapes = self.analyze_all_shapes(contours)
        
        # Generate output files
        base_name = Path(self.image_path).stem
        output_dir = Path("analysis_output")
        output_dir.mkdir(exist_ok=True)
        
        if save_visualization:
            vis_path = output_dir / f"{base_name}_analysis.png"
            self.create_visualization(contours, str(vis_path))
        
        if save_json:
            json_path = output_dir / f"{base_name}_results.json"
            self.save_results(str(json_path))
        
        print("\n" + "=" * 50)
        print("🎉 Analysis completed successfully!")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Analyze drawings and diagrams using OpenCV')
    parser.add_argument('image_path', help='Path to the image file to analyze')
    parser.add_argument('--no-vis', action='store_true', help='Skip visualization output')
    parser.add_argument('--no-json', action='store_true', help='Skip JSON results output')
    
    args = parser.parse_args()
    
    # Check if image file exists
    if not os.path.exists(args.image_path):
        print(f"✗ Error: Image file '{args.image_path}' not found")
        sys.exit(1)
    
    # Create analyzer and run analysis
    analyzer = DiagramAnalyzer(args.image_path)
    success = analyzer.run_analysis(
        save_visualization=not args.no_vis,
        save_json=not args.no_json
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    # Check if OpenCV is installed
    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except ImportError:
        print("✗ Error: OpenCV not installed. Install with: pip install opencv-python")
        sys.exit(1)
    
    main()