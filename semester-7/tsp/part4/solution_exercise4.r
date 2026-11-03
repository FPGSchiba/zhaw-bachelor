rm(list = ls())

library(quantmod)
library(xts)

# Exercise 1

refresh_data<-F

if (refresh_data)
{  
  # Apple
  getSymbols("AAPL")
  head(AAPL,n=3)
  tail(AAPL,n=3)
  APPL<- Cl(AAPL)   #Close Price
  plot(APPL)
    save(APPL,file=paste(getwd(),"/Data/AAPL",sep=""))
  
  # GDP: from Quandl
  USA=US_GDP<-Quandl::Quandl("UNAE/GDPCD_USA")
  TT = dim(USA)[1]
  USA = USA[ rev(1:TT), ]
  plot( x = USA$Date, y = USA[ , 10], xlab = "year", ylab = "GDP",type="l")
  GDP<-USA[ , 10]
  names(GDP)<-USA$Date
  save(GDP,file=paste(getwd(),"/Data/GDP",sep=""))
  
  
  # Industrial production
  quantmod::getSymbols.FRED(Symbols = "IPB50001SQ", env = .GlobalEnv)
  plot(IPB50001SQ)
  INDPRO<-IPB50001SQ
  save(INDPRO,file=paste(getwd(),"/Data/INDPRO",sep=""))
  
  
  # S&P500
  SPX <- quantmod::getSymbols("^GSPC",auto.assign = FALSE, from = "2000-01-01")$GSPC.Close
  plot(SPX)
  save(SPX,file=paste(getwd(),"/Data/SPX",sep=""))
  
  
  # Bitcoin/Ethereum
  BTC <- quantmod::getSymbols("BTC-USD", auto.assign = FALSE,from = "2014-07-01")[,4]
  plot(BTC)
  save(BTC,file=paste(getwd(),"/Data/BTC",sep=""))
  
  ETH <- quantmod::getSymbols("ETH-USD", auto.assign = FALSE,from = "2014-07-01")[,4]
  plot(ETH)
} else
{
  load(file=paste(getwd(),"/Data/AAPL",sep=""))
  APPL
  
  load(file=paste(getwd(),"/Data/GDP",sep=""))
  GDP
  
  load(file=paste(getwd(),"/Data/INDPRO",sep=""))
  INDPRO
  
  load(file=paste(getwd(),"/Data/BTC",sep=""))
  BTC
  
  load(file=paste(getwd(),"/Data/SPX",sep=""))
  SPX
  
}

#----------------------------------------------------------------------------
# Exercise 2
# Select any of the following series

y<-APPL
y<-GDP
y<-BTC
y<-SPX

# Log-returns
lrt<-diff(log(y))

# Plot original data, first differences and log-returns
par(mfrow=c(2,2))
plot(y)
plot(diff(y))
plot(lrt)


len<-length(y)




par(mfrow=c(2,1))
acf(y)
acf(y,type="partial")

#--------------------------------------------
# Exercise 3: Stationary Model
# Forecast converges towards mean (does not make sense)
# The estimation routine does not estimate AR-coefficients (it breaks-down and issues an error message: non-stationary AR-part)
d<-0
maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                 ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)         #k<-3  j<-1
  {
    # Avoid interrupt if optimization fails    
    try_obj<-try(arima(y,order=c(j,d,k)),silent=F)
    if (is.character(try_obj[1]))
    {
      # If interrupted: sigma is set to a large value (`bad' model)      
      sigma_jk[j+1,k+1]<-1.e+99      
    } else
    {
      ARMA_obj<-arima(y,order=c(j,d,k))
      print(c(j,k))
      sigma_jk[j+1,k+1]<-ARMA_obj$sigma
      print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))      
    }
  }
}

