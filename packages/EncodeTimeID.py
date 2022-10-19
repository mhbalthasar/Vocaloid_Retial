import datetime

def __trans_T(src):
    Time_Hash_Map=[
                   [8, 11, 0, 12, 16, 10, 15, 3, 14, 4], 
                   [14, 4, 11, 20, 7, 21, 2, 22, 15, 19], 
                   [18, 0, 11, 15, 12, 5, 8, 6, 16, 24], 
                   [13, 22, 0, 19, 14, 10, 4, 20, 16, 7], 
                   [18, 5, 12, 9, 25, 1, 10, 26, 14, 27], 
                   [8, 23, 3, 24, 6, 9, 11, 15, 2, 20],
                   [15, 18, 0, 19, 25, 17, 22, 3, 21, 4], 
                   [21, 4, 18, 30, 7, 32, 2, 33, 22, 28], 
                   [27, 0, 18, 22, 19, 5, 15, 6, 25, 37], 
                   [20, 33, 0, 28, 21, 17, 4, 30, 25, 7], 
                   [27, 5, 19, 16, 38, 1, 17, 39, 21, 40], 
                   [15, 34, 3, 37, 6, 16, 18, 22, 2, 30]
                  ]
    ret=[]
    rek=[]
    #[0:1] IS YEAR
    yr = src.year % 100
    ret=ret+[Time_Hash_Map[0][int(yr / 10)], Time_Hash_Map[1][yr % 10]]
    rek=rek+[Time_Hash_Map[6][int(yr / 10)], Time_Hash_Map[7][yr % 10]]
    #[2:3] IS MONTH,FILL 0
    mn = src.month
    if mn < 10:
        ret=ret + [18,Time_Hash_Map[3][mn]]
        rek=rek + [27,Time_Hash_Map[9][mn]]
    else:
        ret=ret+[Time_Hash_Map[2][int(mn / 10)], Time_Hash_Map[3][mn % 10]]
        rek=rek+[Time_Hash_Map[8][int(mn / 10)], Time_Hash_Map[9][mn % 10]]
    #[4:5] IS DAY,FILL 0
    dy = src.day
    if dy < 10:
        ret=ret+[18,Time_Hash_Map[5][dy]]
        rek=rek+[27,Time_Hash_Map[10][dy]]
    else:
        ret=ret+[Time_Hash_Map[4][int(dy / 10)], Time_Hash_Map[5][dy % 10]]
        rek=rek+[Time_Hash_Map[10][int(dy / 10)], Time_Hash_Map[11][dy % 10]]
    #RETURN VAL AND HEAVYKEY
    return ret,rek

def __hash_sum_T(src):
    ret=0
    for key in src:
        ret=ret + key
    ret=(0x351 + ret) & 0xff
    return ret

def Encode_TimeID(src):
    TimeSeed,TimeKey=__trans_T(src)
    tKey=__hash_sum_T(TimeKey)
    EncodeSeed="23456789ABCDEFGHKLMNPRSTWXYZ"
    EncodeKey="KL23456789ABCDEF"
    IVSeed="4850C3E"
    Martix1=[
            [7,1,8,8],[4,2,3,0],[8,1,5,0],[1,0,1,0],
            [2,1,1,0],[4,2,9,0],[0,5,0,3],[5,0,5,0],
            [1,7,0,2],[5,9,0,1],[0,0,1,1],[3,1,1,0],
            [1,2,3,1],[3,1,2,2],[8,9,1,2],[9,8,0,1],
            [1,7,5,2],[8,2,9,3],[6,6,1,8],[9,2,7,3],
            [1,8,2,6],[1,3,2,7],[7,3,4,9],[8,2,1,4],
            [6,8,7,8],[3,8,7,5],[2,4,3,2],[7,5,9,1],
            [8,4,6,9],[3,6,4,2],[9,7,0,7],[2,4,1,8]
          ]
    Martix2=[
            [1,8,8,7],[2,3,0,4],[1,5,0,8],[0,1,0,1],
            [1,1,0,2],[2,9,0,4],[5,0,3,0],[0,5,0,5],
            [7,0,2,1],[9,0,1,5],[0,1,1,0],[1,1,0,3],
            [2,3,1,1],[1,2,2,3],[9,1,2,8],[8,0,1,9],
            [2,1,7,5],[3,8,2,9],[8,6,6,1],[3,9,2,7],
            [6,1,8,2],[7,1,3,2],[9,7,3,4],[4,8,2,1],
            [8,6,8,7],[5,3,8,7],[2,2,4,3],[1,7,5,9],
            [9,8,4,6],[2,3,6,4],[7,9,7,0],[8,2,4,1]
          ]
    ID_TYPE=[]
    ID_KEY=[]
    ID_VAL=[]
    ID_CHK=[]
    for i in range(0,6):
        seed_index = TimeSeed[i]
        seed_index = (seed_index + Martix1[tKey >> 4][i % 4]) % 28
        seed_index = (seed_index + Martix2[0x10 + (tKey & 0xF)][i%4]) % 28
        ID_VAL.append(EncodeSeed[seed_index])
    for i in range(0,7):
        seed_index = ord(IVSeed[i])-44
        seed_index = (seed_index + Martix2[tKey >> 4][i % 4]) % 28
        seed_index = (seed_index + Martix1[0x10 + (tKey & 0xF)][i%4]) % 28
        ID_KEY.append(EncodeSeed[seed_index])
    ID_CHK.append(EncodeKey[tKey >> 4])
    ID_CHK.append(EncodeKey[tKey & 0xF])
    ID_TYPE.append('B') # MEAN IS ORIGIN.

    ID_RESULT=ID_TYPE+ID_KEY+ID_VAL+ID_CHK
    ID_RESULT_STRING=''.join(ID_RESULT)
    return ID_RESULT_STRING

if __name__=="__main__":
    src=datetime.datetime.now()
    ret=Encode_TimeID(src)
    print(ret)
