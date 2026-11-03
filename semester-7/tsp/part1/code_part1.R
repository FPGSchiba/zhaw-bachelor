
###################################################
### code chunk number 1: init
###################################################
# R-code: Gaussian white noise
# Introduce rnorm, set.seed, ts.plot
len<-100
# Same set.seed, variance 1
set.seed(1)
eps<-rnorm(len)
set.seed(1)
eps1<-rnorm(len,mean=1,sd=1)
mat<-cbind(eps,eps1)
ts.plot(mat)

# Same set.seed but variance 4
set.seed(1)
sigma<-2
eps<-sigma*rnorm(len)
set.seed(1)
eps1<-rnorm(len,mean=0,sd=2)
mat<-cbind(eps,eps1)
# Compare scale with previous plot
ts.plot(mat)


#  set.seed used once only and variance 2
set.seed(1)
sigma<-sqrt(2)
eps<-sigma*rnorm(len)
eps1<-rnorm(len,mean=0,sd=sigma)
mat<-cbind(eps,eps1)
# Compare scale with previous plot
ts.plot(mat,col=rainbow(ncol(mat)))




###################################################
### code chunk number 2: init
###################################################
# R-code: Dependence structure
# Introduce acf
len<-100
set.seed(1)
eps<-rnorm(len)

acf(eps,plot=F)
acf(eps)
acf(eps,lag.max=10)

# Longer series
len<-10000
set.seed(1)
eps<-rnorm(len)

acf(eps,lag.max=20)



###################################################
### code chunk number 3: init
###################################################

# R-code: acf
# We here apply the acf-formula in slides and check that they correspond to the R-command acf()
set.seed(10)
len_1<-10
y_1<-rnorm(len_1)
len_2<-100
y_2<-rnorm(len_2)
len_3<-1000
y_3<-rnorm(len_3)


# acf according to formula in slides: first column=first series, second column=second series, third column=third series
# Compute acf for lags 0,1,...,9
aucf<-matrix(ncol=3,nrow=10)
for (i in 0:9)
{
  aucf[i+1,1]<-(y_1[(1+i):len_1]-mean(y_1))%*%(y_1[1:(len_1-i)]-mean(y_1))/
  sum((y_1[1:len_1]-mean(y_1))^2)
  aucf[i+1,2]<-(y_2[(1+i):len_2]-mean(y_2))%*%(y_2[1:(len_2-i)]-mean(y_2))/
  sum((y_2[1:len_2]-mean(y_2))^2)
  aucf[i+1,3]<-(y_3[(1+i):len_3]-mean(y_3))%*%(y_3[1:(len_3-i)]-mean(y_3))/
  sum((y_3[1:len_3]-mean(y_3))^2)
}

# acf according to formula in slides: first column=first series, second column=second series, third column=third series
# Lags 0,1,...,9
aucf


# Plot acf with 95% confidence intervals based on +/- 1.96/sqrt{T}
par(mfrow=c(3,1))
plot(aucf[,1],col="blue",main=paste("Sample length=",len_1,sep=""),
     xlab="",ylab="",ylim=c(min(aucf[,1]-1.96/sqrt(len_1)),
                            max(aucf[,1]+1.96/sqrt(len_1))),type="l",axes="F")
lines(rep(0,len_1)-1.96/sqrt(len_1),lty=2,col="blue")
lines(rep(0,len_1)+1.96/sqrt(len_1),lty=2,col="blue")
lines(rep(0,len_1))
axis(1,at=1:length(aucf[,1]),labels=-1+1:length(aucf[,1]))
axis(2)
box()

# Second series
plot(aucf[,2],col="blue",main=paste("Sample length=",len_2,sep=""),
     xlab="",ylab="",ylim=c(min(aucf[,2]-1.96/sqrt(len_2)),
                            max(aucf[,2]+1.96/sqrt(len_2))),type="l",axes="F")
lines(rep(0,len_2)-1.96/sqrt(len_2),lty=2,col="blue")
lines(rep(0,len_2)+1.96/sqrt(len_2),lty=2,col="blue")
lines(rep(0,len_2))
axis(1,at=1:length(aucf[,2]),labels=-1+1:length(aucf[,2]))
axis(2)
box()

# Third series
plot(aucf[,3],col="blue",main=paste("Sample length=",len_3,sep=""),
     xlab="",ylab="",ylim=c(min(aucf[,3]-1.96/sqrt(len_3)),
                            max(aucf[,3]+1.96/sqrt(len_3))),type="l",axes="F")
lines(rep(0,len_3)-1.96/sqrt(len_3),lty=2,col="blue")
lines(rep(0,len_3)+1.96/sqrt(len_3),lty=2,col="blue")
lines(rep(0,len_3))
axis(1,at=1:length(aucf[,3]),labels=-1+1:length(aucf[,3]))
axis(2)
box()



