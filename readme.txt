Steps to run JSRecon:

1) pip install -r requirements.txt
2) Enter to "Code Analysis" (such as cd "./Code Analysis")
3) Paste a obfuscated JavaScript code into test.js or create another .js file with the obfuscated code inside
4) run JSRecon.py with python ./JSRecon.py
5) JSRecon will ask for a file name containing the obfuscated code. E.g test.js
6) Wait for JSRecon to generate the deobfuscated_<filename>.js, deobfuscated_<filename>_predicted.js and ai_security_report.docx

old_code folder contains code that was either prototypes or failed versions of current code