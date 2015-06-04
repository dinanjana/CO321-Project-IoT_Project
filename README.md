# CO321-Project-IoT_Project
In this project we are building an intelligent home security system which is highly flexible and easy to use.

We built a home security and safety system around a raspberry pi. This device can detect humans through a web cam. 
When this detects a human 1st
              
              
              1) A photo will upload in to google drive - this is a fully automated process.no need of logging in to gdrive
                                                          for authentication. upload() function take cares of this.
                                                      
              2)An sms will be sent to user through a   - This is done by sendSMS() function. Serial communication used to talk 
                                                          with the 3g dongle
                3g dongle.
                
              3)An email will be sent                    - This is done by alertUser() function. SMTP protocol will be used.
