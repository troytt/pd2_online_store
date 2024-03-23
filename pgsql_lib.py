import psycopg2



def xstr(s):
    if s is None:
        return ''
    else:
        return s

def xbool(s):
    if s is None:
        return 'false'
    elif s:
        return 'true'
    else:
        return 'false'

def xint(s):
    if s is None:
        return '0'
    else:
        return str(s)

    
#conn = psycopg2.connect(
#        host = '127.0.0.1',
#        port = '5432',
#        user = 'postgres',
#        password = 'Harlequin1',
#        database = 'postgres')

#cursor = conn.cursor()
#sql = """INSERT INTO "public"."Item" (iid) VALUES(23) ON CONFLICT DO NOTHING;"""
#cursor.execute(sql)
#conn.commit()
#cursor.close()
#conn.close()

if __name__ == '__main__':
    print('xstr')
    print([None, xstr(None)])
    print(['', xstr('')])
    print(['a', xstr('a')])

    print('xbool')
    print([None, xbool(None)])
    print([True, xbool(True)])
    print([False, xbool(False)])

    print('xint')
    print([None, xint(None)])
    print([0, xint(0)])
    print([100000, xint(100000)])

