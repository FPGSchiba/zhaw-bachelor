### R code from vignette source 'C:/Users/marca/OneDrive/2023/teaching_unterricht/Time Series Prediction (TSP)/Slides/Rnw/slides_part3'

###################################################
### code chunk number 1: init
###################################################

#-----------------------------------------------------------------
# Source estimation routine
#source(paste(path.pgm,"examples.r",sep=""))


###################################################
### code chunk number 2: init
###################################################
# R-code: simulation ARMA(1,1)

set.seed(10)
sigma<-2
a1<-0.8
b1<-0.9
set.seed(10)
len<-300
y<-arima.sim(n = len, list( ar=a1,ma = b1), sd = sigma)
ts.plot(y)

# acf does not vanish
ARMAacf(ma=b1,ar=a1,lag.max=100)
# pacf does not vanish either
ARMAacf(ma=b1,ar=a1,lag.max=100,pacf=T)

# Neither acf nor pacf vanish: cannot be used to infer model orders p,q (identification)
acf(y)
acf(y)$acf
acf(y,type="partial")





###################################################
### code chunk number 3: slides_part3.Rnw:204-214
###################################################
# R-code: estimate $a_1b_1$

len<-1000
set.seed(10)
sigma<-sqrt(2)
a1<-0.6
b1<-0.5
x<-arima.sim(n = len, list( ar=a1,ma = b1), sd = sigma)
ts.plot(x)
arma_obj<-arima(x,order = c(1, 0, 1))
arma_obj


###################################################
### code chunk number 4: init
###################################################
# R-code: parsimony

set.seed(10)
sigma<-2
a1<-0.8
b1<-0.9
set.seed(10)
len<-300
y<-arima.sim(n = len, list( ar=a1,ma = b1), sd = sigma)
ts.plot(y)

# Try pure MA
acf(y)
# q=6 is not large enough: need q>=7 for OK-diagnostics
# ma7 is still significant 
x_obj<-arima(y,order=c(0,0,7))
x_obj
# Diagnostics
tsdiag(x_obj)

# Try pure AR
# p=5 is not large enough: need p>=6 for OK-diagnostics
# ar6 is still significant 

acf(y,type="partial")
x_obj<-arima(y,order=c(6,0,0))
x_obj
# Diagnostics
tsdiag(x_obj)


# ARMA(1,1)
x_obj<-arima(y,order=c(1,0,1))
x_obj
# Diagnostics
tsdiag(x_obj)



###################################################
### code chunk number 5: slides_part3.Rnw:287-315
###################################################
# R-code: ARMA(1,1) forecast
set.seed(10)
sigma<-sqrt(2)
c<-4
a1<-0.3
b1<-0.7
len<-1000
# Forecast horizon
h<-10

# Compute one additional observation i.e. len+1
y<-arima.sim(n = len+h, list( ar=a1,ma = b1), sd = sigma)
y<-y+c/(1-a1)
ts.plot(y)
# Data
x<-y[1:len]
# Future observation: must be forecasted
x_future<-y[(len+1):(len+h)]
# Estimation
x_obj<-arima(x,order=c(1,0,1))
x_obj
# Diagnostics
tsdiag(x_obj,gof.lag=30)

# Forecasting
h<-10
pred_obj<-predict(x_obj,n.ahead=h)

last_data<-10
plot(y[(len+1-last_data):(len+h)],ylim=c(0,10))
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred),col="blue",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred-2*pred_obj$se),col="red",type="b")
lines(c(rep(NA,last_data-1),x[len],pred_obj$pred+2*pred_obj$se),col="red",type="b")


###################################################
### code chunk number 6: slides_part3.Rnw:578-768
###################################################
# R-code: information criteria
# We simulate an AR(2) and apply information criteria (AIC, BIC)
# Specifically we look for best AR, best MA and best ARMA-models for the AR(2)
# Ideally, the information criteria select the true model orders p=2, q=0
# Let's see...
# 1. Generate data
set.seed(11)
len<-100
sigma<-sqrt(3)
a_1<-1.7
a_2<--0.8
c<-10
mu<-c/(1-a_1-a_2)
y<-mu+arima.sim(n = len, list( ar = c(a_1,a_2)), sd = sigma)
ts.plot(y)
acf(y,type="partial")

# 2. Compute residual error variance for AR(p)-models with p=0,...,10

maxorder<-10
sigma_k<-rep(0,maxorder+1)
# Order zero
sigma_k[1]<-var(y)
# Orders 1,2,...,maxorder
for (k in 1:maxorder)         #k<-20
{
# Fit AR(k)  
  AR_obj<-arima(y,order=c(k,0,0))
# Extract sigma^2  
  sigma_k[k+1]<-mean(AR_obj$res^2)
# This is the same as
  sigma_k[k+1]<-AR_obj$sigma2
  sigma_k[k+1]<-AR_obj$sigma
  print(paste("AR-Order=",k,"  AIC=",AR_obj$aic,sep=""))
}

