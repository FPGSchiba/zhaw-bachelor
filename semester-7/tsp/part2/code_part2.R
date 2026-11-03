# R-code: simulation MA(1)
# Learn: arima.sim, ARMAacf

set.seed(10)
sigma<-2
b_1<-0.5
len<-30
y_1<-arima.sim(n = len, list( ma = b_1), sd = sigma)
set.seed(10)
len<-100
y_2<-arima.sim(n = len, list( ma = b_1), sd = sigma)
set.seed(10)
len<-300
y_3<-arima.sim(n = len, list( ma = b_1), sd = sigma)

# Plot the series
ts.plot(y_1)
ts.plot(y_2)
ts.plot(y_3)

rho<-c(b_1/(1+b_1^2),rep(0,4))
rho
# R-command for computing the acf: both calculations match
ARMAacf(ma=b_1,lag.max=10)
ARMAacf(ma=b_1,lag.max=10,pacf=T)


# In general b1 is unknown and therefore ARMAacf is of limited practical utility. 
# Instead, the acf must be estimated directly from the data, relying on acf-command
# For long data sets (many observations) acf converges to ARMAacf (assuming b1 is known)
par(mfrow=c(3,1))
acf(y_1)
acf(y_2)
acf(y_3)

# Extract estimates from acf-object
acf(y_1)$acf
acf(y_2)$acf
acf(y_3)$acf

#---------------------
# acf and pacf
len<-1000
set.seed(1)
b_1<-0.9
y_4<-arima.sim(n = len, list( ma = b_1), sd = sigma)

# Acf is insignificant for lags>q=1
par(mfrow=c(2,1))
acf(y_4)
# pacf converges 'slowly' to 0
acf(y_4,type="partial")




###################################################
### code chunk number 2: slides_part2.Rnw:207-260
###################################################
# R-code: estimate $b_1$
# Learn: arima

estim<-function(parma,x)
{
# Center the data
  x<-x-mean(x)
# Determine length
  len<-length(x)
# Define q
  q<-length(parma)
  b<-parma
# Define a vector of epsilons
  epsilon<-x
# Compute epsilon_1
  epsilon[1]<-x[1]
# Compute the other epsilons  
  for (i in 2:q)
  {
    epsilon[i]<-x[i]-epsilon[(i-1):1]%*%b[1:(i-1)]
  }
  for (i in (q+1):len)
  {
    epsilon[i]<-x[i]-epsilon[(i-1):(i-q)]%*%b[1:q]
  }
# Return the MSE  
  return(sum(epsilon^2))
}


set.seed(10)
sigma<-sqrt(2)
b_1<-0.7
len<-100
x<-arima.sim(n = len, list( ma = c(b_1)), sd = sigma)
ts.plot(x)
acf(x)

# Set any parameter value: which model corresponds to b1=0?
parma<-c(0)
# This is the wrong parameter: the true parameter is 0.7
# Therefore we expect MSE to be large
estim(parma,x)
# Now we insert the true parameter: MSE is much smaller
estim(b_1,x)
# Now we minimize MSE
estim_obj<-nlminb(parma,estim,x=x)
# Note that MSE is smaller than for true b_1: this is beacuse we minimize MSE (overfitting)
estim_obj
# CSS 
round(estim_obj$par,4)
# R-command: CSS according to arima
ma_obj<-arima(x,order = c(0, 0, 1),method="CSS")
round(ma_obj$coef,4)
# R-command Maximum Likelihood according to arima
ma_obj<-arima(x,order = c(0, 0, 1))
round(ma_obj$coef,4)

# From now we shall rely on default R-command arima()


###################################################
### code chunk number 3: slides_part2.Rnw:306-337
###################################################
# R-code: MA(1) diagnostics
# learn tsdiag
set.seed(10)
sigma<-sqrt(2)
b_1<-0.7
len<-100
x<-arima.sim(n = len, list( ma = b_1), sd = sigma)

ts.plot(x)

# Identification
acf(x)

# Estimation
# You may try white noise by setting order=c(0,0,0) in arima: check the resulting diagnostics below
x_obj<-arima(x,order=c(0,0,1))
x_obj

# Simple diagnostics
par(mfrow=c(1,1))
acf(x_obj$res)

# More sophisticated diagnostics: try a white noise model in arima and check diagnostics again
tsdiag(x_obj,gof.lag=30)

# False (white noise) model: too simple
x_obj<-arima(x,order=c(0,0,0))

tsdiag(x_obj,gof.lag=20)


# We can fit a more complex model: diagnostics also OK but danger of overfitting
# Rely on SIMPLEST model for which diagnostics are OK
x_obj<-arima(x,order=c(0,0,10))

acf(x_obj$res)

tsdiag(x_obj,gof.lag=20)



