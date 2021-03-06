# make sure to also install psutil with memory_profiler
from memory_profiler import memory_usage
import numpy as np

# garbage collection before each memory_usage call does seem to give better estimates
import gc
import cvxpy as cvx
from collections import defaultdict
import scs

def cvx_solve():
    m = 128
    n = 10
    np.random.seed(1)
    A = np.random.randn(m, n)
    b = np.random.randn(m)

    # Construct the problem.
    x = cvx.Variable(n)
    objective = cvx.Minimize(cvx.norm(A*x - b))
    constraints = [0 <= x, x <= 1]
    prob = cvx.Problem(objective, constraints)
    prob.solve('SCS')

def scs_data():
    #data, cone = scs.examples.l1(500)
    data, cone, _ = scs.examples.simple_socp()

def scs_solve():
    #data, cone = scs.examples.l1(500)
    data, cone, _ = scs.examples.simple_socp()
    scs.solve(data, cone, verbose=False)

def scs_work():
    #data, cone = scs.examples.l1(500)
    data, cone, _ = scs.examples.simple_socp()
    work = scs.Workspace(data, cone, verbose=False)
    work.solve()

def dummy():
    a = defaultdict(list)
    n = 1000
    for i in np.random.randint(n,size=2*n):
        a[i] += [i*i]

def ver():
    s = scs.version()


def test(funcs, n=10):
    # run a few times to get any ancillary objects created
    for i in range(3):
        for f in funcs:
            f()
            gc.collect()
            memory_usage(-1, interval=0)
            a = np.zeros(n)
            (a.max() - a.min())/n

    for f in funcs:
        a = np.zeros(n)
        for i in range(n):
            f()
            gc.collect()
            r = memory_usage(-1, interval=0)
            a[i] = r[0]

        yield (a.max() - a.min())/n

#funcs = scs_solve, scs_data, dummy, scs_solve, scs_data, cvx_solve, scs_solve, cvx_solve
funcs = dummy, ver, scs_data, scs_solve, scs_work

print list(test(funcs))
