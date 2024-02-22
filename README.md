# True Care Hospital

The live link can be found here - [True  Care Hospital](https://true-care-hospital-8dee2f42b5aa.herokuapp.com/)

![ScreenShot](https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708595430/samples/true_care/Readme/all-devices-black_jog1mt.png)

Welcome to True Care Hospital, your healthcare destination designed to cater to your medical needs seamlessly. Our platform offers a range of features to enhance your healthcare experience:

1. Hospital Details: Access comprehensive information about our hospital, services, and facilities without the need for sign-in, providing you with transparency and clarity.

2. Appointment Booking: Registered users can effortlessly schedule appointments online, ensuring convenience and efficiency in managing your healthcare appointments.

3. User Profiles: Customize your personal profile by adding details and photos, enabling a personalized experience tailored to your needs and preferences.

4. Doctor Profiles: Our platform empowers doctors to create and manage their profiles, facilitating streamlined communication and interaction with patients. Doctors can efficiently handle appointments, provide diagnoses, and prescribe medications, enhancing the quality of care delivered.

5. Medical Records Access: Patients can securely access and download prescriptions and medical reports from their profiles, promoting transparency and facilitating continuity of care.

True Care Hospital offers a comprehensive solution for both online and offline medical consultations, providing a reliable and efficient healthcare option for all your needs.

(Developer: Eby Chacko)

___

## Table of Contents

- [Project Goals](#project-goals)
- [User Experience](#user-experience)
- [Design](#design)
- [Features](#features)
- [Unimplemented Features](#unimplemented-features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Clone the Repository Code Locally](#clone-the-repository-code-locally)
- [Credits](#credits)

___



## User Experience

- __Target Audience__

    - The True Care Hospital website is designed to cater to a diverse range of users seeking convenient and reliable healthcare solutions. Our targeted users include:

    - Patients: Individuals looking for accessible and high-quality healthcare services both online and offline. They seek convenience in scheduling appointments, accessing medical records, and communicating with healthcare professionals effectively.

    - Caregivers: Family members or guardians responsible for managing the healthcare needs of their loved ones. They require easy access to medical information, appointment scheduling, and communication with healthcare providers to ensure the well-being of those under their care.

    - Medical Professionals: Doctors and healthcare professionals interested in providing online consultations and expanding their patient base. They benefit from features that streamline appointment management, facilitate communication with patients, and ensure efficient delivery of healthcare services.

    - Health-conscious Individuals: Individuals proactively managing their health and seeking information on preventive care, wellness services, and healthcare resources. They appreciate easy access to healthcare information, tips for maintaining well-being, and options for seeking medical advice when needed.

Overall, our website caters to a diverse audience with varying healthcare needs, offering a user-friendly platform that prioritizes accessibility, convenience, and quality in healthcare delivery.
___

## UX
This site was created respecting the Five Planes Of Website Design:<br>
### Strategy

**User Stories and Epics:** <br>
User stories and epics can be viewed here on the project [kanban board ](https://github.com/users/EbyChacko/projects/5)


### Project Goals

The goal of the True Care Hospital project is to create a seamless and user-friendly  healthcare platform that bridges the gap between patients and healthcare providers. Through intuitive features such as appointment booking, personalized user profiles, our aim is to enhance the accessibility, convenience, and quality of healthcare services for individuals seeking both online and offline medical consultations. We strive to empower users to easily access healthcare information, schedule appointments, manage medical records, and receive personalized care, ultimately promoting better health outcomes and patient satisfaction.

- __User Goals__

  - Convenient Access: Users aim to easily access information about True Care Hospital's services, facilities, and medical professionals without requiring a sign-in process.
  - Seamless Appointment Management: Registered users seek to efficiently schedule appointments online, saving time and effort in booking medical consultations.
  - Personalized Experience: Users desire the ability to create and customize their profiles with personal details and photos, enabling a personalized healthcare journey tailored to their needs.
  - Transparent Communication: Patients expect transparent communication with doctors, including the ability to access medical records, prescriptions, and diagnoses conveniently from their profiles.
  - Quality Healthcare: Users aspire to receive high-quality healthcare services both online and offline, ensuring effective diagnoses, treatments, and medical consultations.

- __Site Owner Goals__

  - User Engagement: The site owner aims to attract and engage users by providing comprehensive information about True Care Hospital's services and facilities without the need for sign-in, fostering trust and transparency.
  - Appointment Management Efficiency: The site owner seeks to streamline the appointment booking process for registered users, ensuring efficient management of appointments and optimizing resource utilization.
  - User Database Expansion: By encouraging users to create profiles and engage with the platform, the site owner aims to expand the user database, facilitating targeted marketing efforts and fostering long-term user relationships.
  - Doctor-Patient Communication: Facilitating effective communication between doctors and patients, including the ability for doctors to manage appointments and provide diagnoses, enhances the site owner's goal of providing quality healthcare services and fostering patient satisfaction.
  - Data Security and Compliance: Ensuring the security and privacy of user data, including medical records and personal information, is a priority for the site owner to maintain trust and compliance with healthcare regulations.

### Scope<hr>

Scope for the True Care Hospital Project:

#### Website Development:

- Design and develop a user-friendly website accessible to both desktop and mobile users.
Implement intuitive navigation and responsive design to enhance user experience.
Incorporate features for displaying hospital details, services offered, and facilities available without requiring user sign-in.

#### User Management:

- Develop a user authentication system allowing users to create accounts, log in, and manage their profiles.
- Enable users to personalize their profiles by adding personal details and photos.
- Implement security measures to protect user data and ensure compliance with privacy regulations.

#### Appointment Management:

- Create a booking system allowing registered users to schedule appointments with healthcare professionals.
- Develop features for managing appointment slots, including availability and scheduling conflicts.
- Provide confirmation notifications and reminders to users regarding their upcoming appointments.

#### Doctor Profiles and Appointment Handling:

- Enable doctors to create and manage their profiles, including adding professional details and availability.
- Implement functionalities for doctors to view and manage appointments booked by patients.
- Allow doctors to provide diagnoses, add prescriptions, and update medical records for patient appointments.

#### Communication Features:

- Facilitate secure communication between patients and healthcare professionals through messaging or chat functionalities.
- Enable patients to access medical reports, prescriptions, and diagnoses conveniently from their profiles.
- Implement notification systems to alert users about updates to their medical records or appointments.

#### Data Management and Security:

- Develop a robust database system for storing user profiles, appointment details, medical records, and other relevant data.
- Implement data encryption and security protocols to protect sensitive information and ensure compliance with healthcare data regulations.
- Regularly backup and maintain data integrity to prevent loss or corruption of critical information.

#### Testing and Deployment:

- Conduct thorough testing of all website functionalities to identify and address any bugs or usability issues.
- Deploy the website on a reliable hosting platform with adequate resources to handle user traffic and ensure uptime.
- Provide ongoing maintenance and support to address user feedback, optimize performance, and implement updates as needed.

The scope outlined above encompasses the key features and functionalities of the True Care Hospital project, aiming to create a comprehensive virtual healthcare platform that meets the needs of both patients and healthcare professionals.

___

### Structure

#### All Page Header
- True care logo work as a loink to the home page
- Navigation Bar: navigation links to Home, About Us, Departmentsn Contact US, Appointments.
- If the user is authenticated then the right corner of the nav bar show the user name and the log out button. otherwise it will show two buttons for login and sign up
- the appointment will navigate to the appointment form only if the user is authenticated, otherwise navigate to a signup or login page.

#### All Page Footer
- emergency contact Number
- Appointment contact Number
- Appointment Enquiry e-mail
- Address
- Location Map
- links to the releavent pages
- copyright details
- social media links

#### Home Page
- Carausel Images
- Key features and service details

#### Department Page

- Show all the department with brief discription
- button for each department to show detailed view

#### Department Details Page

- detailed description about he department
- details of doctors who give service in the department

#### Contact Us Page
- Important Contact details
- form to Message to hospital by providing some personal details

#### Appointment Page

- Form to submit an appointment
- If the user has previously updated their personal details, they will automatically populate in the Appointment form. Otherwise, the user need to update it atleast with the appoinment creation.
- when the appoinment is submitted the page is navigated to the page that show all appointments of the user.

#### Profile Page

- This page is splitted into main two parts: Appointments and the personal details
- in appointments ther are 4 deferent navigations to view the All Appointments, Attended Appointments, Upcoming appointments and to the pesonal details.
- in the personal details section, there is update option to the personal details.
- in the appoinment section, the user can update or delete the appointments if wanted.
- the user can click on the view button on the appointment to navigate to the details of the curresponding appointment.
- If the user is a doctor, there will be additionally Professional details along with the personal details.

#### Appointment Details

- In this page the user can view the details of the appointment.
- If the appointment is already happened then the user can view the prescription, medical reports that are uploaded by the doctor.
- The user can download the prescription and the medical reports.

#### Doctor Profile

- When the page is loading the doctor can view all the Appoinments that need to attended by the doctor today
- also there are deferent navigations to All appointments, Upcoming appointments Pending Approval and attended Appointments.
- from this page the doctor can manippulate the appointments, or approve the it
- When the doctor select an appointment it will navigate to the details of the appointment

#### Doctor Appointment details

- In this page doctor can view the personal details of the patient.
- Doctor can add details of the diagnisis, prescription and the medical reports if any.
- When the doctor add any prescription or medical report, it will show instanly in the same page.
- This prescription and the medical report can view or downloaded by the patient.

___

### Skeleton
**Wireframes**<br>
The wireframes for desktop were created with Photoshop tool.

<details>
  <summary>Wire Frames</summary>
  <h4>Base.html</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609035/samples/true_care/Readme/base_i2kjxb.png"><br>
  <h4>Home Page</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609071/samples/true_care/Readme/page-Index_r7xiem.webp"><br>
    <h4>About Us</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609069/samples/true_care/Readme/page-about_nlduvz.webp"><br>
  <h4>Departments</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609070/samples/true_care/Readme/page-department_vqbty7.webp"><br>
  <h4>Department Details</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609068/samples/true_care/Readme/page-department_details_pgcquu.webp"><br>
  <h4>Contact Us</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609069/samples/true_care/Readme/page-contact_plmyfj.webp"><br>
  <h4>Appointments</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609069/samples/true_care/Readme/page-appointment_up2rk7.webp"><br>
  <h4>Patient Profile</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609071/samples/true_care/Readme/page-profile_x52eud.webp"><br>
  <h4>Doctor Profile</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609070/samples/true_care/Readme/page-profile_doctor_qkftpr.webp"><br>
  <h4>Doctor Appointment Details</h4>
  <img src="https://res.cloudinary.com/dgd5gtn1w/image/upload/v1708609070/samples/true_care/Readme/page-diagnosis_page_hytbfs.webp"><br>
</details>

