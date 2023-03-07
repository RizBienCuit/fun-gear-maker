import math
import os
import re

yoyo=input("want info?(y/n):")
if yoyo=="y":
    print("this program will make the fitting gear with the one you put in with any ratio.\n Your svg file has to be composed with only one svg path without transform and without curves.\n the svg path has to be star shaped about the 0,0 point. \n !!! be careful: in inkscape, the 0,0 point is the up left corner of the page!!!")
nFichierIn=input("original gear path: ")
#nFichierIn="/home/ruben/Documents/svgscritp/exemple_6_0.svg"
fichierIn = open(nFichierIn, "r")
textIn=fichierIn.read()
nFichierOut=input("new gear path: ") 
#nFichierOut="/home/ruben/Documents/svgscritp/exemple_6_1.svg"
fichierOut = open(nFichierOut, "w")
textOut=textIn

#lineList=list([[-10,30],[10,6],[10,-10],[-9,-10]])#liste des segments du polygon tel que seg 1 = [0],[1] seg 2 [1],[2] dernier seg [der],[0]
lineList=list([[0,0]])#nombre de segments du poly
NPas=int(input("precision(greater for more precision):"))
ratio=float(input("ratio\n(number of rotations that the other gear makes when the original makes one)\n!!!the step number must be divisible by the ratio\n more than one is not counciled if youre original gear is not regular: "))
finalDistanceList=list(NPas*[0])
finalDistanceListB=list(NPas*[0])
compta=0#pour les atape 2et3 determine l'angle du dernier rayon calculé
rayonVec=0#pour les atape la pente du rayon actuel(compta°)
workSegment=0#pour les atape segment qui intersecte compta-1
sens=0#le sens de la contuinité des segment par rapport au sens des degrés
def deterInter(indexSegment,indexDeusopoint,rayon):
    #indexS:l'index du premier point du segment dans linelist, indexD:idem,mais 2em point,angle du rayon
    cote=1
    rayonVertical=0
    penteRayon=0
    if rayon==90:
        rayonVertical=1
    elif rayon==270:
        rayonVertical=-1
    else:
        if rayon>90 and rayon<270:
            cote=-1
        if rayon!=0:
            penteRayon=math.sin(math.radians(rayon))/math.cos(math.radians(rayon))
    #print(rayonVertical,cote,penteRayon)
    ret=list([0,-1])#ce qu'il ya a a retourner. le premier la distance, le deuxieme l'index a mettre est -1 si il n'y a pas d'inter
    plusgrand=0
    pluspetit=0
    if rayonVertical!=0:#si le rayon est verticos, probleme avc pente ducoup on vérifie juste si le segment contient le point d'ordonnée 0
        #print("rayonver")
        if paraSeg[indexSegment]==False:
            pluspetit=lineList[indexDeusopoint][0] #l'extremite la plus petite en x du segment pour savoir si le point d'inter des 2 droites est bien ds le segment
            plusgrand=lineList[indexSegment][0]
            if lineList[indexSegment][0]<lineList[indexDeusopoint][0]: #determine l'extremite la plus grande et la plus petite
                plusgrand=lineList[indexDeusopoint][0]
                pluspetit=lineList[indexSegment][0]
            if 0<plusgrand and 0>pluspetit:
                if equaSeg[indexSegment][1]*rayonVertical>=0:#verif dans la demi droite(rayon)
                    ret[1]=indexSegment #finir avec le numéro du segment croisant le rayon 0°
                    ret[0]=equaSeg[indexSegment][1]*rayonVertical#ordonnée a l'origine car c'est le point de hauteur a 0 donc la distance a l'origne du point d'inter
    else:
        if paraSeg[indexSegment]==False: #si la droite n'est pas "paraseg" liendes2bou
            #print("normal")
            if penteRayon!=equaSeg[indexSegment][0]:
                pluspetit=lineList[indexDeusopoint][0] #l'extremite la plus petite en x du segment pour savoir si le point d'inter des 2 droites est bien ds le segment
                plusgrand=lineList[indexSegment][0] #la plus grande
                if lineList[indexSegment][0]<lineList[indexDeusopoint][0]: #determine l'extremite la plus grande et la plus petite
                    plusgrand=lineList[indexDeusopoint][0]
                    pluspetit=lineList[indexSegment][0]
                if (-equaSeg[indexSegment][1])/(equaSeg[indexSegment][0]-penteRayon)<plusgrand and (-equaSeg[indexSegment][1])/(equaSeg[indexSegment][0]-penteRayon)>pluspetit: # si le point d'inter est bien dans le segment
                    #print("nd")
                    ret[1]=indexSegment #finir avec le numéro du segment croisant le rayon 0°
                    ret[0]=math.sqrt((-equaSeg[indexSegment][1])/(equaSeg[indexSegment][0]-penteRayon)*(-equaSeg[indexSegment][1])/(equaSeg[indexSegment][0]-penteRayon)+(-equaSeg[indexSegment][1])/(equaSeg[indexSegment][0]-penteRayon)*penteRayon*(-equaSeg[indexSegment][1])/(equaSeg[indexSegment][0]-penteRayon)*penteRayon)
                    if -equaSeg[indexSegment][1]/(equaSeg[indexSegment][0]-penteRayon)*cote<=0:
                        ret[1]=-1
        else :
            #print("vertos")
            pluspetit=lineList[indexDeusopoint][1] #on prends le y([1]) car un paraseg a le meme x sur toute sa droite
            plusgrand=lineList[indexSegment][1]
            if lineList[indexSegment][1]<lineList[indexDeusopoint][1]: #determine l'extremite la plus grande et la plus petite
                plusgrand=lineList[indexDeusopoint][1]
                pluspetit=lineList[indexSegment][1]
            if plusgrand>equaSeg[indexSegment][0]*penteRayon and pluspetit<equaSeg[indexSegment][0]*penteRayon: #si le segment contient le point d'inter
                ret[1]=indexSegment
                ret[0]=math.sqrt(equaSeg[indexSegment][0]*equaSeg[indexSegment][0]+equaSeg[indexSegment][0]*penteRayon*equaSeg[indexSegment][0]*penteRayon)
                if equaSeg[indexSegment][0]*cote<=0:
                    ret[1]=-1

    return ret

