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


def query_array_int_attribute_position(env, model, attrname, total_variables):
    value = ffi.new('int*')
    error = gurobi.GRBgetintattrelement(model, ffi.new('char[]', attrname),
                                        pos, value)
    _check_error(env, error)
    return value(int(value[0]))


def query_array_double_attribute_position(env, model, attrname, pos,
                                          total_variables):
    value = ffi.new('double*')
    error = gurobi.GRBgetdblattrelement(model, ffi.new('char[]', attrname), pos,
                                        value)
    _check_error(env, error)
    return float(value[0])


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


def gurobi_env(log_file):
    env = ffi.new('GRBenv**')
    error = gurobi.GRBloadenv(env, log_file)
    _check_error(env, error)
    return env[0]


def gurobi_free(env):
    gurobi.GRBfreeenv(env)

class GurobiModel(object):
    def __init__(self, env, model, len_vars):
        self.env = env
        self._model = model
        self._len_vars = len_vars

    def query_variable_attribute(self, _type_name, attrname, pos):
        if _type_name == 'int':
            return query_array_int_attribute_position(self.env, self._model,
                                                      attrname,
                                                      pos,
                                                      self._len_vars)
        elif _type_name == 'double':
            return query_array_double_attribute_position(self.env, self._model,
                                                         attrname,
                                                         pos,
                                                         self._len_vars)
        else:
            raise Exception("Unsupported type: {}".format(_type_name))

    @property
    def model(self):
        return self._model


class Gurobi(object):
    def __init__(self, log_file="gurobi.log"):
        self.log_file = log_file
        self.env = gurobi_env(self.log_file)

    def new_model(self, name, ids, values):
        l_ids = len(ids)
        if not l_ids == len(values):
            raise Exception("Invalid size of ids and values")
        self._len_vars = len(ids)

        return GurobiModel(self, new_model(self.env, name, ids, values),
                           len(ids))

    def update(self, model):
        update(self.env, model.model)

    def add_constraint(self, model, indexes, values, obj, name,
                       constraint=GRB_EQUAL):
        add_constraint(self.env, model.model, indexes, values, obj, name,
                       constraint)

    def query_constraint_attribute(self, model, _type_name, attrname, pos):
        return self.query_variable_attribute(model.model, _type_name, attrname, pos)

    def query_variable_attribute(self, model, _type_name, attrname, pos):
        if _type_name == 'int':
            return query_array_int_attribute_position(self.env, model.model,
                                                      attrname,
                                                      pos,
                                                      self._len_vars)
        elif _type_name == 'double':
            return query_array_double_attribute_position(self.env, model.model,
                                                         attrname,
                                                         pos,
                                                         self._len_vars)
        else:
            raise Exception("Unsupported type: {}".format(_type_name))

    def optimize(self, model):
        model_optimize(self.env, model.model)

    def finish(self):
        gurobi_free(self.env)
