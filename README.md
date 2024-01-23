# ProSeedling - (Editing Readme.md, soon will be beautiful and useful)
## Computerized Seedling Processing for Seed Vigor Analysis

The ProSeedling software is an advanced tool developed for the analysis of soybean seeds. It features specific characteristics and innovative functions:

- **Superior Seedling Detection:**
ProSeedling is capable of detecting features of interest even with low contrast between the color of the seedling and the background. Unlike other similar software, it uses the germination paper itself to acquire images of the seedlings, ensuring high performance in evaluations.

<img src="https://github.com/LuizSSenko/ProSeedling/assets/140913035/f22d0cd3-1548-4e79-aa39-8f13701fdc9f" width=100% height=100%>


## Minimizing Damage to Seedlings:
A major advantage of ProSeedling is its ability to minimize the handling of seedlings during the analysis process. This is important as it reduces the risk of damage to the seedlings, which can affect the accuracy of the analysis results.


## User-Friendly Interface:
The software also includes a user interface, designed with PyQT5, to facilitate user interaction with the system. This makes ProSeedling accessible not just to specialized researchers, but also to other users who may be interested in seed analysis.

## Data Processing and Analysis:
ProSeedling employs various open-source libraries for image processing and data manipulation. For instance, it uses OpenCV for image processing, Numpy and Scipy for numerical calculations, and Pandas for tabular data manipulation. This allows for comprehensive and detailed analysis of the captured images.


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/f5e28b9f-5f94-4861-ab3d-253ce653339d)


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/c4b3715f-da83-46d1-bab5-cda4995083b0)


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/59c12655-e787-4795-80bb-7c985f202530)


## Proven efficiency:
ProSeedling, still in its initial development phase, presents remarkable precision and accuracy. Compared to the Vigor-S, which already has proven efficiency for evaluating soybean seedlings, the results of the ProSeedling showed relevant consistency. However, it is essential to highlight the importance of conducting more experiments and improving settings to reach your full potential. A significant differentiator of ProSeedling is its open source nature, enabling researchers and professionals to adjust and adapt the software according to your needs. This feature expands the Future prospects for ProSeedling in the field of seed vigor assessment seeds.

<img src="https://github.com/LuizSSenko/ProSeedling/assets/140913035/991fdc46-6404-4a4f-933e-129e0cea2505" width=100% height=100%>


<img src="https://github.com/LuizSSenko/ProSeedling/assets/140913035/47144125-be77-4e09-aa95-267b3af7b6d4" width=100% height=100%>







# Editing everything below this line (Software Manual)


# Equipment used in the project

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/d452990d-fd1e-4707-b7ec-1d9c0f8a5303)

The equipment used to capture ProSeedling images was developed for acquiring images of seedlings based on the principle of transillumination. The equipment consists of an MDF box (Figure A), the interior of which is painted matte black, in order to avoid reflections (Figure B). In the upper part of the box, at a distance of 33.5 cm from the seeds, a digital camera equipped with an 8 Mpx SONY imx179 sensor and a 100º lens is positioned. This camera is fixed to a movable axis, allowing positioning adjustments (Figure B and C). At the bottom of the box, there is a mobile platform for positioning seedling samples. Complementing the set, there is a lighting system using cold white LEDs (6000k), measuring 40 x 40 cm, with a total power of 32W and an emission of 2200 lumen (Figure D).

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/978ba012-c7c6-4955-a3c4-9f9f25fff7eb)


The figure above shows an image of three-day-old soybean seedlings, captured using the aforementioned equipment. It is observed that the seedlings are highlighted in the image, allowing adequate segmentation of the image for the subsequent stages of software development


# Calibration process (Pixels to cm)

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/55b33d7b-96ac-4f79-b505-8821a4a3caec)

Enter in the main brach of ProSeedling project, open the "Calibration" Folder, download and print the .pdf file (Paying atention to choose the option "Standard" inside the scale section)

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/20415378-f496-4279-9749-6a339e43cc43)

Take a picture with your equipment, it does not need to be exactly like ours, ProSeedling has options that allow the user to use diverse types of capturing systens.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/4b44977f-623d-4bbd-89f6-47f97958a6b8)

In ProSeedling software, choose "Configuration" and then "Set Calibration". Click on "Load Calibration Image" and choose the configuration image captured by your system or enter manually the convertion value of how many pixels there's in 1cm.

# Capturing images

