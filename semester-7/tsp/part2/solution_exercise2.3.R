# Series 3: AR-processes


#Exercise 1

# 1.1

c_i<-6
a_vec<-c(1.6,-1.4,0.5)

# Process is stationary: all roots smaller one in absolute value
abs(polyroot(c(-a_vec[length(a_vec):1],1)))

# 1.2&1.3
#   Second (simpler) formula
mu<-c_i/(1-sum(a_vec))
# Acf decays to zero beyond lag 40: 'long' memory
# The cycle in the acf is indicative of cycles in the data with similar mean-length
ts.plot(ARMAacf( ar = a_vec, lag.max = 100, pacf = FALSE))

# 1.4
len<-300
x<-arima.sim(list(ar=a_vec),n=len)
ts.plot(x)


#--------------------------------------------------------------------------
# Exercise 2

mat<-read.table(paste(getwd(),"/Data/exercise23.txt",sep=""))
ts.plot(mat)

len<-length(mat[,1])

x<-mat[,1]

ts.plot(x)

par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")


# First series looks like a MA(3)

y_ma<-arima(x,order=c(0,0,3))
tsdiag(y_ma,gof.lag=20)
tsdiag(y_ma,gof.lag=200)

# Diagnostics for an AR(6) are OK too.
y_ar<-arima(x,order=c(6,0,0))
tsdiag(y_ar,gof.lag=20)

#----------------------------------------------------------------------------------------
# Exercise 3

# 3.1
set.seed(10)
len<-100
x<-arima.sim(list(ar=0.95),n=len)

ts.plot(x)

par(mfrow=c(2,1))
acf(x)
acf(x,type="partial")

xar_obj<-arima(x,order=c(1,0,0))
tsdiag(xar_obj)

# 3.2

xma_obj<-arima(x,order=c(0,0,5))
tsdiag(xma_obj)
xma_obj<-arima(x,order=c(0,0,6))
tsdiag(xma_obj)


# 3.3

simanz<-100
h<-10
forecast_error_ma<-matrix(nrow=h,ncol=simanz)
forecast_error_ar<-forecast_error_ma
set.seed(10)

for (i in 1:simanz)        #i<-1
{
  x<-arima.sim(list(order=c(1,0,0),ar=0.95),n=len+h)
  y_ma<-arima(x[1:len],order=c(0,0,6))
  y_ar<-arima(x[1:len],order=c(1,0,0))
  forecast_error_ma[,i]<-(predict(y_ma,n.ahead=h)$pred-x[(len+1):(len+h)])^2
  forecast_error_ar[,i]<-(predict(y_ar,n.ahead=h)$pred-x[(len+1):(len+h)])^2
}

# Ratio mean-square out-of-sample forecast errors of MA- over AR-model
#   Numbers larger than 1 suggest that the AR-model does a better job at that forecast horizon
apply(forecast_error_ma,1,mean)/apply(forecast_error_ar,1,mean)






#-----------------------------------------------------------------------------
# Series simulated for identification (file exercise4.txt)

len<-210


set.seed(858)
x1<-arima.sim(list(order=c(0,0,2),ma=c(0.,-0.8)),n=len)-5.
acf(x1)
acf(x1,type="partial")
ts.plot(x1)


set.seed(5)
x2<-arima.sim(list(order=c(1,0,0),ar=0.95),n=len)
acf(x2)
acf(x2,type="partial")
ts.plot(x2)




set.seed(1)
x3<-arima.sim(list(order=c(1,0,1),ar=0.8,ma=0.8),n=len)+3.
acf(x3)
acf(x3,type="partial")
ts.plot(x3)


set.seed(1)
x4<-arima.sim(list(order=c(0,0,1),ma=0.6),n=len)
acf(x4)
acf(x4,type="partial")
ts.plot(x4)

exercise_3<-cbind(x1[1:200],x2[1:200],x3[1:200],x4[1:200])
write.table(exercise_3,file="C:\\wia_desktop\\Projekte\\2013\\Unterricht\\Eco1\\Exercises\\Data\\exercise_3.txt")

