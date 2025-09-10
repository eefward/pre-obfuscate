import re
import string

# patterns
VarPattern = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=].*$'

def maskVariables(file):
    with open(file, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    result = []
    maskedDict = {}
    
    mask_count = 1
    for line in lines:
        masked = line
        match = re.match(VarPattern, line)
        if match:
            var_name = line.split('=', 1)[0].strip()
            var_value = line.split('=', 1)[1].strip()
            masked_name = f'masked{mask_count}'
            masked = f'{masked_name} = {var_value}'
            masked_dict[masked_name] = var_name 
            mask_count += 1
        result.append(masked)
    
    print(maskedDict)
    
    with open('output.csv', 'w') as out:
        for line in result:
            out.write(line + '\n')

maskVariables('file.csv')