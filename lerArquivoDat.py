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
            hashtexto = populaHash(auxText[j], pagina.id, hashtexto)
            #se a palavra tem mais de 4 letras
            # if(len(auxText[j])>4): 
            #     #se a palavra existe no hash eu adiciono a pagina ou 
            #     # conto mais ao contador se ja estiver sido encontrada na mesma pagina
            #     if auxText[j] in hashtexto:   
                    
            #         if hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][0] == pagina.id:
            #             #hashtexto[auxText[j]].append(pagina.id)
            #             aux = [[pagina.id],[1]]
            #             hashtexto[auxText[j]].append(aux)
                        
            #         else:
            #             print('\033[32m'+str(hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][0])+'\033[0;0m')
            #             tabela = int(hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][1])
            #             tabela += 1
            #             hashtexto[auxText[j]][len(hashtexto[auxText[j]])-1][1] = tabela
            #     else:
            #         hashtexto[auxText[j]] = []
            #         aux = [[pagina.id],[1]]
            #         hashtexto[auxText[j]].append(aux)
   
    
    for i in hashtexto:
        print(i, hashtexto[i])
        print('\n')
    
        #percorro cada palavra do titulo
        for j in range(len(auxTitle)):
            auxTitle[j] = auxTitle[j].replace('[^0-9a-zA-Z_]', '').replace('=', '')
            hashtitle = populaHash(auxTitle[j], pagina.id, hashtitle)
            
    # for i in hashtitle:
    #     print(i, hashtitle[i])
    #     print('\n')
    calculaRank('september', hashtexto, True)
    calculaRank('september', hashtitle, False)

#textOrTitle -> True para text; False para Title
def calculaRank(palavra, hashTexto, textOrTitle):
    if(not textOrTitle):  
        print('\033[32m'+'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'+'\033[0;0m')
        elemento = hashTexto["10g-epon"]
    else:
        elemento = hashTexto[palavra]
    pageRank = []

    for i in elemento:
        idPage = int(i[0])
        qtd = int(i[1])
        pontos = 0
        for j in range(1,qtd+1):
            if(textOrTitle):
                pontos += j
            else:
                pontos +=10
        aux =[]
        aux.append(idPage)
        aux.append(pontos)

        pageRank.append(aux)
    if(not textOrTitle):  
        print(pageRank)
    

def populaHash(palavra, idPagina, hashtexto):
    palavra = palavra.replace('[^0-9a-zA-Z_]', '').replace('=', '')
    aux = []
    #se a palavra tem mais de 4 letras
    if(len(palavra)>4): 
        #se a palavra existe no hash eu adiciono a pagina ou 
        # conto mais ao contador se ja estiver sido encontrada na mesma pagina
        if palavra in hashtexto:   
            ultimoElemento = len(hashtexto[palavra])-1
            #hashtexto[palavra][ultimoElemento][0] é o idPagina
            #hashtexto[palavra][ultimoElemento][1] é q quantidade de vezes que a palavra aparece na pg
            if hashtexto[palavra][ultimoElemento][0] != idPagina:
                #hashtexto[auxText[j]].append(pagina.id)
                aux.append(idPagina)
                aux.append(1)
                hashtexto[palavra].append(aux)
                
            else:
                # print('\033[32m'+str(hashtexto[palavra][len(hashtexto[palavra])-1][0])+'\033[0;0m')

                tabela = int(hashtexto[palavra][ultimoElemento][1])
                tabela += 1
                hashtexto[palavra][ultimoElemento][1] = tabela
        else:
            hashtexto[palavra] = []
            aux.append(idPagina)
            aux.append(1)
            hashtexto[palavra].append(aux)
            
    return hashtexto

main()