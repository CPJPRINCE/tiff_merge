import os
import pandas as pd
import shutil
from wand.image import Image as wi
from glob import glob

spread = 'SDCListing-File_Update_v1.1.xlsm'
tab = 'Manual'
xlfile = pd.ExcelFile(spread)

df = pd.read_excel(open(xlfile,'rb'),sheet_name=tab)

for index,row in df.iterrows():
    src = row['FullName']
    ref = row['Reference']
    ofld = row['FoldName']
    nfld = row['NewFold']
    dst = row['NewFull']
    numchk = row['NumberingCheck']
    #print(src)
    #print(dst)
    #print(ofld)
    if os.path.exists(nfld):
        print("Folder Exists - skipping...")
        pass
    else:
        os.makedirs(nfld)
    if numchk:
        #print("True")
        if not os.path.exists(dst):
            print(str(src) + " bundle doesn't exist - combining & copying...")
            print(ref)
            #ref = (ref + '-')
            #print(ref)
            imgs = os.path.join(ofld, ref)
            print(imgs)
            imgs = glob(imgs + '*.tif')
            print(imgs)
            with wi() as img:
                img.sequence.extend( [ wi(filename=f) for f in imgs ] )
                img.format = 'tif'
                img.save(filename=dst)
        else:
            print("Bundle exists - skipping...")
            pass
    else:
        #print("False")
        if not os.path.exists(dst):
            print(str(src) + " is Singular File - copying...")
            #shutil.move(src_file, dst)
            shutil.copy(src,dst)
            print("Moving: " + str(src) + " |  To:" + str(dst))
        else:
            print("Singular File exists - skipping...")
            pass
print("Complete!")