len<-length(y)
log_sigma_jk<-log(sigma_jk)
aic<-sigma_jk
dimnames(aic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
dimnames(aic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
bic<-aic
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)
  {
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic
which(aic == min(aic), arr.ind = TRUE)-1 
which(bic == min(bic), arr.ind = TRUE)-1 
arorder<-which(bic == min(bic), arr.ind = TRUE)[1]-1 
maorder<-which(bic == min(bic), arr.ind = TRUE)[2]-1 

# Numerical optimization does not allow for stationary AR-models

# The following does not make sense since a MA(5) cannot fit the trend
y_obj<-arima(y,order=c(arorder,d,maorder))

tsdiag(y_obj)


# One step 

y_pred<-predict(y_obj,n.ahead=1)

ymin<-min(c(as.vector(y),y_pred$pred-2*y_pred$se))
ymax<-max(c(as.vector(y),y_pred$pred+2*y_pred$se))

ts.plot(c(as.vector(y),y_pred$pred),ylim=c(ymin,ymax))
abline(v=length(y))
lines(c(as.vector(y),y_pred$pred+2*y_pred$se))
lines(c(as.vector(y),y_pred$pred-2*y_pred$se))


# 1000 step: drops to 'mean' and intervals converge to +/- 2*sigma
y_pred<-predict(y_obj,n.ahead=1000)

ymin<-min(c(as.vector(y),y_pred$pred-2*y_pred$se))
ymax<-max(c(as.vector(y),y_pred$pred+2*y_pred$se))

ts.plot(c(as.vector(y),y_pred$pred),ylim=c(ymin,ymax))
abline(v=length(y))
lines(c(as.vector(y),y_pred$pred+2*y_pred$se))
lines(c(as.vector(y),y_pred$pred-2*y_pred$se))




#--------------------------------------------
# Exercise 4: I(1) Model
# Stays on a higher level than mean
d<-1
maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                 ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  
  for (k in 0:maxmaorder)         #k<-4  j<-3
  {
    # Avoid interrupt if optimization fails    
    try_obj<-try(arima(y,order=c(j,d,k)),silent=T)
    if (is.character(try_obj[1]))
    {
      # If interrupted: sigma is set to a large value (`bad' model)      
      sigma_jk[j+1,k+1]<-1.e+99      
    } else
    {
      ARMA_obj<-arima(y,order=c(j,d,k))
      print(c(j,k))
      sigma_jk[j+1,k+1]<-ARMA_obj$sigma
      print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))      
    }
  }
}
len<-length(y)
log_sigma_jk<-log(sigma_jk)
aic<-sigma_jk
dimnames(aic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
dimnames(aic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
bic<-aic
for (j in 0:maxarorder)#j<-5  k<-4
{
  for (k in 0:maxmaorder)
  {
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic
which(aic == min(aic), arr.ind = TRUE)-1 
which(bic == min(bic), arr.ind = TRUE)-1 







arorder<-which(bic == min(bic), arr.ind = TRUE)[1]-1 
maorder<-which(bic == min(bic), arr.ind = TRUE)[2]-1 

y_obj<-arima(y,order=c(arorder,d,maorder))

tsdiag(y_obj)

ts.plot(y)


# Forecast
# 100 steps ahead: 
y_pred<-y_pred_i1<-predict(y_obj,n.ahead=100)

par(mfrow=c(1,1))
# There is some `dynamics` in the forecast of SPX
ts.plot(y_pred$pred)

# 1000 steps: 
y_pred<-y_pred_i1<-predict(y_obj,n.ahead=1000)

ymin<-min(c(as.vector(y),y_pred$pred-2*y_pred$se))
ymax<-max(c(as.vector(y),y_pred$pred+2*y_pred$se))

ts.plot(c(as.vector(y),y_pred$pred),ylim=c(ymin,ymax))
abline(v=length(y))
lines(c(as.vector(y),y_pred$pred+2*y_pred$se))
lines(c(as.vector(y),y_pred$pred-2*y_pred$se))



#--------------------------------------------
# Exercise 5: I(2) Model
d<-2
maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                 ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  
  for (k in 0:maxmaorder)         #k<-4  j<-3
  {
    # Avoid interrupt if optimization fails    
    try_obj<-try(arima(y,order=c(j,d,k)),silent=T)
    if (is.character(try_obj[1]))
    {
      # If interrupted: sigma is set to a large value (`bad' model)      
      sigma_jk[j+1,k+1]<-1.e+99      
    } else
    {
      ARMA_obj<-arima(y,order=c(j,d,k))
      print(c(j,k))
      sigma_jk[j+1,k+1]<-ARMA_obj$sigma
      print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))      
    }
  }
}
len<-length(y)
log_sigma_jk<-log(sigma_jk)
aic<-sigma_jk
dimnames(aic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
dimnames(aic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
bic<-aic
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)
  {
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic
which(aic == min(aic), arr.ind = TRUE)-1 
which(bic == min(bic), arr.ind = TRUE)-1 







arorder<-which(bic == min(bic), arr.ind = TRUE)[1]-1 
maorder<-which(bic == min(bic), arr.ind = TRUE)[2]-1 

y_obj<-arima(y,order=c(arorder,d,maorder))
#!!!!!!!!!!!!!!!!! Huge outliers!!!!!!!!
#   This can impact all statistics (including BIC)!!!!!
tsdiag(y_obj)


# Forecast
# 100 steps ahead: 
y_pred<-y_pred_i1<-predict(y_obj,n.ahead=100)

# Strong trend and some weaker `dynamics` in the forecast of SPX
ts.plot(y_pred$pred)


# 1000 steps: 
y_pred<-y_pred_i1<-predict(y_obj,n.ahead=1000)

ymin<-min(c(as.vector(y),y_pred$pred-2*y_pred$se))
ymax<-max(c(as.vector(y),y_pred$pred+2*y_pred$se))

ts.plot(c(as.vector(y),y_pred$pred),ylim=c(ymin,ymax))
abline(v=length(y))
lines(c(as.vector(y),y_pred$pred+2*y_pred$se))
lines(c(as.vector(y),y_pred$pred-2*y_pred$se))

#------------------------------------------------------------------------------------
# Exercise 6.1 d=1 model shorter subsample
y<-SPX

# Select shorter subsample
y<-y["2019/2020-03-15"]
tail(y)
plot(y)

d<-1
maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                 ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  
  for (k in 0:maxmaorder)         #k<-4  j<-3
  {
    # Avoid interrupt if optimization fails    
    try_obj<-try(arima(y,order=c(j,d,k)),silent=T)
    if (is.character(try_obj[1]))
    {
      # If interrupted: sigma is set to a large value (`bad' model)      
      sigma_jk[j+1,k+1]<-1.e+99      
    } else
    {
      ARMA_obj<-arima(y,order=c(j,d,k))
      print(c(j,k))
      sigma_jk[j+1,k+1]<-ARMA_obj$sigma
      print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))      
    }
  }
}
len<-length(y)
log_sigma_jk<-log(sigma_jk)
aic<-sigma_jk
dimnames(aic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
dimnames(aic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
bic<-aic
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)
  {
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic
which(aic == min(aic), arr.ind = TRUE)-1 
which(bic == min(bic), arr.ind = TRUE)-1 







arorder<-which(bic == min(bic), arr.ind = TRUE)[1]-1 
maorder<-which(bic == min(bic), arr.ind = TRUE)[2]-1 

y_obj<-arima(y,order=c(arorder,d,maorder))
#!!!!!!!!!!!!!!!!! Huge outliers!!!!!!!!
#   This can impact all statistics (including BIC)!!!!!
tsdiag(y_obj)




# 100 step: ARMA(1,1,3) is selected by BIC : flat forecast
y_pred_i1<-y_pred<-predict(y_obj,n.ahead=100)

ymin<-min(c(as.vector(y),y_pred$pred-2*y_pred$se))
ymax<-max(c(as.vector(y),y_pred$pred+2*y_pred$se))

ts.plot(c(as.vector(y),y_pred$pred),ylim=c(ymin,ymax))
abline(v=length(y))
lines(c(as.vector(y),y_pred$pred+2*y_pred$se))
lines(c(as.vector(y),y_pred$pred-2*y_pred$se))

#------------------------------------------------
# Exercise 6.2 d=2 model shorter subsample
d<-2
maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                 ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  
  for (k in 0:maxmaorder)         #k<-4  j<-3
  {
    # Avoid interrupt if optimization fails    
    try_obj<-try(arima(y,order=c(j,d,k)),silent=T)
    if (is.character(try_obj[1]))
    {
      # If interrupted: sigma is set to a large value (`bad' model)      
      sigma_jk[j+1,k+1]<-1.e+99      
    } else
    {
      ARMA_obj<-arima(y,order=c(j,d,k))
      print(c(j,k))
      sigma_jk[j+1,k+1]<-ARMA_obj$sigma
      print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))      
    }
  }
}
len<-length(y)
log_sigma_jk<-log(sigma_jk)
aic<-sigma_jk
dimnames(aic)[[2]]<-paste("MA-order",0:maxmaorder,sep=" ")
dimnames(aic)[[1]]<-paste("AR-order",0:maxarorder,sep=" ")
bic<-aic
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)
  {
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic
which(aic == min(aic), arr.ind = TRUE)-1 
which(bic == min(bic), arr.ind = TRUE)-1 







arorder<-which(bic == min(bic), arr.ind = TRUE)[1]-1 
maorder<-which(bic == min(bic), arr.ind = TRUE)[2]-1 

y_obj<-arima(y,order=c(arorder,d,maorder))
#!!!!!!!!!!!!!!!!! Huge outliers!!!!!!!!
#   This can impact all statistics (including BIC)!!!!!
tsdiag(y_obj)




# 100 step: ARMA(0,2,2) is selected by BIC and long-term forecast is trending down with huge/spreading intervals
y_pred_i2<-y_pred<-predict(y_obj,n.ahead=100)

ymin<-min(c(as.vector(y),y_pred$pred-2*y_pred$se))
ymax<-max(c(as.vector(y),y_pred$pred+2*y_pred$se))

ts.plot(c(as.vector(y),y_pred$pred),ylim=c(ymin,ymax))
abline(v=length(y))
lines(c(as.vector(y),y_pred$pred+2*y_pred$se))
lines(c(as.vector(y),y_pred$pred-2*y_pred$se))

# Discussion: The I(2)-model is generally too adaptive or, stated otherwise, economic time series tend to have simpler 
# (less randomly changing, more persistent) trends. Also, in general the forecast interval spreads out too rapidly 
# for the I(2) model: economic time series tend to be less noisy or less random than assumed by I(2)-models.
# For most economic data, I(1) i.e. d=1 tends to be  the better choice.

#----------------------------------------------------------------------------
# Exercise 7: consensus forecast (take the mean) 


y_pred<-(y_pred_i1$pred+y_pred_i2$pred)/2

# The I(1) forecast is 'flat', The I(2)-forecast is (too) strongly trending. 
# The consensus forecast is a 'good mix'
# Halving the slope (of I(2)) models is a good idea according to forecast competitions...
ts.plot(c(as.vector(y),y_pred),ylim=c(min(c(as.vector(y),y_pred_i2$pred)),max(c(as.vector(y),y_pred_i2$pred))))
lines(c(as.vector(y),y_pred_i1$pred))
lines(c(as.vector(y),y_pred_i2$pred))
abline(v=length(y))

