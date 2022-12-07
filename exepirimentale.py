import part2 as bdd
from start import table
import os
from time import time
from random import randint
import pandas as pd

def count_node(T:bdd.BDD):
	def aux(n, S):	
		if n:
			S = aux(n.left,S)
			S = aux(n.right, S)
			if n.luka not in S:
				S.add(n.luka)
		return S
	return len(aux(T, set()))

def plot(n):
	str_n = str(n)
	file = open("figure/commande.txt", "w")
	s = "set terminal pngcairo\n"
	s += "set style line 1 lt 1 lw 2 pt 7 ps .65\n"
	s += "set output 'figure/image/var_"+ str_n +".png'\n"
	s += "set xlabel 'ROBDD node count for "+ str_n +" variable'\n"
	s += "set ylabel 'Number of Boolean functions'\n"
	s += "plot 'figure/donnees/var_"+ str_n+ ".txt' with linespoints ls 1 notitle\n"
	file.write(s)
	file.close()
	os.system("gnuplot -p < figure/commande.txt")

#sample: contient les entiers qui vont être utilisé pour générer les tables
def experience_var(n,sample,filename):
	D = dict()
	k = pow(2,n)
	for i in sample:
		t = bdd.table(i,k)
		abr = bdd.cons_arbre(t)
		bdd.luka(abr)
		abr = bdd.compression_bdd(abr)
		bdd.luka(abr)
		res = count_node(abr)
		if res not in D:
			D[res] = 1
		else:
			D[res] += 1

	s = ""
	for k in sorted(D.keys()) :
		s += str(k) + " " + str(2*D[k]) + "\n"
	file = open(filename, "w")
	file.write(s)
	file.close()
	return D

#Trace les courbes de la figure 9
def figure9():
	for i in range(1,5):
		k = pow(2,i)
		experience_var(i,range(pow(2, k-1)))
		plot(i)

"""t est un temps en secondes
retourne la chaîne hh:mm:ss
"""
def convert_t(t):
	h,res = t // 3600, t % 3600
	m, s = res // 60, res % 60
	return "{:02.0f}:{:02.0f}:{:02.0f}".format(h,m,s)

#crée la figure 10 et 11
def figure10():
	data = []
	#change i pour varier les variables
	for i in range(5,11):
		k = pow(2,i)
		lst = [randint(1,pow(2,k-1)) for _ in range(500000)]
		lst.append(0)
		tstart = time()
		D = experience_var(i,lst,"figure/donnees/var_"+ str(i)+ ".txt")
		#en secondes
		duree = time() - tstart
		data.append([i,500001,len(D),convert_t(duree),duree / 500001])
		plot(i)

	df = pd.DataFrame(data,columns=['No.Variables','No.Samples', 'No.Unique Sizes', 'Compute Time hh:mm:ss', 'Seconds per ROBDD'])
	df.to_csv('figure/figure11.csv', index=False, mode = "a", header=False)

#Calcule la distribution pour 5 variable et mesure le temps pris
def var5():
	k = pow(2,5)
	t0 = time()
	experience_var(5,range(pow(2, k-1)))
	return time() - t0


if __name__ == "__main__" :
	figure10()
	
	
	