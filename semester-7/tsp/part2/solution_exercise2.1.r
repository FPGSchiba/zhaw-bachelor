
# Exercise 1

# Simulation MA(1)- and MA(5)-Processes
set.seed(71)
len<-100

# First possibility: simulate explicitly with lagged data

eps<-rnorm(len)
x<-eps[2:len]-0.7*eps[1:(len-1)]
y<-eps[6:len]+0.5*eps[1:(len-5)]
par(mfrow=c(2,1))
ts.plot(x,lty=1:2)
ts.plot(y,lty=1:2)
mean(y)
acf(x)
acf(y)


set.seed(71)
# Second possibility: rely on arima.sim
x<-arima.sim(list(ma=-0.7),n=len)
y<-arima.sim(list(ma=c(rep(0,4),0.5)),n=len,sd=1)

# Very difficult to detect dependence by eyeballing the series: acf is informative about dependence structure
par(mfrow=c(2,1))
ts.plot(x,lty=1:2)
ts.plot(y,lty=1:2)
mean(y)
acf(x)
acf(y)

# acf is normalized: does not depend on scaling i.e. sigma


# True acf
ARMAacf( ma = -0.7, lag.max = 10, pacf = FALSE)
####
acf(x,plot=F)
# Check with formula from script for acf(1)
acf_1<--0.7/(1+0.7^2)
acf_1
ARMAacf( ma = c(0,0,0,0,0.7), lag.max = 10, pacf = FALSE)
####
acf(y,plot=F)



# True expectations are zero (mu=0)
mean(x)
mean(y)


#------------------------------------------
# Exercises 2&3

# True processes are revealed at the end of the script file: your guess can differ from true process because data sets are of limited sizes

# Read the data: ma50 is exercise 2, ma300 is exercise 3

ma50<-read.table(paste(getwd(),"/Data/ma50.txt",sep=""))
ma300<-read.table(paste(getwd(),"/Data/ma300.txt",sep=""))

ts.plot(ma50,lty=1:4)

# select any series from either data-sample
x<-ma50[,4]
x<-ma300[,4]

# Compute acf&pacf (acf determines hypothetical model order; pacf will be useful for AR-processes)
par(mfrow=c(2,2))
ts.plot(x)
acf(x)
acf(x,type="partial")

# Select order
maorder<-4
# estimate parameters
x_obj<-arima(x,order=c(0,0,maorder))
# check diagnostics
tsdiag(x_obj,gof.lag=20)

#_________________________________________________________________________________________________________________________________
# Estimation


estim<-function(parma,x)
{
  # Center the data
  x<-x-mean(x)
  # Determine length
  len<-length(x)
  # Define q
  q<-length(parma)
  b<-parma
  # Define a vector of epsilon's
  epsilon<-x
  # Compute epsilon_1
  epsilon[1]<-x[1]
  for (i in 2:q)
  {
    epsilon[i]<-x[i]-epsilon[(i-1):1]%*%b[1:(i-1)]
  }
  for (i in (q+1):len)
  {
    epsilon[i]<-x[i]-epsilon[(i-1):(i-q)]%*%b[1:q]
  }
  return(sum(epsilon^2))
}


# initialization: white noise
maorder<-3

parma<-rep(0,maorder)
estim_obj<-nlminb(parma,estim,x=x)
round(estim_obj$par,4)

x_obj<-arima(x,order=c(0,0,maorder))

x_obj$coef

# Note that arima estimates the intercept too whereas we estimate the MA-parameters only: therefore
# both estimates will generally differ.
# We check that the differences are within the confidence interval of the estimates

abs(estim_obj$par-x_obj$coef[1])<1.96*sqrt(diag(x_obj$var.coef)[1])

####
acf(x_obj$residuals)

tsdiag(x_obj,gof.lag=50)


#--------------------------------------------------------------------------
# True processes of exercise 2
len<-300
len1<-len
# MA(1)
set.seed(1371)
model<-list(order=c(0,0,1),ma=0.5)
x1<-arima.sim(model,n=len1)+15.

tsplot(x1)
#acf(x1)
#acf(x1,type="partial")



# MA(3)
set.seed(1371)
model<-list(order=c(0,0,3),ma=c(0.5,0.8,0.9))
x2<-arima.sim(model,n=len1)

tsplot(x2)
#acf(x2)
#acf(x2,type="partial")


# MA(2)
set.seed(171)
model<-list(order=c(0,0,2),ma=c(-0.9,-0.9))
x3<-arima.sim(model,n=len1)+15.

tsplot(x3)
#acf(x3)
#acf(x3,type="partial")



# MA(6)
set.seed(1371)
model<-list(order=c(0,0,6),ma=c(0,0,0,-1.5,0,0.8))
x4<-arima.sim(model,n=len1)+15.

# Identifikation mit R:
#ma50: ma(1), ma(1), ma(2),  ma(4)
# ma300: ma(1), ma(3), ma(2), ma(4) oder ma(6)


