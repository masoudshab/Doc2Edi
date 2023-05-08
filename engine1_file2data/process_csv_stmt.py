
import pandas as pd

df=pd.read_csv("test/page1_1.csv")
df = df[["Transaction Date","Withdrawal Amount (INR)"]]
#print(df.head(10))

df1=pd.read_csv("test/page2_1.csv")
df1.rename(columns={"Unnamed: 2":"Transaction Date","Unnamed: 6":"Withdrawal Amount (INR)"},inplace=True)
#print(df.columns)
df1 = df1[["Transaction Date","Withdrawal Amount (INR)"]]
#print(df.head(10))

df2=pd.read_csv("test/page3_1.csv")
print(df2.columns)
#df = df[["Transaction Date","Withdrawal Amount (INR)"]]
print(df2.head(10))



