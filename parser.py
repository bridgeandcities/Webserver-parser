from datetime import datetime
import ipaddress

class Parser:
    def __init__(self):
        self.numberOfDays = 0 # Count number of days passed
        
        self.startDate = datetime.today()
        self.endDate = datetime.today()
        
        self.fileTypeDict = {} # Contains file extension - file type information
        self.initializeFileType()
        
    def initializeFileType(self):  # Define file types for each file
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"

        # Stuff I added myself to answer assignment questions
        self.transferredSumBytes = 0 

        self.totalResponseSuccessful = 0
        self.totalResponseNotModified = 0
        self.totalResponseFound = 0
        self.totalResponseUnsuccessful = 0

        self.internalIPCIDR = "128.233.0.0/24"
        self.internalHostname = "usask.ca"
        self.internalIPCount = 0
        self.externalIPCount = 0

        self.internalBytesCount = 0
        self.externalBytesCount = 0

        self.requestTotal = 0
        self.requestHTML = 0
        self.requestImages = 0
        self.requestSound = 0
        self.requestVideo = 0
        self.requestFormatted = 0
        self.requestDynamic = 0
        self.requestOthers = 0

        self.transferredHTMLBytes = 0
        self.transferredImagesBytes = 0
        self.transferredSoundBytes = 0
        self.transferredVideoBytes = 0
        self.transferredFormattedBytes = 0
        self.transferredDynamicBytes = 0
        self.transferredOthersBytes = 0

        self.uniqueObjectDict = {}
        self.uniqueObjectBytesDict = {}
        self.uniqueObjectBytesDictCopy = {}

    def parse(self, logFile):  # Read each line from the log and process output
        for line in logFile:
            elements = line.split()
            
            # Skip to the next line if this line has an empty string
            if line is '':
                continue

            # Skip to the next line if this line contains not equal to 9 - 11 elements
            if not (9 <= len(elements) <= 11):
                continue

            # If there is more than 1 element in user information, correct the index of other elements
            timeStrIndex = 0
            for idx, val in enumerate(elements):
                timeStrIndex = idx - 1
                if '-0600]' == val:
                    break

            sourceAddress = elements[0]
            timeStr = elements[timeStrIndex].replace('[', '')
            requestMethod = elements[timeStrIndex+2].replace('"','')
            requestFileName = elements[timeStrIndex + 3].replace('"', '')
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]

            ################## From Here, implement your parser ##################
            # Inside the for loop, do simple variable assignments & modifications
            # Please do not add for loop/s
            # Only the successful requests should be used from question 6 onward

            # Prints assigned elements. Please comment print statement.
            """print(sourceAddress, timeStr, requestMethod, requestFileName, responseCode, replySizeInBytes, end="")"""
            
            # Assigns & prints format type. Please comment print statement.
            fileType = self.getFileType(requestFileName)
            #print(fileType)
            #####################################################################
            # Sum the bytes transferred in the log file
            
            try:
                self.transferredSumBytes += int(replySizeInBytes)
            except ValueError:
                replySizeInBytes = 0
                continue

            # Check the response code and record the total
            responseType = self.checkResCode(responseCode)
            if responseType == "Successful":
                self.totalResponseSuccessful += 1
            elif responseType == "Found":
                self.totalResponseFound += 1
            elif responseType == "Not Modified":
                self.totalResponseNotModified += 1
            else:
                self.totalResponseUnsuccessful += 1

            # Count whether IP is internal to the network or external
            InternalOrExternalIP = self.checkInternalOrExternal(sourceAddress)
            if InternalOrExternalIP == "Internal":
                self.internalIPCount += 1
                self.internalBytesCount += int(replySizeInBytes)
            elif InternalOrExternalIP == "External":
                self.externalIPCount += 1
                self.externalBytesCount += int(replySizeInBytes)

            # Q1: Write a condition to identify a start date and an end date.
            self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
            self.endDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
            """print(self.startDate, self.endDate)"""

            # Q8-9: 
            self.requestTotal += 1
            if fileType == "HTML":
                self.requestHTML += 1
                self.transferredHTMLBytes += int(replySizeInBytes)
            elif fileType == "Images":
                self.requestImages += 1
                self.transferredImagesBytes += int(replySizeInBytes)
            elif fileType == "Sound":
                self.requestSound += 1
                self.transferredSoundBytes += int(replySizeInBytes)
            elif fileType == "Video":
                self.requestVideo += 1
                self.transferredVideoBytes += int(replySizeInBytes)
            elif fileType == "Formatted":
                self.requestFormatted += 1
                self.transferredFormattedBytes += int(replySizeInBytes)
            elif fileType == "Dynamic":
                self.requestDynamic += 1
                self.transferredDynamicBytes += int(replySizeInBytes)
            elif fileType == "Others":
                self.requestOthers += 1
                self.transferredOthersBytes += int(replySizeInBytes)

            # Q11: 
            self.checkUniqueObject(requestFileName, replySizeInBytes)

        # Outside the for loop, generate statistics output
        # Q3: Total bytes transferred
        print("############Q3: ", "\n", (self.transferredSumBytes / 1000))
        # Q4: Average bytes transferred per 341 days
        print("############Q4: ", "\n", ((self.transferredSumBytes / 213) / 1000))
        # Q5: 
        print("############Q5: ")
        print("Found: ", self.totalResponseFound)
        print("Successful: ", self.totalResponseSuccessful)
        print("Not Modified", self.totalResponseNotModified)
        print("Unsuccessful", self.totalResponseUnsuccessful)
        # Q6:
        print("############Q6: ")
        print("Internal %: ", ((self.internalIPCount / (self.internalIPCount + self.externalIPCount)) * 100))
        print("External %: ", ((self.externalIPCount / (self.internalIPCount + self.externalIPCount)) * 100))
        # Q7:
        print("############Q7: ")
        print("Internal % total bytes: ", ((self.internalBytesCount / (self.internalBytesCount + self.externalBytesCount)) * 100))
        print("External % total bytes: ", ((self.externalBytesCount / (self.internalBytesCount + self.externalBytesCount)) * 100))
        # Q8:
        print("############Q8: ")
        print("Total requests: ", self.requestTotal)
        print("HTML: ", ((self.requestHTML / self.requestTotal) * 100))
        print("Images: ", ((self.requestImages / self.requestTotal) * 100))
        print("Sound: ", ((self.requestSound / self.requestTotal) * 100))
        print("Video: ", ((self.requestVideo / self.requestTotal) * 100))
        print("Formatted: ", ((self.requestFormatted / self.requestTotal) * 100))
        print("Dynamic: ", ((self.requestDynamic / self.requestTotal) * 100))
        print("Others", ((self.requestOthers / self.requestTotal) * 100))
        # Q9:
        print("############Q9: ")
        print("Total bytes: ", self.transferredSumBytes)
        print("HTML: ", ((self.transferredHTMLBytes / self.transferredSumBytes) * 100))
        print("Images: ", ((self.transferredImagesBytes / self.transferredSumBytes) * 100))
        print("Sound: ", ((self.transferredSoundBytes / self.transferredSumBytes) * 100))
        print("Video: ", ((self.transferredVideoBytes / self.transferredSumBytes) * 100))
        print("Formatted: ", ((self.transferredFormattedBytes / self.transferredSumBytes) * 100))
        print("Dynamic: ", ((self.transferredDynamicBytes / self.transferredSumBytes) * 100))
        print("Others: ", ((self.transferredOthersBytes / self.transferredSumBytes) * 100))
        # Q10:
        print("############Q10: ")
        print("Average transfer sizes in bytes: ")
        if self.requestHTML != 0:
            print("HTML: ", (self.transferredHTMLBytes / self.requestHTML))
        else:
            print("HTML: 0")
        if self.requestImages != 0:
            print("Images: ", (self.transferredImagesBytes / self.requestImages))
        else:
            print("Images: 0")
        if self.requestSound != 0:
            print("Sound: ", (self.transferredSoundBytes / self.requestSound))
        else:
            print("Sound: 0")
        if self.requestVideo != 0:
            print("Video: ", (self.transferredVideoBytes / self.requestVideo))
        else:
            print("Video: 0")
        if self.requestFormatted != 0:
            print("Formatted: ", (self.transferredFormattedBytes / self.requestFormatted))
        else:
            print("Formatted: 0")
        if self.requestDynamic != 0:
            print("Dynamic: ", (self.transferredDynamicBytes / self.requestDynamic))
        else:
            print("Dynamic: 0")
        if self.requestOthers != 0:
            print("Others: ", (self.transferredOthersBytes / self.requestOthers))
        else:
            print("Others: 0")
        # Q11: 
        print("############Q11: ")
        d = self.uniqueObjectDict
        s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
        #print("Individual objects and their counts: ")
        #for k, v in s:
            #print(k, v)
        #print("Objects that were only accessed once: ")
        accessedOnce = [(k, v) for k, v in d.items() if v == 1]
        #print(accessedOnce)
        print("What % of unique objects were accessed only once: ")
        print(((len(accessedOnce)/len(d)) * 100))
        print("What % of bytes were only accessed once: ")
        self.uniqueObjectBytesDictCopy = self.uniqueObjectBytesDict.copy()
        for k, v in d.items():
            if v != 1:
                del self.uniqueObjectBytesDict[k]
        if len(self.uniqueObjectBytesDict) > 0:        
            accessedOnceSum = sum(int(v) for k, v in self.uniqueObjectBytesDict.items())
            print(((accessedOnceSum / self.transferredSumBytes) * 100))
        else:
            print("0")       
        
    def getFileType(self, URI):
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'):
            return 'HTML'
        filename = URI.split('/')[-1]
        if '?' in filename:
            return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        return 'Others'

    def checkResCode(self, code):
        if code == '200' : return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'   
        return None

    def checkInternalOrExternal(self, address):
        if self.checkIPValid(address):
            if ipaddress.ip_address(address) in ipaddress.ip_network(self.internalIPCIDR):
                return "Internal"
            else:
                return "External"
        else:
            if self.internalHostname in address:
                return "Internal"
            else:
                return "External"
    
    def checkIPValid(self, address):
        try:
            network = ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    def checkUniqueObject(self, fileName, replyBytes):
        if fileName not in self.uniqueObjectDict:
            self.uniqueObjectDict[fileName] = 1
        else:
            self.uniqueObjectDict[fileName] += 1
        
        if fileName not in self.uniqueObjectBytesDict:
            self.uniqueObjectBytesDict[fileName] = replyBytes

    def makeCDF(self, d1, d2):
        cum = 0
        tempList = []
        countSum = sum(d2.values())                             #total no. times access of all objects
        for k in d1.keys():
            #cum += (d2[k] / countSum)
            #print(cum)
            tempList.append([k, int(d1[k]), d2[k], (d2[k] / countSum)])
        #print(tempList)
        tempList.sort(key=lambda x: x[1])
        #print(tempList)
        for entry in tempList:
            #print(entry[3])
            cum += entry[3]
            entry.append(cum)
        #print(tempList)
        return tempList
        
if __name__ == '__main__':
    logfile = open('UofS_access_log', 'r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
