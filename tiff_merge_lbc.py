import os
import pandas as pd
import shutil
from pathlib import Path
from wand.image import Image as wi
from wand.resource import limits
from glob import glob
import tifftools as tt

limits['memory'] = 1024 * 1024 * 4096

dir = r'C:\Users\Chris.Prince\Downloads\Tiff'
#spread = 'SDCListing-File_Update_v1.1.xlsm'
ndir = r"C:\Users\Chris.Prince\Downloads\LBC_ReBund"

#tab = 'Manual'
#xlfile = pd.ExcelFile(spread)
#df = pd.read_excel(open(xlfile,'rb'),sheet_name=tab)

def listdirs(dir):
    pth = os.chdir(dir)
    pth = os.getcwd()
    ld = os.listdir(pth)
    for f in ld:
        d = os.path.join(pth, f)
        if os.path.isdir(d):
            #listF.append(str(d))
            P = Path(d).parent.name
            #listP.append(str(P))
            nf = os.path.join(ndir,f)
            #listNF.append(str(nf))
            A = "Dir"
            #listA.append(A)
            if os.path.exists(nf):
                print("Folder Exists - skipping...")
                pass
            else:
                os.makedirs(nf)
            listdirs(d)
        else:
            #listF.append(str(d))
            P = Path(d).parent.name
            #listP.append(str(P))
            A = "Arc"
            #listA.append(A)
            nf = os.path.join(ndir,P,P + '.tif')
            print(nf)
            #listNF.append(str(nf))
            if not os.path.exists(nf):
                print(str(nf) + " bundle doesn't exist - combining & copying...")
                #ref = (ref + '-')
                #print(ref)
                imgs = os.path.join(pth, P)
                imgs = sorted(glob(imgs + '*.tif'))
                print(imgs)
                print("saving to:... " + nf)
                tt.tiff_concat(imgs, nf)
                # with wi() as img:
                #     img.sequence.extend( [ wi(filename=f) for f in imgs ] )
                #     print('Using {0} of {1} memory'.format(limits.resource('memory'), limits['memory']))
                #     img.format = 'tif'
                #     img.save(filename=nf)
                #     img.destroy()
            else:
                print("Bundle exists - skipping...")
                pass




def RebundleXL():
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

listF = []
listNF = []
listP = []
listA = []

listdirs(dir)

#print(listF)
#print(listNF)
#print(listP)
#print(listA)
#RebundleXL()