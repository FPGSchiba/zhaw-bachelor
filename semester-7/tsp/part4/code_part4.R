# R-code: random-walk inversion

# Generate three random walk series with different lengths: self-similarity (plots look roughly similar)
set.seed(10)
par(mfrow=c(3,1))
ts.plot(x1<-arima.sim(list(order = c(0,1,0)), n = 100),main="Random-Walk: length 100")
set.seed(10)
ts.plot(x2<-arima.sim(list(order = c(0,1,0)), n = 1000),main="Random-Walk: length 1000")
set.seed(10)
ts.plot(x3<-arima.sim(list(order = c(0,1,0)), n = 10000),main="Random-Walk: length 100'000")


# Plot first differences: stationary series, not self-similar anymore (plots look vastly different)
set.seed(10)
par(mfrow=c(3,1))
ts.plot(diff(x1),main="Diff-Random-Walk: length 100")
set.seed(10)
ts.plot(diff(x2),main="Diff-Random-Walk: length 1000")
set.seed(10)
ts.plot(diff(x3),main="Diff-Random-Walk: length 100'000")


# Random walk is just cumulated noise: both series below are identical (up to arbitrary initialization of arima.sim)
set.seed(3)
x<-arima.sim(list(order = c(0,1,0)),n=100)
# Is the same series as
set.seed(3)
y<-cumsum(rnorm(100)) 

# x starts with 0
head(x)
head(y)
tail(x)
tail(y)
# x starts with 0: longer time series
length(x)
length(y)


###################################################
### code chunk number 4: init
###################################################
# R-code: random-walk moments

# 1. Expectation and variance
# Expectation corresponds to initial value x0 and variance is a straight line increasing linearly with number of observations

# We perform a simulation to verify these claims
  
# Initial value at time point 0
x0<-100
# Compute 1000 realizations of length 100 each, starting at x0:  take mean across realizations and for each time point
anzsim<-1000
len<-100
mean_vec<-var_vec<-rep(0,len)
set.seed(45)

for (i in 1:anzsim)
{
# starts at x0
  x<-x0+arima.sim(list(order = c(0,1,0)),n=len-1) 
  mean_vec<-mean_vec+x
  var_vec<-var_vec+x^2
} 
# Compute mean across realizations and at each team-point
rw_mean<-mean_vec/anzsim
rw_var<-var_vec/anzsim-rw_mean^2
# Plot mean: lies around x0
ts.plot(rw_mean,ylim=c(0,max(rw_mean)))
abline(h=0)

# Should grow linearly to 100*sigma^2=100
ts.plot(rw_var,ylim=c(0,max(rw_mean)))
  
  
# 2. acf should be close to 1 at any lag  
  
set.seed(10)
len<-1000
# Random walk: ARIMA(0,1,0)
x<-arima.sim(list(order = c(0,1,0)), n = len)
y_1<-x
len_1<-len
# First differences
y_2<-diff(x)
len_2<-len-1


lags<-30

aucf<-matrix(ncol=2,nrow=lags)

aucf[,1]<-as.double(acf(y_1,plot=F,lag.max=lags-1)$acf)
aucf[,2]<-as.double(acf(y_2,plot=F,lag.max=lags-1)$acf)

colnames(aucf)<-c("acf RW","acf diff RW")

head(aucf)

par(mfrow=c(2,1))
ts.plot(x,main="Random-Walk ARIMA(0,1,0)")
lines(c(0,diff(x)),col="blue")
mtext("Random-walk", side = 3, line = -1,at=len/2,col="black")
mtext("Differences", side = 3, line = -2,at=len/2,col="blue")
plot(aucf[,1],xlab="",ylab="",ylim=c(min(aucf[,2]),max(aucf[,2])),type="l",axes="F",main="Acf")
lines(aucf[,2],col="blue")
mtext("Acf random-walk", side = 3, line = -1,at=15,col="black")
mtext("Acf differences", side = 3, line = -2,at=15,col="blue")
axis(1,at=1:length(aucf[,1]),labels=-1+1:length(aucf[,1]))
axis(2)
box()





###################################################
### code chunk number 5: init
###################################################
# R-code: random-walk forecasts


set.seed(10)
len<-1000
#Forecast horizon
h<-20
# Random walk: ARIMA(0,1,0): use len-1 because first data point is zero by default
x<-arima.sim(list(order = c(0,1,0)), n = len-1)

rw.obj<-arima(x,order=c(0,1,0))

pred<-predict(rw.obj,n.ahead=h)

last_points<-20
ts.plot(c(x[(len-last_points):len],rep(NA,h)),ylim=c(min(pred$pred-2*pred$se),max(pred$pred+2*pred$se)))
lines(c(rep(NA,last_points),pred$pred))
lines(c(rep(NA,last_points),pred$pred-2*pred$se))
lines(c(rep(NA,last_points),pred$pred+2*pred$se))







