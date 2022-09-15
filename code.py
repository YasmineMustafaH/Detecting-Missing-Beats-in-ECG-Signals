import os,sys
from scipy import stats
import numpy as np
import bottleneck as bn
from scipy import signal
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt 
import numpy as geek 

# Same function as question 1 is included in this file
#____________________________________5 Point Difference_____________________________________________________________________________
def pointDiff5(signal):
   result = np.zeros(len(signal))
   result[0] = signal[0]
   result[1] = signal[1]
   result[len(signal)-1] = signal[len(signal)-1]
   result[len(signal)-2] = signal[len(signal)-2]
   for n in range(2,len(signal)-2):
       result[n] = signal[n+2]+2*signal[n+1]-2*signal[n-1]-signal[n-2]
   r = np.multiply(result,(1/8.0)*256)
   return r
#__________________________________Set Threshold_____________________________________________________________________________________
def setThreshold(smoothed,N):
  # get the variance of the signal 
  # to check how often does the signal change to avoid considering low values 
  # set the variance as the window
  # save the peak of every window
  # get the average peak = Threshold
  peaks = []
  window = []
  j=0
  for i in range(len(smoothed)):
    window.append(smoothed[i])
    if( i % int(np.var(smoothed)) == 0):
      window = np.array(window)
      if(len(peaks)>1 and peaks[j-1]>np.amax(window)):
        peaks[j-1]= np.amax(window)
      else:
        peaks.append(np.amax(window))
        j+=1
      window = []
     
  T = sum(peaks)/float(len(peaks))
  return T
#________________________________Moving Average Window_____________________________________________________________________________________  
def movingAverageWindow(signal,N):
   result = []
   for i in range(len(signal)):
     result.append(np.sum(signal[i-N:i]))
   return np.multiply(result,(1/float(N)))
#___________________________________Filter Signal_____________________________________________________________________________________________
def filterSignal(array):
   #sampling rate
   fs = 256
   # Filter the signal using notch filter
   b, a = signal.iirnotch(50,30, fs)
   afternotch =  lfilter(b, a, array)

   # Filter the signal using BandPass Filter
   nyquist_freq = 0.5 * fs
   low = 0.5 / nyquist_freq
   high = 45 / nyquist_freq
   b, a = butter(1, [low, high], btype="band")
   afterbandPass = lfilter(b, a, afternotch)
  
   return afterbandPass
#_____________________________________QRS Detection_____________________________________________________________________________________________  
def QRS(signal,N):

    #filter signal using notch filter then bandpass filter
    filtered = filterSignal(signal)

    """# Plot signal before and after noise filtering
    fig = plt.figure()
    
    x1=fig.add_subplot(211)
    x1.plot(signal[0:1999])
    x1.title.set_text('ECG Signal Before Noise Filtering')

    x2=fig.add_subplot(212)
    x2.plot(filtered[0:1999])
    x2.title.set_text("ECG Signal After Noise Filtering")
    fig.tight_layout()

    # shift subplots down
    fig.subplots_adjust(top=0.85)
    plt.show()"""
    
    #calculate 5 point difference using the defined function above
    difference = pointDiff5(filtered)
 
    
    # Next, square the values
    squared = difference**2

    # Moving Average Window using defined function above
    smoothed = movingAverageWindow(squared,N)

    # Set Treshold using the defined function above
    T = setThreshold(smoothed,N)
    
    # Detect R waves 
    Timestamps = []
    window = []
    indices = []
    # Set a window of (250) 
    # 250 is chosen using trial and error
    # Take the max of every window, if it is greater than the threshold
    # Add its index in the array of smoothed signal in the timestamps array
    # setting a window helps to avoid multiple stars in a single peak
    for i in range(len(smoothed)):
      window.append(smoothed[i])
      indices.append(i)
      if(i%250==0):
        max = np.max(window)
        ind = np.argmax(window)
        if(max>=T):
          Timestamps.append(indices[ind])
        window=[]
        indices=[]


    
    RR = []
    # Get RR Intervals
    for i in range(1,len(Timestamps)):
      RR.append(Timestamps[i]-Timestamps[i-1])

    
    return Timestamps, RR
# -----------------------------------------------------------------------------------------------------------------------------------------------------

def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t           

    avg = sum_num / len(num)
    return avg
#--------------------------------------------------------------------------------------------------------------------------------------------------
def missingbeats(ecg,w):
   ts,rr= QRS(ecg,w)
   avg1=cal_average(rr)
   i=0
   missingbeats=[]
   
   
   x = ts[1] - ts[0]
   for i in range(2, len(ts)):
       
       
       if ts[i] - ts[i-1] > avg1 : 
           
           missingbeats.append(ts[i]+avg1)

    
    
   
   return missingbeats    
  

#_______________________________MAIN____________________________________________________________________________


with open('C:/Users/yasmi/Desktop/Semester 10/Biomedical/Assignment 1_31990/Data2.txt') as file_in:
      array = []
      for line in file_in:
        array.append(float(line))

#QRS(array,25)
m=missingbeats(array,25)
c = geek.savetxt('C:/Users/yasmi/Desktop/Semester 10/Biomedical/Deliverables/question 2/MissingBeats.txt', m, delimiter =', ')    
a = open('C:/Users/yasmi/Desktop/Semester 10/Biomedical/Deliverables/question 2/MissingBeats.txt', 'r')# open file in read mode 
  
print("the file contains:") 
print(a.read()) 


