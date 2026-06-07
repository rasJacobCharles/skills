#!/usr/bin/env python3
import os
import sys
import argparse
import re

class AmericanToBritishConverter:
    def __init__(self):
        # A dictionary of exact mappings (keys are lowercase US, values are lowercase UK)
        self.vocab_map = {
            "apartment": "flat",
            "apartments": "flats",
            "elevator": "lift",
            "elevators": "lifts",
            "truck": "lorry",
            "trucks": "lorries",
            "diaper": "nappy",
            "diapers": "nappies",
            "gasoline": "petrol",
            "gas station": "petrol station",
            "gas stations": "petrol stations",
            "highway": "motorway",
            "highways": "motorways",
            "sidewalk": "pavement",
            "sidewalks": "pavements",
            "flashlight": "torch",
            "flashlights": "torches",
            "garbage": "rubbish",
            "trash": "rubbish",
            "vacation": "holiday",
            "vacations": "holidays",
            "soccer": "football",
            "mailman": "postman",
            "mailmen": "postmen",
            "parking lot": "car park",
            "parking lots": "car parks",
            "windshield": "windscreen",
            "jello": "jelly",
            
            # Food and ingredient vocabulary differences
            "cilantro": "coriander",
            "zucchini": "courgette",
            "zucchinis": "courgettes",
            "eggplant": "aubergine",
            "eggplants": "aubergines",
            "arugula": "rocket",
            "green onion": "spring onion",
            "green onions": "spring onions",
            "oatmeal": "porridge",
            
            "cozy": "cosy",
            "gray": "grey",
            "grays": "greys",
            "grayed": "greyed",
            "graying": "greying",
            "grayish": "greyish",
            "mustache": "moustache",
            "mustaches": "moustaches",
            "skeptical": "sceptical",
            "skepticism": "scepticism",
            "airplane": "aeroplane",
            "airplanes": "aeroplanes",
            "aluminum": "aluminium",
            "jewelry": "jewellery",
            "tires": "tyres",
            
            # Medical/Greek/Latin ae/oe simplifications
            "leukemia": "leukaemia",
            "leukemias": "leukaemias",
            "anesthesia": "anaesthesia",
            "anesthetic": "anaesthetic",
            "anesthetics": "anaesthetics",
            "pediatric": "paediatric",
            "pediatrics": "paediatrics",
            "pediatrician": "paediatrician",
            "pediatricians": "paediatricians",
            "encyclopedia": "encyclopaedia",
            "encyclopedias": "encyclopaedias",
            "gynecology": "gynaecology",
            "orthopedic": "orthopaedic",
            "orthopedics": "orthopaedics",
            "hemophilia": "haemophilia",
            "hemorrhage": "haemorrhage",
            "hemorrhages": "haemorrhages",
            "hemorrhaged": "haemorrhaged",
            "hemorrhaging": "haemorrhaging",
            "esophagus": "oesophagus",
            "fetus": "foetus",
            "fetuses": "foetuses",
            "fetal": "foetal",
            "estrogen": "oestrogen",
            "homeopathy": "homoeopathy",
            "diarrhea": "diarrhoea",
            "celiac": "coeliac",
            "maneuver": "manoeuvre",
            "maneuvers": "manoeuvres",
            "maneuvered": "manoeuvred",
            "maneuvering": "manoeuvring",
            
            # Other common spelling differences
            "mold": "mould",
            "molds": "moulds",
            "molded": "moulded",
            "molding": "moulding",
            "sulfur": "sulphur",
            "sulfate": "sulphate",
            "sulfide": "sulphide",
            "judgment": "judgement",
            "judgments": "judgements",
            "acknowledgment": "acknowledgement",
            "acknowledgments": "acknowledgements",
            "ax": "axe",
            
            # Directional suffixes -ward to -wards
            "toward": "towards",
            "afterward": "afterwards",
            "backward": "backwards",
            "outward": "outwards",
            "inward": "inwards",
            "downward": "downwards",
            "upward": "upwards",
            
            # Verb forms of practice
            "practicing": "practising",
            "practiced": "practised",
            
            # Cognizance
            "cognizant": "cognisant",
            "cognizance": "cognisance",
            
            # Enrol/Fulfil/Skilful spelling rules
            "enroll": "enrol",
            "enrolls": "enrols",
            "enrollment": "enrolment",
            "fulfill": "fulfil",
            "fulfills": "fulfils",
            "fulfillment": "fulfilment",
            "skillful": "skilful",
            "skillfully": "skilfully",
            
            # Words ending in -or that become -our
            "color": "colour",
            "colors": "colours",
            "colored": "coloured",
            "coloring": "colouring",
            "colorful": "colourful",
            "colorless": "colourless",
            
            "flavor": "flavour",
            "flavors": "flavours",
            "flavored": "flavoured",
            "flavoring": "flavouring",
            "flavorful": "flavourful",
            "flavorless": "flavourless",
            
            "behavior": "behaviour",
            "behaviors": "behaviours",
            "behavioral": "behavioural",
            
            "honor": "honour",
            "honors": "honours",
            "honored": "honoured",
            "honoring": "honouring",
            "honorable": "honourable",
            "honorably": "honourably",
            
            "labor": "labour",
            "labors": "labours",
            "labored": "laboured",
            "laboring": "labouring",
            
            "favor": "favour",
            "favors": "favours",
            "favored": "favoured",
            "favoring": "favouring",
            "favorite": "favourite",
            "favorites": "favourites",
            "favorable": "favourable",
            "favourably": "favourably",
            "unfavorable": "unfavourable",
            "unfavourably": "unfavourably",
            
            "humor": "humour",
            "humors": "humours",
            
            "rumor": "rumour",
            "rumors": "rumours",
            "rumored": "rumoured",
            "rumoring": "rumouring",
            
            "tumor": "tumour",
            "tumors": "tumours",
            
            "valor": "valour",
            "vigor": "vigour",
            
            "splendor": "splendour",
            "splendors": "splendours",
            
            "rancor": "rancour",
            
            "savior": "saviour",
            "saviors": "saviours",
            
            "clamor": "clamour",
            "clamored": "clamoured",
            "clamoring": "clamouring",
            
            "candor": "candour",
            
            "armor": "armour",
            "armored": "armoured",
            
            "harbor": "harbour",
            "harbors": "harbours",
            "harbored": "harboured",
            "harboring": "harbouring",
            
            "neighbor": "neighbour",
            "neighbors": "neighbours",
            "neighbored": "neighbouring",
            "neighboring": "neighbouring",
            "neighborhood": "neighbourhood",
            "neighborhoods": "neighbourhoods",
            
            "endeavor": "endeavour",
            "endeavors": "endeavours",
            "endeavored": "endeavoured",
            "endeavoring": "endeavouring",
            
            # Words ending in -er that become -re
            "center": "centre",
            "centers": "centres",
            "centered": "centred",
            "centering": "centring",
            
            "theater": "theatre",
            "theaters": "theatres",
            
            "caliber": "calibre",
            "calibers": "calibres",
            
            "fiber": "fibre",
            "fibers": "fibres",
            
            "luster": "lustre",
            
            "meter": "metre",
            "meters": "metres",
            
            "liter": "litre",
            "liters": "litres",
            
            "mitre": "mitre",
            
            "kilometer": "kilometre",
            "kilometers": "kilometres",
            "centimeter": "centimetre",
            "centimeters": "centimetres",
            "millimeter": "millimetre",
            "millimeters": "millimetres",
            "nanometer": "nanometre",
            "nanometers": "nanometres",
            "micrometer": "micrometre",
            "micrometers": "micrometres",
            "decimeter": "decimetre",
            "decimeters": "decimetres",
            
            # -se/-ce words
            "defense": "defence",
            "defenses": "defences",
            
            "offense": "offence",
            "offenses": "offences",
            
            "pretense": "pretence",
            "pretenses": "pretences",
            
            "license": "licence",
            "licenses": "licences",
        }
        
    def preserve_case(self, original, replacement):
        if original.isupper():
            return replacement.upper()
        if original.istitle():
            return " ".join(w.capitalize() for w in replacement.split())
        if original.islower():
            return replacement.lower()
        if original and original[0].isupper():
            return replacement[0].upper() + replacement[1:]
        return replacement

    def convert_text(self, text):
        # Phase 1: Exact word/phrase replacements
        sorted_keys = sorted(self.vocab_map.keys(), key=len, reverse=True)
        
        def vocab_replace(match):
            matched_text = match.group(0)
            key_lower = matched_text.lower()
            replacement = self.vocab_map.get(key_lower)
            if replacement:
                return self.preserve_case(matched_text, replacement)
            return matched_text
            
        vocab_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b', 
            re.IGNORECASE
        )
        text = vocab_pattern.sub(vocab_replace, text)
        
        # Phase 2: Suffix Rules
        
        # Rule 2.1: -ize -> -ise (excluding exceptions like seize, size, prize, capsize)
        def ize_replace(match):
            word = match.group(0)
            word_lower = word.lower()
            
            # Check for size/seize/prize exceptions
            is_exception = False
            for exc in ["seiz", "siz", "priz", "capsiz", "assiz", "oversiz", "downsiz", "midsiz", "maiz"]:
                if word_lower.startswith(exc):
                    is_exception = True
                    break
            if is_exception:
                return word
            
            replacement = word_lower
            if "ization" in word_lower:
                replacement = word_lower.replace("ization", "isation")
            elif "izing" in word_lower:
                replacement = word_lower.replace("izing", "ising")
            elif "ize" in word_lower:
                replacement = word_lower.replace("ize", "ise")
            
            return self.preserve_case(word, replacement)

        ize_pattern = re.compile(r'\b\w+iz(?:e[ds]?|ing|ation[s]?)\b', re.IGNORECASE)
        text = ize_pattern.sub(ize_replace, text)

        # Rule 2.2: -yze -> -yse (analyze -> analyse)
        def yze_replace(match):
            word = match.group(0)
            word_lower = word.lower()
            replacement = word_lower.replace("yze", "yse").replace("yzing", "ysing")
            return self.preserve_case(word, replacement)
            
        yze_pattern = re.compile(r'\b\w+yz(?:e[ds]?|ing)\b', re.IGNORECASE)
        text = yze_pattern.sub(yze_replace, text)
        
        # Rule 2.3: Double consonants (traveler -> traveller)
        def double_l_replace(match):
            word = match.group(0)
            stem = match.group(1)
            suffix = match.group(2)
            replacement = stem.lower() + "l" + suffix.lower()
            return self.preserve_case(word, replacement)
            
        double_l_pattern = re.compile(
            r'\b(travel|cancel|model|fuel|signal|label|quarrel|marvel|jewel)(ed|er|ing|ers)\b', 
            re.IGNORECASE
        )
        text = double_l_pattern.sub(double_l_replace, text)
        
        # Rule 2.4: -og -> -ogue (catalog -> catalogue)
        def ogue_replace(match):
            word = match.group(0)
            stem = match.group(1)
            plural = match.group(2)
            replacement = stem.lower() + "ue" + plural.lower()
            return self.preserve_case(word, replacement)
            
        ogue_pattern = re.compile(r'\b(catalog|dialog|analog|travelog)(s?)\b', re.IGNORECASE)
        text = ogue_pattern.sub(ogue_replace, text)

        return text

def main():
    parser = argparse.ArgumentParser(description="Convert American English text and files to British English.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text to convert directly from command line")
    group.add_argument("--file", help="Path to file to convert")
    group.add_argument("--dir", help="Path to directory to recursively convert in-place")
    
    parser.add_argument("--output", help="Path to save the output file (used with --file)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the input file in-place (used with --file)")
    
    args = parser.parse_args()
    
    converter = AmericanToBritishConverter()
    
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
                        
        print(f"Successfully converted {converted_count} files in-place in '{args.dir}'.")

if __name__ == "__main__":
    main()
