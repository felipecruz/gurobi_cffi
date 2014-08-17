from gurobi import *

if __name__ == "__main__":
    size = 1
    var_id = lambda i: "var:{}".format(i)

    ids = [var_id(i) for i in range(1)]
    values = [(i+1)*10. for i in range(size)]

    gurobi = Gurobi()
    model = gurobi.new_model("MyExampleModel", ids, values)

    gurobi.add_constraint(model, [0], [10], 60, "source1")
    gurobi.add_constraint(model, [0], [10], 60, "sink1")

    gurobi.optimize(model)
    gurobi.finish()
