import random

import time
from PIL import Image
import cv2

# static_path=r"C:\Users\Aslaha\Desktop\QrPayment\static\\"
static_path=r"D:\QrPayment\static\\"

class QR_split:
    def qr2vc(self, master_id):

        import qrcode
        img = qrcode.make(master_id)
        img.save(static_path+"temp_files\\"+master_id + '.png')
        img=Image.open(static_path+"temp_files\\"+master_id + '.png')
        img = img.resize((100, 100))
        img.save(static_path+"temp_files\\"+master_id + '.png')
        # Get QR image
        img = cv2.imread(static_path+"temp_files\\"+master_id + '.png', 2)
        ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(static_path+"temp_files\\"+"binary.png", bw_img)

        share1 = Image.new("RGB", size = (100, 100))
        share2 = Image.new("RGB", size = (100, 100))
        share1_pix=share1.load()
        share2_pix=share2.load()
        img = Image.open(static_path+"temp_files\\"+"binary.png")
        img_pix = img.load()
        lst=[]
        for i in range(100):
            if i % 2 == 0:
                # rand = random.randint(10, 120)
                flg="0"
                for j in range(100):
                    pix = img_pix[i,j]
                    print(pix)
                    pix1 = 255 - pix
                    pix2 = 255
                    share1_pix[i, j] = (pix1, pix1, pix1)
                    share2_pix[i, j] = (pix2, pix2, pix2)
            else:
                # rand = random.randint(10, 120)
                flg = "1"
                for j in range(100):
                    pix = img_pix[i, j]
                    print(pix)
                    pix1 = 255
                    pix2 = 255 - pix
                    share1_pix[i, j] = (pix1, pix1, pix1)
                    share2_pix[i, j] = (pix2, pix2, pix2)
            lst.append(flg)
        lst = "#".join(lst)
        dt = time.strftime("%Y%m%d_%H%M%S")
        lst = lst + "$" +dt
        share1.save(static_path+"server1\\"+dt + "_share1.png")
        share2.save(static_path+"server2\\"+dt + "_share2.png")

        print("HHH  ", lst)
        import qrcode
        img = qrcode.make(lst)
        img.save(static_path+"temp_files\\"+dt+'_myqr.png')
        return "/static/temp_files/"+dt+'_myqr.png'


    def vc2qr(self, key):
        lst = key.split("$")[0]
        dt = key.split("$")[1]
        lst=lst.split("#")
        img1 = cv2.imread(static_path+"server1\\" + dt + "_share1.png", 2)
        ret, bw_img = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(static_path + "server1\\" +dt + "_share1.png", bw_img)
        img2 = cv2.imread(static_path+"server2\\" + dt + "_share2.png", 2)
        ret, bw_img = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(static_path + "server2\\" +dt + "_share2.png", bw_img)
        share1 = Image.open(static_path+"server1\\" +dt + "_share1.png")
        share2 = Image.open(static_path+"server2\\" +dt + "_share2.png")

        share1_pix=share1.load()
        share2_pix=share2.load()

        orig_qr = Image.new("RGB", size = (100, 100))
        img_pix = orig_qr.load()
        for i in range(100):
            val = lst[i]
            if val == 0:
                for j in range(100):
                    pix1 = share1_pix[i, j]
                    pix2 = share2_pix[i, j]
                    new_pix_val = pix2 - pix1
                    img_pix[i, j] = new_pix_val
            else:
                for j in range(100):
                    pix1 = share1_pix[i, j]
                    pix2 = share2_pix[i, j]
                    new_pix_val = pix1 - pix2
                    img_pix[i, j] = new_pix_val
        orig_qr.save(static_path+"temp_files\\decrypted.png")
        # read the QRCODE image
        # img = cv2.imread(static_path+"temp_files\\decrypted.png")
        return "/temp_files/decrypted.png"
        # if bbox is not None:
        #     return data




# qr_name="hb.png"
# qr_obj= QR_split()
# bb = qr_obj.qr2vc(qr_name)
# print("Encryption phase completed")
#
# qr_obj.vc2qr(bb)
# print("Decryption phase completed")