def NotCara(chaine,cara):
    ret=-1
    comptI=0
    while ret==-1:
        if chaine[comptI]!=cara:
            ret=comptI
        comptI+=1
        if comptI==len(chaine):
            ret=-2
    return ret
indexString=textIn[textIn.index("<path"):].index(" d=")+textIn.index("<path")+4
print(NotCara(textIn[indexString:]," "))
indexString+=NotCara(textIn[indexString:]," ")
lettre=textIn[indexString]
continuto=True
fin=[0,0]
if lettre=="m" or lettre=="M" or lettre=="l" or lettre=="L":
    indexString+=1
    indexString+=NotCara(textIn[indexString:]," ")
    a=indexString
    indexString+=textIn[indexString:].index(",")
    indexString-=NotCara(textIn[indexString-1::1]," ")
    fin[0]=float(textIn[a:indexString])
    indexString+=textIn[indexString:].index(",")+1
    indexString+=NotCara(textIn[indexString:]," ")
    a=indexString
    indexString+=textIn[indexString:].index(" ")
    fin[1]=float(textIn[a:indexString])
    lineList[0]=fin[:]
    indexString+=NotCara(textIn[indexString:]," ")
    if not (textIn[indexString].isdigit() or textIn[indexString]=="-"):
        lettre=textIn[indexString]
        if textIn[indexString]=="z" or textIn[indexString]=="Z":
            continuto=False
        indexString+=1
        indexString+=NotCara(textIn[indexString:]," ")
    print(fin)
elif lettre=="v" or lettre=="V" or lettre=="h" or lettre=="H":
    a=indexString
    indexString+=textIn[indexString:].index(" ")
    if lettre=="h" or lettre=="H":
        fin[0]=float(textIn[a:indexString])
    else:
        fin[1]=float(textIn[a:indexString])
    lineList+=[fin[:]]
    if lettre=="v" or lettre=="h":
        lineList[-1][0]+=lineList[-2][0]
        lineList[-1][1]+=lineList[-2][1]
    indexString+=NotCara(textIn[indexString:]," ")
    if not (textIn[indexString].isdigit() or textIn[indexString]=="-"):
        lettre=textIn[indexString]
        if textIn[indexString]=="z" or textIn[indexString]=="Z":
            continuto=False
        indexString+=1
        indexString+=NotCara(textIn[indexString:]," ")
print(textIn[indexString])
print(lineList)
print(lettre)

