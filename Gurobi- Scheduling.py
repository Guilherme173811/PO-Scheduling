# -*- coding: utf-8 -*-

Modalidades = {	'Modalidade 1':'Pebolim',
                'Modalidade 2':'Queimada',
               	'Modalidade 3':'Sinuca',
               	'Modalidade 4':'Maratoma',
               	'Modalidade 5':'Beer Pong',
               	'Modalidade 6':'Cabo de guerra',
               	'Modalidade 7':'Truco',
               	'Modalidade 8':'Flip Cup',
                'Modalidade 9':'Jogo da velha'}

P={'Modalidade 1':	20,
   'Modalidade 2':	25,
   'Modalidade 3':	15,
   'Modalidade 4':  10,
   'Modalidade 5':	20,
   'Modalidade 6':	10,
   'Modalidade 7':	15,
   'Modalidade 8':	15,
   'Modalidade 9':	10}

Q={'Modalidade 1':	2,
   'Modalidade 2':	2,
   'Modalidade 3':	2,
   'Modalidade 4':  2,
   'Modalidade 5':	2,
   'Modalidade 6':	2,
   'Modalidade 7':	2,
   'Modalidade 8':	2,
   'Modalidade 9':	2}

RepsM={
'RM1':'Cerca', 
'RM2':'Tumba',
'RM3':'Vamo ET',
'RM4':'Tsu',
'RM5':'13',
'RM6':'Reprodução',
'RM7':'Tcheca',
'RM8':'Quintal',
'RM9':'Peregrinos',
'RM10':'Sipá',
'RM11':'Rocinha',
'RM12':'Trip',
'RM13':'Rota',
'RM14':'Arrocha',
'RM15':'Barrigas',
'RM16':'Ross',
'RM17':'Vaticano',
'RM18':'Thug',
'RM19':'Bixo Pixa',
'RM20':'Bongo',
'RM21':'Gringa',
'RM22':'Repiroca'}

RepsF={
'RF1':'Aras',
'RF2':'Matilha',
'RF3':'Santa Casa',
'RF4':'Breja Flor',
'RF5':'Vegas',
'RF6':'Toroço',
'RF7':'Las Chicas',
'RF8':'D4',
'RF9':'Vai da Nada',
'RF10':'Amazona',
'RF11':'Shot',
'RF12':'After',
'RF13':'Be Happy',
'RF14':'Saia Justa'}

#_______________________________________________________________________________________


Modalidades = {	'Modalidade 1':'Pebolim',
                'Modalidade 2':'Queimada',
               	'Modalidade 3':'Sinuca',
               	'Modalidade 4':'Maratoma',
               	'Modalidade 5':'Beer Pong',
               	'Modalidade 6':'Cabo de guerra',
               	'Modalidade 7':'Truco',
               	'Modalidade 8':'Flip Cup',
                'Modalidade 9':'Jogo da velha'}

P={'Modalidade 1':	20,
   'Modalidade 2':	25,
   'Modalidade 3':	15,
   'Modalidade 4':  10,
   'Modalidade 5':	20,
   'Modalidade 6':	10,
   'Modalidade 7':	15,
   'Modalidade 8':	15,
   'Modalidade 9':	10}

Q={'Modalidade 1':	2,
   'Modalidade 2':	2,
   'Modalidade 3':	2,
   'Modalidade 4':  2,
   'Modalidade 5':	2,
   'Modalidade 6':	2,
   'Modalidade 7':	2,
   'Modalidade 8':	2,
   'Modalidade 9':	2}

RepsM={
'RM1':'Cerca', 
'RM2':'Tumba',
'RM3':'Vamo ET',
'RM4':'Tsu'}

#_______________________________________________________________________________________

Reps=RepsM
from gurobipy import *

m = Model ('Aruliadas')

#Limite do set de tempo
l=sum(P.values())*3

#Variáveis
X = m.addVars(Reps.keys(), Modalidades.keys(), range(l), vtype=GRB.BINARY, name='X')
O = m.addVars(Reps.keys(), Modalidades.keys(), range(l), vtype=GRB.BINARY, name='O')
W = m.addVars(Modalidades.keys(), range(l), vtype=GRB.BINARY, name='W')
Cmax = m.addVar(vtype=GRB.INTEGER, name='Cmax')
m.update()

#Restrições

##Número máximo de modalidades por rep em um instante de tempo
m.addConstrs((quicksum(O.select(i,'*',t)) <= 3 for i in Reps.keys() for t in range(l)),name='MaxMod')


##Todas as reps devem jogar todas as modalidades um única vez
m.addConstrs((quicksum(O.select(i,j,'*')) == P[j] for i in Reps.keys() for j in Modalidades.keys()),name='TodasMods')


##Garante que cada modalidade tenha Qj reps disputando a mesma partida ao mesmo tempo        
m.addConstrs((quicksum(O.select('*',j,t)) == Q[j]*(1-W[j,t]) for j in Modalidades.keys() for t in range(l)),name='Qj')
m.addConstrs((quicksum(O.select('*',j,t)) >= (W[j,t]-1) for j in Modalidades.keys() for t in range(l)),name='Qj-zero')

#Período ocupado: Atribui o valor 1 para as variáveis Oijt
for i in Reps.keys():        
    for j in Modalidades.keys():
        for t in range(l):
            S=t+P[j]-1
            if S>l:
                S=l
            m.addConstr((quicksum(O.select(i,j,range(t,S+1))) >= P[j]*X[i,j,t]),name='O')

#makespan
m.addConstrs((Cmax>=X[i,j,t]*(t+P[j]) for i in Reps.keys() for j in Modalidades.keys() for t in range(l)), name='makespan')

#Forçar x a começar
m.addConstrs((quicksum(X[i,j,t] for t in range(l))==1 for i in Reps.keys() for j in Modalidades.keys()), name='Forca')

m.update()

m.setObjective(Cmax, GRB.MINIMIZE)

#Comando que otimiza o problema
m.optimize()

#Imprimi na tela as variáveis, seus valores e o resultado da função objetivo
for v in X.values():
    if v.x != 0:
         print('%s %g' % (v.varName, v.x))
print('Obj: %g' % m.objVal)




















