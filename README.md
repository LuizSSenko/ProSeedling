# ProSeedling 
## Computerized Seedling Processing for Seed Vigor Analysis

### The ProSeedling software is an advanced tool developed for the analysis of soybean seeds. It features specific characteristics and innovative functions such as: Superior Seedling Detection:

- ProSeedling is capable of detecting features of interest even with low contrast between the color of the seedling and the background. Unlike other similar software, it uses the germination paper itself to acquire images of the seedlings, ensuring high performance in evaluations.

<img src="https://github.com/LuizSSenko/ProSeedling/assets/140913035/f22d0cd3-1548-4e79-aa39-8f13701fdc9f" width=100% height=100%>


## Minimizing Damage to Seedlings:

- A major advantage of ProSeedling is its ability to minimize the handling of seedlings during the analysis process. This is important as it reduces the risk of damage to the seedlings, which can affect the accuracy of the analysis results.

## User-Friendly Interface:

- The software also includes a user interface, designed with PyQT5, to facilitate user interaction with the system. This makes ProSeedling accessible not just to specialized researchers, but also to other users who may be interested in seed analysis.

## Data Processing and Analysis:

- ProSeedling employs various open-source libraries for image processing and data manipulation. For instance, it uses OpenCV for image processing, Numpy and Scipy for numerical calculations, and Pandas for tabular data manipulation. This allows for comprehensive and detailed analysis of the captured images.


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/f5e28b9f-5f94-4861-ab3d-253ce653339d)


![image](https://github.com/user-attachments/assets/77b77790-8031-4b87-b5f0-9cb217f32e1f)



![image](https://github.com/user-attachments/assets/bd5ef4d2-f820-4206-9e02-292f6c0f8d70)



## Proven efficiency:

- ProSeedling, still in its initial development phase, presents remarkable precision and accuracy. Compared to the Vigor-S, which already has proven efficiency for evaluating soybean seedlings, the results of the ProSeedling showed relevant consistency. However, it is essential to highlight the importance of conducting more experiments and improving settings to reach your full potential. A significant differentiator of ProSeedling is its open source nature, enabling researchers and professionals to adjust and adapt the software according to your needs. This feature expands the Future prospects for ProSeedling in the field of seed vigor assessment seeds.
<br/>





<br/>

# Proseedling User Manual
<br/>
<br/>

# Equipment used in the project

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/d452990d-fd1e-4707-b7ec-1d9c0f8a5303)

The equipment used to capture ProSeedling images was specifically designed for acquiring images of seedlings through the principle of transillumination. The equipment comprises an MDF box (Figure A), its interior coated with matte black paint to prevent reflections (Figure B). Positioned in the upper section of the box, at a distance of 33.5 cm from the seeds, is a digital camera equipped with an 8 Mpx SONY IMX179 sensor and a 100º lens. This camera is securely affixed to a movable axis, enabling precise positioning adjustments (Figure B and C). At the bottom of the box, a mobile platform is provided for positioning seedling samples. To complete the setup, a lighting system employing cold white LEDs (6000k), measuring 40 x 40 cm, delivers a total power of 32W with an emission of 2200 lumens (Figure D).

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/978ba012-c7c6-4955-a3c4-9f9f25fff7eb)


The figure above shows an image of three-day-old soybean seedlings, captured using the aforementioned equipment. It is observed that the seedlings are highlighted in the image, allowing adequate segmentation of the image for the subsequent stages of software development


# Calibration process (Pixels to cm)

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/55b33d7b-96ac-4f79-b505-8821a4a3caec)

- Enter the main branch of the ProSeedling project, open the "Calibration" folder, download, and print the .pdf file (Pay attention to choosing the "Standard" option inside the scale section at your printer).

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/20415378-f496-4279-9749-6a339e43cc43)

- Take a picture with your equipment; it does not need to be exactly like ours. ProSeedling has options that allow the user to use diverse types of capturing systems.

![image](https://github.com/user-attachments/assets/8b6c2cc3-8398-4213-8d65-99983276d1d0)


- In the ProSeedling software, choose "Configuration," and then "Set Calibration." Click on "Load Calibration Image" and choose the configuration image captured by your system or enter manually the conversion value of how many pixels there are in 1 cm.

# Capturing images

- As mentioned earlier, your equipment does not need to be like ours; the only requisite is to have controlled light and a fixed camera for all the photos to maintain accuracy and calibration. Don't worry about the illumination spectra either, as ProSeedling gives you the option to adjust the segmentation parameters.

- **IMPORTANT:** It's a good practice to name the seedling images following this pattern: CULTIVAR + SAMPLE + REPETITION
- The repetion needs to be a single letter.

- Also, organize the cultivar by folder, as the software reads the entire folder, the presence of two cultivars will be conflicting.


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/a59e1c1a-d84f-4cab-aba7-3f3ae6315880)


- In this example, the cultivar's name is NEO610IPRO, so I called it "N" + sample number + repetition letter = N1A, N1B... N2A, N2B...


