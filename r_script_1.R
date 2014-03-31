library("randomForest")

args <- commandArgs(trailingOnly = TRUE)


file_price = paste("C:/BC/Subaru/AkhileshAutomation/Subaru/",args[1],sep="") 


train_data_price = read.table(file_price,sep=',',skip=1)

r = randomForest(V1 ~., data=train_data_price, importance=TRUE, ntree=500)

q = ncol(train_data_price)

y = cor(train_data_price[1],train_data_price[2:q])


o_file = "C:/BC/Subaru/AkhileshAutomation/Subaru/Corr.csv"
write.csv(y,file = o_file)

o_file = "C:/BC/Subaru/AkhileshAutomation/Subaru/Imp.csv"
x = importance(r)
write.csv(x,file = o_file)
var_exp = r$rsq[500]
var_exp = var_exp*100
o_file = "C:/BC/Subaru/AkhileshAutomation/Subaru/var_exp.txt"
write(var_exp,file = o_file)