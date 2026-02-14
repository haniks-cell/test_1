# from database.models import Configuration

# def generate_cfg (res:Configuration) -> str:

async def viewarr (arr) -> str:
    outstr:str = ''
    cnt:int = 0
    incnt = 0
    for i in arr:
        outstr += '\n\n\n'
        outstr += i[0]
        for j in i[1::]:
            for z in j:
                cnt +=1
                outstr += f'\n{cnt}. {z}'
        cnt = 0
    return outstr
    