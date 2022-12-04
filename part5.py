from part2 import BDD, show, table, cons_arbre, compression_bdd, dot

"""
Soeint x et y deux étiquettes de l'arbre T
Si x < y, alors dans le parcours de T, y est avant x
"""
def apply(op,B,C,D):
	"""function * BDD * BDD * dict[str:BDD]
	"""
	if B is None:
		return D, C
	if C is None:
		return D, B

	if B.leaf() and C.leaf():
		res = op(B.val, C.val)
		luka = str(res)
		if luka not in D:
			leaf =  BDD(res,luka=luka)
			D[luka] = leaf
		return D, D[luka]

	if B.val == C.val:
		D, left = apply(op,B.left,C.left,D)
		D, right = apply(op,B.right,C.right,D)
		luka = f"{B.val}({left.luka})({right.luka})"

		if left.luka == right.luka:
			D[luka] = left
		elif luka not in D:
			res = BDD(B.val,left,right,luka)
			D[luka] = res
		return D, D[luka]

	if not(B.leaf()) and  (C.leaf() or C.val < B.val):
		D, left = apply(op,B.left,C,D)
		D, right = apply(op,B.right,C,D)
		luka = f"{B.val}({left.luka})({right.luka})"
		
		if left.luka == right.luka:
			D[luka] = left
		elif luka not in D:
			res = BDD(B.val,left,right,luka)
			D[luka] = res
		return D, D[luka]

	if B.leaf() or B.val < C.val:
		D, left = apply(op,B,C.left,D)
		D, right = apply(op,B,C.right,D)
		luka = f"{C.val}({left.luka})({right.luka})"
		
		if left.luka == right.luka:
			D[luka] = left
		elif luka not in D:
			res = BDD(C.val,left,right,luka)
			D[luka] = res
		return D, D[luka]

def combinaison(op,B,C):
	_, g = apply(op,B,C,dict())
	return g


def test(op,B,C,nametest):
	g = combinaison(op,B,C)
	dot(g,nametest)
	execpted_file = open("test/"+nametest + ".dot", "r")
	res_file = open("graphe/"+nametest + ".dot", "r")
	execpted = execpted_file.readlines()
	res = res_file.readlines()
	assert res == execpted
	execpted_file.close()
	res_file.close()


if __name__ == "__main__" :
	_and = compression_bdd(cons_arbre(table(8,4)))
	_or = compression_bdd(cons_arbre(table(14,4)))
	_x1 = compression_bdd(cons_arbre(table(2,2)))
	_not_x1 = compression_bdd(cons_arbre(table(1,2)))
	_not_x2 = compression_bdd(cons_arbre(table(3,4)))

	# test 1 : (x1 and x2) or (not x1 and not x2)
	test(lambda a, b : a or b,_and, compression_bdd(cons_arbre(table(1,4))),"test1")

	#test 2 : (x1 and x2) or (x1 or x2)
	test(lambda a, b : a or b,_and, _or,"test2")

	# test 3 : x1 and (not x2)
	test(lambda a, b : a and b, _x1, _not_x2, "test3")
	

	# test 4 : (x1 and not x2) or (not x1 and x2)
	Z1 = compression_bdd(cons_arbre(table(2,4)))
	Z2 = compression_bdd(cons_arbre(table(4,4)))
	test(lambda a, b: a or b,Z1, Z2,"test4")

	#test 5 : (x2 and x1) or not x2
	test(lambda a, b: a or b,_and,_not_x1,"test5") 


