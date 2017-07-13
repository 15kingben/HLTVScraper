import pandas as pd
import pickle

dm = pickle.load(open('dataMatrix.pickle', 'rb'))

# The data Matrix contains several columns with NA values which correspond to no data
# In time since last match these should probably be filled in with the max value in the column, eg.
# In the month performance these could be filled in with .5, or 0, or whatever corresponds to a .5 winrate
