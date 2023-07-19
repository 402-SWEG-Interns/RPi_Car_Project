score = 0
length = 0
matching = ""
matchingVal = 0

score = 0

file = open("adventText3.txt", "r")


while True:
    contents = file.readline()
    first, second = contents[:len(contents)//2], contents[len(contents)//2:]

    #print(first , second, len(first), len(second))


    firstList = list(first)
    secondList = list(second)

    print(firstList , secondList)

    for i in firstList:
        for y in secondList:
            if i == y:
                matching = i

                if matching.islower():
                    matchingVal = ord(matching) - 96

                    
                if matching.isupper():
                    matchingVal = ord(matching) - 38

                print(matching, matchingVal)

                score += matchingVal

                matchingVal = 0
            matchingVal = 0
            break



    if contents == "":
        break



    
    

    

    
   

        


print(score)
