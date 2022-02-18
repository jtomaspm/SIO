# project-1---vulnerabilities-equipa_18
project-1---vulnerabilities-equipa_18 created by GitHub Classroom

## Authors
| NMec | Name | email |  
|--:|---|---|  
| 89123 | Tomás Candeias | tomascandeias@ua.pt |  
| 89119 | João Machado | jtomaspm@ua.pt |  
| - | André Gomes | tomascandeias@ua.pt |  
| - | Diogo Silva | tomascandeias@ua.pt |  

## Project description
A simple game reviewing website, you can create an account and leave reviews about your desired games. Before commenting, you can use the preview option to preview what you are about to send.  
This app offers special functionalities for the "role" super users , like deleting comments and attributing this role to others.  
Furthermore, you can delete or logout of your account when you want to. There's also an option to search for a specific game if you are having trouble finding it.  
Note: the review system is just a sample for the project to be built around, the main intent for it, is to learn and explore vulnerabilities, such as CWE-79, CWE-89, CWE-269, CWE-799.  

#### Analysis table of contents:  
CWE-269: Improper Privilege Management  

CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')  
Location: “/” vulnerability in “/registerUser”, target: register user  
Location: “/comments” vulnerability in “/addComent”, target: add comment  
Location: “/” vulnerability in “/comments”, target: preview comment  
Location: “/” vulnerability in “/search”, target: search bar  
Location: “/” vulnerability in “/profile”, target: delete account  
Location: “/” vulnerability in “/profile” and “/search”, target: uname  
Location: “/” vulnerability in “/profile”, target: logout  

CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')  
Location: “/” vulnerability in “/verifyUser” and “/registerUser”, target: login and register user  

CWE-799 Improper Control of Interaction Frequency  
