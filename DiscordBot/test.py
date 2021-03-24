with open('parameters.csv') as para_file:
    turn=[row.split(sep=',')[1] for row in para_file]
    print("You are on turn",int(turn[0]),'!')
    print("Your stats")