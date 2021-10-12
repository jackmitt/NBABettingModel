library(dplyr)
library(tidyr)
library(ggplot2)

data = read.csv("C:/Users/JackMitt/Documents/NBABettingModel/csv_data/mid_manipulation/predictions.csv")

KellyDiv = 1

ah = data %>% select(binSpread, Spread.PFITS) %>% drop_na() %>% arrange(Spread.PFITS)
ou = data %>% select(binTotal, Total.PFITS) %>% drop_na() %>% arrange(Total.PFITS)

index = seq(1, nrow(ou))


l = index[0+1:trunc(nrow(ou)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(ou)/2)+1):nrow(ou)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

predictedRate = c(mean(ou$Total.PFITS[one]),mean(ou$Total.PFITS[two]),mean(ou$Total.PFITS[three]),mean(ou$Total.PFITS[four]),mean(ou$Total.PFITS[five]),mean(ou$Total.PFITS[six]),mean(ou$Total.PFITS[seven]),mean(ou$Total.PFITS[eight]),mean(ou$Total.PFITS[nine]),mean(ou$Total.PFITS[ten]),mean(ou$Total.PFITS[eleven]),mean(ou$Total.PFITS[twelve]))
actualRate = c(mean(ou$binTotal[one]),mean(ou$binTotal[two]),mean(ou$binTotal[three]),mean(ou$binTotal[four]),mean(ou$binTotal[five]),mean(ou$binTotal[six]),mean(ou$binTotal[seven]),mean(ou$binTotal[eight]),mean(ou$binTotal[nine]),mean(ou$binTotal[ten]),mean(ou$binTotal[eleven]),mean(ou$binTotal[twelve]))
n = c(length(ou$binTotal[one]),length(ou$binTotal[two]),length(ou$binTotal[three]),length(ou$binTotal[four]),length(ou$binTotal[five]),length(ou$binTotal[six]),length(ou$binTotal[seven]),length(ou$binTotal[eight]),length(ou$binTotal[nine]),length(ou$binTotal[ten]),length(ou$binTotal[eleven]),length(ou$binTotal[twelve]))
oudf = data.frame(predictedRate,actualRate,n)


index = seq(1, nrow(ah))

l = index[0+1:trunc(nrow(ah)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(ah)/2)+1):nrow(ah)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

predictedRate = c(mean(ah$Spread.PFITS[one]),mean(ah$Spread.PFITS[two]),mean(ah$Spread.PFITS[three]),mean(ah$Spread.PFITS[four]),mean(ah$Spread.PFITS[five]),mean(ah$Spread.PFITS[six]),mean(ah$Spread.PFITS[seven]),mean(ah$Spread.PFITS[eight]),mean(ah$Spread.PFITS[nine]),mean(ah$Spread.PFITS[ten]),mean(ah$Spread.PFITS[eleven]),mean(ah$Spread.PFITS[twelve]))
actualRate = c(mean(ah$binSpread[one]),mean(ah$binSpread[two]),mean(ah$binSpread[three]),mean(ah$binSpread[four]),mean(ah$binSpread[five]),mean(ah$binSpread[six]),mean(ah$binSpread[seven]),mean(ah$binSpread[eight]),mean(ah$binSpread[nine]),mean(ah$binSpread[ten]),mean(ah$binSpread[eleven]),mean(ah$binSpread[twelve]))
n = c(length(ah$binSpread[one]),length(ah$binSpread[two]),length(ah$binSpread[three]),length(ah$binSpread[four]),length(ah$binSpread[five]),length(ah$binSpread[six]),length(ah$binSpread[seven]),length(ah$binSpread[eight]),length(ah$binSpread[nine]),length(ah$binSpread[ten]),length(ah$binSpread[eleven]),length(ah$binSpread[twelve]))
ahdf = data.frame(predictedRate,actualRate,n)






ggplot(ahdf, aes(y=actualRate, x=predictedRate, color = n, size = n)) + geom_point() + geom_abline(slope=1, intercept=0) + xlim(0.4,0.6) + ylim(0.4,0.6)

ggplot(oudf, aes(y=actualRate, x=predictedRate, color = n, size = n)) + geom_point() + geom_abline(slope=1, intercept=0) + xlim(0.4,0.6) + ylim(0.4,0.6)
