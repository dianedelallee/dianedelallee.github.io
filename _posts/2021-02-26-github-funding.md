---
title: Funding with Github
author: Diane Delallée
date: 2021-02-26 18:36:00 +0800
categories: [Blog, Github]
tags: [github, funding]
---

Few days ago, I decided to create an account in [Buy me a coffe ☕](https://www.buymeacoffee.com/). 

The goal: allow people to give me a donation 💰 is they want to support the blog or some of my github projects.

Why? Just to help me covering the hosting cost of my website.

Now that my donation account is setup, I just need to inform the community. I only added a small button to my website that
links to this donation page. But how can I share that on github?

## In Github

### For a specific project
On the root folder or your project you want to promote, create a new folder `.github`. In this folder create a `FUNDING.yml` file
that will contains the following lines: 

````yaml
github: <your github username>
patreon: # Replace with a single Patreon username
open_collective: # Replace with a single Open Collective username
ko_fi: # Replace with a single Ko-fi username
tidelift: # Replace with a single Tidelift platform-name/package-name e.g., npm/babel
community_bridge: # Replace with a single Community Bridge project-name e.g., cloud-foundry
liberapay: # Replace with a single Liberapay username
issuehunt: # Replace with a single IssueHunt username
otechie: # Replace with a single Otechie username
custom: ['https://www.buymeacoffee.com/dianedelallee'] # or any other custom website your want to redirect the user
````

### For all your project
You want to allow donation across all your repositories? There is an easy way.

* Go to your github profile
* If you do not have a project called `.github` create it, otherwise just open it. (cf [mine](https://github.com/dianedelallee/.github))
* Add a `FUNDING.yml`  file with exactly what we have define in the other step.
* That's it. Now if you go to another repository, you will see the Sponsor button on the top right of your repo, and
on the left side menu, you will see the section "Sponsor this project"


## Want to support me?

Just make a donation [here](https://www.buymeacoffee.com/dianedelallee)
