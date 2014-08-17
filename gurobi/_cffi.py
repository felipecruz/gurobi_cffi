import cffi

ffi = cffi.FFI()

ffi.cdef('''
typedef ... GRBenv;
typedef ... GRBmodel;

int GRBloadenv(GRBenv **envP, const char *logfilename);
void GRBfreeenv(GRBenv *env);

int GRBnewmodel (GRBenv *env,
                 GRBmodel **modelP,
                 const char *Pname,
                 int numvars,
                 double *obj,
                 double *lb,
                 double *ub,
                 char *vtype,
                 const char **varnames);

int GRBaddvars (GRBmodel *model,
                int numvars,
                int numnz,
                int *vbeg,
                int *vind,
                double *vval,
                double *obj,
                double *lb,
                double *ub,
                char *vtype,
                const char **varnames);

int GRBaddconstr (GRBmodel *model,
                 int numnz,
                 int *cind,
                 double  *cval,
                 char sense,
                 double rhs,
                 const char *constrname);

int GRBupdatemodel(GRBmodel *model);
const char* GRBgeterrormsg(GRBenv *env);
int GRBoptimize(GRBmodel *model);
''')

gurobi = ffi.verify('''
    #include "gurobi_c.h"
''',
    libraries=['gurobi56'],
    include_dirs=['/Library/gurobi563/mac64/include'],
    library_dirs=['/Library/gurobi563/mac64/lib'])
