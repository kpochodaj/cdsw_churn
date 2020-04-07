# Machine Learning Workshops
## Telco churn with refactor code
This is the CML port of the Refractor prototype which is part of the [Interpretability
report from Cloudera Fast Forward Labs](https://clients.fastforwardlabs.com/ff06/report).

### Setup
Add new profile with more resources.
Go to Admin Panel (leave project first).
In Engines tab add new Engine profile with 2 CPUs and 8GB memory - click Add button.
Navigate back to your project (Projects menu).

Start a Python 3 Session with at least 8GB of memory and __run the utils/setup.py code__.  
This will create the minimum setup to use existing, pretrained models.

### 1 Ingest Data
Open `1_data_ingest.py` in a workbench: python3, 1 CPU, 2 GB.

Run the file. Stop session.

### 2 Explore Data
Create new session (Open Workbench) with Jupyter notebook selected as the editor.
In jupyter notebook open the `2_data_exploration.ipynb` and run it (Cell/Run All)

### 3 Train Model using Experiments
The goal of the task is to compare performance of two algorhithms and select the model with better precision.

First open 3_train_model_args.py from Files menu. Can you identify parts of code that mark parameters and output to be captured within experiment?

Run new experiment from Experiment menu.

Select 3_train_model_args.py for script.

The code accepts two arguments - algorhithm and dataset.

In first experiment use the following:
linear telco

Select Python 3 as an Engine Kernel and 1vCPU / 2 GB Memory as Engine Profile.

Run experiment.

While the experiment is being executet click on Run ID to analyse the progress.

When it finishes review performance statistics in Overview / Metrics.

Run new experiment, this time using the following parameters:
gb telco

When it finishes compare metrics on the summary page of Experiments and identify the run with better performance.
Open the experiment, check box next to the model name in Output section and click Add to project

Go to Files section and make sure that the model has been added successfully.

### 4 Deploy Model
Go to the **Models** section and create a new Explainer model with the following:

* **Name**: Explainer
* **Description**: Explain customer churn prediction
* **File**: 4_model_serve_explainer.py
* **Function**: explain
* **Input**: `{"StreamingTV":"No","MonthlyCharges":70.35,"PhoneService":"No","PaperlessBilling":"No","Partner":"No","OnlineBackup":"No","gender":"Female","Contract":"Month-to-month","TotalCharges":1397.475,"StreamingMovies":"No","DeviceProtection":"No","PaymentMethod":"Bank transfer (automatic)","tenure":29,"Dependents":"No","OnlineSecurity":"No","MultipleLines":"No","InternetService":"DSL","SeniorCitizen":"No","TechSupport":"No"}`
* **Kernel**: Python 3

If you created your own model (see above)
* Click on "Set Environment Variables" and add:
  * **Name**: CHURN_MODEL_NAME
  * **Value**: 20191120T161757_telco_linear  **your model name from above**
  Click "Add" and "Deploy Model"

In the deployed Explainer model -> Settings note (copy) the "Access Key" (ie. mukd9sit7tacnfq2phhn3whc4unq1f38)

### 5 Deploy Application

From the Project level click on "Open Workbench" (note you don't actually have to Launch a session) in order to edit a file.
Select the flask/single_view.html file and paste the Access Key in at line 19.
Save and go back to the Project.  

Go to the **Applications** section and select "New Application" with the following:
* **Name**: Visual Churn Analysis
* **Subdomain**: telco-churn
* **Script**: 5_application.py
* **Kernel**: Python 3
* **Engine Profile**: 1vCPU / 2 GiB Memory  

If you created your own model (see above)
* Add Environment Variables:  
  * **Name**: CHURN_MODEL_NAME  
  * **Value**: 20191120T161757_tekci_linear  **your model name from above**  
  Click "Add" and "Deploy Model"  

After the Application deploys, click on the blue-arrow next to the name.  The initial view is a table of rows selected at  random from the dataset.  This shows a global view of which features are most important for the predictor model.  

Clicking on any single row will show a "local" interpretabilty of a particular instance.  Here you
can see how adjusting any one of the features will change the instance's churn prediction.  

* Don't forget** to stop your Models and Experiments once you are done to save resources for your colleagues.  

----- BREAK ------- WAIT FOR SLIDES -------------------

### 6 Create pipeline
The goal of the task is to create a workflow to extract data and train model based on it.

In Jobs section create two jobs:

Name: Ingest data
Script: 1_data_ingest.py
Schedule: Manual (default)
Engine: 1 vCPU and 2 GB RAM (default)

Name: Train model
Script: 3_train_models.py
Schedule: dependent, select Ingest Data from the list
Engine profile: 1 vCPU and 2 GB RAM (default)

Click Run for Ingest data, check if Train model job is triggered after completion of Ingest data.

When workflow finishes try triggering from outside:
1. Open terminal on your PC/laptop
2. Modify the following statement
curl -v -XPOST http://cdsw.34.240.182.60.nip.io/api/v1/projects/kpochodaj/telco-churn/jobs/1/start  --user "uwlznbbwpwdaxdgpbhz54utwiux3la34:" --header "Content-type: application/json"

Replace:
34.240.182.60 with IP of your CDSW
kpochodaj/churn/jobs/3 with corresponding details for your jobs (you can find it in URL of the job - go to Jobs section and open Ingest Data job)
uwlznbbwpwdaxdgpbhz54utwiux3la34 with your API key (you can find it in your Account Settings in top right part of the screen on API Key tab )

Run adjusted command from the terminal. Check if the workflow is triggered.

### 7 Create real-time application
Download Nifi template from Nifi folder in Files section

Open NiFi using link available in the spreadsheet.

Click Upload Template icon from Operate box to import NiFI template

Drag and drop Template icon from top menu onto the main screen, select the template from the list

Right-mouse click on GenerateFlowFile processor, select Properties,
Replace access key with your API key (instructions in previous task)
Confirm with OK and Apply

Open Properties of InvokeHTTP processor
Replace https://modelservice.ml-345fc019-340.sandbox.a465-9q4k.cloudera.site/model
with your CDSW url
You can find it in Explainer model's sample code in Model menu (parts between POST and -d)

Click on the background and press Start button from Operate menu on the left

Wait for data to flow, increasing number of messages in Response box linking InvokeHTTP with PutHDFS suggest positve outcome

Open Monitoring tab in Explainer model from Model section, validate that the number of requests is increasing.

To test deployment of the model and its impact on real-time processes click Deploy new build button in Monitoring tab, leave default settings and click Deploy model. Monitor the state of deployment and flow in Nifi (Refresh on backgroup updates the figures ad-hoc). Notice how many messages are rejected due to lack of availability of REST API of the model.

Stop flow in NiFi.

Leave project. Go to Admin panel. Review content of Users, Activity and Models tabs.
Stop models.
