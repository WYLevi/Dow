import test

mode = input('Please choose a mode. \n1: Monitor Only \n2: AI Detection \n3: Initial Bounding Select \n0: Exit \n[Please enter 1, 2, 3]\n ')
if mode == '1': 
    endtime = input('Please enter the monitoring storage time. \n[Please Enter Minute]\n ')
    test.run(int(endtime))