###################################################
### code chunk number 4: slides_part2.Rnw:398-483
###################################################
# R-code: MA(1) forecast
# learn: predict
# First case: mu=0
set.seed(10)
sigma<-sqrt(2)
b_1<-0.7
len<-1000
# Compute one additional observation i.e. len+1
y<-arima.sim(n = len+1, list( ma = b_1), sd = sigma)
ts.plot(y)

# Data
x<-y[1:len]
# Future observation: must be forecasted
x_future<-y[len+1]
# Identification
acf(x)

# Estimation
x_obj<-arima(x,order=c(0,0,1))
x_obj
par(mfrow=c(1,1))
acf(x_obj$res)

# More sophisticated diagnostics
tsdiag(x_obj,gof.lag=30)

b1<-x_obj$coef["ma1"]

epsilon_T<-sum((-1)^{0:(len-1)}*b1^(0:(len-1))*(x[len:1]-mean(x)))
xhat<-b1*epsilon_T

xhat+mean(x)

# Use R-command predict: the forecast matches with our number up to negligible rounding errors
predict(x_obj,n.ahead=1)

predict(x_obj,n.ahead=1)$pred

#--------------
# Second case: mu!=0

mu<-10
set.seed(10)
sigma<-sqrt(2)
b_1<-0.7
len<-1000
# Shift by mu
y<-mu+arima.sim(n = len+1, list( ma = b_1), sd = sigma)
ts.plot(y)

# Data
x<-y[1:len]
# Future observation: must be forecasted
x_future<-y[len+1]
# Identification 2
acf(x)

# Estimation

x_obj<-arima(x,order=c(0,0,1))
x_obj
par(mfrow=c(1,1))
acf(x_obj$res)

# More sophisticated diagnostics
tsdiag(x_obj,gof.lag=30)

b1<-x_obj$coef["ma1"]


# Formula in slides
epsilon_T<-sum((-1)^{0:(len-1)}*b1^(0:(len-1))*(x[len:1]-mean(x)))
xhat<-mean(x)+b1*epsilon_T

xhat

# Use R-command predict: the forecast matches with our number up to negligible rounding errors
predict(x_obj,n.ahead=1)

predict(x_obj,n.ahead=1)$pred


# R-code: MA(1) pacf pattern
# Simulate MA(1) and compare MA-inversion, pacf and regression
set.seed(10)
sigma<-sqrt(2)
b1<-0.9
len<-1000
z<-arima.sim(n = len, list( ma = b1), sd = sigma)

acf(z,type="partial")
# The coefficients are larger (in absolute) because the pacf relies on finite regression: see regressions below (the absolute value increase for increasing lag)
b1*(-1)^{0:(10)}*b1^(0:(10))

acf(z,type="partial",plot=F)
# Compare pacf(k) with last regression coefficient in each of the following regressions
# Look at a1:  compare with pacf(1)
lm(z[2:len]~z[1:(len-1)])
# Look at a2:  compare with pacf(2)
lm(z[3:len]~z[2:(len-1)]+z[1:(len-2)])
# Look at a3: compare with pacf(3)
lm(z[4:len]~z[3:(len-1)]+z[2:(len-2)]+z[1:(len-3)])




###################################################
### code chunk number 5: slides_part2.Rnw:499-505
###################################################
# R-code: MA(1) h-step forecast
h<-10
predict(x_obj,n.ahead=h)$pred
# Compare with estimated intercept
x_obj$coef



###################################################
### code chunk number 6: slides_part2.Rnw:522-542
###################################################
# R-code: MA(1) interval forecast
# Learn: plot interval forecast
sigma<-sqrt(x_obj$sigma2)
# Plot last ten data-points + forecast
last_data<-20
plot(y[(len+1-last_data):(len+1)],ylim=c(7,14))
lines(c(rep(NA,last_data-1),x[len],xhat),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],xhat-2*sigma),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],xhat+2*sigma),col="red",type="b")

# With the R-code: no (detectable) difference when compared to own calculations
h<-1
pred_obj<-predict(x_obj,n.ahead=h)
plot(y[(len+1-last_data):(len+1)],ylim=c(7,14))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")





###################################################
### code chunk number 7: slides_part2.Rnw:560-568
###################################################
# R-code: MA(1) multi-step interval forecast
# With the R-code
h<-10
pred_obj<-predict(x_obj,n.ahead=h)
plot(c(y[(len+1-last_data):(len+1)],rep(NA,h-1)),ylim=c(6,14))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")


###################################################
### code chunk number 8: init
###################################################
# R-code: simulation MA(2)

set.seed(10)
sigma<-2
b1<--1.3
b2<-0.5
len<-30
y_1<-arima.sim(n = len, list( ma = c(b1,b2)), sd = sigma)
set.seed(10)
len<-100
y_2<-arima.sim(n = len, list( ma = c(b1,b2)), sd = sigma)
set.seed(10)
len<-300
y_3<-arima.sim(n = len, list( ma = c(b1,b2)), sd = sigma)

