from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():

    def bcrypt(self, pwd):
        return pwd_ctx.hash(request.password)