###################################################
### code chunk number 6: init
###################################################
# R-code: ARIMA d=1

# Example 1: ARIMA(0,1,1): as b1 approaches -1 the realization appears less 'non-stationary'
#   For b1=-1 the unit-root cancels i.e. the process is white noise
#   ARIMA(0,1,1)-model is interesting for fitting series 'in between' stationarity/non-stationarity
set.seed(10)
# Detect non-stationarity of first process (unit-root almost cancelled by MA(1)...)
len<-300
b_arima1<--0.99
b_arima2<-0.9
y_1<-arima.sim(list(order = c(0,1,1),ma=b_arima1), n = len)
y_2<-arima.sim(list(order = c(0,1,1),ma=b_arima2), n = len)
len_1<-len
len_2<-len
ts.plot(y_2,main="ARIMA(0,1,1)",ylab="",xlab="",col="red",ylim=c(min(min(y_1),min(y_2)),max(max(y_1),max(y_2))))
lines(y_1,col="blue")
mtext(paste("b_1=",b_arima1,sep=""), side = 3, line = -1,at=len/2,col="blue")
mtext(paste("b_1=",b_arima2,sep=""), side = 3, line = -2,at=len/2,col="red")


# Nearly stationary processes, very long samples
set.seed(10)
# Detect non-stationarity of first process (unit-root almost cancelled by MA(1)...)
len<-100000
b_arima1<--0.99
b_arima2<--0.90
y_1<-arima.sim(list(order = c(0,1,1),ma=b_arima1), n = len)
y_2<-arima.sim(list(order = c(0,1,1),ma=b_arima2), n = len)
len_1<-len
len_2<-len
ts.plot(y_2,main="ARIMA(0,1,1)",ylab="",xlab="",col="red",ylim=c(min(min(y_1),min(y_2)),max(max(y_1),max(y_2))))
lines(y_1,col="blue")
mtext(paste("b_1=",b_arima1,sep=""), side = 3, line = -1,at=len/2,col="blue")
mtext(paste("b_1=",b_arima2,sep=""), side = 3, line = -2,at=len/2,col="red")


#----------------
# Example 2: ARIMA(2,1,0)
# We can work with data in levels or in first differences: the following example illustrates both cases
# Generate Data
set.seed(10)
sigma<-1
len<-100
a_1<-1.8
a_2<--0.9
a_vec<-c(a_1,a_2)
x<-arima.sim(n = len, list(order = c(2,1,0), ar = a_vec), sd = sigma)

par(mfrow=c(2,1))
ts.plot(x,xlab="",ylab="",main="Non-stationary ARIMA(2,1,0)")
ts.plot(diff(x),xlab="",ylab="",main="Stationary AR(2) differences")



# Working with original data: d=1
x_obj<-arima(x,order=c(2,1,0))
tsdiag(x_obj)

# Forecast of non-stationary series does not revert to mean; width of interval increases unboundedly (square-root function)
par(mfrow=c(1,1))
h<-100
ymin<-min(predict(x_obj,n.ahead=h)$pred-2*predict(x_obj,n.ahead=h)$se)
ymax<-max(predict(x_obj,n.ahead=h)$pred+2*predict(x_obj,n.ahead=h)$se)
ts.plot(c(x,rep(NA,h)),xlab="",ylab="",
main="ARIMA(2,1,0): multi steps ahead interval forecast ",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred-2*predict(x_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred+2*predict(x_obj,n.ahead=h)$se),
col="blue",lty=2)

# Same as above but working with first differences
# Forecast of differenced stationary series reverts to mean; width of interval converges (remains bounded)
y<-diff(x)
# Here d=0
y_obj<-arima(y,order=c(2,0,0),include.mean=F)
ymin<-min(predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se)
ymax<-max(predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se)
ts.plot(c(y,rep(NA,h)),xlab="",ylab="",
main="AR(2): multi-step ahead interval forecast ",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se),
col="blue",lty=2)



##########################################
# R-code: ARIMA d=2
# Example 1: simple (0,2,0) process: no parameters required for estimation
# Path of I(2) process appears very smooth (because of summation)
#   After differences (first and second order) the paths appear noisier
#   After second order differences the data lies about a fixed mean (mean-reversion: stationarity)
set.seed(10)
len<-1000
y_1<-arima.sim(list(order = c(0,2,0)), n = len)
len_1<-len
y_2<-diff(y_1)
len_2<-len-1
y_3<-diff(y_2)
len_3<-len_2-1
par(mfrow=c(2,1))
ts.plot(y_1,main="Integrated Random-Walk: ARIMA(0,2,0)",ylab="",xlab="")
ts.plot(y_2,main="First and second order differences of ARIMA(0,2,0)",
col="blue",ylab="",xlab="")
lines(c(0,y_3),col="red")
mtext("First differences", side = 3, line = -1,at=len/2,col="blue")
mtext("Second differences", side = 3, line = -2,at=len/2,col="red")

