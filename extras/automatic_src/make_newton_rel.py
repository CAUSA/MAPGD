import sympy 
import sys
from sympy.utilities.codegen import codegen
from sympy.printing import print_ccode

#The Data
Q=sympy.Symbol('pair.m')

lMM2=sympy.Symbol('pair.Y_MM')
lMm2=sympy.Symbol('pair.Y_Mm')
lmm2=sympy.Symbol('pair.Y_mm')

lMM1=sympy.Symbol('pair.X_MM')
lMm1=sympy.Symbol('pair.X_Mm')
lmm1=sympy.Symbol('pair.X_mm')

#The Parameters
g_XY=sympy.Symbol('rel.gamma_XY_')
g_YX=sympy.Symbol('rel.gamma_YX_')
T=sympy.Symbol('rel.theta_XY_')
D=sympy.Symbol('rel.Delta_XY_')
d=sympy.Symbol('rel.delta_XY_')
F_Y=sympy.Symbol('rel.f_Y_')
F_X=sympy.Symbol('rel.f_X_')

#An array of the parameters.
params=[F_X, F_Y, T, g_XY, g_YX, d, D]

#The three componenents of the likelihood function. H00 is homozygous for the major allele, H01 heterozygous, and H11 homozygous minor.

P=1-Q
var=P*(1.-P)
std=var**(0.5);
skew=(1.-2.*P)/std;
kurtosis=1./(1.-P)+1./P-3.;

mmmm=(Q**4+(F_X+F_Y+4*T)*var*Q**2-2*(g_XY+g_YX)*skew*Q+d*kurtosis+D*var**2);

MMMM=(P**4+(F_X+F_Y+4*T)*var*P**2-2*(g_XY+g_YX)*skew*P+d*kurtosis+D*var**2);

Mmmm=(2*P*Q**3+2*(F_Y*P*Q-F_X*Q**2-2*T*(Q**2-P*Q))*var-4*g_XY*(P-Q)*skew+2*g_YX*(Q-P)*skew-2*d*kurtosis-2*D*var**2);
mmMm=(2*P*Q**3+2*(F_X*P*Q-F_Y*Q**2-2*T*(Q**2-P*Q))*var-4*g_YX*(P-Q)*skew+2*g_XY*(Q-P)*skew-2*d*kurtosis-2*D*var**2);

MmMM=(2*Q*P**3+2*(F_Y*P*Q-F_X*P**2-2*T*(P**2-P*Q))*var-4*g_XY*(Q-P)*skew+2*g_YX*(P-Q)*skew-2*d*kurtosis-2*D*var**2);
MMMm=(2*Q*P**3+2*(F_X*P*Q-F_Y*P**2-2*T*(P**2-P*Q))*var-4*g_YX*(Q-P)*skew+2*g_XY*(P-Q)*skew-2*d*kurtosis-2*D*var**2);

MmMm=(4*P**2*Q**2+4*(T*(P**2+Q**2-2*P*Q)-F_X*P*Q-F_Y*P*Q)*var+4*g_XY*(P-Q)*skew+4*g_YX*(Q-P)*skew+4*d*kurtosis+4*D*var**2);

MMmm=(P**2*Q**2+(F_Y*P**2+F_X*Q**2-4*T*P*Q)*var+2*g_XY*P*skew-2*g_YX*Q*skew+d*kurtosis+D*var**2);
mmMM=(P**2*Q**2+(F_X*P**2+F_Y*Q**2-4*T*P*Q)*var+2*g_YX*P*skew-2*g_XY*Q*skew+d*kurtosis+D*var**2);

#The log likelihood equation
lnL=sympy.log( mmmm*sympy.exp(-lmm1-lmm2)+mmMm*(sympy.exp(-lmm1-lMm2))+mmMM*sympy.exp(-lmm1-lMM2)+Mmmm*sympy.exp(-lMm1-lmm2)+MmMm*sympy.exp(-lMm1-lMm2)+MmMM*sympy.exp(-lMm1-lMM2)+MMmm*sympy.exp(-lMM1-lmm2)+MMMm*sympy.exp(-lMM1-lMm2)+MMMM*sympy.exp(-lMM1-lMM2) )

system_eq=[]

#We first need the three equations we are going to try and set to zero, i.e. the first partial derivitives wrt e h and F.
print "/*This code was automatically generated by "+str(sys.argv[0])+"*/\n"
print "#include \"allele.h\""
print "#include \"quartet.h\""
print "#include \"typedef.h\""
print 
#numpy.set_printoptions(precission=18)
for x in range(0, 7):
	system_eq.append(sympy.diff(lnL, params[x]) )
	print "inline float_t H"+str(x)+" (const Genotype_pair &pair, const Relatedness &rel) {"
	sys.stdout.write("\treturn ")
	print_ccode(  system_eq[-1] )
	print ";\n}\n"

#Then we need to make the Jacobian, which is a matrix with ...
for x in range(0, 7):
	for y in range(0, 7):
		print "inline float_t J"+str(x)+str(y)+" (const Genotype_pair &pair, const Relatedness &rel) {"
		sys.stdout.write("\treturn ")
		print_ccode(sympy.diff(system_eq[x], params[y]))
		print ";\n}\n"

print "inline float_t lnL_NR (const Genotype_pair &pair, const Relatedness &rel) {"
sys.stdout.write("\treturn ")
print_ccode(lnL)
print ";\n}\n"

quit()