#Work in progress    
#Just going to modify some stuff to check out Version Control
# Input/Output Files
currInputfile = open('teraterm_Poundit_new.log', 'r')
outputfile = open('results1.csv', 'w')

#Variables
numberOfLines = 0
allocatedKey = 'Allocated:'
freedKey = 'Freed:'

msgIndexArray = range(0,256)

msgExtStartTimestamp = 0
msgExtEndTime = 0
allocatedFound = 0
freedFound = 0
deltaTime = 0
sampleCount = 0
doubleAllocationCount = 0
doubleDeallocationCount = 0
swappedDeltas = 0
badLines = 0
maxDeltaRecorded = 0

#print "Total Number of lines in this file: ", len(currInputfile)

# Go through indeces one by one
for currMsgIndex in msgIndexArray:
    # Write the current index into the file
    currMsgIndex = str(hex(currMsgIndex))    
    outputfile.write('\n')
    outputfile.writelines(currMsgIndex)
    outputfile.write(',')
    
    print 'Searching for index: ', currMsgIndex
    # Go through each line for each index separately
    for line in currInputfile:
        # Separate the line into elemenets
        currentParsingLine = line.split()
        # Make sure the printf is correct
        if len(currentParsingLine) == 7:
            # Record the timestamp of the line
            currentTimeStamp = currentParsingLine[1]
            # Find the MsgExt index in that line
            if currentParsingLine[6] == currMsgIndex:
               #print "Found index ", currMsgIndex + " line ", line
               # Look for allocation first
               if currentParsingLine[5] == allocatedKey:
                  msgExtStartTimestamp = int(currentTimeStamp,0)
                  if allocatedFound == 1:
                     print "Double Allocation for ", currMsgIndex
                     doubleAllocationCount += 1
                  allocatedFound = 1
               # Make sure the freeing is on an allocated extension
               if (currentParsingLine[5] == freedKey) and (allocatedFound == 1):
                  msgExtEndTime = int(currentTimeStamp,0)
                  if freedFound == 1:
                    print "Double Deallocation for ", currMsgIndex
                    doubleDeallocationCount += 1
                  freedFound = 1
               if (freedFound == 1 and allocatedFound == 1):
                  freedFound = 0
                  allocatedFound = 0
                  
                  #print "Start time = ", msgExtStartTimestamp
                  #print "End time = ", msgExtEndTime
                  # Calculate the delta time between allocation and de-allocation
                  deltaTime = msgExtEndTime - msgExtStartTimestamp
                  if deltaTime <= 0:
                     print "Time Swapped, delta is ", deltaTime
                     swappedDeltas += 1
                  else:
                     #print "Delta for msg ", currMsgIndex + " is ", deltaTime
                     # Write the measurement into a file
                     sampleCount +=1
                     if deltaTime > maxDeltaRecorded:
                        maxDeltaRecorded = deltaTime
                     #if sampleCount == 16384:
                     #   print "Collected max Samples for CSV file, Breaking the loop"
                     #   break
                     outputfile.write(str(deltaTime))
                     outputfile.write(',')
                  
        else:
            # Log the bad entry
            print "Bad Line ", currentParsingLine
            badLines += 1
     #change in a different place to test out merge
    if sampleCount == 0:
       print "No Samples for Msg ", currMsgIndex
    else:
       print "Total samples for Msg ", currMsgIndex + " is ", sampleCount
       print "Max Delta Time Recorded for Msg ", currMsgIndex + " is ", maxDeltaRecorded
       print "Total Double Allocation Count for Msg ", currMsgIndex + " is ", doubleAllocationCount
       print "Total Double De-allocation Count for Msg ", currMsgIndex + " is ", doubleDeallocationCount
       print "Total Swapped (Erroneous) Delta times for Msg ", currMsgIndex + " is ", swappedDeltas
       print "Total Bad Lines in the run for Msg ", currMsgIndex + " is ", badLines
    sampleCount=0
    doubleAllocationCount = 0
    doubleDeallocationCount = 0
    swappedDeltas = 0
    badLines = 0
    maxDeltaRecorded = 0
    currInputfile.seek(0)
        
# Close the outputfile
outputfile.close()