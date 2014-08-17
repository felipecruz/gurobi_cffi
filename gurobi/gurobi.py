from ._cffi import ffi, gurobi
from .constants import *

def _check_error(env, error):
    if error:
        msg = ffi.string(gurobi.GRBgeterrormsg(env))
        exception_msg = "Error code: {} - msg: {}".format(error, msg)
        raise Exception(exception_msg)

def update(env, model):
    error = gurobi.GRBupdatemodel(model)
    _check_error(env, error)


def add_constraint(env, model, indexes, values, obj, name, constraint):
    c_indexes = ffi.new('int[]', indexes)
    c_values = ffi.new('double[]', values)
    size = len(indexes)

    error = gurobi.GRBaddconstr(model,
                                ffi.cast('int', size),
                                c_indexes,
                                c_values,
                                ffi.cast('char', constraint),
                                ffi.cast('double', obj),
                                ffi.new('char[]', name))
    _check_error(env, error)


def new_model(env, name, ids, values):
    _c_strings = [ffi.new('char[]', _id) for _id in ids]
    varnames = ffi.new('char *[]', _c_strings)
    objs = [ffi.cast("double", value) for value in values]
    num_vars = len(varnames)
    model = ffi.new('GRBmodel**')

    error = gurobi.GRBnewmodel(env, model, name, num_vars, objs,
                               ffi.NULL, ffi.NULL, ffi.NULL, varnames)
    _check_error(env, error)
    return model[0]


def model_optimize(env, model):
    error = gurobi.GRBoptimize(model)
    _check_error(env, error)


def gurobi_env(log_file="facility.log"):
    env = ffi.new('GRBenv**')
    error = gurobi.GRBloadenv(env, log_file)
    _check_error(env, error)
    return env[0]


def gurobi_free(env):
    gurobi.GRBfreeenv(env)


class Gurobi(object):
    def __init__(self, log_file="gurobi.log"):
        self.log_file = log_file
        self.env = gurobi_env()

    def new_model(self, name, ids, values):
        return new_model(self.env, name, ids, values)

    def update(self, model):
        update(self.env, model)

    def add_constraint(self, model, indexes, values, obj, name,
                       constraint=GRB_EQUAL):
        add_constraint(self.env, model, indexes, values, obj, name,
                       constraint)

    def optimize(self, model):
        model_optimize(self.env, model)

    def finish(self):
        gurobi_free(self.env)
