import sys

import os

#imput is the form select Age>30(employees)
#must support select, project, join, set

databaseNum = 0

loadedDatabases = {}

#this function all chat gpt
def loadDatabase(file_path):
    entries = []
    
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                line = toAlphanumeric(line)
                if i == 0:
                    info = line.split()
                    title = info[0]
                    labels = info[1:]
                else:
                    entry = line.split(' ')
                    entries.append(entry)
                    
    except FileNotFoundError:
        return None

    entries = entries[:-1]#for some reason it always sticks an empty at the end

    database = {
        'title': title,
        'labels': labels,
        'entries': entries
    } 
    return database

def indexOf(string, matchChars):
    for i, char in enumerate(string):
        if(char in matchChars):
            return i
    return -1

def toAlphanumeric(input):
    return "".join([char for char in input if char.isalnum() or char == ' '])
        
        
        
def printDatabase(data):
    print(data['title'])
    print(data['labels'])
    for line in data['entries']:
        print(line)


def filter_entries(database, labelIndex, condition, targetQuantity):
    if condition == "!=":
        # not equal
        predicate = lambda entry: entry[labelIndex] != targetQuantity
    elif condition == "<=":
        # less than or equal
        predicate = lambda entry: entry[labelIndex] <= targetQuantity
    elif condition == ">=":
        # greater than or equal
        predicate = lambda entry: entry[labelIndex] >= targetQuantity
    elif condition == "<":
        # less than
        predicate = lambda entry: entry[labelIndex] < targetQuantity
    elif condition == ">":
        # greater than
        predicate = lambda entry: entry[labelIndex] > targetQuantity
    elif condition == "=":
        # equal
        predicate = lambda entry: entry[labelIndex] == targetQuantity
    else:
        print("Invalid condition, please type one of the following: = <= < > >= !=")
        return None

    copyDatabase = database.copy()

    # Apply the filter based on the predicate
    result = list(filter(predicate, copyDatabase["entries"]))
    copyDatabase["entries"] = result

    return copyDatabase


def select(args):
    #command is select, need to find the label and condition and number and database
                #find the label and the condition
    index = indexOf(args, "<=>!")
    targetLabel = args[0:index]
    endIndex = index+1
    condition = args[index]
    if(args[index+1] in "<=>!"):#most it will be is 2 long, <=, >=, =<, =>, != 
        condition += args[index+1]
        endIndex += 1
        
    targetDatabaseIndex = indexOf(args, '(')+1
    targetQuantity = args[endIndex:targetDatabaseIndex-1]
    
    targetDatabase = args[targetDatabaseIndex:indexOf(args,")")]
    
    #if(not targetQuantity.isnumeric()):
    #    print("Invalid target quantity")
    #    return None
    targetQuantity = targetQuantity
    
    if(targetDatabase not in loadedDatabases):
        print("Target database not loaded")
        return None
    
    database = loadedDatabases[targetDatabase]
    if(targetLabel not in database["labels"]):
        print("label not found in target database")
        return None
    
    #actually indexed by number not label
    #so convert that
    labelIndex = database["labels"].index(targetLabel)
    
    condition = "".join(sorted(condition))
    #so now the order doesnt matter
    
    return filter_entries(database, labelIndex, condition, targetQuantity)


def databaseSet(args):
    print(args)
    #or(Employees, Managers)
    #and(Employees, Managers)
    #minus(Employees, Managers)
    
    firstDatabaseIndex = indexOf(args, '(')+1

    dataBases = args[firstDatabaseIndex:-1].split(",")
    commandType = args[0:firstDatabaseIndex-1].upper()

    for i in dataBases:
        if(i not in loadedDatabases):
            print("Target database not loaded")
            return None
    newDatabase = {}
    
    #chat gpt
    db1 = loadedDatabases[dataBases[0]]
    db2 = loadedDatabases[dataBases[1]]
    
    if(commandType == "UNION"):
         result_db = {
        "title": f"{db1['title']}Union{db2['title']}",
        "labels": db1["labels"],
        "entries": db1["entries"] + [entry for entry in db2["entries"] if entry not in db1["entries"]]
        }
    elif(commandType == "INTERSECT"):
         # Combine titles and labels
        result_db = {
            "title": f"{db1['title']}Intersect{db2['title']}",
            "labels": db1["labels"],
            "entries": [entry for entry in db1["entries"] if entry in db2["entries"]]
        }
    elif(commandType == "DIFFERENCE"):
        # Combine titles and labels
        result_db = {
            "title": f"{db1['title']}Difference{db2['title']}",
            "labels": db1["labels"],
            "entries": [entry for entry in db1["entries"] if entry not in db2["entries"]]
        }
    else:
        print("Unknown type of set")
        return None    
    
    return result_db
    
