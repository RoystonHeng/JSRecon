test = [0,0,0,0]

IsVisibleOnlyToAdmin , ValidateIsAdmin ,ItemCreatedByUserFucntion, ValidateIsUser , *discard = test

reporttext = []
if IsVisibleOnlyToAdmin == 1 and ValidateIsAdmin == 0:
    reporttext.append("CRITICAL. Privilege escalation vulnerability. Function is intended to be an admin function but can be used by non admins! Non admins will be able to run the function if invoked directly\n")
if IsVisibleOnlyToAdmin == 0 and ValidateIsAdmin == 1:
    reporttext.append("CRITICAL. Potential Privilege escalation vulnerability. Is this an admin only function? or is the permission check for this function wrong?\n")
if ItemCreatedByUserFucntion == 1 and ValidateIsUser == 0:
    reporttext.append("CRITICAL. Potential data leakage. Function does not check if user is allowed to access/edit this item.\n")

if not reporttext:
    reporttext=["This function is likely secure\n"]

print(reporttext)
with open("report.txt","wt") as f:
    f.writelines(reporttext)