# Twitter Summarizer

## AWS EC2
The API is running on an AWS EC2 instance inside of a docker container. I am using two containers to server the app: one running nginx and one running gunicorn to serve the flask app.

The nginx container is used to forward the HTTP request on port 80 to gunicorn which runs the flask app. This way, I can easily add services to my application in the future by adding containers or making certain subdomains route to different ports using nginx.

You can find the application at: `http://ec2-18-234-114-0.compute-1.amazonaws.com`.

## How To Use
### /
Going to the index page will show "Hello world!" to prove that the server is running. This was mostly used when deploying to see if nginx and gunicorn were properly running and forwarding the request to the flask app.

### /video
We can test the api by running:
```
curl localhost:5000/video?user=elonmusk
```
This will return a json object with a message letting you know that the video has been queued for processing and a URL to view the video which will be available when it finishes. 


### /display
If we browse to the display_url returned when queueing a new video, we can view the video directly in our browser. This is simpler than downloading the video if all you want to do is watch it.

### /videos/VIDEO_ID
This is the endpoint to download the video. It will download the video associated with the VIDEO_ID provided.

### /progress
We can check the progress of the video on the "/progress" endpoint, which will tell us what step of the task it is on and when it finishes. The response looks as follows, where VIDEO_ID is the video UUID:
```
{
    "video_id": VIDEO_ID,
    "status": "In queue",
    "finished": False
}
```
The status is changed as the video is processed to the current stage of the task. The finished variable is set to True when the video is finished.


### Example app
We can see an example of an app using the api in the "web/tests/example_app.py" file. This app simply queues up a video and waits for it to complete and prints the response.
```
$ python3 ./tests/example_app.py

{'display_url': 'http://ec2-3-82-12-125.compute-1.amazonaws.com/display/elonmusk-313be417018546bead43ac4615a11573', 'progress_url': 'http://ec2-3-82-12-125.compute-1.amazonaws.com/progress/elonmusk-313be417018546bead43ac4615a11573', 'response': 'Creating video named elonmusk-313be417018546bead43ac4615a11573.ogg.'}
{'video_id': 'elonmusk-313be417018546bead43ac4615a11573', 'status': "Generating images from elonmusk's tweets", 'finished': False}
Task status: Generating images from elonmusk's tweets
Task status: Generating images from elonmusk's tweets
Task status: Creating video from tweets
Task status: Creating video from tweets
Video is ready! Watch it at http://ec2-3-82-12-125.compute-1.amazonaws.com/display/elonmusk-313be417018546bead43ac4615a11573
```

### Video encoding
By default, the video is encoded into the 'OGG' video file format because it is supported by all browsers. However, we can specify a different encoding by passing the "format" parameter:
```
curl localhost:5000/video?user=elonmusk&format=mp4
```
This will encode the video into an MP4 video instead of an OGG video.

Note: this can cause error with the display page, as it cannot detect your custom format. This will only work with the /videos/VIDEO_ID page to download the video IF you append your custom format. For example, if you chose mp4 as your format:

```
curl localhost:5000/videos/elonmusk-0123456789.mp4 --output elonmusk.mp4
```

### Email
The API can also send an email once the video is finished by adding the "email" parameter:
```
curl localhost:5000/video?user=elonmusk&email=rjewing@bu.edu
```
This will send an email to rjewing@bu.edu when the video finishes.

## Explanation
The API call queues up a task to convert the Twitter user's timeline into a video. A worker running on a seperate thread pulls tasks from this queue and begins the tweet to video conversion. We can configure the number of workers with the NUM_WORKERS config variable.

First the worker pulls the user's timeline and extracts the necessary information from the tweets. It then generates an image for each tweet using the Pillow library. These images are then converted to a video using ffmpeg where each tweet is shown for 3 seconds.

When the video is finished, the video becomes available under the /display/VIDEO_ID path. Additionally, the finished variable from the progress report is set to True. Finally, if an email was provided in the request, the worker sends an email with the link to view the video to the user.

