
import streamlit as st

# Import the necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open('database_ori_mat.pkl', 'rb') as f:
    database_ori_mat = pickle.load(f)
with open('totalcost_mat.pkl', 'rb') as f:
    totalcost_mat = pickle.load(f)



# import the matlab file .mat, database_original.mat is a 1*1 struct with 7 fields, inlcude all the original data from 130 simulaitons
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

totalcost_ori = totalcost_mat['totalcost_num']
    # define new vlue in the database
def read_database():
    # Import the necessary packages
    import streamlit as st
    import pandas as pd


    import matplotlib.pyplot as plt
    # Set up the header
    st.header("Economic impact of performance-based structural fire design")
    with st.sidebar:
        # Set up the part for user input file
        st.markdown("## **User Input Parameter**")
        BT = st.number_input("Input Building type", value=1, step=1)

    with st.container():
        st.subheader('Results')
        st.write("---")

        with st.expander('Database Summary'):
            st.write("Building information summary")
            bound = [0, 20, 35, 60, 70, 85, 95, 120, 130]
            low_limit = bound[BT-1]
            up_limit = bound[BT]
            Building_informaiton_df = pd.DataFrame(building_information_ori[low_limit:up_limit,[1,2,4,5,6,8,11,12]],
                                                   columns=['Area (sq.ft)', '# story', 'Total cost ($)', 'sq.ft cost ($)','IBC fire type'
                                                            ,'Building type','beam fire rating','column fire rating'])
            st.table(data = Building_informaiton_df)
            st.write("---")
            st.write("Fire service cost summary")
            Fire_service_cost_df = pd.DataFrame(building_information_ori[low_limit:up_limit,[19,20,21,22,23,24,25]],
                                                columns=['Floor','Column','Partition','Sprinkler','Fire pump','Alarm','Ceiling'])
            st.table(data = Fire_service_cost_df)

        st.write("---")
        st.subheader('Fire protection cost multiplier summary')
        # columns = ["Floor system", "Column"]
        columns = ['Floor system','Column','Partition','Sprinkler','Fire pump','Alarm systems','ceiling']
        chartdata=pd.DataFrame(proportion_ori[low_limit:up_limit, 0:7],
                               columns = ['Floor system','Column','Partition','Sprinkler','Fire pump','Alarm systems','ceiling'])
        st.bar_chart(chartdata, width=0, height=0)

        chartdata=pd.DataFrame(proportion_ori[:, 0:7],
                               columns = ['Floor system','Column','Partition','Sprinkler','Fire pump','Alarm systems','ceiling'])

        st.bar_chart(chartdata, width=0, height=0)
        st.write("---")
        st.subheader('Fire protection cost value summary')
        chartdata_value=pd.DataFrame(costdetails_ori[low_limit:up_limit, 0:7],
                                     columns = ['Floor system','Column','Partition','Sprinkler','Fire pump','Alarm systems','ceiling'])
        st.bar_chart(chartdata_value, width=0, height=0)

        chartdata_value=pd.DataFrame(costdetails_ori[:, 0:7],
                                     columns = ['Floor system','Column','Partition','Sprinkler','Fire pump','Alarm systems','ceiling'])
        st.bar_chart(chartdata_value, width=0, height=0)


def Modify_database():
    st.header("Economic impact of performance-based structural fire design")


    with st.sidebar:
        st.markdown("## **User Input Parameters**")

        # Set up the input for Column Type selected by users

        BI = st.number_input("Input Building index (start from 1)", value=1, step=1, key=3)
        # Set up the inputs for Material Properties
        Building_para_modi = st.checkbox('Modify default building paramter')
        if Building_para_modi:
            col1,col2 = st.columns(2)
            with col1:
                story_height_inp = st.number_input("story height",value=1, step=1)
            with col2:
                total_floor_area_inp = st.number_input("total floor area (sq.ft)",value=1, step=1)
            col1, col2 = st.columns(2)
            with col1:
                bayload_inp = st.number_input("bay total load (kips)")
            with col2:
                building_storys = st.number_input("Building storys",value=1, step=1)
            col1, col2 = st.columns(2)
            with col1:
                baysize1_inp = st.number_input("bay size x direction (ft)",value=1, step=1)
            with col2:
                baysize2_inp = st.number_input("bay size y direction (ft)",value=1, step=1)

            Interpolation_agree = st.checkbox('Enable interpolation when the default building parameter is changed')

        st.write("---")
    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("bar chart,table, Construction cost of different components")


def User_defined_building():
    st.header("Economic impact of performance-based structural fire design")

    # Set up the second section on the left part
    with st.sidebar:
        # Set up the part for user input file
        st.markdown("## **User Input File**")
        uploaded_file = st.file_uploader("Choose a file")
        Thickness_method = st.selectbox(
            'How would you like to calculate the protection thickness',
            ('Use thickness adjust equation', 'Thickness is given', 'RSMeans default value'))
        if Thickness_method == 'Use thickness adjust equation':
            col1, col2 = st.columns(2)
            with col1:
                cost_a = st.number_input("Cost equation parameter a")
            with col2:
                cost_b = st.number_input("Cost equation parameter b")




        if uploaded_file is not None:
            st.write(uploaded_file)
            st.write(uploaded_file.type)
            fileExtension = uploaded_file.type

            # Add a button for the user to process
            if st.button("Process"):
                if fileExtension == 'text/plain':
                    # Read the text file in byte type
                    # rawtext = uploaded_file.read()

                    # Read the text file and convert as string type
                    rawtext = str(uploaded_file.read(), "utf-8")


                if fileExtension == 'text/csv':
                    # Read the table in csv file
                    csvdata = pd.read_csv(uploaded_file)
                    csvarray = np.asarray(csvdata)
                    coldata = csvarray[:,2]
                    targdata = "W16"
                    # finddata = FindIndexfromList(coldata, targdata)
    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("bar chart, Construction cost of different components")



