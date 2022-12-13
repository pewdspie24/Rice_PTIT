# Rice_PTIT
<br />

The project includes 6 types of model in order to find out the best model for Rice Leaf Classification. Also, an API for data collector is also available for using
Dataset link for download: https://ptiteduvn-my.sharepoint.com/:f:/g/personal/quangtd_b18cn485_stu_ptit_edu_vn/EnSQUz7vHCRGgrOfvQ1HLEIB4Fxhzm7kVMes72ZDFHlcFw?e=efKPwu

## Instruction for using Data Collector API

Access address `https://203.162.88.122:18008/` to using API. As a demo, the interface is pretty simple because it's meant to be used in other applications

![Main](https://gcdnb.pbrd.co/images/Zomc0Di9PcOB.png?o=1 "Main")

It has 2 main functions: Predict and Save. 

- Predict can be used when we need to predict some rice leaf image and get the score as a JSON string, which is include 4 types of diseases and their correspondence scores. The flow can be described by 3 steps:
    1. Choosing image by click on button `Choose` or `Chọn tệp`. It's worth to know that you can only choose one image at a time:
    ![Choosing](https://gcdnb.pbrd.co/images/gBpRnAXIFZse.png?o=1 "Choosing")
    2. Click `predict` button to get prediction:
    ![After Choosing](https://gcdnb.pbrd.co/images/XJ5b0siCI69Z.png?o=1 "After Choosing")
    3. The result will be shown in JSON string format as below. The higher the score, the more likely it is predicted to that class by model:
    ![After Choosing](https://gcdnb.pbrd.co/images/fMNGDaLhL5yx.png?o=1 "After Choosing")
- Save can be used when we are sure about the class of image we upload. The flow can be described by 3 steps:
    1. Choosing image just like step 1 on predict task.
    2. Choose class name like below and click `save` to continue:
    ![After Choosing for Save](https://gcdnb.pbrd.co/images/sxEaE0E4N6Ji.png?o=1 "After Choosing for Save")
    3. A message will be shown to prove that the image has been save on the server with exact class name you chose before.
    ![Save message](https://gcdnb.pbrd.co/images/YF0fSlxwkyfn.png?o=1 "Save message")
    
