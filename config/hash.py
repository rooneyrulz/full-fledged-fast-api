from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():

    def bcrypt(self, pwd):
        return pwd_ctx.hash(pwd)

    
    def verify(self, hashed_pwd, plain_pwd):
        return pwd_ctx.verify(plain_pwd, hashed_pwd)