while continuto:
    fin=[0,0]
    #print("A")
    if lettre=="m" or lettre=="M" or lettre=="l" or lettre=="L":
        print(lineList[-1])
        print(lettre)
        a=indexString
        indexString+=textIn[indexString:].index(",")
        #print(textIn[a:indexString])
        indexString-=NotCara(textIn[indexString-1::1]," ")
        #print(textIn[a:indexString])
        fin[0]=float(textIn[a:indexString])
        indexString+=textIn[indexString:].index(",")+1
        indexString+=NotCara(textIn[indexString:]," ")
        a=indexString
        indexString+=textIn[indexString:].index(" ")
        print(textIn[a:indexString])
        fin[1]=float(textIn[a:indexString])
        lineList+=[fin[:]]
        if lettre=="m" or lettre=="l":
            lineList[-1][0]+=lineList[-2][0]
            lineList[-1][1]+=lineList[-2][1]
        indexString+=NotCara(textIn[indexString:]," ")
        if not (textIn[indexString].isdigit() or textIn[indexString]=="-"):
            lettre=textIn[indexString]
            if textIn[indexString]=="z" or textIn[indexString]=="Z":
                break
            indexString+=1
            indexString+=NotCara(textIn[indexString:]," ")
    elif lettre=="v" or lettre=="V" or lettre=="h" or lettre=="H":
        a=indexString
        indexString+=textIn[indexString:].index(" ")
        if lettre=="h" or lettre=="H":
            fin[0]=float(textIn[a:indexString])
            fin[1]=lineList[-1][1]
        else:
            fin[1]=float(textIn[a:indexString])
            fin[0]=lineList[-1][0]
        lineList+=[fin[:]]
        if lettre=="v":
            lineList[-1][1]+=lineList[-2][1]
        if lettre=="h":
            lineList[-1][0]+=lineList[-2][0]
        indexString+=NotCara(textIn[indexString:]," ")
        if not (textIn[indexString].isdigit() or textIn[indexString]=="-"):
            lettre=textIn[indexString]
            if textIn[indexString]=="z" or textIn[indexString]=="Z":
                break
            indexString+=1
            indexString+=NotCara(textIn[indexString:]," ")
print(lineList)

#lineList=list([[-10,30],[10,6],[10,-10],[-9,-10]])
nSeg=len(lineList)
equaSeg=nSeg*[[0,0]]#equation de tous les segments/droites du polygon. [x][0]pente et [x][1]OAO(ordonné a l'origine)
paraSeg=nSeg*[False]#si les segments du polygone sont parallèles a l'axe d'ordonnée. si oui equaSeg correspondant[x][0]=absice de la droite

compteur=0
while compteur<nSeg-1:
    pente=0
    if lineList[compteur][0]==lineList[compteur+1][0]:
        paraSeg[compteur]=True
        equaSeg[compteur]=[lineList[compteur][0],0]
    else :
        if lineList[compteur+1][1]!=lineList[compteur][1]:#si le segment n'est pas horizontal
            pente=(lineList[compteur+1][1]-lineList[compteur][1])/(lineList[compteur+1][0]-lineList[compteur][0])
        equaSeg[compteur]=[pente,lineList[compteur][1]-(lineList[compteur][0]*pente)]
    compteur+=1
pente=0
if lineList[nSeg-1][0]==lineList[0][0]:#liendes2bou(operation pour le dernier segment qui va de [nseg-1] a [0] car ne peut etre fait ds boucle)
    paraSeg[nSeg-1]=True
    equaSeg[nSeg-1]=[lineList[nSeg-1][0],0]
else :
    if lineList[0][1]!=lineList[nSeg-1][1]:#si le segment n'est pas horizontal
        pente=(lineList[0][1]-lineList[nSeg-1][1])/(lineList[0][0]-lineList[nSeg-1][0])
    equaSeg[nSeg-1]=[pente,lineList[nSeg-1][1]-(lineList[nSeg-1][0]*pente)]
print(equaSeg)
print(paraSeg)
#quit()
stepLenght=360/NPas#la longueur(degrés) de chaques pasbol
leSegmentCoupant=-1
compta=0
while leSegmentCoupant==-1:#1ere atape 
    deto=deterInter(compta,compta+1,0)
    if deto[1]!=-1:
        leSegmentCoupant=deto[1]
        finalDistanceList[0]=deto[0]
    """if compta==nSeg-2 and leSegmentCoupant==-1:
        leSegmentCoupant=0
        print("error")
        quit()"""
    if compta==nSeg-2 and leSegmentCoupant==-1:
        deto=deterInter(compta+1,0,0)
        if deto[1]!=-1:
           leSegmentCoupant=deto[1]
           finalDistanceList[0]=deto[0]
        else:
            leSegmentCoupant=0
            print("error")
            quit()
    compta+=1

