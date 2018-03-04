#Inspiration
Current surveillance and control still require human intervention. This project presents automatic detection of possible criminal activities across all the areas for following reasons:

Surveillance: For keeping track of types of criminal activities occurring in the nearby regions.
Control: Alerting nearby patrolling officers about the possible threats to minimize the crimes. To put it more technical, we aim to minimize the number of false positives that occur in the detection to increase the prediction.

#What it does
The real-time video stream is fed to the application from security cameras. The application will start tracking the video in frames and detects if the scene has any harmful weapon.Statistical data is generated from relevant information extraction from previous records of criminal events. Weighted probability of the person having the weapon and crime rate in the area, a local authority will be notified. Moreover, the application does consider Emotion Analytics while evaluating the probability of the possible threat. If the probability is beyond the threshold, an alert event is triggered to notify local security services.

#How we built it
The application is written in Python. Real Time video streaming and Frame extraction are done using OpenCV.
Weapon detection is powered by Custom Computer Vision Learning from Microsoft Cognitive Services.
Used Microsoft Text Analytics API for text extraction and determined the relevant information score.
Trained our model on custom DataSet using Custom Vision services.
Video Frame data is stored in the Azure Cloud Storage.
Creating alert using Twilio Messaging API.
Challenges we ran into
Picking correct frames from the real-time for the analysis and Handling all the processing asynchronously was one of the challenges.

#Accomplishments that we're proud of
We have achieved 85% accuracy in weapon detection and 95% accuracy in detecting the face and emotion of the person.

#What we learned
We experienced the power of cognitive vision and text learning. Microsoft Custom Vision API allowed us to train model according to the requirement of the application.

#What's next for Live Streaming Criminal Activity Analysis.
Having built such a system, it can be improved by incorporating Active Learning - collecting feedback on system generated alert.