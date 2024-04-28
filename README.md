## PocDoc - Healthcare on Demand

- Chloe Crozier | [cscrozi@clemson.edu](mailto:cscrozi@clemson.edu)
- Justin Silva  | [jggueva@clemson.edu](mailto:jggueva@clemson.edu)
- James Tribble | [jjtribb@clemson.edu](mailto:jjtribb@clemson.edu)
- Nayha Hussain | [nayhah@clemson.edu](mailto:nayhah@clemson.edu)

This is our team's submission for Hacklytics '24, GT's Data Science Hackathon. We created a PocDoc app that triages mobile health units to patients based on severity level. We allow patients to interact with a language model trained on medical data from Hugging Face to predict the severity of their condition. We then use k-means clustering, linear regression modeling (based on current local hospital burden, patient's severity level, and pre-existing conditions), and the patient's geographical location to dispatch mobile health units to a given area. The goal is to solve overburdened healthcare facilities in metro areas and improve access to healthcare in rural areas. We used the OpenAI API for patient interaction and the Mapbox API to display an interactive map of patients and their assigned mobile units.
