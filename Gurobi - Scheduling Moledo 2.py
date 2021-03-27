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
'RM22':'Repiroca',
'RF23':'Aras',
'RF24':'Matilha',
'RF25':'Santa Casa',
'RF26':'Breja Flor',
'RF27':'Vegas',
'RF28':'Toroço',
'RF29':'Las Chicas',
'RF30':'D4',
'RF31':'Vai da Nada',
'RF32':'Amazona'}

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
#_________________________________________________________________________________

#Modalidades = {	'Modalidade 1':'Pebolim',
#                'Modalidade 2':'Queimada',
#               	'Modalidade 3':'Sinuca',
#               	'Modalidade 4':'Maratoma',
#               	'Modalidade 5':'Beer Pong',
#               	'Modalidade 6':'Cabo de guerra',
#               	'Modalidade 7':'Truco',
#               	'Modalidade 8':'Flip Cup',
#                'Modalidade 9':'Jogo da velha'}
#
#P={'Modalidade 1':	20,
#   'Modalidade 2':	25,
#   'Modalidade 3':	15,
#   'Modalidade 4':  10,
#   'Modalidade 5':	20,
#   'Modalidade 6':	10,
#   'Modalidade 7':	15,
#   'Modalidade 8':	15,
#   'Modalidade 9':	10}
#
#Q={'Modalidade 1':	2,
#   'Modalidade 2':	2,
#   'Modalidade 3':	2,
#   'Modalidade 4':  2,
#   'Modalidade 5':	2,
#   'Modalidade 6':	2,
#   'Modalidade 7':	2,
#   'Modalidade 8':	2,
#   'Modalidade 9':	2}
#
#RepsM={
#'RM1':'Cerca', 
#'RM2':'Tumba',
#'RM3':'Vamo ET',
#'RM4':'Tsu',
#'RM5':'13',
#'RM6':'Reprodução',
#'RM7':'Tcheca',
#'RM8':'Quintal',
#'RM9':'Peregrinos',
#'RM10':'Sipá',
#'RM11':'Rocinha',
#'RM12':'Trip',
#'RM13':'Rota',
#'RM14':'Arrocha',
#'RM15':'Barrigas',
#'RM16':'Ross'}


#_________________________________________________________________________________

Reps=RepsM
from gurobipy import *

m = Model ('Aruliadas')

#Limite do set de tempo
l=sum(P.values())*3

#Variáveis
X = m.addVars(Reps.keys(), Modalidades.keys(), range(l), vtype=GRB.BINARY, name='X')
W = m.addVars(Modalidades.keys(), range(l), vtype=GRB.BINARY, name='W')
V = m.addVars(Modalidades.keys(), range(l), vtype=GRB.BINARY, name='V')
Cmax = m.addVar(vtype=GRB.INTEGER, name='Cmax')
m.update()


#Jogar todas as modalidades 
m.addConstrs((quicksum(X.select(i,'*','*')) == len(list(Modalidades.keys())) for i in Reps.keys()),name='TodasMods')

#Jogar todas as modalidades apenas uma vez
m.addConstrs((quicksum(X.select(i,j,'*')) == 1 for i in Reps.keys() for j in Modalidades.keys()),name='ModsUmaVez')

#Cada slot tem 2 ou 0 tarefas 
for j in Modalidades.keys():
    for t in range(l):
        s=t-P[j]+1
        S=max(0,s)
        #Cada slot esta ocupado por 2 ou 0 tarefas
        m.addConstr((quicksum(X.select('*',j,range(S,t+1))) == Q[j]*(1-W[j,t])),name='Q')
        m.addConstr((quicksum(X.select('*',j,range(S,t+1))) >= (W[j,t]-1)),name='Qzero')
        #Começam 2 ou nenhuma tarefa em cada slot
        m.addConstr((quicksum(X.select('*',j,t)) == Q[j]*(1- V[j,t])),name='Q1')
        m.addConstr((quicksum(X.select('*',j,t)) >= (V[j,t]-1)),name='Q1zero')
        


for i in Reps.keys():
    for t in range(l):
        somas=[]
        for j in Modalidades.keys():
            S=max(0,t-P[j]+1)
            soma=quicksum(X.select(i,j,range(S,t+1)))
            somas.append(soma)
            
        m.addConstr(sum(somas)<= 3,name='Q')
        
m.addConstrs((Cmax>=X[i,j,t]*(t+P[j]) for i in Reps.keys() for j in Modalidades.keys() for t in range(l)), name='makespan')

m.update()

m.setObjective(Cmax, GRB.MINIMIZE)

#Comando que otimiza o problema
m.optimize()

#Imprimi na tela as variáveis, seus valores e o resultado da função objetivo
for v in X.values():
    if v.x != 0:
         print('%s %g' % (v.varName, v.x))
print('Obj: %g' % m.objVal)
        





