#Libraries
import json
import pandas as pd
import os
import xml.etree.ElementTree as xml
from tqdm import tqdm
from PIL import Image
import argparse

#Create xml files for individual images
def create_pascal_voc_xml(o_name,imdir):
    
    #Create a folder for imgs if  dir doesnt exust
    if not os.path.exists(imdir):
        os.makedirs(imdir)
    
    #open the  odgt file
    data= open(o_name,'r')
    
    #Create list of all individual jsons
    json_list=[]
    for i in tqdm(data,desc='Loading Jsons'):
        json_list.append(json.loads(i))
    
    #Create xml files according to pascal Voc
    for i in tqdm(json_list,desc='Xml Creation'):
        
        root=xml.Element('annotation')
    
        folder=xml.Element('folder')
        folder.text=imdir

        fname=xml.Element('filename')
        fname.text=i['ID']+'.jpg'
        
        

        p=xml.Element('path')
        p.text=os.getcwd()+'/'+imdir

        source=xml.Element('source')
        db=xml.SubElement(source,'database')
        db.text='Unknown'
        
        img_path=imdir+'/'+i['ID']+'.jpg'
        im = Image.open(img_path)
        W, H = im.size
        #print(img_path)
        #print(W,H)
        
        size=xml.Element('size')
        width=xml.SubElement(size,'width')
        width.text=str(W)
        height=xml.SubElement(size,'height')
        height.text=str(H)
        depth=xml.SubElement(size,'depth')
        depth.text='3'


        seg=xml.Element('segmented')
        seg.text='0'
        root.append(folder)
        root.append(fname)
        root.append(p)
        root.append(source)
        root.append(size)
        root.append(seg)
        
        for gtbox in i['gtboxes']:
            
            if gtbox['tag']=='person':
                
                #For Body
            
                obj = xml.Element('object')
                name = xml.SubElement(obj,'name')
                name.text = 'Body'
                pos =xml.SubElement(obj,'pose')
                pos.text = 'Unspecified'
                trunc=xml.SubElement(obj,'truncated')
                trunc.text ='1'
                difficult = xml.SubElement(obj,'difficult')
                difficult.text ='0'
                bndbox = xml.SubElement(obj,'bndbox')
                xmin=xml.SubElement(bndbox,'xmin')
                xmin.text=str(gtbox['vbox'][0])
                ymin=xml.SubElement(bndbox,'ymin')
                ymin.text=str(gtbox['vbox'][1])
                xmax=xml.SubElement(bndbox,'xmax')
                xmax.text=str(gtbox['vbox'][0]+gtbox['vbox'][2])
                ymax=xml.SubElement(bndbox,'ymax')
                ymax.text=str(gtbox['vbox'][1]+gtbox['vbox'][3])
                root.append(obj)
                
                #For NonMask[Head] in individual bodies
                obj = xml.Element('object')
                name = xml.SubElement(obj,'name')
                name.text = 'Unmasked Head'
                pos =xml.SubElement(obj,'pose')
                pos.text = 'Unspecified'
                trunc=xml.SubElement(obj,'truncated')
                trunc.text ='0'
                difficult = xml.SubElement(obj,'difficult')
                difficult.text ='0'
                bndbox = xml.SubElement(obj,'bndbox')
                xmin=xml.SubElement(bndbox,'xmin')
                xmin.text=str(gtbox['hbox'][0])
                ymin=xml.SubElement(bndbox,'ymin')
                ymin.text=str(gtbox['hbox'][1])
                xmax=xml.SubElement(bndbox,'xmax')
                xmax.text=str(gtbox['hbox'][0]+gtbox['hbox'][2])
                ymax=xml.SubElement(bndbox,'ymax')
                ymax.text=str(gtbox['hbox'][1]+gtbox['hbox'][3])
                root.append(obj)
                
        
        tree=xml.ElementTree(root)
        
        #Storing xmls
        with open(os.path.join(imdir,i['ID']+'.xml'),'wb') as files:
            tree.write(files) 
if __name__=="__main__": 
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True,
        help="Path To annotation .odgt file")
    ap.add_argument("-i", "--image", required=True,
        help="Path To images")
    
    args = vars(ap.parse_args())
    path = args['path']
    i_path = args['image']
    
    create_pascal_voc_xml(path,i_path)   
        
        
            
            
            
            