# Theoretical acf (generally unknown...)
ARMAacf(ma=c(b1,b2),lag.max=10)

# Empirical acf: can always be computed from data
par(mfrow=c(3,1))
acf(y_1)
acf(y_2)
acf(y_3)

# Extract estimates from acf-object
acf(y_1)$acf
acf(y_2)$acf
acf(y_3)$acf



###################################################
### code chunk number 9: slides_part2.Rnw:657-690
###################################################
# R-code: MA(2) forecast
# mu
mu<-10
# Forecast horizon
h<-10
set.seed(10)
# sigma
sigma<-sqrt(2)
# MA coefficients
b1<--1.3
b2<-0.7
# Sample length
len<-100
# Generate data and shift by mu
y<-mu+arima.sim(n = len+h, list( ma = c(b1,b2)), sd = sigma)
# Data
x<-y[1:len]

ts.plot(x)
# Identification: Acf suggests AR(2)
acf(x)
# Estimation
x_obj<-arima(x,order=c(0,0,2))
x_obj
# Diagnostics
tsdiag(x_obj)

# Prediction
last_data<-10
pred_obj<-predict(x_obj,n.ahead=h)
plot(y[(len-last_data+1):(len+h)],ylim=c(4,16))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")


###################################################
### code chunk number 10: init
###################################################
# R-code: simulation AR(1)

set.seed(10)
sigma<-2
len<-100

# This is a non-stationary AR(1) process: a1>1
a1<-1.5
# This is a stationary AR(1) process
a1<-0.5
# arima.sim implicity assumes that c=0
y1<-arima.sim(n = len, list( ar = a1), sd = sigma)
ts.plot(y1)

# c!=0: Simulate AR(1) 'by hand'
set.seed(10)
eps<-rnorm(len)
c<-5
# Arbitrary zero-initialization
y1<-rep(0,len)
for (i in 2:len)
{
  y1[i]<-c+a1*y1[i-1]+eps[i]
}
# Arbitrary zero-initialization is not 'smart': would have been better to initialize with c/(1-a1)
ts.plot(y1)
abline(h=c/(1-a1))
# Check mean and expectation formula in slides
mean(y1)
c/(1-a1)
# Check autocorrelation: in contrast to MA(q) acf does not vanish (converges to 0 though)
rho<-a1^(1:10)
rho
# R-command for computing acf
ARMAacf(ar=a1,lag.max=10)
ARMAacf(ar=a1,lag.max=10,pacf=T)
# Acf converges to 0
acf(y1)
# pacf vanishes for k>1
acf(y1,type="partial")


# Different a1>0
set.seed(10)
a1<-0.95
y2<-arima.sim(n = len, list( ar = a1), sd = sigma)
# Longer 'memory'
ts.plot(y2)
abline(h=0)
rho<-a1^(1:10)
rho
ARMAacf(ar=a1,lag.max=10)
# Acf converges to 0: slower convergence than previous AR(1)
acf(y2)
# pacf vanishes for k>1
acf(y2,type="partial")


# Different a1<0
set.seed(10)
a1<--0.9
y3<-arima.sim(n = len, list( ar = a1), sd = sigma)
ts.plot(y3)
rho<-a1^(1:10)
rho
ARMAacf(ar=a1,lag.max=10)
par(mfrow=c(2,1))
# Acf converges to 0 alternating signs
acf(y3)
# pacf vanishes for k>1
acf(y3,type="partial")





###################################################
### code chunk number 11: slides_part2.Rnw:903-924
###################################################
# R-code: estimate $c,a_1$

set.seed(10)
sigma<-sqrt(2)
a1<-0.7
c<-5
len<-500
x<-arima.sim(n = len, list( ar = c(a1)), sd = sigma)
# Shift by mu=c/(1-a1)
x<-x+c/(1-a1)
ts.plot(x)

# Linear regression
lm_obj<-lm(x[2:len]~x[1:(len-1)])
lm_obj
# Linear regression estimates c

ts.plot(x)
# arima function
ma_obj<-arima(x,order = c(1, 0, 0))
ma_obj
# arima does not estimate c but mu
c/(1-a1)


###################################################
### code chunk number 12: slides_part2.Rnw:957-985
###################################################
# R-code: AR(1) diagnostics
# learn tsdiag
set.seed(10)
sigma<-sqrt(2)
a1<-0.7
len<-100
x<-arima.sim(n = len, list( ar = a1), sd = sigma)

# Identification
par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")

# Estimation
x_obj<-arima(x,order=c(1,0,0))
x_obj

# Diagnostics
tsdiag(x_obj,gof.lag=30)

# We can fit a more complex model: diagnostics also OK but danger of overfitting
# Rely on SIMPLEST model for which diagnostics are OK
x_obj<-arima(x,order=c(2,0,0))