# 3. Plot sigma^2 as a function of increasing model order p: sigma^2 should decrease with increasing p (this is called overfitting)
par(mfrow=c(2,1))
anf<-1
plot((sigma_k)[anf:(maxorder+1)],col="blue",xlab="AR-order",ylab="",
main="Sample mean-square error of AR(2)",type="l",axes="F")
axis(1,at=anf:(maxorder+1),labels=-1+anf:(maxorder+1))
axis(2)
box()
anf<-3
plot((sigma_k)[anf:(maxorder+1)],col="blue",xlab="AR-order",ylab="",
main="Same as above for orders=2,3,...,10 (larger or equal than true order 2)",type="l",axes="F")
axis(1,at=1:(maxorder-anf+2),labels=-1+anf:(maxorder+1))
axis(2)
box()



# 4. Compute AIC and plot: AIC is minimal at p=3 (true model is p=2)
log_sigma_k<-log(sigma_k)
par(mfrow=c(2,1))
anf<-1
aic<-(log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder+1)]
plot((log_sigma_k)[anf:(maxorder+1)],col="blue",xlab="AR-order",ylab="",
main="log sample MSE and AIC for AR(2)",type="l",axes="F")
lines(aic,col="red")
mtext("log sample MSE", side = 3, line = -1,at=maxorder/2,col="blue")
mtext("AIC", side = 3, line = -2,at=maxorder/2,col="red")
axis(1,at=anf:(maxorder+1),labels=-1+anf:(maxorder+1))
axis(2)
box()
anf<-3
aic<-(log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder+1)]
ymin<-min((log_sigma_k)[anf:(maxorder)])
ymax<-max((log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder)])
plot((log_sigma_k)[anf:(maxorder+1)],col="blue",xlab="AR-order",ylab="",
main="log sample MSE and AIC for AR(2)",type="l",axes="F",ylim=c(ymin,ymax))
lines(aic,col="red")
mtext("log sample MSE", side = 3, line = -1,at=maxorder/2,col="blue")
mtext("AIC", side = 3, line = -2,at=maxorder/2,col="red")
axis(1,at=1:(maxorder-anf+2),labels=-1+anf:(maxorder+1))
axis(2)
box()

# 5. Compute BIC and compare with AIC: BIC is minimal at p=2 (true model order correctly identified by BIC)
par(mfrow=c(2,1))
anf<-1
aic<-(log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder+1)]
bic<-(log_sigma_k+log(len)*(0:maxorder)/len)[anf:(maxorder+1)]
plot(bic,col="blue",xlab="AR-order",ylab="",
main="BIC (blue) vs. AIC (red) for AR(2)",type="l",axes="F")
lines(aic,col="red")
mtext("BIC", side = 3, line = -1,at=maxorder/2,col="blue")
mtext("AIC", side = 3, line = -2,at=maxorder/2,col="red")
axis(1,at=anf:(maxorder+1),labels=-1+anf:(maxorder+1))
axis(2)
box()
anf<-3
aic<-(log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder+1)]
bic<-(log_sigma_k+log(len)*(0:maxorder)/len)[anf:(maxorder+1)]
ymin<-min(aic)
ymax<-max(bic)
plot(bic,col="blue",xlab="AR-order",ylab="",
main="BIC (blue) vs. AIC (red) for AR(2)",type="l",axes="F",ylim=c(ymin,ymax))
lines(aic,col="red")
mtext("BIC", side = 3, line = -1,at=maxorder/2,col="blue")
mtext("AIC", side = 3, line = -2,at=maxorder/2,col="red")
axis(1,at=1:(maxorder-anf+2),labels=-1+anf:(maxorder+1))
axis(2)
box()


# 6. Fit (wrong) MA-models

maxorder<-10
sigma_k<-rep(0,maxorder+1)
# Order zero
sigma_k[1]<-var(y)
for (k in 1:maxorder)         #k<-10
{
  MA_obj<-arima(y,order=c(0,0,k))
  sigma_k[k+1]<-mean(MA_obj$res^2)
# This is the same as
  sigma_k[k+1]<-MA_obj$sigma
  print(paste("MA-Order=",k,"  AIC=",MA_obj$aic,sep=""))
}
log_sigma_k<-log(sigma_k)

