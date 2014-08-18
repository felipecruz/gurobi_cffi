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

int GRBgetintattr(GRBmodel *model, const char *attrname, int *valueP);
int GRBsetintattr(GRBmodel *model, const char *attrname, int newvalue);
int GRBgetintattrelement(GRBmodel *model, const char *attrname,
                         int element, int *valueP);
int GRBsetintattrelement(GRBmodel *model, const char *attrname,
                         int element, int newvalue);
int GRBgetintattrarray(GRBmodel *model, const char *attrname,
                       int first, int len, int *values);
int GRBsetintattrarray(GRBmodel *model, const char *attrname,
                       int first, int len, int *newvalues);
int GRBgetintattrlist(GRBmodel *model, const char *attrname,
                      int len, int *ind, int *values);
int GRBsetintattrlist(GRBmodel *model, const char *attrname,
                      int len, int *ind, int *newvalues);


int GRBgetdblattr(GRBmodel *model, const char *attrname, double *valueP);
int GRBsetdblattr(GRBmodel *model, const char *attrname, double newvalue);

int GRBgetdblattrelement(GRBmodel *model, const char *attrname,
                         int element, double *valueP);
int GRBsetdblattrelement(GRBmodel *model, const char *attrname,
                         int element, double newvalue);
int GRBgetdblattrarray(GRBmodel *model, const char *attrname,
                       int first, int len, double *values);
int GRBsetdblattrarray(GRBmodel *model, const char *attrname,
                       int first, int len, double *newvalues);
int GRBgetdblattrlist(GRBmodel *model, const char *attrname,
                      int len, int *ind, double *values);
int GRBsetdblattrlist(GRBmodel *model, const char *attrname,
                      int len, int *ind, double *newvalues);


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
