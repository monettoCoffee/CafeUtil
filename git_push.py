import os
forbidden_branch = []
results = os.popen('git branch;').readlines()
now_branch = "None"
for _result in results:
    if _result.find("*") != -1:
        now_branch = _result[2 : len(_result)].replace("\n", "")
        break
# git rm -r --cached .;
if now_branch not in forbidden_branch:
    os.popen('git config --global user.name "monetto"').readlines()
    os.popen('git config --global user.email "j3jzy@163.com"').readlines()
    now_command = 'git add .;git commit -m "Auto_Commit";git push origin ' + now_branch
    print(str(os.popen(now_command).readlines()))
else:
    print("Forbidden Branch!")
