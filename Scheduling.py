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
   'Modalidade 4':  4,
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

#
#Modalidades = {	'Modalidade 1':'Pebolim'}
#
#P={'Modalidade 1':	20}
#
#Q={'Modalidade 1':	2}
#
#RepsM={
#'RM1':'Cerca', 
#'RM2':'Tumba'}
#
#RepsF={
#'RF1':'Aras',
#'RF2':'Matilha',
#'RF3':'Santa Casa',
#'RF4':'Breja Flor',
#'RF5':'Vegas',
#'RF6':'Toroço',
#'RF7':'Las Chicas',
#'RF8':'D4',
#'RF9':'Vai da Nada',
#'RF10':'Amazona',
#'RF11':'Shot',
#'RF12':'After',
#'RF13':'Be Happy',
#'RF14':'Saia Justa'}




#_______________________________________________________________________________________
from ortools.linear_solver import pywraplp

#Limite do set de tempo
l=sum(P.values())*3

#Declarando o solver
aruli = pywraplp.Solver('Aruliadas', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

#Definindo se são as reps masculinas ou femininas
Reps=RepsM

#Variáveis
X={(i,j,t):aruli.IntVar(0,1,'X '+str(i)+str(j)+str(t)) for i in Reps.keys() for j in Modalidades.keys() for t in range(l)}

O={(i,j,t):aruli.IntVar(0,1,'O '+str(i)+str(j)+str(t)) for i in Reps.keys() for j in Modalidades.keys() for t in range(l)}

W={(j,t): aruli.IntVar(0,1,'W '+str(j)+str(t)) for j in Modalidades.keys() for t in range(l)}

Cmax=aruli.IntVar(0,aruli.infinity(),'Cmax')

#Restrições

#Número máximo de modalidades por rep em um instante de tempo
for i in Reps.keys():
    for t in range(l):
        aruli.Add( aruli.Sum(O[(i,j,t)] for j in Modalidades.keys() ) <= 3)
        
#Todas as reps devem jogar todas as modalidades um única vez
for i in Reps.keys():        
    for j in Modalidades.keys():
        aruli.Add( aruli.Sum(O[(i,j,t)] for t in range(l) ) == P[j])

#Garante que cada modalidade tenha Qj reps disputando a mesma partida ao mesmo tempo        
for j in Modalidades.keys():
    for t in range(1,l):
        aruli.Add( aruli.Sum(O[(i,j,t)] for i in Reps.keys() ) == Q[j]*(1-W[(j,t)]))
        aruli.Add( aruli.Sum(O[(i,j,t)] for i in Reps.keys() ) >= (W[(j,t)]-1))
        
#Período ocupado: Atribui o valor 1 para as variáveis Oijt
for i in Reps.keys():        
    for j in Modalidades.keys():
        for t in range(l):
            S=t+P[j]-1
            if S>l:
                S=l
            aruli.Add( aruli.Sum(O[(i,j,s)] for s in range(t,S)) >= P[j]*X[(i,j,t)])
#Makespan
for i in Reps.keys():        
    for j in Modalidades.keys():
        for t in range(l):
            aruli.Add(Cmax>=X[(i,j,t)]*(t+P[j]))

#for i in Reps.keys():        
#    for j in Modalidades.keys():
#        aruli.Add( aruli.Sum(X[(i,j,t)] for t in range(l)) == 1 )
#     
    

#FO    
aruli.Minimize(Cmax)   

result_status = aruli.Solve()
# The problem has an optimal solution.
assert result_status == pywraplp.Solver.OPTIMAL
assert aruli.VerifySolution(1e-7, True)

print('Objective value =', aruli.Objective().Value())




