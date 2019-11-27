import xml.dom.minidom as XML

class Page: 
    def __init__(self):
        self.id = ''
        self.text = ''
        self.title = ''

class Hash:
    def __init__(self):
        self.word = ''
        self.idPages = []
def main():
    paginas = []
    
    hashtexto = {}
    hashtitle = {}
    
    file = open('testCollection.dat', 'r', encoding='UTF-8')
    conteudo = file.read()
   
    conteudo = conteudo.replace('<collection>','').replace('</collection>','').replace('\n', '')
    conteudo = conteudo[1:]
    conteudo = conteudo.split('<page>')
    
    for  i in range(len(conteudo)):
        pagina = Page()
            
        id= conteudo[i].split('<id>')
        id = id[1]
        title = id.split("<title>")
        pagina.id  = title[0].replace('</id>', '')
        pagina.id = pagina.id.lower()

        text = title[1].split('<text>')
        pagina.title = text[0].replace('</title>', '')
        pagina.title = pagina.title.lower()

        pagina.text = text[1].replace('</text>', '').replace('</page>', '')
        pagina.text = pagina.text.lower()
        paginas.append(pagina)
    

    for i in range(len(paginas)):
        pagina = paginas[i]
        #separo cada palavra no texto
        auxText = pagina.text.split(' ')
        #separo cada palavra no titulo
        auxTitle = pagina.title.split(' ')

        #percorro cada palavra do texto da pagina 
        for j in range(len(auxText)):
            auxText[j] = auxText[j].replace('[^0-9a-zA-Z_]', '').replace('=', '')
            #se a palavra tem mais de 4 letras
            if(len(auxText[j])>4): 
                #se a palavra existe no hash eu adiciono a pagina ou 
                # conto mais ao contador se ja estiver sido encontrada na mesma pagina
                if auxText[j] in hashtexto:   
                    
                    if hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][0] == pagina.id:
                        #hashtexto[auxText[j]].append(pagina.id)
                        aux = [[pagina.id],[1]]
                        hashtexto[auxText[j]].append(aux)
                        
                    else:
                        print('\033[32m'+str(hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][0])+'\033[0;0m')
                        tabela = int(hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][1])
                        tabela += 1
                        hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][1] = tabela
                else:
                    hashtexto[auxText[j]] = []
                    aux = [[pagina.id],[1]]
                    hashtexto[auxText[j]].append(aux)

    # for i in hashtexto:
    #     print(i, hashtexto[i])
    #     print('\n')
    '''    
        #percorro cada palavra do titulo
        for j in range(len(auxTitle)):
            auxTitle[j] = auxTitle[j].replace('[^0-9a-zA-Z_]', '').replace('=', '')
            #se a palavra tem mais de 4 letras
            if(len(auxTitle[j])>4):
                if auxTitle[j] in hashtexto:
                    print( hashtexto[auxTitle[j]][len(hashtitle[auxTitle[j]])-1][0])
                    if hashtexto[auxTitle[j]][len(hashtitle[auxTitle[j]])-1][0] != pagina.id:
                        hashtitle[auxTitle[j]].append([[pagina.id], [1] ])
                    else: 
                        hashtitle[auxTitle[j]][len(hashtitle[auxTitle[j]])-1][1] +=1
                else:
                    #instancio o dicionario
                    hashtexto[str(auxTitle[j])] = []
                    hashtitle[auxTitle[j]].append([[pagina.id], [1] ])
    
    for i in hashtitle:
        print(i, hashtitle[i])
        print('\n')
        


    temNoHash = False
    for i in range(len(paginas)):
        pagina = paginas[i]
        #separo cada paralavra
        auxText = pagina.text.split(' ')
        
        #percorro cada palavra
        for j in range(len(auxText)):
            temNoHash = False
            auxText[j] = auxText[j].replace('.', '').replace(',', '')
           # print(auxText[j])
            #se a palavra tem mais de 4 letras
            if(len(auxText[j])>4):
                
                for k in range(len(hashs)):
                    #verifica se a palavra que achei ja existe no hash
                    if auxText[j] == hashs[k].word:
                        if hashs[k].idPages[len(hashs[k].idPages)-1] != pagina.id:
                            hashs[k].idPages.append(pagina.id)
                        temNoHash = True   
                                           
                if temNoHash == False:
                    hashAux = Hash()
                    hashAux.word = auxText[j]
                    hashAux.idPages.append(pagina.id)
                    hashs.append(hashAux)
                    #print(hashAux.word+ '  '+ str(hashAux.idPages))
'''
    
def populaHash(palavra, idPagina, hashtexto):
    palavra = palavra.replace('[^0-9a-zA-Z_]', '').replace('=', '')
    #se a palavra tem mais de 4 letras
    if(len(palavra)>4): 
        #se a palavra existe no hash eu adiciono a pagina ou 
        # conto mais ao contador se ja estiver sido encontrada na mesma pagina
        if palavra in hashtexto:   
            
            if hashtexto[palavra][len(hashtexto[palavra)-1][0] == idPagina:
                #hashtexto[auxText[j]].append(pagina.id)
                aux = [[idPagina],[1]]
                hashtexto[palavra].append(aux)
                
            else:
                print('\033[32m'+str(hashtexto[palavra][len(hashtexto[palavra])-1][0])+'\033[0;0m')
                tabela = int(hashtexto[palavra][len(hashtexto[palavra])-1][1])
                tabela += 1
                hashtexto[palavra][len(hashtexto[palavra])-1][1] = tabela
        else:
            hashtexto[palavra] = []
            aux = [[idPagina],[1]]
            hashtexto[palavra].append(aux)
    return hashtexto

main()