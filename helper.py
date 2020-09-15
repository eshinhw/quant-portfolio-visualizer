
def jprint(obj):
    
    output = json.dumps(obj, indent=2)
    line_list = output.split("\n")
    for line in line_list:
        print line