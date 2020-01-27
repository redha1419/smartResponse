# Smart Response

Smart Response is made to minimize the overhead time notifying first responders when there has been an incident that is potentially life-threatening. Using the cityIQ API we connected to the Hamilton cityIQ nodes to receive real-time audio and video from nodes around the city. Using the audio data, we trained and implemented a model using Python to detect when there has been a significant event and then notify first responders. The application would then geotag the location of the incident with a real-time image and classify it (car crash, gunshot etc.) based on the audio properties. First responders can view the image to determine the severity of the incident and determine what actions to take next.

![Main Page](https://user-images.githubusercontent.com/24720856/73195437-d7d12b80-40fb-11ea-936d-8712122ac5c2.png)

## Technologies Used

We built this system using many technologies.

Front-end app: React Native and Apple Maps

Back-end: Node.js + express, Python, Math and machine learning libraries such as librosa, openCV, matplolib, scikit, tensorFlow; and finally PostgreSQL for the database

API: We used the cityIQ api to get live audio and images of Hamilton.

## Authors

* **Pavneet Gill** 
* **Reza Shahriari**
* **Matthew Ruigrok**


