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



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

