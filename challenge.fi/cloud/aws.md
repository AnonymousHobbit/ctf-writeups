# Challenge.fi - AWS


## Challenge 1

### Description
---
I built a Docker image just for you. Can you check if it has any security issues?

The image can be found from DockerHub: [https://hub.docker.com/r/challengeapp/myapp](https://hub.docker.com/r/challengeapp/myapp)

---

### Solve
In the description we are given a link to a docker-image. So let's pull it: `docker pull challengeapp/myapp`.  Now run it with  `docker run -p 8080:8080 challengeapp/myapp`. 

If we go to http://localhost:8080 and view the source we will see a aws s3 bucket address.


Flag is located in https://frk-bucket-challenge-1234.s3.amazonaws.com/settings/stuff/flag.txt


## Challenge 2

### Description
---

Can you log in to to my super secure AWS EC2 Linux instance to find the flag?

---

### Solve

So we have to log in into their aws instance but we do not have credentials. However the first hint tells us we only need username and private key, so I assumed they key is somewhere hidden. 

When I first went inside the container, it had logged in as Joe. I checked Joe's home directory but couldn't find the  `.ssh` folder. Then I switched over to the root user and found the private key in `/root/.ssh` folder. 

So we have possible credentials to log in to the instance, but still missing an IP. 

We previously found an IP in [https://frk-bucket-challenge-1234.s3.amazonaws.com/settings/stuff/settings.txt](https://frk-bucket-challenge-1234.s3.amazonaws.com/settings/stuff/settings.txt) so I tried to ssh into it with the private key and username joe. 

Like I have learned in HackTheBox, the flags are usually stored in the home folder. I found a `/home/joe/.secret` file which looked interesting.

Turns out, the file contained the flag

## Challenge 3
### Description
---

You need to find out the password of Liisa to succeed in this challenge!

---

### Solve
After enumerating for a while, I didn't find anything special so I checked the first hint.
`EC2 instances expose a metadata service that can be queried.`

I then researched about this metadata service and AWS docs told to curl for `http://169.254.169.254/latest/meta-data/` inside the instance. 

Researching more of this service, I found the /latest/userdata/ endpoint and there was password for account `Liisa`. I tried to ssh into the user liisa with the password and it worked. 

However there wasn't any flag files inside `/home/liisa`. Usually it is recommended to check `.bash_history` Luckily there was a flag inside that file



## Challenge 4
### Description
---

I stored a secret in the AWS enviroment. It is encrypted, so it must be secure, right?

---

### Solve

After the 3rd challenge, I continued to enumerate the meta-data service. Finally I found an aws accesskey, secretkey and token from `/latest/meta-data/iam/security-credentials/FraktalSecretsManager`

I had just done an HackTheBox machine which required attacker to use aws-cli to enumerate the box. Based on that expierience I guessed these keys could be used as aws-cli credentias. However, I still needed to find the region, which I later found from `/latest/dynamic/instance-identity/document`

AWS has an secretsmanager where people can store some secret stuff. With aws-cli that I had installed, I was able to list all secrets in the manager: `aws secretsmanager list-secrets`
There was a secret called `fisc-chall-secret` and I was able to retrieve data inside that secret with command: `aws secretsmanager get-secret-value --secret-id fisc-chall-secret`

The secret contained the flag















