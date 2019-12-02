import xml.dom.minidom as XML
import re

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
    vetorPageRank = []
    Rankfinal = []
    file = open('testCollection.dat', 'r', encoding='UTF-8')
    
    #####################################################
    frasePesquisa = "Computer Science robot"

    #####################################################

    #Lê e separa as paginas, title de cada pagina e text tambem
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
        pagina.title = re.sub(r'[^A-Za-z0-9 ]+', ' ', pagina.title)

        pagina.text = text[1].replace('</text>', '').replace('</page>', '')
        pagina.text = pagina.text.lower()
        pagina.text = re.sub(r'[^A-Za-z0-9 ]+', ' ', pagina.text)
        paginas.append(pagina)
    
    #percorro as paginas mapeando as ocorrencias das palavras
    for i in range(len(paginas)):
        pagina = paginas[i]
        #separo cada palavra no texto
        auxText = pagina.text.split(' ')
        #separo cada palavra no titulo
        auxTitle = pagina.title.split(' ')

        #percorro cada palavra do texto da pagina 
        for j in range(len(auxText)):
            # auxText[j] = re.sub(r'[^A-Za-z0-9 ]+', ' ', auxText[j]) #.replace('[^0-9a-zA-Z_]', '').replace('=', '')
            hashtexto = populaHash(auxText[j], pagina.id, hashtexto)
        #percorro cada palavra do titulo
        for j in range(len(auxTitle)):
            #auxTitle[j] =re.sub(r'[^A-Za-z0-9 ]+', ' ', auxTitle[j]) #auxTitle[j].replace('[^0-9a-zA-Z_]', '').replace('=', '')
            hashtitle = populaHash(auxTitle[j], pagina.id, hashtitle)

    vetorPalavrasPesquisa = frasePesquisa.split(' ')
    
    #faz um pageRank de todas as palavras maiores que 4 letras e poe em um vetor de PageRank
    for i in vetorPalavrasPesquisa:
        # print(i)
        
        if len(i)>=4:
            pageRankText = calculaRank(i.lower(), hashtexto, True)
            #print(pageRankText[0])
            pageRankTitle = calculaRank(i.lower(), hashtitle, False)
            #print(pageRankTitle[0])
            AllPageRank = mergePageRankTitleText(pageRankText, pageRankTitle)
            
            AllPageRank  = sorted(AllPageRank,  key=lambda ranks: ranks[1],  reverse=True)
            # print(AllPageRank)
            vetorPageRank.append(AllPageRank)
           
            # print(len(AllPageRank))
        # print(AllPageRank) 
        # print('\033[32m'+'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' +'\033[0;0m')
    
    
    
    if len(vetorPageRank) > 0:
        Rankfinal = vetorPageRank[0]
        #percorre o vetor de pagerank
        for i in range(len(vetorPageRank)):
            if (i+1) < len(vetorPageRank):
                # print(len(vetorPageRank))
                # Rankfinal = []
                Rankfinal = mergePagesRanks(Rankfinal, vetorPageRank[i+1])
                # print("Rank", Rankfinal)
        Rankfinal = sorted(Rankfinal,  key=lambda ranks: ranks[1],  reverse=True)
        cont = 0
        for i in Rankfinal:
            # print("Rank", Rankfinal)
            print('\033[32m', 'Pagina: ', i[0], ' Ponto de Rank: ', i[1],'\033[0;0m')

            # cont+=1
            # if cont == 20:
            #     break
    
def mergePagesRanks(rank1, rank2):
    allPage = []
    vezesPalavra = 0
    # print(rank1)
    for i in rank1:
        aux = []
        elemento =  []
        for j in rank2:
            if j[0] == i[0]:
                elemento = j
                break

        #se tem o mesmo elemento nos dois ranks
        if len(elemento)> 0:  
            aux.append(i[0])
            aux.append(i[1]+ j[1])
            vezesPalavra +=1
            rank2.remove(j)
        #se entrou no if anterior e preencheu o aux
        if(len(aux)>0):
            allPage.append(aux)
            aux = []
        
        #senão ele preenche o aux com os dados do rank1
        else:
            aux.append(i[0])
            aux.append(i[1])
            allPage.append(aux)
            aux = []
           
        
    #se ainda existir um rank em no rank 2
    if len(rank2)>0:
        for i in rank2:
            aux.append(i[0])
            aux.append(i[1])
            allPage.append(aux) 
           
            aux = [] 
    return allPage
        

    

def mergePageRankTitleText(pageRankText, pageRankTitle):
    allPageRank = []
    for i in pageRankText:
        aux =[]
        elemento = []
        #adicionando id
        aux.append(i[0])
        #pego o elemento com mesmo id do outro vetor
        for j in pageRankTitle:
            if j[0] == i[0]:
                elemento = j
                # print(i, j)
                break
        #se o valor existe no vetor do title eu elimino ele 
        if len(elemento)> 0:
            aux.append(i[1]+elemento[1])
            pageRankTitle.remove(elemento)
            # del pageRankTitle[i[0]]
        else:
            aux.append(i[1])    
        #somo o pageRank do title e do text
        #aux.append(i[1]+elemento[1])
        allPageRank.append(aux)
    if len(pageRankTitle)>0:
        #se depois que eu somar todos os pageRank iguais entre title e text ainda sobrar algum, eu simplemente adiciono
        for i in pageRankTitle:
            allPageRank.append(i)

    return allPageRank
    
#textOrTitle -> True para text; False para Title
def calculaRank(palavra, hashTexto, textOrTitle):
    
    elemento = hashTexto.get(palavra, 0)
    
    pageRank = []
    if elemento != 0:
        for i in elemento:
            idPage = int(i[0])
            qtd = int(i[1])
            # if idPage ==16796:
                # print(qtd)
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
        # if(not textOrTitle):  
        #     print(pageRank)
    return pageRank
     


def populaHash(palavra, idPagina, hashtexto):
   # palavra = re.sub(r'[^A-Za-z0-9 ]+', ' ', palavra)  #palavra.replace('[^0-9a-zA-Z_]', ' ').replace('=', '')
    aux = []
    #se a palavra tem mais de 4 letras
    if(len(palavra)>=4): 
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