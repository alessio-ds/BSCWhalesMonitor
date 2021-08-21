import requests
from time import sleep
import telegram

bot=telegram.Bot(token='1952741322:AAFrpD_vTN8dUKaH8w8luGfX1iKs_qHrWiE')

'''
try:
    with open('api.txt', mode='r') as a:
        a=a.read()
        if len(a)==34:
            api=a
        else:
            print('Your api key is wrong. Delete the api.txt file and try again.')
except:
    with open('api.txt', mode='w') as a:
        api=input('Input your bscscan.com API key:')
        a.write(api)
'''
api='IB36KSNURJBSDVWWFPUS619ZPDYUNFVDBZ'

def bc():
    # CURRENT BLOCK CHECK
    blockurl='https://bscscan.com/'
    b=requests.get(blockurl)
    b=b.text
    ppb=b.find('Block</span> <a href=')
    ppb+=21
    ppb=b.find('/block/')
    ppb+=7
    pe=b[ppb:].find("'")
    b=b[ppb:ppb+pe]
    try:
        d=int(b)
        #print('Current block: ',b)
        return(b)
    except:
        print("COULDN'T FIND THE CURRENT BLOCK!")
        quit()


#s is the number to subtract to the actual block.
s=50

b=bc()
pb=str(int(b)-s)
token='0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82'
while True:
    try:
        b=bc()
        # -50 TO THE ACTUAL BLOCK - BSC is mining 1 block every 3 seconds
        # every 100 blocks, there are approx 161+ cake tx - 187
        # 100 blocks = 5 mins - 50 = 2m 30s
        # checking 187 txs takes 2m 25s
        # so, 200tx checks = 50 new blocks, 200/4=50
        # 16 txs = 1 block,

        cb=b #current block

        print('\nBlocks to check:',str(int(cb)-int(pb)))
        print('Checking block',pb,'to',cb,'(current block)\n') #100 - 150

        while cb<pb:
		          cb+=1
        r=0
        # CHECKS TOKEN TXs FROM THE CURRENT BLOCK
        apiurl='https://api.bscscan.com/api?module=account&action=txlist&address='+token+'&startblock='+pb+'&endblock='+cb+'&sort=asc&apikey='+api
        l=(requests.get(apiurl)).text

        t=l.count('hash')

        if t<16:
            print('Waiting for at least 16 transactions.')
        while t<16:
            cb=bc()
            apiurl='https://api.bscscan.com/api?module=account&action=txlist&address='+token+'&startblock='+pb+'&endblock='+cb+'&sort=asc&apikey='+api
            l=(requests.get(apiurl)).text
            t=l.count('hash')
            print(f"Checking block {pb} to {cb} ({str(int(cb)-int(pb))}) - Txs to check: {t}", end="\r")
            '''
            print(f"Blocks to check: {str(int(cb)-int(pb))}", end="\r")
            print(f"Checking block {pb} to {cb}", end="\r")
            print(f"Waiting for at least 16 transactions. Txs to check: {t}", end="\r")
            '''
            sleep(3)

        # REPEATS ITSELF
        print('\n')
        for c in range(t):
            sleep(0.33) # the cap is 5 requests per second. This makes 3 requests per second at max.
            pos=l.find('hash')
            l=l[pos+4:]
            pos=l.find('0')
            h=l[pos:pos+66] # 66 is the lenght of every tx hash
            url='https://bscscan.com/tx/'+h
            r=requests.get(url)
            testo=r.text
            #print(testo)
            pos=testo.find(' / Cake">')
            pos+=9
            testo=testo[pos:]
            pos2=testo.find('<')
            testo=testo[:pos2]

            posdolla=(testo.find('$'))+1
            posdolla2=(testo.find(')'))-1
            dolla=testo[posdolla:posdolla2]
            print(f"{c/t*100:.3f} %", end="\r")
            try:
                if ',' in dolla:
                    dolla=float(dolla.replace(',',''))
                else:
                    dolla=float(dolla)
                if dolla>=100000:
                    hw=r.text
                    pos=hw.find("From</b> </span><span class='hash-tag text-truncate  mr-1'><a href='/token/")
                    hw=hw[pos:]
                    pos2=hw.find('Binance')
                    pos3=hw.find('To')
                    if pos2<pos3:
                        # BUY
                        e=''
                        for _ in range(round(dolla/100000)):
                            e+='🟢'
                        hw=e+'\nBOUGHT '
                    else:
                        # SELL
                        e=''
                        for _ in range(round(dolla/100000)):
                            e+='🔴'
                        hw=e+'\nSOLD '

                    ds=h+'\n'+testo+'\n'
                    dstg='https://bscscan.com/tx/'+h+'\n'+hw+'CAKES '+testo
                    with open('logs.txt', mode='a') as f:
                        f.write(ds)
                    print('\n',h)
                    print(testo,'\n')
                    status=bot.send_message(chat_id='@cakewhales', text=dstg, parse_mode=telegram.ParseMode.HTML)


            except:
                pass
        pb=cb #previous block
    except:
        # Since the response will always be <200>, I didn't want to implement a smart feature to detect when you get blocked.
        print("You got momentarily blocked by bscscan.com, will try again in 15 seconds")
        sleep(15)
