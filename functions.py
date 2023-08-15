import numpy as np
import scipy.io





# Define functions for searching data
def FindIndexfromList(List, Target):
    # This function find a target from a list and return the index of the target's position
    # Inputs:
    # List: a list to carry out the search (input a 1-D vector)
    # Target: the target searched for

    # Output:
    # Index of the Target found in this List

    # Covert the list into numpy array form
    NPlist = np.asarray(List)
    # Find the total number of elements in this list
    nele = np.shape(NPlist)[0]
    # Initialize the output list
    IndexList = []
    # Loop over the whole list
    for i in range(0, nele):
        if Target in NPlist[i]:
            IndexList.append(i)

    # Convert the index list to numpy array form
    IndexList = np.asarray(IndexList)
    return IndexList


def find_closest_larger_index(array, target):
    absolute_diff = array - target
    filtered_diff = np.where(absolute_diff > 0, absolute_diff, np.inf)
    closest_index = np.argmin(filtered_diff)
    return closest_index


# calculate column cost
def column_cost( total_A, total_story, baysize1, baysize2, bay_total_load, story_height,
                column_tabular, column_fire_cost_tabular):
        building_index=1
        i1 = building_index - 1
        max_input_index = building_index
        # define the floor area
        A = total_A / total_story
        # get the size of the projection of the building
        x2 = 2 * A**0.5 / (3 ** 0.5)
        x1 = x2 * 3 / 4
        perimeter = x1 + x2

        # initiate the record variable
        record = np.zeros((max_input_index, 8))
        cost_column = np.zeros((max_input_index, 5))
        # record the data of the input building

        record[i1][0] = total_A
        record[i1][1] = total_story
        record[i1][2] = perimeter
        # get the area per story and per bay
        floorarea = total_A / total_story
        bayarea = baysize2 * baysize1

        # initiate the floor load as 0 at different stories
        floor_load = np.zeros((total_story + 1, 9, max_input_index))

        for i2 in range(total_story-1, -1, -1):
            # calculate the floor load at different stories
            floor_load[i2][0][i1] = bayarea * bay_total_load + floor_load[i2 + 1][0][i1]
            # get the number of columns at each story
            floor_load[i2][1][i1] = (floorarea / (baysize1 * baysize2) + x1 / baysize1 + x2 / baysize2 + 1) * story_height

        if max(floor_load[:, 0, i1]) > 1000:
            print(f"Warning: the maximum floor load exceed the column capacity, building index={i1}")

        for i4 in range(total_story - 1, -1, -1):
            closest_index = find_closest_larger_index(column_tabular[:, 0],floor_load[i4][0][i1])
            floor_load[i4][2][i1] = column_tabular[closest_index][0]  # 3 column load
            floor_load[i4][3][i1] = column_tabular[closest_index][4]  # 4 price V.L.F
            floor_load[i4][4][i1] = column_tabular[closest_index][6] - 1 # 5 fire protection index

            floor_load[i4][5][i1] = column_fire_cost_tabular[int(floor_load[i4][4][i1]), 3]  # 6 fire protection cost 1h
            floor_load[i4][6][i1] = column_fire_cost_tabular[int(floor_load[i4][4][i1]), 4]  # 6 fire protection cost 2h
            floor_load[i4][7][i1] = column_fire_cost_tabular[int(floor_load[i4][4][i1]), 5]  # 6 fire protection cost 3h
            floor_load[i4][8][i1] = column_fire_cost_tabular[int(floor_load[i4][4][i1]), 6]  # 6 fire protection cost 4h
            i4 -= 1

        cost_column[i1, 0] = 0
        cost_column[i1][1] = 0
        cost_column[i1][2] = 0
        cost_column[i1][3] = 0

        for i5 in range(total_story - 1, -1, -1):
            # price*number
            cost_column[i1, 0] += floor_load[i5][3][i1] * floor_load[i5][1][i1]
            cost_column[i1][1] += floor_load[i5][5][i1] * floor_load[i5][1][i1]
            cost_column[i1][2] += floor_load[i5][6][i1] * floor_load[i5][1][i1]
            cost_column[i1][3] += floor_load[i5][7][i1] * floor_load[i5][1][i1]
            cost_column[i1][4] += floor_load[i5][8][i1] * floor_load[i5][1][i1]
            i5 += 1

        record[i1][3] = cost_column[i1, 0]
        record[i1][4] = cost_column[i1][1]
        record[i1][5] = cost_column[i1][2]
        record[i1][6] = cost_column[i1][3]
        record[i1][7] = cost_column[i1][4]
        column_cost = cost_column[i1, 0]
        column_protection_cost = cost_column[i1][1:4]

        i1 += 1
        return column_cost, column_protection_cost


def floor_system_cost(total_A, floor_composite, beam_fire_cost, fireprotectionbeam_ori):
    # fire protection cost on floor system per sq.ft for different building type
    # fireprotectionbeam_default = [0.86, 0.86, 0.79, 0.79, 0.79, 0.79, 0.79, 0.79]
    # floor_defalut_rsmeans = [27.63, 20.56, 13.99, 13.99, 15.39, 13.99, 15.39, 15.39]
    floor_cost = (floor_composite-fireprotectionbeam_ori)*total_A
    floor_protection_cost = beam_fire_cost*total_A
    return floor_cost, floor_protection_cost



