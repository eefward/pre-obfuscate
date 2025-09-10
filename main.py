import re
import string
import time
from faker import Faker
fake = Faker()

# patterns
VarPattern = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=].*$'
CommentPattern = r'^\s*#.*$'

def maskVariables(file):
    with open(file, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    result = []
    maskedDict = {}

    matches = [re.match(VarPattern, line) for line in lines]
    totalVars = sum(1 for match in matches if match)

    mask_count = 0
    for line, match in zip(lines, matches):
        masked = line
        if match:
            var_name = line.split('=', 1)[0].strip()
            var_value = line.split('=', 1)[1].strip()
            masked_name = f'masked{mask_count}'
            masked = f'{masked_name} = {var_value}'
            maskedDict[var_name] = masked_name
            mask_count += 1

            print(f"Masked variables [{mask_count}/{totalVars}]", end='\r')
            time.sleep(0.25)
        result.append(masked)
    
    print()
    
    final_result = []
    for line in result:
        masked_line = line
        for var_name, masked_name in maskedDict.items():
            masked_line = re.sub(rf'\b{var_name}\b', masked_name, masked_line)
        final_result.append(masked_line)
    
    with open('file.csv', 'w') as out:
        for line in final_result:
            out.write(line + '\n')

    return True

def removeComments(file):
    with open(file, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    result = []

    matches = [re.match(CommentPattern, line) for line in lines]
    totalComments = sum(1 for match in matches if match)

    CommentCount = 0
    for line, match in zip(lines, matches):
        if match:
            result.append("# " + fake.sentence())
            CommentCount += 1

            print(f"Masked comments [{CommentCount}/{totalComments}]", end='\r')
            time.sleep(0.25)
        else:
            result.append(line)
    
    print()

    with open('file.csv', 'w') as out:
        for line in result:
            out.write(line + '\n')

def preObfuscate(file):
    maskVariables(file)
    removeComments(file)
    maskStrings(file)

    print("Successfully obfuscated")

preObfuscate('file.csv')