import ast
import pandas as pd
import csv
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()  # Read the entire Python file
        
        # Analyze the code using AST
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

    tree = ast.parse(code_snippet)

    for node in ast.walk(tree):
        # Detect role-based access control (RBAC)
        if isinstance(node, ast.If):
            test_code = ast.unparse(node.test)
            if "{% if current_user.is_admin%}" in test_code:
                features["NeedAdminApproval"] = 1
            if "current_user.is_admin" in test_code:
                features["AreYouAdmin"] = 1

     # Detect user ownership validation
        if isinstance(node, ast.Compare):
            left = ast.unparse(node.left)
            if "note.user_id" in left and "current_user.id" in ast.unparse(node.comparators[0]):
                features["ValidateAgainstUser"] = 1

    return features

code_file_path = input("Enter file of code to test: ")
features = read_file(code_file_path)
if features:
    csv_filename = "test.csv"
    # Convert to DataFrame and Save to CSV
    df = pd.DataFrame([features])
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writerows(features)
    
    print(f"{csv_filename} has been created")
