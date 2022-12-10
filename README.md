# CMPT353-Group-Project

Before trying to the the python programs, ensure that following libraries/packages are installed:
1) NumPy
2) Pandas
3) Matplotlib
4) Seaborn
5) Scikit-learn
6) Scipy

To retrieve U-test results for: Senior-Adult (Age 67 to 25), Shoes-NoShoes (Individual), Uphill-Downhill (Individual), Flat-Uphill (Individual), Flat-Downhill (Individual), run the following commands on a Windows terminal within the project directory. You will probably need to specify the python version if on Linux (ex. python3):

**1) python TransformLoad.py**


Afterwards, to get the ML classification validation data, run the following command after running the TransformLoad.py program:

**2) python Classification.py flat.csv uphill.csv downhill.csv noshoes.csv**



To get the p-values for different combinations of height, run:

**1) python height.py**



To get the p-value of injured VS normal step frequency by using U-test, run the command line below:

**1) python injured.py**



All results should be printed onto the terminal. 
