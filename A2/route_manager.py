##!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: chetavdic
@author: V00968783
"""
import sys
import pandas as pd
import numpy as np
import yaml 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



def sample_function(input: str) -> str:
    """Sample function (removable) that illustrations good use of documentation.
            Parameters
            ----------
                input : str, required
                    The input message.

            Returns
            -------
                str
                    The text returned.
    """
    return input.upper()



def main():
    """Main entry point of the program."""

    interpret_args()


def interpret_args() -> None:
    """Function that calls yamlToDataFrame to load all data into dataframes. It then interprets given arguments to call each individual question passing the dataframes as parameters.
       If q1-q5 is not found, prints error message.
    """
    airlines_df,airports_df,routes_df = yamlToDataFrame()

    if len(sys.argv) > 1:

        question_param = sys.argv[4]

        if "--QUESTION=q1" in question_param:
            q1(airlines_df,airports_df,routes_df)

        elif "--QUESTION=q2" in question_param:
            q2(airlines_df,airports_df,routes_df)

        elif "--QUESTION=q3" in question_param:
            q3(airlines_df,airports_df,routes_df)

        elif "--QUESTION=q4" in question_param:
            q4(airlines_df,airports_df,routes_df)

        elif "--QUESTION=q5" in question_param:
            q5(airlines_df,airports_df,routes_df)

        else:
            print("ERROR. PLEASE ENTER VALID QUESTION NUMBER")



def q1(airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame) -> None:
    """Function that performs pandas operations to produce formatted q1.csv and calls makeGraph to produce q1.pdf.
            Parameters
            ----------
                airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame

            Returns
            -------
                None
    """
    airlines_df.drop(['airline_country'],inplace = True, axis = 1)
    airports_df.drop(['airport_city','airport_name','airport_altitude'],inplace = True, axis = 1)

    merged_df = pd.merge(airlines_df, routes_df, left_on='airline_id', right_on='route_airline_id')

    merged_df = pd.merge(merged_df,airports_df, left_on = 'route_to_airport_id', right_on = 'airport_id')

    merged_df = merged_df[merged_df['airport_country']=='Canada']

    answer_df = merged_df.groupby(['airline_name','airline_icao_unique_code']).size().reset_index(name='statistic').sort_values(['statistic','airline_name'], ascending=[False,True]).head(20)

    answer_df.rename(columns={'airline_name':'subject'},inplace = True)
    answer_df['subject'] = answer_df['subject'] + ' (' +answer_df['airline_icao_unique_code'] + ')'
    answer_df = answer_df.drop(columns=['airline_icao_unique_code'])
    answer_df.to_csv('q1.csv', index = False)

    makeGraph(answer_df,'q1','Top 20 airlines that offer the greatest number of routes with destination country as Canada','Airlines','Routes to Canada',0.3,0.4,0.9,0.7)




def q2(airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame) -> None:
    """Function that performs pandas operations to produce formatted q2.csv and calls makeGraph to produce q2.pdf.
            Parameters
            ----------
                airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame

            Returns
            -------
                None
    """

    airlines_df.drop(['airline_name','airline_icao_unique_code'], inplace = True, axis =1)
    airports_df.drop(['airport_name','airport_city','airport_altitude','airport_icao_unique_code'], inplace = True, axis =1)
    
    merged_df = pd.merge(airports_df,routes_df, left_on = 'airport_id', right_on = 'route_to_airport_id')

    merged_df['airport_country'] = merged_df['airport_country'].str.strip() 

    answer_df = merged_df.groupby(['airport_country']).size().reset_index(name='statistic').sort_values(['statistic','airport_country'], ascending = [True,True]).head(30)

    answer_df.rename(columns={'airport_country':'subject'},inplace = True)
    answer_df.to_csv('q2.csv', index = False)

    makeGraph(answer_df,'q2','Top 30 countries with least appearances as destination country on the routes data','Countries','Appearances as destination country',0.3,0.4,0.9,0.7)



def q3(airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame) -> None:
    """Function that performs pandas operations to produce formatted q3.csv and calls makeGraph to produce q3.pdf.
            Parameters
            ----------
                airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame

            Returns
            -------
                None
    """

    airlines_df.drop(['airline_name','airline_icao_unique_code'], inplace = True, axis = 1)

    merged_df = pd.merge(airports_df,routes_df, left_on = 'airport_id', right_on = 'route_to_airport_id')

    answer_df = merged_df.groupby(['airport_name','airport_icao_unique_code','airport_city','airport_country']).size().reset_index(name='statistic').sort_values(['statistic','airport_name'],ascending = [False,True]).head(10)

    answer_df['subject'] = answer_df['airport_name'] + ' (' + answer_df['airport_icao_unique_code'] + '), ' + answer_df['airport_city'] + ', ' + answer_df['airport_country']
    answer_df = answer_df[['subject', 'statistic']]
    answer_df.to_csv('q3.csv', index=False)

    makeGraph(answer_df,'q3','Top 10 destination airports','Airports','Appearances as destination airports',0.3,0.6,0.9,0.9)



def q4(airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame) -> None:
    """Function that performs pandas operations to produce formatted q4.csv and calls makeGraph to produce q4.pdf.
            Parameters
            ----------
                airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame

            Returns
            -------
                None
    """

    airlines_df.drop(['airline_name','airline_icao_unique_code'], inplace = True, axis = 1)

    merged_df = pd.merge(airports_df,routes_df, left_on = 'airport_id', right_on = 'route_to_airport_id')

    answer_df = merged_df.groupby(['airport_city','airport_country']).size().reset_index(name='statistic').sort_values(['statistic','airport_country'],ascending = [False,True]).head(15)

    answer_df["subject"] = answer_df["airport_city"] + ", " + answer_df["airport_country"] 
    answer_df = answer_df[['subject', 'statistic']] 
    answer_df.to_csv('q4.csv', index=False, header=['subject', 'statistic'])

    makeGraph(answer_df,'q4','Top 15 destination cities','Cities','Appearances as destination city',0.3,0.6,0.9,0.9)



def q5(airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame) -> None:
    """Function that performs pandas operations to produce formatted q5.csv and calls makeGraph to produce q5.pdf.
            Parameters
            ----------
                airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame

            Returns
            -------
                None
    """

    airports_df['airport_altitude'] = pd.to_numeric(airports_df['airport_altitude'], errors='coerce')

    merged_df= pd.merge(routes_df,airports_df,left_on='route_to_airport_id', right_on='airport_id')

    merged_df= pd.merge(merged_df,airports_df,left_on='route_from_aiport_id', right_on='airport_id')

    merged_df = merged_df[(merged_df['airport_country_y'] == 'Canada') & (merged_df['airport_country_x'] == 'Canada')]

    altitude_diff: float = abs(merged_df['airport_altitude_x'] - merged_df['airport_altitude_y'])

    merged_df['altitude_diff'] = altitude_diff

    merged_df.drop(['route_airline_id','route_airline_id', 'route_from_aiport_id', 'route_to_airport_id',
       'airport_id_x', 'airport_name_x', 'airport_city_x', 'airport_country_x','airport_id_y',
       'airport_name_y', 'airport_city_y', 'airport_country_y'], inplace = True, axis = 1)

    answer_df = merged_df.sort_values('altitude_diff',ascending = False).head(10)

    answer_df['subject'] = answer_df['airport_icao_unique_code_y'] + '-' + answer_df['airport_icao_unique_code_x']
    answer_df['statistic'] = answer_df['altitude_diff']
    answer_df = answer_df[['subject', 'statistic']] 
    answer_df.to_csv('q5.csv', index=False)

    makeGraph(answer_df,'q5',' Unique top 10 Canadian routes with most difference between the destination altitude and the origin altitude','Routes','Altitude_difference',0.3,0.6,0.7,0.9)



def yamlToDataFrame() -> tuple:
    """This function opens each required yaml file, safely loads it as a dictionary, and converts the dictionary to DataFrame using json.normalize(). It then replaces all values of backslash N with NaN.
        Assumes files are correctly named as given in assignment description.
            Parameters
            ----------
                None

            Returns
            -------
                Tuple[airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame]
    """

    with open('airlines.yaml') as file:
        airlines = yaml.safe_load(file)

    airlines_dict_df = pd.DataFrame(airlines)

    airlines_df = pd.json_normalize(airlines_dict_df['airlines'])

    with open ("airports.yaml") as file:

        airports = yaml.safe_load(file)

    airports_dict_df = pd.DataFrame(airports)

    airports_df = pd.json_normalize(airports_dict_df['airports'])

    with open ("routes.yaml") as file:
        routes = yaml.safe_load(file)

    routes_dict_df = pd.DataFrame(routes)

    routes_df = pd.json_normalize(routes_dict_df['routes'])

    airlines_df = airlines_df.replace(r'\N', np.nan)
    airports_df = airports_df.replace(r'\N', np.nan)
    routes_df = routes_df.replace(r'\N', np.nan)

    return airlines_df, airports_df, routes_df



def makeGraph(input_dataframe_df: pd.DataFrame, question_name:str, graph_title:str, xlab:str, ylab:str, left:int, bottom:int, right:int, top:int)-> None:
    """ This function interprets given GRAPH_TYPE argument and then creates an appropriate graph in pdf form depending on which type is requested. It also sizes it according to values given when called, since different questions
        require different sizings.
        Saves the graph to current directory.
            Parameters
            ----------
                input_dataframe_df: pd.DataFrame, question_name:str, graph_title:str, xlab:str, ylab:str, left:int, bottom:int, right:int, top:int

            Returns
            -------
                None
    """

    desired_graph_type = sys.argv[5]

    if "--GRAPH_TYPE=bar" in desired_graph_type:

        plt.bar(input_dataframe_df['subject'],input_dataframe_df['statistic'])

        plt.xticks(fontsize = 7, rotation=45, ha='right')

        plt.yticks(fontsize = 7)

        plt.xlabel(xlab, fontsize=7)

        plt.ylabel(ylab, fontsize=7)

        plt.title(graph_title, fontsize =7)

        plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=0.2, hspace=0.2)

        filename = question_name + '.pdf'

        with PdfPages(filename) as pdf:
            pdf.savefig()

    elif "--GRAPH_TYPE=pie" in desired_graph_type:

        plt.pie(input_dataframe_df['statistic'], labels=input_dataframe_df['subject'], autopct='%1.1f%%',textprops={'fontsize': 7} )

        plt.title(graph_title, fontsize = 7)

        filename = question_name + '.pdf'

        with PdfPages(filename) as pdf:
            pdf.savefig()

if __name__ == '__main__':
    main()
