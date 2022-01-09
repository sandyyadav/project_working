import cv2, os

def conv(base_path,new_path):
    print(base_path)
    print(new_path)
    for infile in os.listdir(base_path):
        print ("file : " + infile)
        read = cv2.imread(base_path + infile)
        outfile = infile.split('.')[0] + '.jpg'
        cv2.imwrite(new_path+outfile,read,[int(cv2.IMWRITE_JPEG_QUALITY), 200])

for i in range(1,16):
    print(i)
    base_path = f"./leaf{i}/"
    new_path = f"./l{i}/"
    conv(base_path,new_path)

# base_path = "./leaf1/"
# new_path = "./l1/"
