# **Student Exchange Forum of BJUT**
## **1.  Introduction**
This project is a special forum for the communication of students, called **Student Exchange Forum of BJUT**.

## 2. Deployment
### 1. Docker

Pull the docker image:

```shell
docker push echo0821/web-methodology
```

Start this docker image:

```shell
docker run -p 5000:5000 echo0821/web-methodology
```

### 2. kubernetes

Apply the config:

```shell
kubctl apply -f k8s/web-methodology.yaml
```


## 3. Test

### 3.1 Student Account 

#### 3.1.1 Registration to verify identity

This is a forum platform for students at Beijing University of Technology, so you need to complete verification to successfully enroll student users.

> Only the Student ID, ID and Student ID in the database match the Student ID, ID can complete the student user registration. 

Here's the data for you to test registration to verify identity.

| StudentID | ID                 |
| --------- | ------------------ |
| 18372301  | 111111111111111111 |
| 18372302  | 222222222222222222 |
| 18372303  | 333333333333333333 |
| 18372304  | 444444444444444444 |
| 18372305  | 555555555555555555 |
| 18372306  | 666666666666666666 |
| 18372307  | 777777777777777777 |
| 18372308  | 888888888888888888 |

#### 3.1.2 A Student Account For Test

Here is an student account for you to test.

| StudentID | Password |
| --------- | -------- |
| 84291189  | password |



### 3.2 Organization Account

#### 3.2.1 Organization Account Registration

Organizational account registration needs to go through the administrator to review the organization  account application information. If the information is true and reliable, the administrator will click the successful application button to send an email to the applicant to represent the success of the registration. On the contrary, the application failure of the mail.

**Since the project is not actually deployed online, you need to play the role of administrator on your computer.** 

| Administrator Email | Password   |
| ------------------- | ---------- |
| sefbjut@163.com     | bjut123456 |

> You need to log in to this mailbox and perform the administrator's action to complete the registration of the user account.

After clicking register success, your registration email will receive an email containing your organization's account information.

#### 3.2.2 A Organization Account For Test

Student accounts can post and second-hand trading information. Organization accounts can post and activity information.

Here is an organization account for you to test.

| OrganizationID | Password |
| -------------- | -------- |
| 99999999       | password |