# Color calibration

- Your system will very likely have a different spectrum of illumination. To configure this difference, ProSeedling has an HSV tuning function located in "Configuration," "Set HSV Values."

![image](https://github.com/user-attachments/assets/d9dc6ef4-eaa3-4764-96c8-a9dc276ad09d)


- First, move the sliders of HSV (Hue, Saturation, Value) to filter only the cotyledons.

![image](https://github.com/user-attachments/assets/f6f324d8-e0bb-4132-852c-dc590363661e)


- After filtering the cotyledons, choose the option "Set Values for hypocotyl and root," and do the same: move the slider until you get the seedling image.
- As seen in the image above, some artifacts will be selected too, which is not a problem as ProSeedling will filter them out.

# Image analysis

- Click on "File" and then "Open Folder," after which you need to choose the folder with your seedling images.
- Afterwards, a popup will appear, asking you for the cultivar name, the number of seeds, and other information. This information will be saved inside the .csv result file and can be changed at any time by choosing "File," "Inputs."


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/023853ac-fc9d-4e1e-a178-cbaae98c34d8)


- This is the image you will see if everything went right.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/8d1d4229-45e8-420d-b089-689a456b3110)

- This is the data related to the entire image. Pay attention to the Growth, Vigor, and Uniformity numbers, as the maximum value is 1000. If the values look a little weird, it's because the standard parameters don't fit your system.
- Let's change them: From the "Configuration" menu, click on "Change Settings."


![image](https://github.com/user-attachments/assets/f5d2a088-cc6b-4f35-8c02-411cf8e3cdd2)


- The upper part of the window is related to the image, and the lower part is related to the vigor index calculation parameters.
- In the upper part, "Number of segments" and "root thickness" are used to detect and sort what is hypocotyl and root, finding the breakpoint between them. Play around with the values and find the ones that suit your system.
- "Dead," "Normal," and "Abnormal" parameters are related to the seed classification, as the names suggest: Dead, Normal, and Abnormal. They are used in the formula to calculate the Growth, Uniformity, and Vigor indexes. The best way to configure these parameters is by capturing images of distinct seed conditions and adjusting the parameters until they are correct.
- "Average seed length = 12.5" is related to an average soybean seedling at 3 days old.
- The lower part is related to Vigor calculation parameters. I advise you not to change these values. I have provided the option to change them because someone may try to use the software on different species other than soybean, and these values may not work with them.
- In the lower part of the window you have the option to export and import configurations, as well as returning to the default settings.

# Fixing segmentation errors

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/fd041d7b-9b7f-464e-b18f-b2bfa192ec0a)

- In the first seedling, the software wrongly detected part of the cotyledon as hypocotyl.
- In the second seedling, the software placed the breakpoint a little too low.

## How to fix:

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/b24550a1-0680-46d8-93bb-08ef53650299)

- In the main screen, with zero percent zoom, left-click on top of the seedling you need to edit. Alternatively, you can select it by clicking on the table. The seed editor will open.

![image](https://github.com/user-attachments/assets/c6c007f3-3b40-46bb-ac3e-217a2123d8c5)


- In the seed editor, we have the options to change the breakpoint position (everything above will be hypocotyl, and everything below will be root), erase lines, manually draw lines, and change the seed status.

![image](https://github.com/user-attachments/assets/51508bac-31c3-43d0-a34c-345cb8c111e1)

- As you change the seed parameters, the seed information will update in real-time as well.
- You can use the keyboard's arrows key to change the seedling selected to edit.
- TIP: Since the software (1.0) doesn't have the seed status on the main window's table, you can use the seed editor to configure the seed status values in the "Change settings" menu.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/ebf224f3-b931-4170-8d00-f37bd6fcf6d0)


**Observation:** Everything will be saved in a .csv file in the image folder; you don't need to save each image manually. Just click on the next button, fix the seedlings if needed, and click on the next button again.

# Dealing with ProSeeding data

- The software will save the results in the same directory as the image folder you selected, as seen below where "0" is the lot number, inputted at the beginning of the analysis:

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/3098a73a-2833-4457-bf7b-d776f7bc4300)

- Inside the "0" folder, you will find two folders with self-explanatory names "processed_images" and "results," where you will find the processed images and the results:

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/cdce2647-bef9-44ee-9cbc-1928dfb228e2)

- The .csv files follow the nomenclature of the image that originated the results, and they will have the following formatting:

![image](https://github.com/user-attachments/assets/36a7eddc-c434-401e-b565-8212fa345039)


- Now you have the data you need from all the repetitions and samples of your lot of soybean seeds. Sometimes (more often than not), you need to analyze the data from the entire lot instead of a single repetition. To solve this issue, concatenated file will be present in the same folder as the other .csv, named "ProSeedling_data.csv"

![image](https://github.com/user-attachments/assets/5caf30ca-7aa9-4073-b0e0-6d948bbea8fa)


  







