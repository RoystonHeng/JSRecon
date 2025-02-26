import jsbeautifier
import re
import json
import argparse
from pathlib import Path
import esprima
import escodegen


class Deobfuscator:
    def __init__(self, input_file, verbose=False):
        self.input_file = Path(input_file).resolve()
        self.input_file = Path(str(self.input_file).replace("\\", "/"))
        print(f"DEBUG: Absolute path to input file: {self.input_file}")
        self.source_code = self.load_code()
        self.ast = None
        self.verbose = verbose
        self.renamed_vars = {}
        self.current_scope = [{}]
        self.array_maps = {}  # Store array declarations and their values

    def load_code(self):
        print(f"DEBUG: Loading code from: {self.input_file}")
        with open(self.input_file, 'r', encoding="utf-8") as f:
            code = f.read()
            print(f"DEBUG: Code loaded successfully.")
            return code

    def beautify_and_unpack(self):
        self.source_code = jsbeautifier.beautify(self.source_code)

    def parse_ast(self):
        try:
            self.ast = esprima.parse(self.source_code)
            print(f"DEBUG: AST parsed successfully.")
            if self.verbose:
                print("AST:", json.dumps(self.ast.toDict(), indent=2))
        except Exception as e:
            print(f"Error parsing JavaScript: {e}")
            return

    def deobfuscate_string_arrays(self):
        array_pattern = r'(?:var|let|const)\s+([\w\d_]+)\s*=\s*\[([^\]]+?)\];'
        for match in re.finditer(array_pattern, self.source_code):
            array_name = match.group(1)
            array_elements = match.group(2).split(',')
            array_elements = [e.strip().strip('"').strip("'") for e in array_elements]
            self.array_maps[array_name] = array_elements

            def replace_access(m):
                index = m.group(1)
                if index.isdigit():
                    idx = int(index)
                    if 0 <= idx < len(array_elements):
                        return f'"{array_elements[idx]}"'
                return m.group(0)

            self.source_code = re.sub(rf'{re.escape(array_name)}\[(\d+)\]', replace_access, self.source_code)

    def deobfuscate_escapes(self):
        self.source_code = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), self.source_code)
        self.source_code = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), self.source_code)

    def deobfuscate_function_calls(self):
        array_pattern = r'(?:var|let|const)\s+([\w\d_]+)\s*=\s*\[([^\]]+?)\];'
        for match in re.finditer(array_pattern, self.source_code):
            array_name = match.group(1)
            array_elements = [s.strip() for s in match.group(2).split(',')]
            access_pattern = re.escape(array_name) + r'\[(\d+)\](\([^)]*\))'

            def replace_call(access_match):
                try:
                    index = int(access_match.group(1))
                    function_name = array_elements[index]
                    arguments = access_match.group(2)
                    return f'{function_name}{arguments}'
                except (IndexError, ValueError):
                    return access_match.group(0)

            self.source_code = re.sub(access_pattern, replace_call, self.source_code)

    def deobfuscate_numbers(self):
        self.source_code = re.sub(r'0x([0-9a-fA-F]+)', lambda m: str(int(m.group(1), 16)), self.source_code)

    def deobfuscate_object_properties(self):
        self.source_code = re.sub(r'([\w\d_]+)\[\s*["\']([\w\d_]+)["\']\s*\]', r'\1.\2', self.source_code)

    def simplify_if_statements(self):
        if not self.ast:
            return

        def traverse_and_simplify(node):
            if isinstance(node, dict):
                if node.get('type') == 'IfStatement' and node.get('test', {}).get('type') == 'Literal':
                    value = node['test'].get('value')
                    if value is True:
                        node.clear()
                        node.update(node.get('consequent', {}))
                    elif value is False:
                        node.clear()
                        node.update(node.get('alternate', {}))

                for key, value in node.items():
                    traverse_and_simplify(value)
            elif isinstance(node, list):
                for item in node:
                    traverse_and_simplify(item)

        traverse_and_simplify(self.ast)

    def rename_variables(self):
        if not self.ast:
            return

        def traverse_and_rename(node, scope):
            if isinstance(node, dict):
                if node.get('type') in ('FunctionDeclaration', 'FunctionExpression', 'Program'):
                    scope.append({})

                if node.get('type') == 'Identifier' and node.get('name', '').startswith('_0x'):
                    current_scope = scope[-1]
                    original_name = node['name']
                    if original_name not in current_scope:
                        new_name = f"var{len(current_scope) + 1}_scope{len(scope)}"
                        current_scope[original_name] = new_name
                    node['name'] = current_scope[original_name]

                for key, value in node.items():
                    traverse_and_rename(value, scope)

                if node.get('type') in ('FunctionDeclaration', 'FunctionExpression', 'Program'):
                    scope.pop()

            elif isinstance(node, list):
                for item in node:
                    traverse_and_rename(item, scope)

        traverse_and_rename(self.ast, self.current_scope)

    def run(self):
        self.beautify_and_unpack()
        self.deobfuscate_string_arrays()
        self.deobfuscate_function_calls()
        self.deobfuscate_escapes()
        self.deobfuscate_object_properties()
        self.deobfuscate_numbers()
        self.parse_ast()

        if not self.ast:
            return

        self.rename_variables()
        self.simplify_if_statements()

        try:
            self.source_code = escodegen.generate(self.ast)
        except Exception as e:
            print(f"Error generating code: {e}")
            return

        output_file = self.input_file.with_name(f"deobfuscated_{self.input_file.name}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.source_code)

        print(f"\n✅ Deobfuscated code saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="JavaScript Deobfuscator")
    parser.add_argument("input_file", help="Path to the JavaScript file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (show AST)")
    args = parser.parse_args()

    deobfuscator = Deobfuscator(args.input_file, verbose=args.verbose)
    deobfuscator.run()

if __name__ == "__main__":
    main()
