
void ddpoly(float c[], int nc, float x, float pd[], int nd);
void ddpoly_debug(float c[], int nc, float x, float pd[], int nd);
void poldiv(float u[], int n, float v[], int nv, float q[], float r[]);
void poldiv_debug(float u[],int n,float v[],int nv,float q[],float r[]);
float dfridr(float (*func)(float), float x, float h, float *err);
float simplenumerical(float (*func)(float), float x, float h);
void chebft(float a, float b, float c[], int n, float (*func)(float));
float chebev(float a, float b, float c[], int m, float x);
float chebev_debug(float a, float b, float c[], int m, float x);

