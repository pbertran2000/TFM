import numpy as np
import matplotlib.pyplot as plt


w=np.array([1.8,1.6,1.4,1.2,1.0])

########### Read the potentialVSwidth file

min1=np.loadtxt("PotentialVSwidth.txt")[:, 1]
min2=np.loadtxt("PotentialVSwidth.txt")[:, 2]
maxim=np.loadtxt("PotentialVSwidth.txt")[:, 3]
errmin1=np.loadtxt("PotentialVSwidth.txt")[:, 4]
errmin2=np.loadtxt("PotentialVSwidth.txt")[:, 5]
errmaxim=np.loadtxt("PotentialVSwidth.txt")[:, 6]

################## Calculate the value of the potential barrier and its error. Also the linear regression.

averagemin=(min1+min2)/2
erraveragemin=(errmin1+errmin2)/2

difference=maxim-averagemin
errdifference=errmaxim+erraveragemin

A = np.vstack([w, np.ones(len(w))]).T
m, c = np.linalg.lstsq(A, difference, rcond=None)[0]

y_pred = m * w + c

############### Plot the barrier of potential for each width and make a linear regression

plt.scatter(w,difference, color='green', s=10, label='Experimental data with error')
plt.errorbar(w,difference, yerr=errdifference, color='green', fmt='none')
plt.plot(w, y_pred, label='Regression Line')
plt.xlabel('x ($\mu$m)')
plt.ylabel('U (k$_B$T)')
plt.ylim(1,3.5)
plt.xlabel('x ($\mu$m)', fontsize=15)
plt.ylabel('U (k$_B$T)', fontsize=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend()
plt.show()

############## Calculate the the slope and the intercept and its errors of the linear regression

residuals = difference - (m * w + c)
sum_squared_residuals = np.sum(residuals**2)
n = len(w)
inverse_matrix = np.linalg.inv(np.dot(A.T, A))
error_slope = np.sqrt((sum_squared_residuals / (n - 2)) * inverse_matrix[0, 0])
intercept_error = np.sqrt((sum_squared_residuals / (n - 2)) * inverse_matrix[1, 1])

print(m)
print(error_slope)
print(c)
print(intercept_error)


print(difference)


