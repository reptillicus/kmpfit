import numpy
from kmpfit import kmpfit

def residuals(p, data):  # Residuals function needed by kmpfit
   x, y = data           # Data arrays is a tuple given by programmer
   a, b = p              # Parameters which are adjusted by kmpfit
   return (y-(a+b*x))

d = numpy.array([42, 6.75, 25, 33.8, 9.36, 21.8, 5.58, 8.52, 15.1])
v = numpy.array([1294, 462, 2562, 2130, 750, 2228, 598, 224, 971])

paramsinitial = [0, 70.0]
fitobj = kmpfit.Fitter(residuals=residuals, data=(d,v))
fitobj.fit(params0=paramsinitial)

print "\nFit status kmpfit:"
print "===================="
print "Best-fit parameters:        ", fitobj.params
print "Asymptotic error:           ", fitobj.xerror
print "Error assuming red.chi^2=1: ", fitobj.stderr
print "Chi^2 min:                  ", fitobj.chi2_min
print "Reduced Chi^2:              ", fitobj.rchi2_min
print "Iterations:                 ", fitobj.niter
print "Number of free pars.:       ", fitobj.nfree
print "Degrees of freedom:         ", fitobj.dof