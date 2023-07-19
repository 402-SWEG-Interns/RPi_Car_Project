localMax = 0
max = 0
max1 = 0
max2 = 0
counter = 0
lowest = ""

file = open("adventText.txt", "r")

while True:
    contents = file.readline()


    if max < max1 and max < max2:
        lowest = "max"
    if max1 < max and max1 < max2:
        lowest = "max1"
    if max2 < max and max2 < max1:
        lowest = "max2"
    if max == 0:
        lowest = "max"
    if max1 == 0:
        lowest = "max1"
    if max2 == 0:
        lowest == "max2"
    
    if contents == "\n":
        if localMax > max2 or localMax > max1 or localMax > max:
            if lowest =="max":
                max = localMax
            if lowest =="max1":
                max1 = localMax
            if lowest =="max2":
                max2 = localMax
            
            
        localMax = 0
        
        

    elif contents == "":
        break
    else:
        localMax += int(contents)

    counter = counter + 1

        

print(max + max1 + max2)
