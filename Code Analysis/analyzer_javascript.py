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
        "ValidateAgainstUser": 0
    }

    try:
        # ✅ Parse JavaScript code into AST using PyJsParser
        tree = pyjsparser.parse(code_snippet)

        for node in tree['body']:
            # ✅ Detect IfStatements for `isAdmin`
            if node['type'] == 'IfStatement':
                test_expr = node.get('test', {})

                # Check if `isAdmin:` is anywhere in the IfStatement condition
                if "isAdmin" in str(test_expr):
                    features["NeedAdminApproval"] = 1
                    features["AreYouAdmin"] = 1

            # ✅ Detect user ownership validation (`if (userId !== currentUserId)`)
            if node['type'] == 'IfStatement' and node['test']['type'] == 'BinaryExpression':
                left = node['test']['left']
                right = node['test']['right']
                operator = node['test']['operator']

                if left['type'] == 'Identifier' and right['type'] == 'Identifier':
                    if left['name'] == "userId" and right['name'] == "currentUserId" and operator in ["!==", "==="]:
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
                      "ValidateAgainstUser"
                      ]
        
        df = pd.DataFrame([features])
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(features)
        
        print(f"{csv_filename} has been created successfully.")
