# Introduction

It seems that many other people, in addition to myself, want to use Google Drive as a backup solution.  I expect that this is because, depending upon your specific requirements, at the moment, Google Drive is less expensive per gb than other alternatives, such as Amazon S3.  This may change over time.  However, Google Drive is not only not marketed as a robust backup solution, but Google appears to be actively discouraging its use as such.  Please see comments in forums here:

https://productforums.google.com/forum/#!topicsearchin/drive/backup$20solution

# How to Use Google Drive as a robust automated backup solution anyway

For any backup system you employ, it is strongly recommended that the system be fully automated.  If you want to use Google Drive as a robust automated backup solution, there are a few issues you're going to have to work out specific to your individual requirements.  First you will probably want to create batch (.bat) file(s) (for Windows) or a shell script(s) (.sh) for Linux to and run these from a Scheduled Task(s) (Windows) or Cron Job (Linux) to automate your backup.  You're probably also going to need a local storage location to backup to.  To backup a couple of Windows machines I created automated scripts using disk2vhd.exe (a free SysInternals tool) as well as a number of other customized tools and scripts.  I backed these files up to a local NAS.  Further I encrypted these backups using 7zip (also free.)  I used administrative tools on the NAS to migrate this data (automatically and scheduled) to a separate share on the NAS that the original machines did not have credentials to access.  This was done to prevent any potential ransomware from being able to access my backup data.  However, I also required that my encrypted data be automatically stored in the cloud and I chose Google Drive based on cost and the amount of data that I needed to store.  Your requirements may vary.  In order to automate using Google Drive as a backup solution, I needed to solve three problems.  Judging by the mentions in the Google Drive forums, I was not the first to address these issues.

# Google Drive Desktop Application does not synch from a SMB Share

The first problem I ran into was that Google Drive for Mac/PC supports only HFS+ (on OS X) and NTFS (on Windows). There is currently no support for network volumes (e.g. SMB or NFS) or other file systems such as FAT32.  https://support.google.com/a/answer/2490100?hl=en  This meant that I would have to create another automated batch script to copy files from my NAS to another physical disk on a different machine in order to support the local Google Drive Desktop Application.  In my case I decided to do this and let the Google Drive Desktop Application do the automated heavy-lifting of synching all of my files to my Google Drive.  However, another alternative would be to write a python script (for example) to copy files directly from the network share to Google Drive.  This would be reproducing the functionality of the Google Drive Desktop Application, but adding support for network volumes.  In my case these uploads or synchronization jobs run for days so the script would need to include functionality to gracefully recover from short network outages.  I opted not to do this and instead bought another external drive to stage the data and then used the Google Drive Desktop Application to synch these files to Google Drive.  I created another batch job to move the data from the network share volume to the mapped external drive.

# Google Drive has no way to programmatically or automatically empty the trash or disable the trash, other than the Google Drive API

In order to not run out of space on Google Drive, I have regularly scheduled batch files that delete older data from the NAS and the local storage synched to Google Drive.  When I run these, Google Drive moves these files to the trash.  However, the trash still uses your Google Drive storage quota.  In a fully automated system, you'd either want the option to permanently delete files, turn-off the trash function, or delete from trash after a certain period of time.  At the time of this writing, Google Drive does not offer this feature.  Here is a link to one of many discussions on the topic on the Google forums:

https://productforums.google.com/forum/#!topic/drive/_pkbcBOHjKo;context-place=topicsearchin/drive/automatically$20delete$20from$20trash

This project includes a python script called emptytrash.py that can be run as a scheduled task or a cron job that will empty the trash, resolving this issue.

# Google Drive does not provide data integrity checking of synched files

It is very important to me that after I have synched all of my files, that I be able to validate the integrity of these files.  I wanted to be able to compare the hashes of the files in the cloud with the hashes of the files stored locally.

This project includes a python script called validate_drive_hashes.py that can be run as a scheduled task or a cron job that will compare these hashes and send me an email confirmation including success or failure.

# Google Drive API

In order to run either of these apps, you will need to enable the Google API for your account, create and authorize Google API credentials, and authorize the application by name.  Save the credentials file to the same directory as the scripts.  I found this process well documented and fairly straight-forward.  Google provides a Python Quick Start guide here:

https://developers.google.com/drive/v2/web/quickstart/python

Detailed documentation of the API is here:

https://developers.google.com/drive/v2/web/about-sdk

# Additional Notes

If Google Drive is actively uploading files when you run the validate_drive_hashes.py script, then the files will fail validation until they are fully synched.  Adjust the timing of your scheduled task or cron job so that you can be sure that the files should have completed uploading when the script is run.

The validate_drive_hashes.py script is hard-coded with email details as well as the path of the local root folder of the Google Drive, so you will need to be update the script for your environment before you run it on your system.

These are sample proof-of-concept scripts.  I am not a very good coder, so there are a lot of details that I have left out of these.  Most of this was taken from other examples I found on the web and I claim no original authorship of this code.  I'd thank and acknowledge those that contributed the originals, but I didn't record that information.  I take no responsibility for how you use these scripts in your own environment and you need to judge their suitability for your application or function.  If you would like to suggest changes/updates or would like git commit permissions to this project, please contact me.
