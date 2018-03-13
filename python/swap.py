x=int(input("enter first amount: "))
y=int(input("enter second amount: "))

sum=x+y

print("the sum of two numbers is: ", sum)

if sum>50:
		print ("amount greater than 50")

elif sum==60:
		print("morethan fifty")
else :
		temp=x
		x=y
		y=temp
		print("final values are :",x,y,temp,sum)
		print ("check your code")