As mentioned earlier, your equipment does not need to be like ours, the only requisite is to have a controled light and a fixed camera for all the photos, in order to mantain accuracy and calibration. Don't worry about the ilumination sprectra either, as ProSeedling gives you the option to adjust the segmentation parameters.

**IMPORTANT:** It's a good practice to name the seedling images following this pattern:
CULTIVAR + SAMPLE + REPETITION

Also, organize the cultivar by folder, as the software reads the entire folder, the presence of two cultivars will be conflicting.


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/a59e1c1a-d84f-4cab-aba7-3f3ae6315880)


In this example, the cultivar's name is NEO610IPRO, so i called it "N" + sample number + repetition letter = N1A, N1B... N2A, N2B...


# Color calibration
Your system will very likely have a different spectra of ilumination, in order to configure this difference ProSeedling has a HSV tunning function located in "Configuration", "Set HSV Values".

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/7a9a77ed-f0fe-49a1-bdfd-90e2f3d907c7)

First move the sliders of HSV (Hue, Saturation, Value) in order to filter only the cotyledons.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/61a4afda-64eb-41ec-9480-3037c558dcac)

After filtering the cotyledons, choose the option "Set Values for hypocotyl and root", and so the same, move the slider until you get the seedling image.
As seem in the image above, some artifacts will be selected too, wich this is not a problem as ProSeedling will filter it out.

# Image analysis

Click on "File" and then "Open Folder", after that you need to choose the folder with your seedlings image.
Afterwards, a popup will appear asking you the cultivar name, number of seeds, and other information. These information will be save inside the result file, and can be changed at anytime choosing "File", "Inputs".


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/023853ac-fc9d-4e1e-a178-cbaae98c34d8)


This is the image you gonna see if everything went right.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/8d1d4229-45e8-420d-b089-689a456b3110)

This is the data related to the entire image. Pay attention to the Growth, Vigor and Uniformity number, as the max. value is 1000. If the values are looking a litte weird, is because the standard parameters dont fit your system, Let's change them: From the "Configuration" menu, click on "Change ettings".


![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/47c556aa-1530-42d8-82e5-e74fb67dc2e2)

- The upper part of the window is related to the image, the lower part is related to the vigor index calculation parameters.
- In the upper part, "Number of segments" and "root thickness" are used to detect and sort what is hypocotyl and root, finding the breakpoint between them. Play around the values and find the ones that suits your system.
- "Dead", "Normal" and "Abnormal" parameters are related to the seed classification in, as the name said: Dead, Normal and Abnormal, and is used in the formula to calculate the Growth, Uniformity and Vigor indexes. The best way to configure theses parameters is by capturing an image of distinct seed conditions, changing the parameters until it get right.
- "Average seed lenght = 12.5" is related to an average soybean seedling at 3 days old.
- The lower part is related to Vigor calculation parameters. I advise you to not change the values. Actually i only gave the option of change because someday someone can try to use the software on different species other than soybean, and maybe these values dont work with it.

  ![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/f9d429db-1bcb-4989-bb58-9ee7cc10d03b)

- Finishing this section: in the menu "Configurations" you have the option to export and import configurations, as returning to defaut as well.

# Fixing segmentation errors

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/fd041d7b-9b7f-464e-b18f-b2bfa192ec0a)

- In the first seedling, the software wrongly detected part of the cotyledon as hypocotyl.
- In the second seedling, the software placed the breakpoint a litte to low.

## How to fix:

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/b24550a1-0680-46d8-93bb-08ef53650299)

- In the main screen, with zero percent zoom, left click on top of the seedling you need to edit. Or you can select cliking on the table either. The seed editor will open.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/9f609b4d-9eec-4ad1-b2c9-ed87dff293a8)

- In the seed editor we have the options of: change the breakpoint position (everything up will be hypocotyl, and everything down will be root), erase lines, manualy draw lines, and change the seed status.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/d7f08d8d-6ab8-48f3-a715-e5b5e9405f5a)

- As you change the seed parameters, the seed information will change in real time as well.
- TIP: As the software dont have the seed status on the main window's table, you can use the seed editor to configure the seed status values in the "Change settings" menu.

![image](https://github.com/LuizSSenko/ProSeedling/assets/140913035/ebf224f3-b931-4170-8d00-f37bd6fcf6d0)


**Observation:** Everything will be saved in a .csv file in the image folder, you dont need to save each image mannualy, just click on the next button, fix the seedlings if needed and click on the next button again