"""if paraSeg[compta]==False: #si la droite n'est pas "paraseg" liendes2bou
    pluspetit=lineList[0][0] #l'extremite la plus petite en x du segment pour savoir si le point d'inter des 2 droites est bien ds le segment
    plusgrand=lineList[compta][0] #la plus grande
    if lineList[compta][0]<lineList[0][0]: #determine l'extremite la plus grande et la plus petite
        plusgrand=lineList[0][0]
        pluspetit=lineList[compta][0]
    if equaSeg[compta][0]!=0: #si la droite n'est pas parrallele a laxe des abscisses
        if (equaSeg[compta][1])/(equaSeg[compta][0])<plusgrand and (equaSeg[compta][1])/(equaSeg[compta][0])>pluspetit: # si le point d'inter est bien dans le segment
            if ((equaSeg[compta][1])/(equaSeg[compta][0])>0): #si l'abscisse du point d'inter est bien positif donc est bien sur le rayon 0°
                leSegmentCoupant=compta #finir avec le numéro du segment croisant le rayon 0°
                finalDistanceList[0]=equaSeg[leSegmentCoupant][1]/equaSeg[leSegmentCoupant][0]
    elif equaSeg[compta][1]==0: #si la droite est la meme que le rayon 0°
        if pluspetit>0:
            leSegmentCoupant=compta
            finalDistanceList[0]=equaSeg[leSegmentCoupant][1]/equaSeg[leSegmentCoupant][0]
        elif plusgrand>0:
            leSegmentCoupant=compta
            finalDistanceList[0]=equaSeg[leSegmentCoupant][1]/equaSeg[leSegmentCoupant][0]
elif equaSeg[compta][0]>0: #sila droite verticale(ou paraseg) a son abscisse plus grande que 0
    pluspetit=lineList[0][1] #on prends le y([1]) car un paraseg a le meme x sur toute sa droite
    plusgrand=lineList[compta][1]
    if lineList[compta][1]<lineList[0][1]: #determine l'extremite la plus grande et la plus petite
        plusgrand=lineList[0][1]
        pluspetit=lineList[compta][1]
    if plusgrand>0 and pluspetit<0: #si le segment contient le point d'inter
        leSegmentCoupant=compta
        finalDistanceList[0]=equaSeg[leSegmentCoupant][0]"""
deto=deterInter(nSeg-1,0,0)
if deto[1]!=-1:
    leSegmentCoupant=deto[1]
    finalDistanceList[0]=deto[0]
print(leSegmentCoupant)

compta=0
sensSegment=leSegmentCoupant+1
bol=True
bolade=True
comptade=compta#G DciD de ne pas faire le sens avec les segment mais plutot avec compta. comptade est le compta du sens -1
while bol or bolade:#atape 2
    compta+=1
    comptade-=1
    print(compta)
    if deterInter(leSegmentCoupant%nSeg,(leSegmentCoupant+1)%nSeg,(compta*stepLenght)%360)[1]==-1:
        bol=False
    else:
        finalDistanceList[compta%NPas]=deterInter(leSegmentCoupant%nSeg,(leSegmentCoupant+1)%nSeg,(compta*stepLenght)%360)[0]       
    if deterInter(leSegmentCoupant%nSeg,(leSegmentCoupant+1)%nSeg,(comptade*stepLenght)%360)[1]==-1:
        bolade=False
    else:
        finalDistanceList[compta%NPas]=deterInter(leSegmentCoupant%nSeg,(leSegmentCoupant+1)%nSeg,(compta*stepLenght)%360)[0]       

    #verif inter avec leSegmentCoupant. si ouui oncontinue. sinon on arrete
#compta-=1#compta a été augmenté de trop dans le while précédant car on s'arrete si pas de coupe, donc celui qui n'est pas coupé est incrémenté dans compta, mé ne devraitpas
print(sensSegment)
print(compta,comptade)

