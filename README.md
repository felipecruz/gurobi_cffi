# Gurobi cffi bindings

This project aims to be a low level interface to Gurobi 5.6 C API (http://www.gurobi.com/documentation/5.6/reference-manual/c_reference_manual).

It can be used as backend for more high level solver interfaces with plugabble backends.

# Example

```python
from gurobi_cffi import *

ids = ['var1', 'var2', 'var3']
values = [8.0, 7.0, 10.0]

gurobi = Gurobi()
model = gurobi.new_model("MyExampleModel", ids, values)

gurobi.add_constraint(model, [0, 1, 2], [10, 10, 10], 60, "source1")
gurobi.add_constraint(model, [0, 1, 2], [10, 10, 10], 60, "sink1")

gurobi.optimize(model)

q1 = gurobi.query_variable_attribute(model, 'double', 'X', 0)
q2 = gurobi.query_variable_attribute(model, 'double', 'X', 1)
q3 = gurobi.query_variable_attribute(model, 'double', 'X', 2)

print("E1 flow: {}".format(q1))
print("E2 flow: {}".format(q2))
print("E3 flow: {}".format(q3))

gurobi.finish()
```

Output:

```
Optimize a model with 2 rows, 3 columns and 6 nonzeros
Presolve removed 2 rows and 3 columns
Presolve time: 0.00s
Presolve: All rows and columns removed
Iteration    Objective       Primal Inf.    Dual Inf.      Time
       0    4.2000000e+01   0.000000e+00   0.000000e+00      0s

Solved in 0 iterations and 0.00 seconds
Optimal objective  4.200000000e+01
E1 flow: 0.0
E2 flow: 6.0
E3 flow: 0.0
```

# Contact

felipecruz@loogica.net
