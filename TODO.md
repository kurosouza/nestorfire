# Todo: nestorfire
+ Extract fire entry from in-memory data without saving to disk
    + Save file to disk. Delete after importing to db
+ Use postgres db 
+ Add rq-dashboard
+ setup DI with punq

+ Add endpoint to query available days
+ Add endpoint to fetch detections-per-country
+ Add endpoint to fetch detections for a specific country for a given day

# Client

+ fire dashboard 

showing:
    - total number of detections (for the last day)
    - total number of countries with fires (for the last day)
    - display map showing fires per country
    - for a given detection, drop a pin and show satellite imagery

# Deployment

+ setup posgres db on dokku instance
+ setup redis instance on dokku instance