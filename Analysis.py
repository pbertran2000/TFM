import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

N_frames=17322
N_part=1000
Len=N_frames*N_part
A=[]
conversion_factor=1/8.51
U_particle=[]
x_coordinate=[]
distance=[]

####### Read the file and take only the position in x and y, and the ID

pm_df2 = pd.read_csv(r"/Users/montserrattrullsjuanola/Desktop/TFM/Videosanalitzats/1,8/ColAcid2.8um_Q22_1.8_2023_03_23_15_15_41_tracking.dat", delim_whitespace=True, index_col=0, header=0)

pm_df2['x'] = pd.to_numeric(pm_df2['x'])
pm_df2['particle'] = pd.to_numeric(pm_df2['particle'])
pm_df2['y'] = pd.to_numeric(pm_df2['y'])

df2columns = pd.DataFrame(pm_df2, columns=['particle','x','y'])


############## Filter for each particle (ID)

for i in range(0,N_part,1):
    
    track_id_to_filter = i
    
    filtered_x = df2columns.loc[df2columns['particle'] == track_id_to_filter, 'x']
    filtered_y = df2columns.loc[df2columns['particle'] == track_id_to_filter, 'y']
    
    if len(filtered_x)>N_frames/2:      ##### Filter if there are sufficient frames
    
        xmin = np.min(filtered_x)
        xmax = np.max(filtered_x)
    
        ymin = np.min(filtered_y)
        ymax = np.max(filtered_y)
    
        distance_x = xmax-xmin
        distance_y = ymax-ymin

        if distance_y>distance_x:    ######### Filter the traps according if they move in x or in y, and overlap all the traps
        
            if distance_y<40 and distance_y>20:
                
                distance.append(distance_y)
        
                filtered_y = filtered_y - (ymax+ymin)/2
        
                A.extend(filtered_y)

                ######### Calculate the potential
                
                PosHistogram, x = np.histogram(filtered_y, density=True, bins=20)
                
                for cordi in range(0,len(x)-1,1):
                    
                    x_coordinate.append(((x[cordi]+x[cordi+1])/2)*conversion_factor)
                
                U_particle.extend(-np.log(PosHistogram))
       
        else:
        
            if distance_x<40 and distance_x>20:
                
                distance.append(distance_x)
            
                filtered_x = filtered_x - (xmax+xmin)/2
        
                A.extend(filtered_x)
                
                PosHistogram, x = np.histogram(filtered_x, density=True, bins=20)
                
                for cordi in range(0,len(x)-1,1):
                    
                    x_coordinate.append(((x[cordi]+x[cordi+1])/2)*conversion_factor)
                
                U_particle.extend(-np.log(PosHistogram))
            
                #plt.hist(filtered_x, bins=30)
                

        
################# Make the analysis of all data, computing the means and the errors

U_final=[]
x_final=[]
U_err=[]
X_err=[]
bins=20
s=int(len(U_particle)/bins)
print(s)
    
for l in range(0,bins,1):
    
    U_average=[]
    X_average=[]
    
    for m in range(0,len(U_particle),bins):
    
        U_average.append(U_particle[m+l])
        
        X_average.append(x_coordinate[m+l])
        
    U_final.append(np.mean(U_average))
    
    U_err.append(np.std(U_average)/np.sqrt(s))
    
    x_final.append(np.mean(X_average))
    
    X_err.append(np.std(X_average)/np.sqrt(s))
       

print(np.mean(distance)*conversion_factor, np.std(distance)/np.sqrt(s)*conversion_factor)

########## Plot of the potential as a function of the position

plt.scatter(x_final,U_final, s=10)
plt.errorbar(x_final,U_final, yerr=U_err, xerr=X_err, fmt='none')
plt.xlabel('x ($\mu$m)', fontsize=15)
plt.ylabel('U (k$_B$T)', fontsize=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.arrow(0.0, 3.0, 0.0, 1.0, color='blue', head_length = 0.2, head_width = 0.1, length_includes_head = True)
plt.arrow(0.0, 4.0, -0.0, -1.0, color='blue', head_length = 0.2, head_width = 0.1, length_includes_head = True)
plt.text(-0.7, 2.2, '$\Delta$U = 2.50 k$_B$T', fontsize=15, color='blue')
plt.xlim(-2,2)
plt.ylim(2,8)
plt.show()
