# Convert .odgt annotations to PASCALVoc
## Convert .odgt annotations from CrowdHuman Dataset to PascalVoc and csv used  tf.records  in Tensorflow Object Detection
[CrowdHuman Dataset](http://www.crowdhuman.org/download.html)

## hbox to label Head[NonMasked] an vbox to label body

* ## How to use
  * convert annotation to xml files
  ```python
    python odgt2xml.py -p <Path to .odgt file>  -m <Path to images>
  ```
  * convert xml files to csv 
  ```python
    python xml2csv -p <Path to xml files>
  ```
