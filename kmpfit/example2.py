import numpy
from matplotlib.pyplot import figure, show, rc
from kmpfit import kmpfit

def my_model(p, x):
   #-----------------------------------------------------------------------
   # This describes the model and its parameters for which we want to find
   # the best fit. 'p' is a sequence of parameters (array/list/tuple).
   #-----------------------------------------------------------------------
   A, mu, sigma, zerolev = p
   return( A * numpy.exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma)) + zerolev )


def my_residuals(p, data):
   #-----------------------------------------------------------------------
   # This function is the function called by the fit routine in kmpfit
   # It returns a weighted residual. De fit routine calculates the
   # square of these values.
   #-----------------------------------------------------------------------
   x, y, err = data
   return (y-my_model(p,x)) / err


# Artificial data
N = 100
x = numpy.linspace(-5, 10, N)
truepars = [10.0, 5.0, 1.0, 0.0]
p0 = [9, 4.5, 0.8, 0]
y = my_model(truepars, x) + 0.3*numpy.random.randn(len(x))
err = 0.3*numpy.random.randn(N)

# The fit
fitobj = kmpfit.Fitter(residuals=my_residuals, data=(x, y, err))
try:
   fitobj.fit(params0=p0)
except Exception, mes:
   print "Something wrong with fit: ", mes
   raise SystemExit

print "\n\n=============== Results of kmpfit  ==================="
print "Params:        ", fitobj.params
print "Errors from covariance matrix         : ", fitobj.xerror
print "Uncertainties assuming reduced Chi^2=1: ", fitobj.stderr 
print "Chi^2 min:     ", fitobj.chi2_min
print "Reduced Chi^2: ", fitobj.rchi2_min
print "Iterations:    ", fitobj.niter
print "Function ev:   ", fitobj.nfev 
print "Status:        ", fitobj.status
print "Status Message:", fitobj.message
print "Covariance:\n", fitobj.covar 

# Plot the result
rc('font', size=9)
rc('legend', fontsize=8)
fig = figure()
frame = fig.add_subplot(1,1,1)
frame.errorbar(x, y, yerr=err, fmt='go', alpha=0.7, label="Noisy data")
frame.plot(x, my_model(truepars,x), 'r', label="True data")
frame.plot(x, my_model(fitobj.params,x), 'b', lw=2, label="Fit with kmpfit")
frame.set_xlabel("X")
frame.set_ylabel("Measurement data")
frame.set_title("Least-squares fit to noisy Gaussian data using KMPFIT",
                fontsize=10)
leg = frame.legend(loc=2)
show()