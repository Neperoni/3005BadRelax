


#imput is the form select Age>30(employees)
#must support select, project, join, set

#this function all chat gpt
def loadDatabase(file_path):
    entries = []
    
    # Open the file and read its content
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regular expression to extract employee entries
    pattern = r'E(\d+), (\w+), (\d+)'
    matches = re.findall(pattern, content)

    # Create a list of entries
    for match in matches:
        entry = {'EID': match[0], 'Name': match[1], 'Age': match[2]}
        entries.append(entry)

    return entries