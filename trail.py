from functions import column_cost, floor_system_cost
import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt


# import the matlab file .mat, database_original.mat is a 1*1 struct with 7 fields, inlcude all the original data from 130 simulaitons
database_ori_mat = scipy.io.loadmat('database_original.mat')
database_ori = database_ori_mat['database_original']

# get the detailed original value from rsmeans
costdetails_ori_mat = database_ori['costdetails']
costdetails_ori = costdetails_ori_mat[0, 0]

# the cost multiplier
proportion_ori_mat = database_ori['proportion']
proportion_ori = proportion_ori_mat[0, 0]

# import the building information, include the fire rating, floor area, building type, stories
building_information_ori_mat = database_ori['building_information']
# variable in different columns: 1floor area, 2story, 3perimeter, 4total cost, 5sq. cost, 6fire type in IBC, 7fire type index, 8building type,
# 9beam fire rating in rsmeans, 10column fire rating in rsmeans, 11 IBCbeam, 12 IBC column,
# 13 adjusted column cost,
# 14 adjusted column fire protection cost for 1h, 15 adjusted column fire protection cost for 2h, 16 adjusted column fire protection cost for 3h
building_information_ori = building_information_ori_mat[0, 0]

# the total cost,1 - 2 columns: total cost (original rsmeans value, without adjustment in floor system, column, fire rating), second column is sq.ft cost
# 3 - 4 columns: rsmeans value minus the floor system cost, column system cost
# 5 - 6 columns: value with adjusted floor system and columns, fire rating is based on IBC coding

totalcost_mat = scipy.io.loadmat('building_total_cost.mat')
totalcost_ori = totalcost_mat['totalcost_num']
# define new vlue in the database


# all  the inputs needed:

# define the fire protection material
building_index = 1
total_A=building_information_ori[building_index-1][1] #sq.ft
total_story=int(building_information_ori[building_index-1][2])


column_fire_rating = int(building_information_ori[building_index-1][10])
Beam_fire_rating = int(building_information_ori[building_index-1][9])
Building_type = int(building_information_ori[building_index-1][8])

baysize1=20 #ft
baysize2=25 #ft
bay_total_load_default = [0.115, 0.115, 0.080, 0.08, 0.08, 0.08, 0.08, 0.08]
bay_total_load = bay_total_load_default[Building_type-1] #kips
story_height = 10 #ft


fire_protection_material_column = 1
fire_protection_material_beam = 1
floor_default_composite = [20.65, 20.65, 19.99, 19.99, 19.99, 19.99, 19.99, 19.99]
fireprotectionbeam_default = [0.86, 0.86, 0.79, 0.79, 0.79, 0.79, 0.79, 0.79]

floor_composite = floor_default_composite[building_index-1]
fireprotectionbeam_ori = fireprotectionbeam_default[building_index-1]
# import the cost data related to column and fire protecion
filename = 'unit_cost_data.csv'
# get the data frame
data_frame = pd.read_csv(filename)


# get the column cost arrays
column_tabular = np.asarray(data_frame.iloc[0:15, 0:8], float)
# get the indices for different fire protection materials
row_indices_column = [i + 12 + fire_protection_material_column*6 for i in range(0, 4)]
# get the numerical value for given fire protection materials
column_fire_cost_tabular = np.asarray(data_frame.iloc[row_indices_column, 0:7], float)

# get the indices for different fire protection materials for beams
row_indices_beam = [i - 8 + fire_protection_material_beam * 10 for i in range(0, 8)]

beam_fire_cost_tabular = np.asarray(data_frame.iloc[row_indices_beam, 9:14], float)

# beam fire cost at different fire rating with given building index
beam_fire_cost=beam_fire_cost_tabular[building_index-1][2:5]

# building_index, total_A, total_story, baysize1, baysize2, bay_total_load, story_height,
#                column_tabular, column_fire_cost_tabular
#
column_cost, column_protection_cost = column_cost(total_A,total_story,baysize1,baysize2,bay_total_load,story_height,column_tabular, column_fire_cost_tabular)
#         record[i1][0] = total_A
#         record[i1][1] = total_story
#         record[i1][2] = perimeter
# record[i1][3] = cost_column[i1, 0] column cost
# record[i1][4] = cost_column[i1][1] 1 h fire protection cost
# record[i1][5] = cost_column[i1][2] 2 h fire protection cost
# record[i1][6] = cost_column[i1][3] 3 h fire protection cost
# record[i1][7] = cost_column[i1][4] 4 h fire protection cost

floor_cost, floor_protection_cost = floor_system_cost(total_A, floor_composite, beam_fire_cost, fireprotectionbeam_ori)

total_cost = totalcost_ori[building_index-1][2] + floor_cost + column_cost + column_protection_cost[column_fire_rating-1] + floor_protection_cost[Beam_fire_rating-1]
total_cost_sqft = total_cost/total_A

print(costdetails_ori[:, 0:2])

