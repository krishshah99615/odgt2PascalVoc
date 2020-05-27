#Libraries
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import tqdm
import argparse

def xml_to_csv(path):
    xml_list = []
    for xml_file in tqdm.tqdm(glob.glob(path + '/*.xml'),desc="Parsing XML"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df





if __name__=="__main__": 
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True,
        help="Path To xml annotation and images")
    
    
    args = vars(ap.parse_args())
    path = args['path']
    
    
    xml_df = xml_to_csv(path)
    xml_df.to_csv('labels.csv', index=None)
    print('Successfully converted xml to csv.')