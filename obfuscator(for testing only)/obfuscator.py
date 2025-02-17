import jsbeautifier
import random
import re
import json
import argparse
from pathlib import Path
import esprima
import escodegen

class Obfuscator:
    def __init__(self, input_file, verbose=False):
        self.input_file = Path(input_file).resolve()
        self.input_file = Path(str(self.input_file).replace("\\", "/"))
        print(f"DEBUG: Absolute path to input file: {self.input_file}")
        self.source_code = self.load_code()
        self.ast = None
        self.verbose = verbose
        self.var_map = {}
        self.function_map = {}
        self.string_map = []

    def load_code(self):
        print(f"DEBUG: Loading code from: {self.input_file}")
        with open(self.input_file, 'r', encoding="utf-8") as f:
            code = f.read()
            print(f"DEBUG: Code loaded successfully.")
            return code

    def beautify_and_minify(self):
        # Beautify and then minify the code
        self.source_code = jsbeautifier.beautify(self.source_code)
        self.source_code = re.sub(r"\s+", " ", self.source_code).strip()  # Minify by removing extra spaces

    def parse_ast(self):
        try:
            self.ast = esprima.parse(self.source_code)
            print(f"DEBUG: AST parsed successfully.")
            if self.verbose:
                print("AST:", json.dumps(self.ast.toDict(), indent=2))
        except Exception as e:
            print(f"Error parsing JavaScript: {e}")
            return

    def obfuscate_variable_names(self):
        """Replaces variable names with obfuscated names (_0x-style)."""
        def generate_var_name():
            return f"_0x{random.randint(100000, 999999)}"

        def traverse_and_obfuscate(node):
            if isinstance(node, dict):
                if node.get('type') == 'VariableDeclarator' and 'id' in node:
                    original_name = node['id']['name']
                    if original_name not in self.var_map:
                        self.var_map[original_name] = generate_var_name()
                    node['id']['name'] = self.var_map[original_name]

                if node.get('type') == 'Identifier' and node['name'] in self.var_map:
                    node['name'] = self.var_map[node['name']]

                for key, value in node.items():
                    traverse_and_obfuscate(value)
            elif isinstance(node, list):
                for item in node:
                    traverse_and_obfuscate(item)

        traverse_and_obfuscate(self.ast)

    def encode_strings(self):
        """Encodes string literals into hex escape sequences."""
        def hex_encode(match):
            return ''.join(f"\\x{ord(c):02x}" for c in match.group(0))

        self.source_code = re.sub(r'"([^"]*?)"', lambda m: f'"{hex_encode(m)}"', self.source_code)
        self.source_code = re.sub(r"'([^']*?)'", lambda m: f"'{hex_encode(m)}'", self.source_code)

    def obfuscate_function_calls(self):
        """Replaces function calls with array-based obfuscation."""
        function_names = re.findall(r'function\s+(\w+)\s*\(', self.source_code)
        self.function_map = {name: f"_0x{random.randint(100000, 999999)}" for name in function_names}

        for original, obfuscated in self.function_map.items():
            self.source_code = re.sub(rf'\b{original}\b', obfuscated, self.source_code)

    def add_fake_control_flow(self):
        """Injects fake if-else statements to confuse reverse engineers."""
        obfuscation_patterns = [
            "if (Math.random() > 1) { console.log('This will never run'); }",
            "if (false) { alert('Fake security check'); }",
            "if (typeof window === 'undefined') { console.log('Fake Node.js check'); }"
        ]
        random.shuffle(obfuscation_patterns)
        self.source_code = obfuscation_patterns[0] + "\n" + self.source_code

    def run(self):
        self.beautify_and_minify()
        self.parse_ast()
        
        if not self.ast:
            return

        self.obfuscate_variable_names()
        self.encode_strings()
        self.obfuscate_function_calls()
        self.add_fake_control_flow()

        try:
            self.source_code = escodegen.generate(self.ast)
        except Exception as e:
            print(f"Error generating code: {e}")
            return

        output_file = self.input_file.with_name(f"obfuscated_{self.input_file.name}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.source_code)

        print(f"\n Obfuscated code saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="JavaScript Obfuscator")
    parser.add_argument("input_file", help="Path to the JavaScript file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (show AST)")
    args = parser.parse_args()

    obfuscator = Obfuscator(args.input_file, verbose=args.verbose)
    obfuscator.run()

if __name__ == "__main__":
    main()