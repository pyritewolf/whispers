# Setting up the Google project

We use Google's APIs to authenticate a user with Youtube and fetch their videos and chats. These instructions will help you set up all necessary configurations to get an instance of this project working.

If you're setting up things for a local environment, wherever it says `{YOUR_DOMAIN}` you should use `localhost:5000`. If you're setting up a live environment, assume this to be your environment's domain.

## Creating a Google Project

Head over to the [Google Console](https://console.cloud.google.com/) (you might wanna bookmark that one). In the upper left area, next to the platform's logo you should find a button that will allow you to create a Project. This project will englobe all the keys and features you'll be using.

The creation will take a hot minute, go put a kettle on for mate 🧉

## Enabling APIs

Once the project is created, from the [dashboard](https://console.cloud.google.com/home/dashboard) head to "APIs and Services" on the menu to the left. Enter the "Library". You want to add to your project the "YouTube Data API".

Bear in mind that the quota for all things Youtube-related is of 10000 requests per day.

## Setting up OAuth

To allow users to sync up their Google / YouTube accounts with the system we'll be using OAuth.

### The consent screen

<div float="right">
![Always ask for consent](https://c.tenor.com/SqU2FTBPU5sAAAAC/critical-role-crit-role.gif)
</div>
Whenever you authorize something to interact with Google, you get that nice auth screen where you click "yes, i'm giving all my data to this random stranger on the internet!!". You configure that one by heading from the Dashboard to "APIs & Services" and then "OAuth consent screen".

You won't have to configure much here, but do be make sure to include:

- The app name (Whisper)
- The `/auth/userinfo.email`, `/auth/youtube.readonly` and `/auth/youtube` scopes
- Any test users you want to enable, if you're working on the development version of the app

### Credentials

For the final step, you'll need to head over to Credentials on the left. Click on "Create credentials", make them OAuth credentials. It's important that in your Redirect URIs you include `http://{YOUR_DOMAIN}/oauth/google/callback`.

Once that's done, you'll get a Client ID and Secret that you can configure in your project's environment variables as `GOOGLE_OAUTH_CLIENT` and `GOOGLE_OAUTH_SECRET`
