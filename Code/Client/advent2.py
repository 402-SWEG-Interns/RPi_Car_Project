score = 0

file = open("adventText2.txt", "r")

while True:
    contents = file.readline()

    if contents == "":
        break

    contents.split()


    if contents[2] == "X":
        score += 0
        if contents[0] == "A":
            score += 3
        if contents[0] == "B":
            score += 1
        if contents[0] == "C":
            score += 2
    if contents[2] == "Y":
        score += 3

        if contents[0] == "A":
            score += 1
        if contents[0] == "B":
            score += 2
        if contents[0] == "C":
            score += 3

    if contents[2] == "Z":
        score += 6

        if contents[0] == "A":
            score += 2
        if contents[0] == "B":
            score += 3
        if contents[0] == "C":
            score += 1

    

    

    # if (contents[0] == "A" and contents[2] == "X") or (contents[0] == "B" and contents[2] == "Y") or (contents[0] == "C" and contents[2] == "Z"):
    #     score += 3
    #     print("tie")
    # if contents[0] == "A" and contents[2] == "Y":
    #     score += 6
    # if contents[0] == "B" and contents[2] == "Z":
    #     score += 6
    # if contents[0] == "C" and contents[2] == "X":
    #     score += 6

    
    

    

    
   

        


print(score)
