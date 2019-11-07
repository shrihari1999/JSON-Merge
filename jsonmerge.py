import os
import json

folderPath=input() #arg1
inputPrefix=input() #arg2
outputPrefix=input() #arg3
maxSize=int(input()) #arg4   

maxInputFileSuffix=-1;                                                                             
for file in os.listdir(folderPath):
    name,ext = os.path.splitext(file)
    if(name.startswith(inputPrefix) and ext=='.json'):                   #Filters non JSON files
        remaining_name=name.split(inputPrefix)[1]
        if(remaining_name.isalpha()==False):                             #Filters string suffix (dataxyz.json)
            if(int(remaining_name)>maxInputFileSuffix):
                maxInputFileSuffix=int(remaining_name)
        else:
            print('Encountered file with prefix, without valid suffix')
            
outdata={}      
outcount=1
i=1                                                                                                                 
while(i<=maxInputFileSuffix):
    if(os.path.isfile(inputPrefix+str(i)+'.json')):                      #handles data_x.json missing between two suffixes
        with open(inputPrefix+str(i)+'.json') as f:
            data = json.load(f)
        for key in data:
            if(key in outdata):
                for row in data[key]:   
                    outdata[key].append(row)
            else:
                outdata[key]=[]
                for row in data[key]:
                    outdata[key].append(row)
            outFilePath=outputPrefix+str(outcount)+'.json'
            with open(outFilePath,'w') as outfile:
                json.dump(outdata,outfile,indent=2)  
            print(os.stat(outFilePath).st_size)
            if(os.stat(outFilePath).st_size>maxSize):
                print('Limit exceeded, creating new file...')
                entry = outdata[key].pop()
                print(entry)
                with open(outFilePath,'w') as outfile:
                    json.dump(outdata,outfile,indent=2)
                outcount+=1
                outdata={}
                outdata[key]=[entry]
    i+=1
outFilePath=outputPrefix+str(outcount)+'.json'
with open(outFilePath,'w') as outfile:
    json.dump(outdata,outfile,indent=2)