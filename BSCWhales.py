import requests
from time import sleep

try:
    with open('apikey.txt', mode='r') as a:
        a=a.read()
        if len(a)==34:
            api=a
        else:
            print('Your api key is wrong. Try again.')
            quit()
except:
    with open('apikey.txt', mode='w') as a:
        api=input('Input your bscscan.com API key: ')
        a.write(api)


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
token=input('Which token would you like to scan? \nFor example, $CAKE is: 0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82\n')
burn=input("What's the burn contract address, if any? \n For example, $CAKE burn contract address is: 0x8488cb2f54ecb9aa1cdc1bc83bc1d200bb2f216b\nIf there's none, press ENTER\n")
while len(token)!=42: # 42 is the lenght of every token address
    token=input('Wrong token. Try again: ')
if burn=='':
    pass
else:
    while len(burn)!=42: # 42 is the lenght of every burn contract address
        burn=input('Wrong burn contract address. Try again: ')
b=bc()
pb=str(int(b)-s)
#pos token name

tn=(requests.get('https://bscscan.com/address/'+token)).text
ptn=tn.find('View Token Tracker Page')
tn=tn[ptn:]
startp=tn.find('(')
startp+=1
endp=tn.find(')')
token_name=tn[startp:endp]
print('Token found: '+token_name)
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
        if burn=='':
            pass
        else:
            burnurl='https://api.bscscan.com/api?module=account&action=txlist&address='+burn+'&startblock='+pb+'&endblock='+cb+'&sort=asc&apikey='+api
            burnl=(requests.get(burnurl)).text
            tb=burnl.count('hash')


        if t<16:
            print('Waiting for at least 16 transactions.')
        while t<16:
            cb=bc()
            apiurl='https://api.bscscan.com/api?module=account&action=txlist&address='+token+'&startblock='+pb+'&endblock='+cb+'&sort=asc&apikey='+api
            l=(requests.get(apiurl)).text
            t=l.count('hash')
            if burn=='':
                pass
            else:
                burnurl='https://api.bscscan.com/api?module=account&action=txlist&address='+burn+'&startblock='+pb+'&endblock='+cb+'&sort=asc&apikey='+api
                burnl=(requests.get(burnurl)).text
                tb=burnl.count('hash')

            print(f"Checking block {pb} to {cb} ({str(int(cb)-int(pb))}) - Txs to check: {t}", end="\r")
            '''
            print(f"Blocks to check: {str(int(cb)-int(pb))}", end="\r")
            print(f"Checking block {pb} to {cb}", end="\r")
            print(f"Waiting for at least 16 transactions. Txs to check: {t}", end="\r")
            '''
            sleep(3)

        # REPEATS ITSELF
        print('\n')
        if burn=='':
            pass
        else:
            for c in range(tb):
                sleep(0.33) # the cap is 5 requests per second. This makes 3 requests per second at max.
                pos=burnl.find('hash')
                burnl=burnl[pos+4:]
                pos=burnl.find('0')
                h=burnl[pos:pos+66] # 66 is the lenght of every tx hash
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
                try:
                    if ',' in dolla:
                        dolla=float(dolla.replace(',',''))
                    else:
                        dolla=float(dolla)
                    if dolla>=100000:
                        hw=r.text
                        e=''
                        for _ in range(round(dolla/100000)):
                            e+='🔥'
                        dstg='\n\nhttps://bscscan.com/tx/'+h+'\n'+e+'\nTOKEN BURN of '+token_name+' '+testo
                        with open('logs.txt', mode='a', encoding='UTF-8') as f:
                            f.write(dstg)
                        print(dstg)
                except:
                    pass
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
                if dolla>=100:
                    hw=r.text
                    if hw.count('Binance: Hot Wallet')==0:
                        e=''
                        for _ in range(round(dolla/100000)):
                            e+='💸'
                        dstg='\n\nhttps://bscscan.com/tx/'+h+'\n'+e+'\nToken Transfer of '+token_name+' '+testo
                    elif hw.count('Binance: Hot Wallet')==2 and hw.find('Binance: Hot Wallet 6')!=-1 and '0x7c51ded61930fb26eb257db7eb04e0bdff4820f5' in hw:
                        e=''
                        for _ in range(round(dolla/100000)):
                            e+='🔀'
                        dstg='https://bscscan.com/tx/'+h+'\n'+e+'\nBinance Hot Wallets bought '+token_name+' '+testo
                    elif hw.count('Binance: Hot Wallet')>3:
                        e=''
                        for _ in range(round(dolla/100000)):
                            e+='🔀'
                        dstg='\n\nhttps://bscscan.com/tx/'+h+'\n'+e+'\nBinance Hot Wallet Token Transfer of '+token_name+' '+testo

                    else:
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
                        dstg='\n\nhttps://bscscan.com/tx/'+h+'\n'+hw+' '+token_name+' '+testo

                    with open('logs.txt', mode='a', encoding='UTF-8') as f:
                        f.write(dstg)
                    print(dstg)


            except:
                pass
        pb=cb #previous block
    except:
        # Since the response will always be <200>, I didn't want to implement a smart feature to detect when you get blocked.
        print("You got momentarily blocked by bscscan.com, will try again in 15 seconds")
        sleep(15)
