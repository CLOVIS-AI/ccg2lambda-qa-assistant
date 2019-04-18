# ccg2lambda QA Assistant: Google Assistant API

This directory contains the Google Assistant API link to the project.

This directory is a heavily-modified copy of the [official repository](https://github.com/actions-on-google/actionssdk-say-number-java),
which is legally allowed by the Apache 2 license that the repository is distributed under. The `LICENSE` file in this
directory is the unmodified license of the original repository.

## Installation

### Prerequisites & configuration

#### Action Console
1. From the [Actions on Google Console](https://console.actions.google.com/), add a new project (this will become your *Project ID*) > **Create Project**.
1. Scroll down > under **More options** select **Actions SDK** > keep **Use Actions SDK to add Actions** modal open

#### GActions CLI

1. [Install the gactions CLI](https://developers.google.com/actions/tools/gactions-cli).

#### GCloud

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
1. Setup the SDK:
    + Run `gcloud auth application-default login` with your Gooogle account
    + Install and update the App Engine component,`gcloud components install app-engine-java`
    + Update other components, `gcloud components update`

#### App Engine Deployment

1. Configure the GCloud: `gcloud init`
1. Deploy:
    + `cd google-assistant`
    + `gradle appEngineDeploy`
1. Open the `action.json` file:
   + If it is missing, copy it from [the official repository](https://github.com/actions-on-google/actionssdk-say-number-java/blob/master/action.json).
   + In the **conversations object** > replace the placeholder **URL** values with `https://<YOUR_PROJECT_ID>.appspot.com`
1. In terminal, run `gactions update --action_package action.json --project <YOUR_PROJECT_ID>`
1. Back in the [Actions console](https://console.actions.google.com), from the **Use Actions SDK to add Actions** window > select **OK**.
1. From the left menu under **Test** > select **Simulator** to open the Actions on Google simulator then say or type `Talk to my test app`.