# Compare numerical values: formula in slides vs. R-function acf()
acf(y_1,plot=F,lag.max=9)
round(aucf[,1],3)
# sample length 100
acf(y_2,plot=F,lag.max=9)
round(aucf[,2],3)
# sample length 1000
acf(y_3,plot=F,lag.max=9)
round(aucf[,3],3)


# Compare plots
# From now on we will work with R-function acf()
par(mfrow=c(2,1))
plot(aucf[,2],col="blue",main=paste("Sample length=",len_2,sep=""),
     xlab="",ylab="",ylim=c(min(aucf[,2]-1.96/sqrt(len_2)),
                            max(aucf[,2]+1.96/sqrt(len_2))),type="l",axes="F")
lines(rep(0,len_2)-1.96/sqrt(len_2),lty=2,col="blue")
lines(rep(0,len_2)+1.96/sqrt(len_2),lty=2,col="blue")
lines(rep(0,len_2))
axis(1,at=1:length(aucf[,2]),labels=-1+1:length(aucf[,2]))
axis(2)
box()
acf(y_2,lag.max=9)


###################################################
### code chunk number 4: init
###################################################
# R-code: partial acf (pacf)

# Note: pacf starts at lag 1 (in contrast to above acf which starts at lag 0)
acf(y_1,lag.max=9,type="partial")
# sample length 100
acf(y_2,type="partial",lag.max=9)
# sample length 1000
acf(y_3,type="partial",lag.max=9)



###################################################
### code chunk number 5: init
###################################################
# R-code: Forecasting white noise
len<-101
# Point forecast: try 0, 2 and -2
epshat<-2
epshat<-0.0
# Mean-square forecast error
mse<-0
# Number simulations
anzsim<-100
plot_T<-T
set.seed(1)
# The best point forecast epshat=0 is neither too high nor too low; just right in the middle
for (i in 1:anzsim)
{  
  eps<-rnorm(len)
  mse<-mse+(epshat-eps[len])^2
  if (plot_T)
  {
    mat<-cbind(eps,c(rep(NA,len-1),epshat))
    colnames(mat)<-c("Series","Forecast")
    plot(eps,type="l",col="black")
    lines(c(rep(NA,len-1),epshat),type="b",col="blue")
    abline(v=len-1)    
  }
}
# epshat=0 minimizes mse: OPTIMALITY
mse/anzsim



###################################################
### code chunk number 6: init
###################################################
# R-code: Forecast error and interval forecast
len<-101
anzsim<-100
# The best point forecast epshat=0 is neither too high nor too low; just right in the middle
# The variable number_outside counts the number of future observations outside the forecast interval
number_outside<-0
sigma<-1
# Set plot_T<-T to see 95% forecast interval
plot_T<-T
# Point forecast: ideal forecast is 0 (in this case 5% future observations lie outside 95% forecast interval)
# For any epshat!=0 the number of future observations outside the interval is larger than 5%
epshat<-0
set.seed(1)
for (i in 1:anzsim)
{  
  eps<-sigma*rnorm(len)
# If future epsilon outside interval: add 1 to number_outside  
  if (eps[len]>epshat+1.96*sigma | eps[len]<epshat-1.96*sigma)
    number_outside<-number_outside+1
# Plot of interval  
  if (plot_T)
  { 
    mat<-cbind(eps,c(rep(NA,len-1),epshat))
    colnames(mat)<-c("Series","Forecast")
    plot(eps,type="l",col="black",ylim=c(-4,4))
    lines(c(rep(NA,len-1),epshat+1.96*sigma),type="b",col="blue")
    lines(c(rep(NA,len-1),epshat-1.96*sigma),type="b",col="blue")
    abline(v=len-1) 
  }
}
number_outside/anzsim


###################################################
### code chunk number 7: init
###################################################
# R-code: MA(1)
# Try various settings for mu, sigma and b1: have a look at acf and pacf 
len<-100
eps<-rnorm(len)
sigma<-1
mu<-0
b1<--0.9
mu<-10
b1<-0.5
set.seed(1)
# MA(1)
x<-mu+eps[2:len]+b1*eps[1:(len-1)]

ts.plot(x)

# Non-vanishing dependence structure
par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")