def direct_damage_loss():
    st.header("Economic impact of performance-based structural fire design")


    with st.sidebar:
        # Set up the part for user input file
        st.markdown("## **User Input Parameter**")

        uploaded_file_fragility = st.file_uploader("Choose a file with fragility functions (column: probability, row: damage state)")
        fire_load_distribution = st.selectbox(
            'How would you like to define the fire load distribution',
            ('Use given distribution', 'Upload file'))
        if fire_load_distribution=='Upload file':
            uploaded_file_fire = st.file_uploader("Choose a file")

        DS = st.number_input("Input number of damage states", value=1, step=1)

        # Display a text area for the user to input the array
        array_input = st.text_area("Enter your damage state value (comma-separated):")
        # Process the input and convert it into a NumPy array
        if array_input:
            try:
                input_list = [float(item.strip()) for item in array_input.split(',')]
                input_array = np.array(input_list)
                st.write("Input Array:", input_array)
            except ValueError:
                st.write("Invalid input. Please enter a valid comma-separated list of numbers.")

    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("bar chart, curve of fragility function")
        st.write("---")
        st.write("curve of vulnerability function")
        st.write("---")
        st.write("bar chart, fire load in 1000 times")
        st.write("---")
        st.write("bar chart, distribution of loss in 1000 times ")
        st.write("---")
        st.write("table, annual loss ")


def indirect_damage_loss():
    st.header("Economic impact of performance-based structural fire design")

    with st.sidebar:
        # Set up the part for user input file
        st.markdown("## **User Input Parameter**")

        indirect_damage_method = st.selectbox(
            'How would you like to define unit labor hour of fire protection',
            ('Use default value', 'input own'))

        if indirect_damage_method == 'input own':
            labor_hour_unit = st.number_input("Input labor hour needed for sq.ft fire protection")
        Unit_rent_loss = st.number_input("Input rent loss per hour per sq.ft")

    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("bar chart, indirect damage loss in present value with respect to the affected days/hours")


def maintenance_cost():
    st.header("Economic impact of performance-based structural fire design")

    with st.sidebar:
        st.markdown("## **User Input Parameter**")

        maintenance_cost_method = st.selectbox(
            'How would you like to define maintenance cost',
            ('Constant percentage of total construction cost', 'input own value with respected to year'))

        if maintenance_cost_method == 'Constant percentage of total construction cost':
            maintenance_cost_annually_percentage = st.number_input("Input percentage as initial construction cost")

        if maintenance_cost_method == 'input own value with respected to year':
            uploaded_file_maintenance = st.file_uploader(
                "Choose a file with maintenance cost and year (value in future)")
    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("bar chart, maintenance_cost with respected to year")

def cobenefits():
    st.header("Economic impact of performance-based structural fire design")

    with st.sidebar:
        st.markdown("## **User Input Parameter**")
        cobenefits_method = st.selectbox(
            'How would you like to define cobenefits cost',
            ('Default method', 'input own value'))
        if cobenefits_method == 'Default method':
            st.write("you select default method")
        if cobenefits_method == 'input own value':
            cobenefits_value = st.number_input("Input labor hour needed for sq.ft fire protection")
    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("cobenefits_value")

def astm_index():
    st.header("Economic impact of performance-based structural fire design")

    with st.sidebar:
        st.markdown("## **User Input Parameter**")
        astm_index_method = st.selectbox(
            'How would you like to input cost value (present value)',
            ('type value', 'upload file with given format'))
        if astm_index_method == 'type value':

            CI_alt = st.number_input("Input initial construction cost for alternative design")
            CI_ref = st.number_input("Input initial construction cost for reference design")
            DD_alt = st.number_input("Input direct damage loss for alternative design")
            DD_ref = st.number_input("Input direct damage loss cost for reference design")
            ID_alt = st.number_input("Input indirect damage loss for alternative design")
            ID_ref = st.number_input("Input indirect damage loss cost for reference design")
            CM_alt = st.number_input("Input maintenance cost for alternative design")
            CM_ref = st.number_input("Input maintenance cost  for reference design")
            CB_alt = st.number_input("Input co-benefit for alternative design")
            CB_ref = st.number_input("Input co-benefit cost for reference design")

            net_b = DD_ref + ID_ref-CB_ref - DD_alt - ID_alt + CB_alt
            net_c = -CI_ref - CM_ref + CI_alt + CM_alt
            pvlcc = [0, 0]  # Initialize the list

            pvlcc[0] = CI_ref + CM_ref + DD_ref + ID_ref - CB_ref
            pvlcc[1] = CI_ref + CM_ref + DD_alt + ID_alt - CB_alt

            bcr = net_b / net_c
            pnv = net_b - net_c


        if astm_index_method == 'upload file with given format':
            astm_index_method_file = st.file_uploader(
                "Choose a file with all the cost data")

    with st.container():
        st.subheader('Results')
        st.write("---")
        st.write("BCR,LCC,PNV of provided design values")


page_names_to_funcs = {
    "Construction cost estimation: Read_database": read_database,
    'Construction cost estimation: Modify database': Modify_database,
    "Construction cost estimation: User defined building": User_defined_building,
    "Damage estimation: Direct Damage": direct_damage_loss,
    "Damage estimation: Indirect Damage": indirect_damage_loss,
    "Maintenance estimation": maintenance_cost,
    "Co-benefits estimation": cobenefits,
    "ASTM index calculation": astm_index
}

demo_name = st.sidebar.selectbox("Choose a sub tool", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()