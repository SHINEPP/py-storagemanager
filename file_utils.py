import os

if __name__ == '__main__':
    os.symlink('/Users/zhouzhenliang/Desktop/temp/build/signed.apk.idsig',
               './l_signed.apk.idsig1')
    print(os.readlink('./l_signed.apk.idsig1'))
