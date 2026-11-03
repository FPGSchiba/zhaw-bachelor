# Series 5



# Exercise 1
sigma<-1
a_vec<-c(1.6,-0.9)
b_vec<-c(1,-0.8,0.4)

# 1.1 Expectation
6/(1-sum(a_vec))

# 1.2 acf: relatively long memory with cycles (slowly decaying cyclical acf): see simulated 
# data below for confirmation
ts.plot(ARMAtoMA(ar = a_vec, ma = b_vec[2:3], lag.max=100))


# 1.3 theoretical and empirical acf
len<-300
sigma<-1
x<-arima.sim(list(ar=a_vec,ma=b_vec),n=len,sd=sigma)

# The damped cycle in the ACF matches the stochastic cycle of the series 
ts.plot(x)

acf(x)



#----------------------------------------------------
# Exercise 2


y_data<-read.table(paste(getwd(),"/Data/exercise3.txt",sep=""))

x<-y_data[,1]

par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")

# Series 1
arorder<-1
maorder<-1

# Series 2
arorder<-2
maorder<-1

# Series 3
arorder<-1
maorder<-2

x_obj<-arima(x,order=c(arorder,0,maorder))
#x_obj$sigma2
tsdiag(x_obj)


#-------------------------------------------------------------------------------------
# Exercise 3

# 3.1


y<-y_data[,3]
ts.plot(y)
len<-length(y)

par(mfrow=c(2,1))
acf(y)
acf(y,type="partial")



maxarorder<-5
maxmaorder<-5
sigma_jk<-matrix(rep(0,(maxmaorder+1)*(maxarorder+1)),
                 ncol=maxmaorder+1,nrow=maxarorder+1)
# Order (zero,zero)
sigma_jk[1,1]<-var(y)
for (j in 0:maxarorder)
{
  for (k in 0:maxmaorder)         #k<-4  j<-4
  {
    ARMA_obj<-arima(y,order=c(j,0,k))
    sigma_jk[j+1,k+1]<-ARMA_obj$sigma
    #    print(paste("  AR-order=",j,"MA-Order=",k,"  AIC=",ARMA_obj$aic,sep=""))
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
    aic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+2*(j+k)/len
    bic[j+1,k+1]<-log_sigma_jk[j+1,k+1]+log(len)*(j+k)/len
  }
}
aic
bic

which(aic == min(aic), arr.ind = TRUE) 
which(bic == min(bic), arr.ind = TRUE) 

# Model orders
which(aic == min(aic), arr.ind = TRUE)-1 
which(bic == min(bic), arr.ind = TRUE)-1 


# 3.2


arorder<-(which(bic == min(bic), arr.ind = TRUE)-1)[1] 
maorder<-(which(bic == min(bic), arr.ind = TRUE)-1)[2] 
y_obj<-arima(y,order=c(arorder,0,maorder))

tsdiag(y_obj)


#------------------------------------------------------------------------
# Exercise 4



recession_data<-read.table(paste(getwd(),"/Data/recession_data.txt",sep=""))

x<-recession_data[,1]
ts.plot(x)

# 4.1
arorder<-2
maorder<-1

x_obj<-arima(x,order=c(arorder,0,maorder))


tsdiag(x_obj)

x_pred<-predict(x_obj,n.ahead=36)

# 4.2 &4.3
# 90% intervals!!!!
quant<-1.6

ymin<-min(x_pred$pred-quant*x_pred$se)
ymax<-max(x_pred$pred+quant*x_pred$se)

ts.plot(c(x,x_pred$pred),ylim=c(ymin,ymax))
lines(c(x,x_pred$pred+quant*x_pred$se))
lines(c(x,x_pred$pred-quant*x_pred$se))
abline(h=0)

# The point forecast has its minimum (dip) in t=120. The point forecast is positive in t=139

# The upper 90%-interval dips in t=117; the lower interval dips in t=125





####################################################################

set.seed(1000)
a_vec<-0.8
b_vec<-0.99
sigma<-10
mu<-0

len<-220
x1<-mu+arima.sim(list(ar=a_vec,ma=b_vec),n=len,sd=sigma)



set.seed(10)
a_vec<-c(0.7,-0.7)
b_vec<-0.99
sigma<-1
mu<--5

len<-220
x2<-mu+arima.sim(list(ar=a_vec,ma=b_vec),n=len,sd=sigma)


set.seed(13)
a_vec<-0.5
b_vec<-rep(1,2)
sigma<-3
mu<-10

len<-220
x3<-mu+arima.sim(list(ar=a_vec,ma=b_vec),n=len,sd=sigma)

# Specify the system-matrices A_mat and B_mat

#x<-arima.sim(n = 63, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)),
#          sd = sqrt(0.1796))

y_data<-cbind(x1,x2,x3)