#compta+=1
compteur=0
while sens==0 and compteur<nSeg+1:
    #compta+=1
    print(compta%NPas,sensSegment%nSeg)
    if deterInter(sensSegment%nSeg,(sensSegment+1)%nSeg,(compta*stepLenght)%360)[1]!=-1:
        print("Yaah")
        sens=1
        finalDistanceList[compta%NPas]=deterInter(sensSegment%nSeg,(sensSegment+1)%nSeg,(compta*stepLenght)%360)[0]
    if deterInter(sensSegment%nSeg,(sensSegment+1)%nSeg,(comptade*stepLenght)%360)[1]!=-1:
        print("Yooh")
        sens=-1
        finalDistanceList[compta%NPas]=deterInter(sensSegment%nSeg,(sensSegment+1)%nSeg,(comptade*stepLenght)%360)[0]
    #verif inter avc senssegment 1et2. si ooui compta++ et booucle est bouclee. si non si worksegment==0,
    sensSegment+=1
    compteur+=1
#compta+=1
workSegment=sensSegment
if sens==-1:
    compta=comptade
compteur=0
while compteur<NPas:
    compta+=sens
    compteur+=1
    print(workSegment%nSeg,"bol")
    print(compta%NPas)
    if deterInter(workSegment%nSeg,(workSegment+1)%nSeg,(compta*stepLenght)%360)[1]!=-1:
        print("okay")
        finalDistanceList[compta%NPas]=deterInter(workSegment%nSeg,(workSegment+1)%nSeg,(compta*stepLenght)%360)[0]
    else:
        print("vouf")
        compta-=sens
        workSegment+=1
        compteur-=1

compta=0
theta=math.radians(stepLenght)
dist=math.sqrt(finalDistanceList[1]*finalDistanceList[1]+finalDistanceList[0]*finalDistanceList[0]-2*finalDistanceList[0]*finalDistanceList[1]*math.cos(theta))

b=30/dist
DMoyenne=0
teethState=input("add teeth? (y/n)")
if teethState=="y":
   nFichierInTeeth=input("path of the original gear with theeth added:")
   print(stepLenght*NPas)
   while compta<NPas:
      DMoyenne+=finalDistanceList[compta]
      compta+=1
   DMoyenne=DMoyenne/NPas
   print(DMoyenne)
   compta=0
   numTeeth=int(input("number of teeth:"))
   while compta<NPas:
      #dist=math.sqrt(finalDistanceList[(compta+1)%NPas]*finalDistanceList[(compta+1)%NPas]+finalDistanceList[compta]*finalDistanceList[compta]-2*finalDistanceList[compta]*finalDistanceList[(compta+1)%NPas]*math.cos(theta))
      #finalDistanceList[compta]=finalDistanceList[compta]+5*math.sin(math.radians(compta*stepLenght)*dist*b)
      sensDent=1
      if math.sin(math.radians(compta*stepLenght*numTeeth))<0:
         sensDent=-1
      finalDistanceList[compta]=finalDistanceList[compta]+DMoyenne/15*20/numTeeth*sensDent     
      compta+=1
#finalussss
#first etape: trouver le plus grand rayon puis D =2* le grand rayon pour commencer
#finalDistanceList=list(NPas*[50])
compta=0
D=0
while compta<NPas:
    if finalDistanceList[compta]>D:
        D=finalDistanceList[compta]
    compta+=1
DAround=[D,-1]
D=D*2
TourPossible=0

while 360*ratio-(TourPossible)>stepLenght or 360*ratio-(TourPossible)<(-stepLenght):
    TourPossible=0
    compta=0
    while compta<NPas:
        TourPossible+=(finalDistanceList[compta]/(D-finalDistanceList[compta]))*stepLenght
        print(TourPossible)
        compta+=1
    if TourPossible<360*ratio  and (360*ratio-(TourPossible)>stepLenght or 360*ratio-(TourPossible)<(-stepLenght)):
        print("pluspti")
        DAround[1]=D
        if DAround[0]==-1:
            D=D/2
        else:
            D=(D-DAround[0])/2+DAround[0]
    elif TourPossible>360*ratio and (360*ratio-(TourPossible)>stepLenght or 360*ratio-(TourPossible)<(-stepLenght)):
        print("plusgrand")
        DAround[0]=D
        if DAround[1]==-1:
            D=D*2
        else:
            D=(DAround[1]-D)/2+D
    print(TourPossible,DAround,D)
print(TourPossible,DAround)

