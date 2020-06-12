# s3dataviewer
A web based viewer tool to view data stored on s3

# requirements
This is tool for easing viewing and manipulation of large amounts of data stored on s3. Version 1 of the tool should aim to have the following features: 
  - (~done) All aspects of the tool shall support large amounts of images. Both single images that are large in size (~100MB) and large amounts of images (>1,000,000). 
  - (not yet done) Support batch operations on images. Move, copy, delete images on S3 and operations on images such as crop, transform, convert format.
  - (somewhat done) Selection, search, query and filter opertions. Ability to filter out results with regex on key names. Pagination and image downsampling and sizing. 
  - The tool should support many of the common image formats, as well as buckets with mixed formats
  - (done) Users can write custom bokeh applications to render any kind of visualization from their data
---

 # architecture
The tool has an angular web based frontend. There is a backend python aiohttp server for indexing a bucket/prefix on s3. 
There is another python server running bokeh. Custom bokeh applications can be crated to render different types of data.

# running
First set the AWS environment credentials in the docker-compose.yml file. The 
AWS credentials must grant read access to S3.

Docker and docker-compose must be installed

Then run

`docker-compose up`

Then navigate in a browser to

http://localhost:8888

Enter and S3 bucket and prefix. Then build the index, then request the plots.
 
You can create a new visualization for a custom type of data object by creating a new bokeh app. 
The bokeh app are located in 

bokeh-backend/s3DataViewerPlotServer/apps

Currently the only type of data for which rendering is supported is images
 ## backend 
  The backend will coordinate all S3 and image transform operations using a jobs scheduler. It will also manage a bokeh server that will handle generating all image plots and live downsampling of large images as required using datashader. 
  
  The backend will have a REST API defined via swagger. The API architecture will be built out in a way that makes sense as the tool is built. Since the tool will make heavy use of the boto3 pacakge, the REST api will be somewhat built out as a wraper around that API.
  
  Instructions for running backend:
  
    In the backend directory run 
    
    docker build . -t s3DataViewerBackend
    
    Then to run the server
    
    docker run -it -p 8080:8080 s3DataViewerBackend
    
    REST API docs can be found at
    
    http://localhost:8080/api/docs
    
   
   Instructions for running bokeh server:
    
    In the bokeh-backend directory run 
    
    docker build . -t s3bokehplotserver
    
    Then to run the bokeh server
    
    docker run -it -p 5006:5006 s3bokehplotserver

    
 ### rest api design
 
    - endpoints 
        /plots - GET
            
            gets a list of bokeh html plots to be embedded in fronend web app
        
            - parameters
                - bucket
                - bucket prefix
                - key filter regex (probably can't be url encoded)
                - sort
                - order
                - limit
                - offset
                
        /ping - GET
            
            get the status to see server is up
            
        /index - PUT
            
            builds the index of and s3 bucket/prefix 
         
                
          
        

