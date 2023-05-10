<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/nuttapol-kor/fake-news-project">
    <img src="https://i.imgur.com/KqWANUL.png" alt="Logo" width="80" height="80" style="border-radius:50%">
  </a>

  <h3 align="center">UNFAKE</h3>

  <p align="center">
    Thai Fake news detection and summarization using LINE Bot
    <br />
    <br />
    <a href="https://youtu.be/rq8f50ldQZI">View Demo</a>
    ·
    <a href="https://github.com/nuttapol-kor/fake-news-project/issues">Report Bug</a>
    ·
    <a href="https://github.com/nuttapol-kor/fake-news-project/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![Imgur](https://i.imgur.com/gZ2qXDZ.png)

Right now, Fake news are becoming more and more of a major concern for many countries. Fake news can mislead people and create confusion. People who thought that fake news are true might spread it even more. Elderly people or adults who are not used to new technology will believe in fake news more and spread it to their friends. This happens a lot in LINE groups with elderly people, where they might spread fake news around without thinking or checking first

We mostly use the LINE app for communication between friends and family. We are met with many fake news in a group that contains elderly people or adults. Worse than that, many adults believe in those fake news. There are some news that can affect their health, for example, “Lemon soda can treat cancer”. This will result in further detrimental effects on health.


Here's why:
* We are trying to reduce the spreading of fake news by creating a model that can detect fake news

* We are creating a LINE bot that checks if the news is a fake news.

* We are assist individuals who may have difficulty reading lengthy news articles by providing them with summarized versions

Our project aims to detect and summarize fake news; however, the user is required to manually send the news to our Line bot as it cannot be added to a Line group to filter incoming news. Therefore, as part of our future work, we plan to develop a model for news classification, which will enable our bot to automatically detect news articles and provide a summarized version of the article as well as classify it as real or fake. Once the bot has detected and classified the news, it will then send the result to the user's designated group

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Py][Python]][Python-url]
* [![Fast][FastAPI]][FastAPI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Our Line bot is deployed on AWS Lambda, so you can use our line bot directly by adding our Line bot to your Line account. However, if you want to connect our API with your Line bot account you can follow our instruction below.

### Prerequisites

You have to install the python 3.10 or higher version on your machine and run the below command to make sure that your python is installed on your machine.

* check your python version
  ```sh
  python --version
  ```

  or 

  ```sh
  python3 --version
  ```

Install ngrok -> https://ngrok.com/download

### Installation

If python is installed on your machine. You are ready to do a following instruction

1. Clone the repo
   ```sh
   git clone https://github.com/nuttapol-kor/fake-news-project.git
   ```

2. Sign up Line Developer account at https://developers.line.biz/console/

3. Create a provider and message API channel. then get the chanel access token

4. Create `.env` in `./line_bot/unfake_bot` and enter your chanel access token
   ```env
   CHANNEL_ACCESS_TOKEN='ENTER YOUR Chanel Access Token';
   ```

5. change directory to `./line_bot/unfake_bot`

   ```sh
   cd line_bot/unfake_bot
   ```

6. Install the necessary modules

   ```sh
   pip install -r requirements.txt
   ```

7. Run the server

   ```sh
   python main.py
   ```

8. Open ngrok and run this command

   ```sh
   ngrok http 8000
   ```

9. Copy the endpoint in forwarding

   ![Imgur](https://i.imgur.com/z8RVuz2.png)
   
   add `/webhook` behide the link for example `https://3866-2001-fb1-b8-f4a6-c8c3-b63e-134a-51f2.ap.ngrok.io/webhook`

   and put the following link in to your Line Messaging API

   ![Imgur](https://i.imgur.com/0kgofZ4.png)

10. Happy with our Line bot!!

<!-- USAGE EXAMPLES -->
## Usage

You can send news as a text message to the line bot to check the news is fake or not. Our bot will send the response and confidential score

![Imgur](https://i.imgur.com/KgYKTUU.png)

As you can see, the response message has a result and "สรุปข่าว" button. When user click on the button, our bot will send the summarize news message to the user.

![Imgur](https://i.imgur.com/9fhKB0G.png)

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Nuttapol Korcharoenrat - nuttapol.kor@ku.th

Purich Trainorapong - purich.t@ku.th


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

We would like to acknowledge the support of Department of Computer Engineering, Kasetsart University for providing us all software development and technical knowledge and also the opportunity to prepare the project.

We would like to express our deepest gratitude to our advisor Asst.
Prof. Dr. Paruj Ratanaworabhan for his mentorship throughout this project.

We are highly indebted to Assoc. Prof. Pradondet Nilagupta for the
guidance and encouragement as well as providing necessary information
in making our project.

Last but not the least, we would like to thank our faculty professors
who always gave us valuable knowledge and every important details of
Software and Knowledge Engineering.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/