# Forecast MA(1): basic centering (we will learn how to improve upon that simple forecast rule)
len<-101
anzsim<-10000
# xhat=0 is nomore the best point forecast: if x_T is 'larger' (or smaller) than zero, then x_{T+1} tends to be larger (or smaller) than zero too
number_outside<-0
plot_T<-F
set.seed(1)
for (i in 1:anzsim)
{  
  eps<-rnorm(len)
# Generate  MA(1): will be of length len-1
  x<-mu+eps[2:(len)]+b1*eps[1:(len-1)]
# Point forecast: center at mu (otherwise forecast systematically too large or too small: biased) 
  xhat<-mu
  if (x[length(x)]>xhat+1.96*sigma | x[length(x)]<xhat-1.96*sigma)
    number_outside<-number_outside+1
  if (plot_T)
  { 
# x is shorter  
    mat<-cbind(x,c(rep(NA,len-2),xhat))
    colnames(mat)<-c("Series","Forecast")
    plot(x,type="l",col="black",ylim=c(-4,4))
    lines(c(rep(NA,len-2),xhat+1.96*sigma),type="b",col="blue")
    lines(c(rep(NA,len-2),xhat-1.96*sigma),type="b",col="blue")
    abline(v=len-2) 
    abline(h=0)
  }
}
# There are generally substantially more than 5% observations outside the interval mu\pm 2*sigma (width is too small)
# But mu is still the best constant for predicting x
number_outside/anzsim



###################################################
### code chunk number 8: init
###################################################
# R-code: stationarity
# The following three series are non-stationary because the mean (mu) is changing over time
set.seed(10)
len<-100
mu_1<-1:len/(len/4)
# linear trend
y_1<-mu_1+rnorm(len)
# cyclical component
mu_2<-cos(pi/12*(1:len))
y_2<-mu_2+rnorm(len)
# deterministic shift
mu_3<-c(rep(0,len/2),rep(1,len-len/2))
y_3<-mu_3+rnorm(len)

par(mfrow=c(3,1))
ts.plot(y_1,col="blue",main="Linear trend")
lines(mu_1,col="black")
ts.plot(y_2,col="blue",main="Cycle")
lines(mu_2,col="black")
ts.plot(y_3,col="blue",main="Shift")
lines(mu_3,col="black")


# The following two series are stationary: fixed mean (mu)
set.seed(10)
len<-100
# White noise
y_1<-rnorm(len)
# cyclical AR(2)
eps<-rnorm(1000)
x<-rep(0,1000)
a1<-2*cos(pi/6)*0.95
a2<--0.95^2
for (i in 3:1000)
  x[i]<-a1*x[i-1]+a2*x[i-2]+eps[i]
y_3<-x[(1000-len+1):1000]


par(mfrow=c(2,1))
ts.plot(y_1,col="blue",main="Zero-mean white noise")
lines(rep(0,len),col="black")
ts.plot(y_3,col="blue",main="Zero-mean stationary (stochastic) cycle")
lines(rep(0,len),col="black")





#----------------------------------------------
# The following two series are non-stationary because the variance is changing over time
set.seed(10)
# Try len<-1000 or len<-100
len<-1000
len<-100
mu_2<-rep(0,len)
# stationary level but inflating variance
y_2<-mu_1+sqrt(1:len)*rnorm(len)
# non-stationary level and variance
mu_3<-1:len/(len/2)
y_3<-mu_3+sqrt(mu_3)*rnorm(len)

par(mfrow=c(2,1))
ts.plot(y_2,col="blue",main="Constant level, inflating variance")
lines(mu_2,col="black")
ts.plot(y_3,col="blue",main="Variance proportional to level")
lines(mu_3,col="black")



#------------------------------------------------------
# The following example compares a stationary series with a non-stationary, whereby 
#   the dependence structure (autocovariance) of the latter is changing over time
set.seed(100)
len<-100
# fixed AR(1)
a1<-0.9
# Time-varying AR(1)-parameter
a1t<-0.9*cos(2*pi*(1:len)/len+pi/2)
y_1<-y_2<-rep(0,len)
eps<-rnorm(len)
# fixed coefficient and time varying AR(1)
for (i in 2:len) #i<-2
{
	y_1[i]<-a1*y_1[i-1]+eps[i]
	y_2[i]<-a1t[i]*y_2[i-1]+eps[i]
}

par(mfrow=c(2,1))
ts.plot(y_1,col="blue",main="Fixed (stationary) dependency")
abline(h=0)
ts.plot(y_2,col="blue",main="Changing dependency")
abline(h=0)

###################################################
### code chunk number 9: init
###################################################
# R-code: log-returns

reload_data<-F

if (reload_data)
{
# Download data (Apple) from Yahoo finance
  library(quantmod)
  library(xts)

  getSymbols("AAPL")
  head(AAPL,n=3)
  tail(AAPL,n=3)
  price_s<- Cl(AAPL)   #Close Price
  save(price_s,file=paste(getwd(),"/Data/AAPL",sep="")) 
} else
{
  load(file=paste(getwd(),"/Data/AAPL",sep=""))
}
library(xts)

# Series is non-stationary: level (mu) is changing and variance is changing too
plot(price_s)
# Differences stabilize the level: mu is fixed
plot(diff(price_s))
# The logarithm stabilizes the variance:  R(0) (i.e. the variance) is fixed
plot(log(price_s))
# Log-returns: fixes mu and to some extent R(0) (vola-clusters remain: crises, time episodes of higher uncertainty)
rt<-diff(log(price_s))
plot(rt)