indexString=textOut.index("path")
indexString-=textOut[indexString::-1].index("<")
indexRetenu=indexString
indexString+=textOut[indexString+1:].index(">")+2
baseShape=textOut[indexRetenu:indexString]
#print(baseShape)
compta=0
textEntre=""
rototo=0
"""while compta<NPas:
    finalDistanceListB[compta]=D-finalDistanceList[compta]
    rototo+=(finalDistanceList[compta]/(D-finalDistanceList[compta]))*stepLenght
    textEntre+="<g transform=\"rotate("+str(rototo)+") translate("+str(D)+") rotate("+str(compta*stepLenght)+")\">"
    textEntre+=baseShape
    textEntre+=" </g>"
    compta+=1
print(textEntre)
textOut=textOut[:indexRetenu]+textOut[indexString:]
textOut=textOut[:indexRetenu]+textEntre+textOut[indexRetenu:]"""

compta=0
while compta<NPas:
    #if compta%(1/ratio)==0:
    print(compta*ratio)
    finalDistanceListB[compta]=D-finalDistanceList[int((compta/ratio)%NPas)]
    """elif ratio>1:
        finalDistanceListB[int(compta*ratio)]=D-finalDistanceList[compta%NPas]"""
    compta+=1

if teethState=="y":
   textOutA=textIn
   indexString=textOutA.index("path")
   indexString+=textOutA[indexString:].index(" d=")
   indexString+=textOutA[indexString:].index("\"")+1
   indexRetenu=indexString
   indexString+=textOutA[indexString:].index("\"")
   textOutA=textOutA[:indexRetenu]+textOutA[indexString:]
#print(textOut)
   textEntre=" M "
   compta=0
   rototo=0
   while compta<NPas:
       textEntre+=str(float(finalDistanceList[compta]*math.cos(math.radians(compta*stepLenght)))) + "," + str(float(finalDistanceList[compta]*math.sin(math.radians(compta*stepLenght)))) + " "
       compta+=1
   baseShape="<g transform=\" translate("+str(D)+")\">"+baseShape+" </g>"
   textOutA=textOutA[:indexRetenu]+textEntre+"z"+textOutA[indexRetenu:]
   """indexString+=textOut[indexString:].index("/>")+3
   textOut=textOut[:indexString]+baseShape+textOut[indexString:]"""
#print(textOut)
   fichierInTeeth = open(nFichierInTeeth, "w")
   fichierInTeeth.write(textOutA)
   fichierInTeeth.close()

textOutB=textIn
indexString=textOutB.index("path")
indexString+=textOutB[indexString:].index(" d=")
indexString+=textOutB[indexString:].index("\"")+1
indexRetenu=indexString
indexString+=textOutB[indexString:].index("\"")
textOutB=textOutB[:indexRetenu]+textOutB[indexString:]
#print(textOut)
textEntre=" M "
compta=0
rototo=0
while compta<NPas:
    rototo+=(finalDistanceList[int((compta/ratio)%NPas)]/(D-finalDistanceList[int((compta/ratio)%NPas)]))*stepLenght/ratio
    textEntre+=str(float(0-(finalDistanceListB[compta]*math.cos(math.radians(rototo))))) + "," + str(float(finalDistanceListB[compta]*math.sin(math.radians(rototo)))) + " "
    compta+=1
baseShape="<g transform=\" translate("+str(D)+")\">"+baseShape+" </g>"
textOutB=textOutB[:indexRetenu]+textEntre+"z"+textOutB[indexRetenu:]
"""indexString+=textOut[indexString:].index("/>")+3
textOut=textOut[:indexString]+baseShape+textOut[indexString:]"""
#print(textOut)
fichierOut.write(textOutB)
#print(deterInter(0,1,2*stepLenght))
#A=premiere droite. B = 2eme droite point d'inter=X,X*a+b quand X*aA+bA=X*aB+bB
#y=x*a+b
#point d'inter=(bB-bA)/(aB-aA) b=yA-(a*xA)
#premiere atape: trouver le point dinter de [0,0] avec le polygon en verif chaques segments=prems
#2eme atape: verifier si inter entr [360/NPas*x degrés] et prems segment. sinon,verif prems+1 et prems-1. si premier cas, recommencer jusqua 2em cas. sens
#3eme atape: verifier si inter entr [360/NPas*x degrés] et x-1 segment+y*sens

#finalum: df2=(r1(f1)/D-r1(f1))*df1 df2 est l'angle dont l'engrenage a construire tourne  r1(f1) le rayon de l'engr D ce qui change, la distance entre les deux centres d'engrenages et df1 le pas d'angle
print(sens)
print(finalDistanceList)
print(leSegmentCoupant)
print("The Two gears have to be spaced by",D,"(move the second gear(not the orignal) by",D)
fichierIn.close()
fichierOut.close()
quit()
