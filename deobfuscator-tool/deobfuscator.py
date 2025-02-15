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
        with open(self.input_file, 'r') as f:
            code = f.read()
            print(f"DEBUG: Code loaded successfully:\n{code}")
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
        # Enhanced pattern to match var, let, and const declarations
        array_pattern = r'(?:var|let|const)\s+([\w\d_]+)\s*=\s*\[([^\]]+?)\];'
        for match in re.finditer(array_pattern, self.source_code):
            array_name = match.group(1)
            array_elements = []

            # Parse array elements more carefully
            elements_str = match.group(2)
            current_element = ''
            in_string = False
            string_char = None
            bracket_depth = 0

            for char in elements_str:
                if char in '"\'':
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                elif char == '[':
                    bracket_depth += 1
                elif char == ']':
                    bracket_depth -= 1
                elif char == ',' and not in_string and bracket_depth == 0:
                    array_elements.append(current_element.strip())
                    current_element = ''
                    continue

                current_element += char

            if current_element:
                array_elements.append(current_element.strip())

            # Store array in our map for complex access patterns
            self.array_maps[array_name] = array_elements

            # Handle nested array access patterns
            def replace_nested_access(code, array_name, elements):
                # Pattern for array access with computed indices
                computed_pattern = rf'{re.escape(array_name)}\[([^\]]+)\]'

                def evaluate_index(index_expr):
                    try:
                        # Handle simple arithmetic in index
                        return eval(index_expr)
                    except:
                        return None

                def replace_access(match):
                    index_expr = match.group(1)

                    # Try to evaluate the index expression
                    index = evaluate_index(index_expr)

                    if index is not None and 0 <= index < len(elements):
                        element = elements[index]
                        # If the element looks like a string literal, return it as is
                        if element.startswith('"') or element.startswith("'"):
                            return element
                        # Otherwise, wrap it in quotes
                        return f'"{element}"'

                    return match.group(0)

                return re.sub(computed_pattern, replace_access, code)

            # Apply replacements
            self.source_code = replace_nested_access(self.source_code, array_name, array_elements)

    def deobfuscate_complex_array_access(self):
        """Handle more complex array access patterns including nested arrays and computed indices."""
        for array_name, elements in self.array_maps.items():
            # Pattern for nested array access like arr[0][1] or arr[i][j]
            nested_pattern = rf'{re.escape(array_name)}(\[\d+\])+'

            def replace_nested(match):
                try:
                    # Extract all indices
                    indices = re.findall(r'\[(\d+)\]', match.group(0))
                    current = elements

                    # Navigate through nested arrays
                    for idx in indices:
                        idx = int(idx)
                        if isinstance(current, list) and idx < len(current):
                            current = current[idx]
                        else:
                            return match.group(0)

                    # Return the final value
                    if isinstance(current, str):
                        return f'"{current}"'
                    return str(current)
                except:
                    return match.group(0)

            self.source_code = re.sub(nested_pattern, replace_nested, self.source_code)

    def deobfuscate_escapes(self):
        def replace_hex(match):
            try:
                return chr(int(match.group(1), 16))
            except ValueError:
                return match.group(0)

        def replace_unicode(match):
            try:
                return chr(int(match.group(1), 16))
            except ValueError:
                return match.group(0)

        self.source_code = re.sub(r'\\x([0-9a-fA-F]{2})', replace_hex, self.source_code)
        self.source_code = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, self.source_code)

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
        def replace_hex(match):
            try:
                return str(int(match.group(1), 16))
            except ValueError:
                return match.group(0)

        self.source_code = re.sub(r'0x([0-9a-fA-F]+)', replace_hex, self.source_code)

        def simplify_arithmetic(match):
            try:
                return str(eval(match.group(0)))
            except (SyntaxError, TypeError, ZeroDivisionError):
                return match.group(0)

        self.source_code = re.sub(r'\([\d\s+\-*/]+\)', simplify_arithmetic, self.source_code)

    def deobfuscate_object_properties(self):
        pattern = r'([\w\d_]+)\[\s*["\']([\w\d_]+)["\']\s*\]'

        def replace_property_access(match):
            object_name = match.group(1)
            property_name = match.group(2)
            return f"{object_name}.{property_name}"

        self.source_code = re.sub(pattern, replace_property_access, self.source_code)

    def simplify_if_statements(self):
        if not self.ast:
            return

        def traverse_and_simplify(node):
            if isinstance(node, dict):
                if node.get('type') == 'IfStatement':
                    test = node.get('test')
                    if test and test.get('type') == 'Literal':
                        value = test.get('value')
                        if value is True:
                            node.clear()
                            node.update(node.get('consequent'))
                        elif value is False:
                            alternate = node.get('alternate')
                            if alternate:
                                node.clear()
                                node.update(alternate)
                            else:
                                node.clear()
                                node['type'] = 'EmptyStatement'

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

                if node.get('type') == 'Identifier':
                    original_name = node.get('name')
                    if original_name and original_name.startswith('_0x'):
                        current_scope = scope[-1]
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
        self.deobfuscate_complex_array_access()  # New step
        self.deobfuscate_function_calls()
        self.deobfuscate_escapes()
        self.deobfuscate_object_properties()
        self.deobfuscate_numbers()
        self.parse_ast()

        if not self.ast:
            return

        self.rename_variables()
        self.simplify_if_statements()

        if self.verbose:
            print("Modified AST:")
            print(json.dumps(self.ast.toDict(), indent=2))

        try:
            self.source_code = escodegen.generate(self.ast)
        except Exception as e:
            print(f"Error generating code: {e}")
            return

        print("\nDeobfuscated Code:\n", self.source_code)


def main():
    parser = argparse.ArgumentParser(description="JavaScript Deobfuscator")
    parser.add_argument("input_file", help="Path to the JavaScript file")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output (show AST)")
    args = parser.parse_args()

    deobfuscator = Deobfuscator(args.input_file, verbose=args.verbose)
    deobfuscator.run()


if __name__ == "__main__":
    main()