def join(args):   
    #join EmployeeID(Employees,Managers)")
    
    firstDatabaseIndex = indexOf(args, '(')+1
    dataBases = args[firstDatabaseIndex:-1].split(",")
    targetLabel = args[0:firstDatabaseIndex-1]
   
    if(len(dataBases) != 2):
        print("Please specify 2 databases")
        return None
    
    for i in dataBases:
        if(i not in loadedDatabases):
            print("Target database not loaded: " + i)
            return None
        
    if(targetLabel not in loadedDatabases[dataBases[0]]["labels"]):
        print("Label not in database left database")
    if(targetLabel not in loadedDatabases[dataBases[0]]["labels"]):
        print("Label not in database right database")
           
        
    newDatabase = {}

    return database_inner_join(loadedDatabases[dataBases[0]], loadedDatabases[dataBases[1]], targetLabel)
    
#chat gpt
def database_inner_join(db1, db2, join_column):
    # Find the index of the join column in both databases
    index_db1 = db1["labels"].index(join_column)
    index_db2 = db2["labels"].index(join_column)

    # Combine titles and labels
    result_db = {
        "title": f"{db1['title']} Join {db2['title']} on {join_column}",
        "labels": db1["labels"] + [label for label in db2["labels"] if label != join_column],
        "entries": []
    }

    # Perform the join
    for entry1 in db1["entries"]:
        for entry2 in db2["entries"]:
            if entry1[index_db1] == entry2[index_db2]:
                result_db["entries"].append(entry1 + [value for j, value in enumerate(entry2) if j != index_db2])

    return result_db

def project(args):
    #displays the column specified
    #project Age(Employees)
    index = indexOf(args, "(")
    targetLabel = args[0:index]
    
    targetDatabase = args[index+1:-1]
    
    if(targetDatabase not in loadedDatabases):
        print("Target database not loaded " + targetDatabase)
        return None
    
    database = loadedDatabases[targetDatabase]
    if(targetLabel not in database["labels"]):
        print("label not found in target database "+ targetLabel)
        return None
    
    labelIndex = database["labels"].index(targetLabel)
    copyDatabase = database.copy()
    copyDatabase["labels"] = [targetLabel]
    entries = []
    for entry in database["entries"]:
        entries += entry[labelIndex]
    copyDatabase["entries"] = entries
    return copyDatabase

def splitArguments(argument):
    #so if you count the number of open and closed parenthesis
    #you can keep track of what depth you are at
    #if the depth is 1, and you find a comma, thats the comma you're looking for
    leftP = None
    rightP = None
    depth = 0
    comma = None
    for i, char in enumerate(argument):
        if(char == '('):
            if(depth == 0):
                leftP = i
            depth += 1
        if(char == ')'):
            depth -= 1
            if(depth == 0):
                rightP = i
        if(depth == 1 and char == ','):
            comma = i
    return (leftP, rightP,comma)
    #malformed equation i suppose

    

    
    
def recursiveParser(argument):
    global databaseNum
    #union(select Age(Employees), select Age(Managers))
    
    #find the leftmost command, should be space separated
    command = argument.split()[0]
    command = command.upper()
    
    if(command == "SET"):#binary
        #binary
        #need to find middle comma
        leftP, rightP, argumentSplitIndex = splitArguments(argument)
        
        arg1 = argument[leftP+1:argumentSplitIndex].strip()
        arg2 = argument[argumentSplitIndex+1:rightP].strip()
        
        extraArg = argument[len(command)+1:leftP+1]
        
        arg = extraArg+recursiveParser(arg1)+","+recursiveParser(arg2)+")"
        result = databaseSet(arg)
        if(result == None):
            return None
        result["title"] = str(databaseNum)
        databaseNum+=1     
        loadedDatabases[result["title"]] =result
        return result["title"] 

    elif(command == "JOIN"):#binary
        #binary
        #need to find middle comma
        leftP, rightP, argumentSplitIndex = splitArguments(argument)
                
        arg1 = argument[leftP+1:argumentSplitIndex].strip()
        arg2 = argument[argumentSplitIndex+1:rightP].strip()
        
        extraArg = argument[len(command)+1:leftP+1]
        
        recursiveA = recursiveParser(arg1)
        recursiveB = recursiveParser(arg2)
        if(recursiveA == None or recursiveB == None):
            return None
        
        arg = extraArg+recursiveA+","+recursiveB+")"
        result = join(arg)
        if(result == None):
            return None
        result["title"] = str(databaseNum)
        databaseNum+=1     
        loadedDatabases[result["title"]] = result
        return result["title"] 
    
    elif(command == "SELECT"):#unary
        
        leftP, rightP, argumentSplitIndex = splitArguments(argument)
        extraArg = argument[len(command)+1:leftP+1]

        recursiveArg = argument[leftP+1:rightP].strip()
        recursive = recursiveParser(recursiveArg)
        if(recursive == None):
            return None
        arg = extraArg+recursive+")"
        result = select(arg)   
        if(result == None):
            return None
        
        result["title"] = str(databaseNum)
        databaseNum+=1     
        loadedDatabases[result["title"]] =result
        return result["title"] 
    
    elif(command == "PROJECT"):#unary
        leftP, rightP, argumentSplitIndex = splitArguments(argument)
        extraArg = argument[len(command)+1:leftP+1]
        
        recursiveArg = argument[leftP+1:].strip()
        arg = recursiveParser(recursiveArg)
        if(arg == None):
            return None
        result = project(arg)   
    
        result["title"] = str(databaseNum)
        databaseNum+=1     
        loadedDatabases[result["title"]] =result
        return result["title"] 
    else:
        #base case, no more commands to process
        return argument    


