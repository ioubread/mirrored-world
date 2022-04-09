from pathlib import Path
import datetime
import os
import shutil
from progress.bar import Bar

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)

            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


td = datetime.datetime.today()
todayString = str(td.year) + (str(td.month)).rjust(2, "0") + (str(td.day)).rjust(2, "0")

originalDir = Path.cwd()


configFile = open("locations.txt", "r")
configContent = configFile.read()
configFile.close()

totalSize = 0
countFile = 0
countDirectory = 0

totalItems = []


# First loop
for location in (configContent).split("\n\n"):
    linesOfLocation = location.split("\n")
    actualLocation = linesOfLocation[0]
    
    if len(linesOfLocation) > 1:
        blackListed = linesOfLocation[1:]
    else:
        blackListed = None


    chunksOfDirectory = actualLocation.split("\\")
    finalChunksOfDirectory = [todayString] + chunksOfDirectory[3:]

    mirroredDirectory = originalDir / Path("\\".join(finalChunksOfDirectory))
    Path(mirroredDirectory).mkdir(parents=True, exist_ok=True)


    for item in os.listdir(Path(actualLocation)):
        pathToSpecificItem = Path(actualLocation) / Path(item)
        
        if blackListed and (str(item) in blackListed):
            continue

        elif os.path.isdir(pathToSpecificItem):
            countDirectory += 1
            sourceFolder = pathToSpecificItem
            destinationFolder = Path(mirroredDirectory) / item

            totalItems.append(["folder", sourceFolder, destinationFolder])


        elif os.path.isfile(pathToSpecificItem):
            countFile += 1
            sourceFile = pathToSpecificItem
            destinationFile = Path(mirroredDirectory) / item

            totalItems.append(["file", sourceFile, destinationFile])


        totalSize += get_size(pathToSpecificItem)





finishedSize = 0
finishedFile = 0
finishedDirectory = 0


lengthTotalItems = len(totalItems)




freezeFolder = originalDir / todayString / ('requirements' + todayString + ".txt")
os.system(f'pip freeze > {freezeFolder}')


os.chdir(originalDir)
pathFile = open(originalDir / todayString / ("PATH" + todayString + ".txt", "w"))
pathFile.write(os.environ['PATH'])
pathFile.close()

print(f"Backing up: {round(totalSize / (1024 * 1024 * 1024))}GB -> {originalDir / todayString}")




with Bar('Backing up', fill='#', suffix='%(percent).1f%%') as bar:
    for i in range(lengthTotalItems):

        itemType, itemSource, itemDestination = totalItems[i]

        if os.path.isdir(itemSource):
            
            shutil.copytree(itemSource, itemDestination)

        elif os.path.isfile(itemSource):

            shutil.copy(itemSource, itemDestination)

        bar.next()
            
