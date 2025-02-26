import pyjsparser
import pandas as pd
import csv
import os

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return analyze_code(code)
    except FileNotFoundError:
        print("Error: The file was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

import pyjsparser

def traverse_ast(node, features):
    """
    Recursively traverse the AST to find relevant features.
    """
    if isinstance(node, dict):  # If it's a dictionary (AST node)
        #Detect `isAdmin:` in IfStatements
        if node.get('type') == 'IfStatement' and 'test' in node:
            test_expr = str(node['test'])  # Convert to string for detection
            if "isAdmin" in test_expr:
                features["NeedAdminApproval"] = 1
                features["AreYouAdmin"] = 1

        #Detect `if (!noteId || typeof noteId !== "number")`
        if node.get('type') == 'IfStatement' and 'test' in node:
            test = node['test']

            #Check for `!noteId` (UnaryExpression)
            if test.get('type') == 'LogicalExpression' and test.get('operator') == '||':
                left_expr = test.get('left', {})
                right_expr = test.get('right', {})

                #Left side: `!noteId`
                if left_expr.get('type') == 'UnaryExpression' and left_expr.get('operator') == '!' and left_expr['argument'].get('name') == "noteId":
                    features["CreatedByUser"] = 1

        #Detect user validation `if (userId !== currentUserId)`
        if node.get('type') == 'IfStatement' and node.get('test', {}).get('type') == 'BinaryExpression':
            left = node['test']['left']
            right = node['test']['right']
            operator = node['test']['operator']

            if left['type'] == 'Identifier' and right['type'] == 'Identifier':
                if left['name'] == "userId" and right['name'] == "currentUserId" and operator in ["!==", "==="]:
                    features["ValidateAgainstUser"] = 1

        #Detect `fetch()` calls inside function bodies
        if node.get('type') == 'FunctionDeclaration' and 'body' in node:
            traverse_ast(node['body'], features)

        #Detect `ObjectExpression` properties (e.g., body: JSON.stringify({ isAdmin: isAdmin }))
        if node.get('type') == 'Property' and 'value' in node:
            value = node['value']
            if value.get('type') == 'CallExpression' and 'callee' in value:
                callee = value['callee']

                #Look for JSON.stringify()
                if callee.get('type') == 'MemberExpression' and callee['object'].get('name') == "JSON" and callee['property'].get('name') == "stringify":
                    #Check the first argument of JSON.stringify (must be an object)
                    if value['arguments'] and value['arguments'][0].get('type') == 'ObjectExpression':
                        for prop in value['arguments'][0]['properties']:
                            if prop['key']['name'] == "isAdmin":
                                features["AreYouAdmin"] = 1 

        #Recursively search inside child nodes
        for key, value in node.items():
            traverse_ast(value, features)

    elif isinstance(node, list):  # If it's a list (array of AST nodes)
        for item in node:
            traverse_ast(item, features)

def analyze_code(code_snippet):
    features = {
        "NeedAdminApproval": 0,
        "CreatedByUser": 0,
        "AreYouAdmin": 0,
        "ValidateAgainstUser": 0
    }

    try:
        #Parse JavaScript code into AST using PyJsParser
        tree = pyjsparser.parse(code_snippet)



        #Recursively search the AST
        traverse_ast(tree, features)

    except Exception as e:
        print(f"Error parsing JavaScript code: {e}")

    return features

if __name__ == "__main__":
    code_file_path = input("Enter file of code to test: ")
    
    # Check if test.csv exists, and delete it if it does
    csv_filename = "test.csv"
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
        print(f"Deleted old {csv_filename}")
        
    features = read_file(code_file_path)

    if features:
        csv_filename = "test.csv"
        fieldnames = ["NeedAdminApproval", 
                      "AreYouAdmin", 
                      "CreatedByUser", 
                      "ValidateAgainstUser"
                      ]
        
        df = pd.DataFrame([features])
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(features)
        
        print(f"{csv_filename} has been created successfully.")
