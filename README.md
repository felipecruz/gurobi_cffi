# Gurobi cffi bindings

This project aims to be a low level interface to Gurobi 5.6 C API (http://www.gurobi.com/documentation/5.6/reference-manual/c_reference_manual).

It can be used as backend for more high level solver interfaces with plugabble backends.

# Example

```python
ids = ["r1"]
values = [10.0]

gurobi = Gurobi()
model = gurobi.new_model("MyExampleModel", ids, values)

gurobi.add_constraint(model, [0], [10], 60, "source1")
gurobi.add_constraint(model, [0], [10], 60, "sink1")

gurobi.optimize(model)
gurobi.finish()
```

# Contact

felipecruz@loogica.net
