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

def analyze_code(code_snippet):
    features = {
        "NeedAdminApproval": 0,
        "CreatedByUser": 0,
        "AreYouAdmin": 0,
        "ValidateAgainstUser": 0,
        "ValidateAgainstAdmin": 0,
        "IsItSecure": 0  # Default to insecure
    }

    try:
        # ✅ Parse JavaScript code into AST using PyJsParser
        tree = pyjsparser.parse(code_snippet)

        for node in tree['body']:
            # ✅ Detect IfStatements with `currentUser.isAdmin`
            if node['type'] == 'IfStatement':
                test_expr = node.get('test', {})  # Safely get condition
                if test_expr.get('type') == 'MemberExpression':
                    object_name = test_expr['object'].get('name', '')
                    property_name = test_expr['property'].get('name', '')

                    if f"{object_name}.{property_name}" == "currentUser.isAdmin" or f"{object_name}.{property_name}" == "user.isAdmin":
                        features["NeedAdminApproval"] = 1
                        features["AreYouAdmin"] = 1

            # ✅ Detect user ownership validation (e.g., `if (note.userId == currentUser.id)`)
            if node['type'] == 'IfStatement' and node['test']['type'] == 'BinaryExpression':
                left = node['test']['left']
                right = node['test']['right']

                if left['type'] == 'MemberExpression' and right['type'] == 'MemberExpression':
                    left_obj = left['object']['name']
                    left_prop = left['property']['name']
                    right_obj = right['object']['name']
                    right_prop = right['property']['name']

                    if f"{left_obj}.{left_prop}" == "note.userId" and f"{right_obj}.{right_prop}" == "currentUser.id":
                        features["ValidateAgainstUser"] = 1

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
                      "ValidateAgainstUser",
                      "ValidateAgainstAdmin",
                      "IsItSecure"
                      ]
        
        df = pd.DataFrame([features])
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(features)
        
        print(f"{csv_filename} has been created successfully.")
