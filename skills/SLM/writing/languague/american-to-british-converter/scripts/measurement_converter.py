#!/usr/bin/env python3
import os
import sys
import argparse
import re

class MeasurementConverter:
    def __init__(self):
        # Setup regex patterns for US Customary units
        
        # 1. Fahrenheit to Celsius
        self.fahrenheit_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(°\s*[Ff]\b|degrees?\s+[Ff]ahrenheit\b|[Ff]ahrenheit\b|F\b)',
            re.IGNORECASE
        )
        
        # 2. Pounds to Kilograms
        self.pounds_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(pounds?|lbs?)\b',
            re.IGNORECASE
        )
        
        # 3. Fluid Ounces to Milliliters
        self.fluid_ounces_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(?:fl\s*oz|fluid\s*ounces?)\b',
            re.IGNORECASE
        )
        
        # 4. Ounces to Grams
        self.ounces_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(ounces?|oz)\b',
            re.IGNORECASE
        )
        
        # 5. Inches to Centimeters (we omit 'in' to avoid preposition collisions)
        self.inches_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(inches|inch)\b',
            re.IGNORECASE
        )
        
        # 6. Feet to Meters
        self.feet_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(feet|foot|ft)\b',
            re.IGNORECASE
        )
        
        # 7. Yards to Meters
        self.yards_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(yards?|yd)\b',
            re.IGNORECASE
        )
        
        # 8. Gallons to Litres (British spelling)
        self.gallons_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(gallons?|gal)\b',
            re.IGNORECASE
        )

    def convert_fahrenheit(self, match):
        val_str = match.group(1)
        unit_str = match.group(2).lower()
        val = float(val_str)
        celsius = (val - 32) * 5 / 9
        
        # Check if Celsius should be integer or float
        if celsius.is_integer() or abs(celsius - round(celsius)) < 0.01:
            c_val = int(round(celsius))
        else:
            c_val = round(celsius, 1)
            
        if "degree" in unit_str or "celsius" in unit_str:
            if "degrees" in unit_str:
                return f"{c_val} degrees Celsius"
            elif "degree" in unit_str:
                return f"{c_val} degree Celsius"
            else:
                return f"{c_val} Celsius"
        elif "°" in match.group(0):
            return f"{c_val}°C"
        else:
            spacing = " " if " " in match.group(0) else ""
            return f"{c_val}{spacing}C"

    def convert_pounds(self, match):
        val_str = match.group(1)
        val = float(val_str)
        kg = val * 0.45359237
        
        if kg >= 10:
            kg_val = int(round(kg))
        else:
            kg_val = round(kg, 1)
            if kg_val.is_integer():
                kg_val = int(kg_val)
                
        return f"{kg_val} kg"

    def convert_fluid_ounces(self, match):
        val_str = match.group(1)
        val = float(val_str)
        ml = val * 29.5735
        ml_val = int(round(ml))
        return f"{ml_val} ml"

    def convert_ounces(self, match):
        val_str = match.group(1)
        val = float(val_str)
        g = val * 28.3495231
        
        if g >= 100:
            g_val = int(round(g))
        else:
            g_val = round(g, 1)
            if g_val.is_integer():
                g_val = int(g_val)
                
        return f"{g_val} g"

    def convert_inches(self, match):
        val_str = match.group(1)
        val = float(val_str)
        cm = val * 2.54
        
        if cm >= 10:
            cm_val = int(round(cm))
        else:
            cm_val = round(cm, 1)
            if cm_val.is_integer():
                cm_val = int(cm_val)
                
        return f"{cm_val} cm"

    def convert_feet(self, match):
        val_str = match.group(1)
        val = float(val_str)
        m = val * 0.3048
        
        m_val = round(m, 1)
        if m_val.is_integer():
            m_val = int(m_val)
            
        return f"{m_val} m"

    def convert_yards(self, match):
        val_str = match.group(1)
        val = float(val_str)
        m = val * 0.9144
        
        m_val = round(m, 1)
        if m_val.is_integer():
            m_val = int(m_val)
            
        return f"{m_val} m"

    def convert_gallons(self, match):
        val_str = match.group(1)
        val = float(val_str)
        litres = val * 3.785411784
        
        l_val = round(litres, 1)
        if l_val.is_integer():
            l_val = int(l_val)
            
        return f"{l_val} litres"

    def convert_text(self, text):
        # Order matters to prevent collision (e.g. convert fluid ounces before ounces)
        text = self.fahrenheit_pattern.sub(self.convert_fahrenheit, text)
        text = self.pounds_pattern.sub(self.convert_pounds, text)
        text = self.fluid_ounces_pattern.sub(self.convert_fluid_ounces, text)
        text = self.ounces_pattern.sub(self.convert_ounces, text)
        text = self.inches_pattern.sub(self.convert_inches, text)
        text = self.feet_pattern.sub(self.convert_feet, text)
        text = self.yards_pattern.sub(self.convert_yards, text)
        text = self.gallons_pattern.sub(self.convert_gallons, text)
        return text

def main():
    parser = argparse.ArgumentParser(description="Convert American measurement units in text and files to British/Metric equivalents.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text containing measurements to convert directly from command line")
    group.add_argument("--file", help="Path to file containing measurements to convert")
    group.add_argument("--dir", help="Path to directory to recursively convert measurements in-place")
    
    parser.add_argument("--output", help="Path to save the output file (used with --file)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the input file in-place (used with --file)")
    
    args = parser.parse_args()
    
    converter = MeasurementConverter()
    
    if args.text:
        converted = converter.convert_text(args.text)
        print(converted)
        
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' does not exist.", file=sys.stderr)
            sys.exit(1)
            
        with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        converted = converter.convert_text(content)
        
        if args.inplace:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"File '{args.file}' converted in-place.")
        elif args.output:
            out_dir = os.path.dirname(args.output)
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"File '{args.file}' converted and saved to '{args.output}'.")
        else:
            print(converted, end="")
            
    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"Error: Directory '{args.dir}' does not exist.", file=sys.stderr)
            sys.exit(1)
            
        supported_extensions = {
            '.txt', '.md', '.html', '.css', '.js', '.jsx', '.ts', '.tsx', 
            '.py', '.json', '.yaml', '.yml', '.csv', '.xml', '.ini', '.cfg'
        }
        
        converted_count = 0
        for root, _, files in os.walk(args.dir):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in supported_extensions:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        converted = converter.convert_text(content)
                        
                        if content != converted:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(converted)
                            converted_count += 1
                    except Exception as e:
                        print(f"Warning: Could not convert '{file_path}': {e}", file=sys.stderr)
                        
        print(f"Successfully converted measurements in {converted_count} files in-place in '{args.dir}'.")

if __name__ == "__main__":
    main()