import os

if __name__ == "__main__":

    #order of commands is separated by space

    print("Loading databases in data file")

    #chat gpt
    data_directory = "Data/"
    absolute_data_directory = os.path.abspath(data_directory)
    for filename in os.listdir(absolute_data_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(absolute_data_directory, filename)
            
            newdatabase = loadDatabase(file_path)
            loadedDatabases[newdatabase["title"]] = newdatabase
            print(newdatabase["title"])
         
    print("")
    print("EXAMPLE COMMANDS:")
    print("SELECT Age<30(Employees)")
    print("PROJECT Age(Employees)")
    print("")
    print("SET Union(Employees,Managers)")
    print("SET Intersect(Employees,Managers)")
    print("SET Difference(Employees,Managers)")
    print("")
    print("JOIN EID(Employees,Managers)")  
    print("")
    print("EXAMPLES OF NESTING COMMANDS")
    print("JOIN EID(SELECT Age>30(SET Union(Employees, Managers)),Salaries)")
    print("SELECT Age>30(SET Union(Employees, Managers))")
    
    while True:
        print("Please type in a command")
        comamnd = input()
        if(not comamnd):
            continue#skip empties
        result = recursiveParser(comamnd)
        if(result != None):
            data = loadedDatabases[result]
            printDatabase(data)
        
        #clean out the numbers
        # Collect keys with numeric values
        numeric_keys = [key for key in loadedDatabases.keys() if key.isnumeric()]

        # Remove key-value pairs with numeric keys
        for key in numeric_keys:
            del loadedDatabases[key]
                



    def oneAtAtime():

        # Get the file path from the command-line argument
        #file_path = sys.argv[1]
        file_path = "Data/Employees.txt"
        
        # Example usage
        newdatabase = loadDatabase(file_path)
        loadedDatabases[newdatabase["title"]] = newdatabase

        file_path = "Data/Managers.txt"
        
        # Example usage
        newdatabase = loadDatabase(file_path)
        loadedDatabases[newdatabase["title"]] = newdatabase

        file_path = "Data/Salaries.txt"
        
        # Example usage
        newdatabase = loadDatabase(file_path)
        loadedDatabases[newdatabase["title"]] = newdatabase


        print("Loaded database: ")
        #printDatabase(database)


        while True:
            print("\nPlease input a command")
            print("available commands: select, join, project, set, list, help")

            #operations
            inputString = input()
            if(not inputString):
                continue

            data = inputString.split()
            command = data[0]
            args = inputString[len(command):].strip()
            
            if(command == "load"):
                newdatabase = loadDatabase(file_path)
                if(newdatabase == None):
                    print("File not found")
                loadedDatabases[newdatabase["title"]] = newdatabase
            
            elif(command == "examples" or command == "help"):
                print("Examples of commands: ")
                print("")
                print("list")
                print("load filepath")
                print("")
                print("select Age<30(Employees)")
                print("project Age(Employes)")
                print("")
                print("set Union(Employees,Managers)")
                print("set Intersect(Employees,Managers)")
                print("set Difference(Employees,Managers)")
                print("")
                print("join EmployeeID(Employees,Managers)")  
                
            elif(command == "list"):
                print("Loaded databases:")
                for item in loadedDatabases:
                    print(item)            
                    
                    
            elif(command == "select"):
                result = select(args)
                if(result == None):
                    continue
                else:
                    printDatabase(result)
                
            elif(command == "join"):
                result = join(args)
                if(result == None):
                    continue
                else:
                    printDatabase(result)
                
            elif(command == "project"):
                result = project(args)
                if(result == None):
                    continue
                else:
                    printDatabase(result)
                    
                    
            elif(command == "set"):
                result = databaseSet(args)
                if(result == None):
                    continue
                else:
                    printDatabase(result)