# Example 2 forecasting
# Simple I(1)- and I(2)-series (without drift)
#   I(1): forecast has no trend; does not converge to 'mean'; interval increases at square-root rate 
#   I(2): forecast has a drift; width of forecast interval increases rapidly (high uncertainty)
#         In general economic data is not I(2) (uncertainty is less pronounced)

set.seed(10)
len<-100
# I(1): must be differenced once
x<-arima.sim(list(order = c(0,1,0)), n = len)
# I(2): must be differenced twice
z<-arima.sim(list(order = c(0,2,0)), n = len)
x_obj<-arima(x,order=c(0,1,0),include.mean=F)
z_obj<-arima(z,order=c(0,2,0),include.mean=F)
par(mfrow=c(2,1))
# random walk
ymin<-min(predict(x_obj,n.ahead=h)$pred-2*predict(x_obj,n.ahead=h)$se)
ymax<-max(predict(x_obj,n.ahead=h)$pred+2*predict(x_obj,n.ahead=h)$se)
ts.plot(c(x,rep(NA,h)),xlab="",ylab="",
main="ARIMA(0,1,0): multi steps ahead interval forecast ",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred-2*predict(x_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred+2*predict(x_obj,n.ahead=h)$se),
col="blue",lty=2)
# Integrated random-walk
ymin<-min(c(z,predict(z_obj,n.ahead=h)$pred-2*predict(z_obj,n.ahead=h)$se))
ymax<-max(c(z,predict(z_obj,n.ahead=h)$pred+2*predict(z_obj,n.ahead=h)$se))
ts.plot(c(z,rep(NA,h)),xlab="",ylab="",
main="ARIMA(0,2,0): multi steps ahead interval forecast ",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(z)),predict(z_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(z)),predict(z_obj,n.ahead=h)$pred-2*predict(z_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(z)),predict(z_obj,n.ahead=h)$pred+2*predict(z_obj,n.ahead=h)$se),
col="blue",lty=2)







###################################################
### code chunk number 8: init
###################################################

# R code: integrate forecasts
# We rely on same example 2 above: ARIMA(2,1,0)
# We here show how the forecasts of the original (non-stationary) data can be obtained from the forecasts of the differenced (stationary) data

# Generate Data
set.seed(10)
sigma<-1
len<-100
a_1<-1.8
a_2<--0.9
a_vec<-c(a_1,a_2)
x<-arima.sim(n = len, list(order = c(2,1,0), ar = a_vec), sd = sigma)

par(mfrow=c(2,1))
ts.plot(x,xlab="",ylab="",main="Non-stationary ARIMA(2,1,0)")
ts.plot(diff(x),xlab="",ylab="",main="Stationary AR(2) differences")



# Working with original data: d=1
x_obj<-arima(x,order=c(2,1,0))
tsdiag(x_obj)

# Forecast of non-stationary series does not revert to mean; width of interval increases unboundedly (square-root function)
par(mfrow=c(1,1))
h<-100
ymin<-min(predict(x_obj,n.ahead=h)$pred-2*predict(x_obj,n.ahead=h)$se)
ymax<-max(predict(x_obj,n.ahead=h)$pred+2*predict(x_obj,n.ahead=h)$se)
ts.plot(c(x,rep(NA,h)),xlab="",ylab="",
main="ARIMA(2,1,0): multi steps ahead interval forecast ",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred-2*predict(x_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(x)),predict(x_obj,n.ahead=h)$pred+2*predict(x_obj,n.ahead=h)$se),
col="blue",lty=2)

# Same as above but working with first differences
# The secon (bottom) plot shows the 'integrated' point forecast obtained by summing-up forecasts of the differenced (stationary) series  
y<-diff(x)
# Here d=0
y_obj<-arima(y,order=c(2,0,0),include.mean=F)
par(mfrow=c(2,1))
ymin<-min(predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se)
ymax<-max(predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se)
ts.plot(c(y,rep(NA,h)),xlab="",ylab="",
main="AR(2): multi-step ahead interval forecast ",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred),col="blue")
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred-2*predict(y_obj,n.ahead=h)$se),
col="blue",lty=2)
lines(c(rep(NA,length(y)),predict(y_obj,n.ahead=h)$pred+2*predict(y_obj,n.ahead=h)$se),
col="blue",lty=2)

# Integrate forecasts manually
ymin<-min(c(x,x[length(x)]+cumsum(predict(y_obj,n.ahead=h)$pred)))
ymax<-max(c(x,x[length(x)]+cumsum(predict(y_obj,n.ahead=h)$pred)))
ts.plot(c(x,rep(NA,h)),xlab="",ylab="",main="Cusum of AR(2) forecasts",
ylim=c(ymin,ymax))
lines(c(rep(NA,length(x)),x[length(x)]+cumsum(predict(y_obj,n.ahead=h)$pred)),col="blue")


