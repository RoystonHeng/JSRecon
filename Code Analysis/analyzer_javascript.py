import pyjsparser
import pandas as pd
import csv

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
        # Parse JavaScript using PyJsParser
        tree = pyjsparser.parse(code_snippet)
        
        for node in tree['body']:
            if node['type'] == 'IfStatement':
                test_code = code_snippet[node['test']['range'][0]:node['test']['range'][1]]
                if "currentUser.isAdmin" in test_code or "user.isAdmin" in test_code:
                    features["NeedAdminApproval"] = 1
                    features["AreYouAdmin"] = 1
            
            if node['type'] == 'ExpressionStatement' and 'expression' in node:
                expression = node['expression']
                left_range = expression.get('left', {}).get('range', [None, None])
                right_range = expression.get('right', {}).get('range', [None, None])

                left = code_snippet[left_range[0]:left_range[1]] if None not in left_range else ""
                right = code_snippet[right_range[0]:right_range[1]] if None not in right_range else ""

                
                if "note.userId" in left and "currentUser.id" in right:
                    features["ValidateAgainstUser"] = 1
    
    except Exception as e:
        print(f"Error parsing JavaScript code: {e}")

    return features

if __name__ == "__main__":
    code_file_path = input("Enter file of code to test: ")
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
