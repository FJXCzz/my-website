TORTOISE_ORM={
        'connections':{
            'default':{
                'engine':'tortoise.backends.mysql',
                'credentials':{
                    'host':'192.168.31.119',
                    'port':'3306',
                    'user':'root',
                    'password':'123456',
                    'database':'website',
                    'minsize':1,
                    'maxsize':5,
                    'charset':'utf8mb4',
                    'echo':True
                }


            }
        },
        'apps':{
            'models':{
                'models':['models'],
                'default_connection':'default'
            }
        },
        'use_tz':False,
        'timezone':'Asia/Shanghai'
        
    }


#openssl rand -hex 32    生成加密token的密钥
SECRET_KEY = "77522fa54d6bd15dd6ddd07cdb5cf48c0e3b9bd5991c233dd7b6dad19f0ea663"
ALGORITHM = "HS256"  #token加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30   #token过期时间