par(mfrow=c(2,1))
anf<-1
aic<-(log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder+1)]
bic<-(log_sigma_k+log(len)*(0:maxorder)/len)[anf:(maxorder+1)]
plot(bic,col="blue",xlab="MA-order",ylab="",
main="BIC (blue) vs. AIC (red) for AR(2) based on false MA-models",
type="l",axes="F",ylim=c(min(aic),max(aic)))
lines(aic,col="red")
mtext("BIC", side = 3, line = -1,at=maxorder/2,col="blue")
mtext("AIC", side = 3, line = -2,at=maxorder/2,col="red")
axis(1,at=anf:(maxorder+1),labels=-1+anf:(maxorder+1))
axis(2)
box()
anf<-3
aic<-(log_sigma_k+2*(0:maxorder)/len)[anf:(maxorder+1)]
bic<-(log_sigma_k+log(len)*(0:maxorder)/len)[anf:(maxorder+1)]
ymin<-min(aic)
ymax<-max(bic)
plot(bic,col="blue",xlab="MA-order",ylab="",
main="BIC (blue) vs. AIC (red) for AR(2)",type="l",axes="F",ylim=c(ymin,ymax))
lines(aic,col="red")
mtext("BIC", side = 3, line = -1,at=maxorder/2,col="blue")
mtext("AIC", side = 3, line = -2,at=maxorder/2,col="red")
axis(1,at=1:(maxorder-anf+2),labels=-1+anf:(maxorder+1))
axis(2)
box()


acf(y)

# 7. Fit ARMA-models: BIC identifies correct model (AIC is totally wrong: selects (4,3)-model)

maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)         #k<-10
  {
#    ARMA_obj<-arima(y,order=c(j,0,k),method="CSS")
    ARMA_obj<-arima(y,order=c(j,0,k))
    sigma_jk[j+1,k+1]<-ARMA_obj$sigma
    print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))
  }
}
log_sigma_jk<-log(sigma_jk)
aic<-sigma_jk
dimnames(aic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
dimnames(aic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
bic<-aic
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)
  {
#    aic[j,k]<-log_sigma_jk[j,k]+2*(j+k)/len
#    bic[j,k]<-log_sigma_jk[j,k]+log(len)*(j+k)/len
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic




###################################################
### code chunk number 7: slides_part3.Rnw:783-881
###################################################
# R-code: ARMA(p,q) forecasting
# Generate data for ARMA(1,1)
set.seed(10)
a_1<-0.9
b_1<-0.6
len<-100
mu<-10/(1-0.9)
sigma<-sqrt(3)
y<-mu+arima.sim(n = len, list( ar = a_1, ma = b_1), sd = sigma)
ts.plot(y)

# acf and pacf: the latter suggests AR(2). Let's see...
par(mfrow=c(2,1))
acf(y)
acf(y,type="partial")

if (F)
{
# AR(2) and ARMA(1,1) are both OK
  arorder<-2
  maorder<-0
  y_ar<-arima(y,order=c(arorder,0,maorder))
  arorder<-1
  maorder<-1
  y_arma<-arima(y,order=c(arorder,0,maorder))
  tsdiag(y_ar)
  tsdiag(y_arma)
}


# Set-up BIC in a function
  
bic_func<-function(maxarorder,maxmaorder,y)
{
  sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                   ncol=maxmaorder+1,nrow=maxarorder+1)
  len<-length(y)
  for (j in 0:maxarorder)
  {
    for (k in 0:maxmaorder)         #k<-10
    {
      ARMA_obj<-arima(y,order=c(j,0,k))
      sigma_jk[j+1,k+1]<-ARMA_obj$sigma
    }
  }
  log_sigma_jk<-log(sigma_jk)
  bic<-sigma_jk
  dimnames(bic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
  dimnames(bic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
  for (j in 0:maxarorder)
  {
    for (k in 0:maxmaorder)
    {
      #    bic[j,k]<-log_sigma_jk[j,k]+log(len)*(j+k)/len
      bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
    }
  }
  return(list(bic=bic))
  
}


# Set max orders and apply bic_func (not too large because of potential numerical issues)
maxarorder<-5
maxmaorder<-5

# ARMA(1,1) (true model) is preferred to AR(2)
bic<-bic_func(maxarorder,maxmaorder,y)$bic

bic

# Model orders
which(bic == min(bic), arr.ind = TRUE)-1 
arorder<-(which(bic == min(bic), arr.ind = TRUE)-1)[1] 
maorder<-(which(bic == min(bic), arr.ind = TRUE)-1)[2] 


# Estimate parameters: arorder=maorder=1 minimize above BIC-matrix
y_arma<-arima(y,order=c(arorder,0,maorder))

# Check model
tsdiag(y_arma,gof.lag=15)

# Compute forecasts: 10-steap ahead
h<-10
pred_obj<-predict(y_arma,n.ahead=h)

yhat<-pred_obj$pred
sd_yhat<-pred_obj$se

y_lower<-yhat-2*sd_yhat
y_upper<-yhat+2*sd_yhat

par(mfrow=c(1,1))
ts.plot(c(rep(NA,31),yhat),col="red",xlab="",ylab="",
main="Interval forecasts ARMA(1,1)",
ylim=c(min(y[(len-30):len]),max(y_upper)))
lines(c(rep(NA,31),y_lower),col="red",lty=2)
lines(c(rep(NA,31),y_upper),col="red",lty=2)
lines(c(y[(len-30):len],rep(NA,h)),col="blue")
abline(v=31)





