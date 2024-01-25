import sys



#imput is the form select Age>30(employees)
#must support select, project, join, set


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
    
    if(not targetQuantity.isnumeric()):
        print("Invalid target quantity")
        return None
    targetQuantity = int(targetQuantity)
    
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
    
    if(condition == "!="):
        #not equal
        predicate = lambda entry: (int(entry[labelIndex]) != targetQuantity)
    elif(condition == "<="):
        #less than or equal
        predicate = lambda entry: (int(entry[labelIndex]) <= targetQuantity) 
    elif(condition == "=>"):
        #greather than or equal
        predicate = lambda entry: (int(entry[labelIndex]) >= targetQuantity) 
    elif(condition == "<"):
        #less than
        predicate = lambda entry: (int(entry[labelIndex]) < targetQuantity) 
    elif(condition == ">"):
        #greater than
        predicate = lambda entry: (int(entry[labelIndex]) > targetQuantity) 
    elif(condition == "="):
        #equal
        predicate = lambda entry: (int(entry[labelIndex]) == targetQuantity) 
    else:
        print("Invalid condition, please type one of the following: = <= < > >= !=")
        return None
    
    copyDatabase = database.copy()
    
    result = list(filter(predicate, copyDatabase["entries"]))
    copyDatabase["entries"] = result
    
    return copyDatabase

def databaseSet(args):
    pass
    
def join(args):
    pass

def project(args):
    pass
    
if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    print("Usage: python code.py <database file path>")
    #    sys.exit(1)
        
    # Get the file path from the command-line argument
    #file_path = sys.argv[1]
    file_path = "Data/test1.txt"
    
    # Example usage
    newdatabase = loadDatabase(file_path)
    loadedDatabases[newdatabase["title"]] = newdatabase

    print("Loaded database: ")
    #printDatabase(database)


    while True:
        print("Please input a command")
        print("available commands: select, join, project, set, list")

        #operations
        inputString = input()

        data = inputString.split()
        command = data[0]
        args = data[1:]
        

        if(command == "load"):
            newdatabase = loadDatabase(file_path)
            if(newdatabase == None):
                print("File not found")
            loadedDatabases[newdatabase["title"]] = newdatabase
        elif(command == "list"):
            print("loaded databases:")
            for item in loadedDatabases:
                print(item)            
        elif(command == "select"):
            result = select(args[0])
            if(result == None):
                continue
            else:
                printDatabase(result)
            
        elif(command == "join"):
            join(args)  
        elif(command == "project"):
            project(args)
        elif(command == "set"):
            databaseSet(args)
