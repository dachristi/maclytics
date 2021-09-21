# maclytics

Software designed to capture Wi-Fi MAC addresses from unauthenticated devices in an effort to help retailers measure
* Unique Visitor Count
* Repeat Visitor Count
* Average Dwell Time

This information can be useful for managers in charge of optimizing operations, improving the shopping experience, and ultimately driving the bottom line.

Note that manufacturers have implemented MAC address randomization techniques to protect users' privacy.  While I 100% agree with consumer privacy protections, these changes reduce the effectiveness and quality of aggregate tools such as this one.

The software is build on a Linux/Python/MySQL stack and has been successfully deployed on a laptop as well as Raspberry Pi.  Edge devices with internet connectivity can transfer data to a remote server, alternatively a local network can be created with a local server to process and build reports on-site.

