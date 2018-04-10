from sage.numerical.mip import MixedIntegerLinearProgram,MIPSolverException
import sys
from sage.all import *

g = graphs.PetersenGraph()
p = MixedIntegerLinearProgram(maximization=False)
b = p.new_variable()
for (u,v) in g.edges(labels = None):
    p.add_constraint(b[u] + b[v], min = 1)
p.set_objective(sum([b[v] for v in g]))
p.solve()
values = p.get_values(b).values()[::-1]
notDecideList = range(g.order())
upperBound = 100
g.plot()


def branch_and_cut(lp, var, val, u, notDecideList):
    try:
        global upperBound
        if u != -1:
            lp.add_constraint(var[u] - val[u] == 0)
            lp.show()
            optimal_object = lp.solve()
            
            print 'it have a solution'
            print lp.get_values(var)
            print 'op'
            print optimal_object
            print 'ub'
            print upperBound
            if optimal_object >= upperBound:
                print 'optimal_object >= upperBound'
                return 100
            else:
                print 'optima_object < upperBound'
                
                if len(notDecideList) == 0:
                    upperBound = optimal_object
                    return optimal_object
                else:
                    min_diff = 1
                    index_min = -1
                    integer = -1
                    
                    for i in notDecideList:
                        if 1 -val[i] < min_diff or val[i] < min_diff:
                            if 1 - val[i] < val[i]:
                                min_diff = 1 -val[i]
                                integer = 1
                                index_min = i
                            elif 1 - val[i] == val[i]:
                                min_diff = 1 -val[i]
                                integer = 0
                                index_min = i
                            else:
                                min_diff = 1 -val[i]
                                integer = 1
                                index_min = i
                                
                    u = index_min
                    val[u] = integer
                    notDecideList.remove(u)
                    print 'yin'
                    print val[u]
                    op1 = branch_and_cut(lp, var, val, u, notDecideList)
                    print 'op1'
                    print op1
                    
                    lp.remove_constraint(lp.number_of_constraints() - 1)
                    val[u] = 1 - val[u]
                    print 'zhuo'
                    print upperBound
                    op2 = branch_and_cut(lp, var, val, u, notDecideList)
                    print 'op2'
                    print op2
                    lp.remove_constraint(lp.number_of_constraints() - 1)
                    notDecideList.insert(0, u)
                    
                    if op1 < op2:
                        print 'op1'
                        print op1
                        print 'op2'
                        print op2
                        upperBound = op1
                        print 'op1 < op2'
                        return upperBound
                    elif op2 < op1:
                        print 'op1'
                        print op1
                        print 'op2'
                        print op2
                       	upperBound = op2
                        print 'op2 < op1'
                        return upperBound
                    else:
                       	return 100
            
        else:
            print 'diyici'
            min_diff = 1
            index_min = -1
            integer = -1
            
            for i in notDecideList:
                if 1 -val[i] < min_diff or val[i] < min_diff:
                    if 1 - val[i] < val[i]:
                        min_diff = 1 -val[i]
                        integer = 1
                        index_min = i
                    elif 1 - val[i] == val[i]:
                        min_diff = 1 -val[i]
                        integer = 0
                        index_min = i
                    else:
                        min_diff = 1 -val[i]
                        integer = 1
                        index_min = i
                        
            u = index_min
            val[u] = integer
            notDecideList.remove(u)
            op1 = branch_and_cut(lp, var, val, u, notDecideList)
            print 'op1'
            print op1
            lp.remove_constraint(lp.number_of_constraints() - 1)
            val[u] = 1 - val[u]
            op2 = branch_and_cut(lp, var, val, u, notDecideList)
            print 'op2'
            print op2
            lp.remove_constraint(lp.number_of_constraints() - 1)
            notDecideList.insert(0, u)
            
            if op1 < op2:
                print 'op1'
                print op1
                print 'op2'
                print op2
                upperBound = op1
                return upperBound
            elif op2 < op1:
                print 'op1'
                print op1
                print 'op2'
                print op2
               	upperBound = op2
                return upperBound
            else:
               	return 100                  
    except MIPSolverException:
    	print 'no feasiable solution'
    	return 100


optimal_object = branch_and_cut(p, b, values, -1, notDecideList)
print 'chao'
print optimal_object