acf(x_obj$res)

tsdiag(x_obj,gof.lag=20)



###################################################
### code chunk number 13: slides_part2.Rnw:1007-1054
###################################################
# R-code: AR(1) forecast
# learn: predict
set.seed(10)
sigma<-sqrt(2)
a1<-0.7
c<-3
len<-100
# Compute one additional observation i.e. len+1
y<-arima.sim(n = len+1, list( ar = a1), sd = sigma)
# Shift by mu
y<-y+c/(1-a1)
ts.plot(y)
# Data
x<-y[1:len]
# Future observation: must be forecasted
x_future<-y[len+1]
# Identification
par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")

# Estimation
x_obj<-arima(x,order=c(1,0,0))
x_obj

# Possible to fit a MA: but this would require more parameters: worse forecast performances
if (F)
{  
  x_obj<-arima(x,order=c(0,0,4))
  x_obj
  tsdiag(x_obj,gof.lag=30)
  
}

# Diagnostics
tsdiag(x_obj,gof.lag=30)

a1<-x_obj$coef["ar1"]
c<-x_obj$coef["intercept"]*(1-a1)

# One step ahead point forecast
# Formula in slides
xhat1<-c+a1*x[len]
xhat1

# Use R-command predict: replicates our calculation
predict(x_obj,n.ahead=1)$pred[1]

#--------------
# h-step ahead
h<-4
# Formula in slides
xhat<-c*sum(a1^(0:(h-1)))+a1^h*x[len]
xhat
# Use R-command predict
predict(x_obj,n.ahead=h)$pred[h]



###################################################
### code chunk number 14: slides_part2.Rnw:1073-1094
###################################################
# R-code: AR(1) interval forecast
# Learn: plot interval forecast
sigma<-sqrt(x_obj$sigma2)
# Plot last ten data-points + forecast
last_data<-10
par(mfrow=c(1,1))
plot(y[(len+1-last_data):(len+1)],ylim=c(7,14))
lines(c(rep(NA,last_data-1),x[len],xhat1),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],xhat1-2*sigma),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],xhat1+2*sigma),col="red",type="b")

# With the R-code
h<-1
pred_obj<-predict(x_obj,n.ahead=h)
plot(y[(len+1-last_data):(len+1)],ylim=c(7,14))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")





###################################################
### code chunk number 15: slides_part2.Rnw:1117-1125
###################################################
# R-code: AR(1) multi-step interval forecast
# With the R-code
h<-100
pred_obj<-predict(x_obj,n.ahead=h)
plot(c(y[(len+1-last_data):(len+1)],rep(NA,h-1)),ylim=c(5,15))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")


###################################################
### code chunk number 16: slides_part2.Rnw:1170-1214
###################################################
# R-code: AR(2)
# c
c<-10
# Forecast horizon
h<-10
set.seed(1)
# sigma
sigma<-sqrt(2)
# AR coefficients
a1<-1.3
a2<--0.7
# Mean: see slides
mu<-c/(1-a1-a2)
# Sample length
len<-100
# Generate data and shift by mu
y<-mu+arima.sim(n = len+h, list( ar = c(a1,a2)), sd = sigma)
ts.plot(y)

# Check stationarity: roots of characteristic polynomial should be smaller one in absolute value
abs(polyroot(c(-a2,-a1,1)))

# Data
x<-y[1:len]

ts.plot(x)
# Identification: pacf suggests AR(2)
par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")

# Estimation
x_obj<-arima(x,order=c(2,0,0))
x_obj

# Diagnostics
tsdiag(x_obj)

# Prediction
par(mfrow=c(1,1))
pred_obj<-predict(x_obj,n.ahead=h)
plot(y[(len-last_data+1):(len+h)],ylim=c(10,40))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")

#---------------------------------
# Examples of a non-stationary AR(2)

# Example 1
a1<-1.3
a2<--1.1
# Example 2: both coefficients smaller 1 (in absolute value) but process non-stationary
a1<-0.6
a2<-0.5
# Sample length
len<-100
# Generate data and shift by mu
y<-mu+arima.sim(n = len+h, list( ar = c(a1,a2)), sd = sigma)

# Check stationarity: roots of characteristic polynomial should be smaller one in absolute value
abs(polyroot(c(-a2,-a1,1)))


# c!=0: Simulate AR(1) 'by hand'
set.seed(10)
eps<-rnorm(len)
c<-5
# Arbitrary zero-initialization
y1<-rep(0,len)
for (i in 3:len)
{
  y1[i]<-c+a1*y1[i-1]+a2*y1[i-2]+eps[i]
}
# Arbitrary zero-initialization is not 'smart': would have been better to initialize with c/(1-a1)
ts.plot(y1)
abline(h=c/(1-a1))


