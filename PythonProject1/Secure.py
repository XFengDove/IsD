import os
import pickle
from pickle import Pickler
from cryptography.fernet import Fernet

class SecuerT:
    def __init__(self,KeyPath="Save/Yueqs.key"):
        """读取密钥，若密钥不存在则生成密钥

        :param KeyPath: 存储密钥的路径
        """
        if os.path.exists(KeyPath):
            with open(KeyPath,"rb") as f:
                self.Key=f.read()
                self.Cipher=Fernet(self.Key)
        else:
            os.mkdir("Save")
            Key=Fernet.generate_key()
            with open(KeyPath,"wb") as f:
                f.write(Key)
                self.Key=Key
                self.Cipher = Fernet(self.Key)
        self.KeyPath=KeyPath
    def Save(self,SavePath_AndFileName:str,Data):
        """加密一个新文件

        :param Data: 需要保存的数据
        :return: None
        """
        #序列化数据
        Pickler=pickle.dumps(Data)
        #加密数据
        EncodData=self.Cipher.encrypt(Pickler)
        with open(SavePath_AndFileName,"wb") as f:
            f.write(EncodData)
    def SecuerData(self,Data_Path):
        """加密一个已存的文件"""
        with open(Data_Path,"r") as f:
            Txt=f.read()
            self.Save(Data_Path,Txt)
    def DecryptData(self,Data_Path):
        """逆向一个文件"""
        Txt=self.Load_SData(Data_Path)
        with open(Data_Path,"w") as f:
            f.write(Txt)
    def Load_SData(self,Data_Path:str):
        with open(Data_Path,"rb") as f:
            Data=f.read()

            return pickle.loads(self.Cipher.decrypt(Data))

