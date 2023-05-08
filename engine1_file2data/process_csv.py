
import pandas as pd

df=pd.read_csv("test/page1_1.csv")
df = df.drop(["Unnamed: 0","TAX"],axis=1)
df.rename(columns={"PRICE DISCOUNT":"AMOUNT","ITEM DESCRIPTION QTY":"ITEM DESCRIPTION"},inplace=True)
df["ITEM DESCRIPTION"][1]=df["ITEM DESCRIPTION"][0]+df["ITEM DESCRIPTION"][1]
df["AMOUNT"][1]="PRICE"
df = df.drop(0)

df.to_csv("test/Invoice.csv",index=False)

