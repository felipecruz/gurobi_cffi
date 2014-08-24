from gurobi_cffi import *

if __name__ == "__main__":
    ids = ['var1', 'var2', 'var3']
    values = [8.0, 7.0, 10.0]

    gurobi = Gurobi()
    model = gurobi.new_model("MyExampleModel", ids, values)

    model.add_constraint([0, 1, 2], [10, 10, 10], 60, "source1")
    model.add_constraint([0, 1, 2], [10, 10, 10], 60, "sink1")

    model.optimize()

    q1 = model.query_variable_attribute('double', 'X', 0)
    q2 = model.query_variable_attribute('double', 'X', 1)
    q3 = model.query_variable_attribute('double', 'X', 2)

    print("E1 flow: {}".format(q1))
    print("E2 flow: {}".format(q2))
    print("E3 flow: {}".format(q3))

    gurobi.finish()
