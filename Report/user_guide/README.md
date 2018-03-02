# User documentation

Authors:
- Florian GARIBAL
- Guillaume HOTTIN
- Quentin JAUBERTIE
- Luc SAPIN
- François-Xavier STEMPFEL

## Introduction 
The Cervical Kinematic Recorder is an open-source software developped to acquire, display and analyse cervical movements thanks to an Oculus Rift headset. Cervical Kinematic Recorder was developed in the context of a last year project in the engineeing school E.N.S.E.E.I.H.T in colaboration with the Osteopathy Institute of Toulouse. This project was under the supervision of M. Denis Ducommun, Mme Sandrine Mouysset and M. Jérôme Ermont.

![Oculus Rift Headset](./images/oculus.png "Oculus Rift Headset")

## Setup environment and start application

The installation process is divided in two parts: Oculus Rift headset configuration and then the main app (CervicalKineRecord) set up.

In order to get the application running as well as expected and especially the Oculus Rift headset, it is necessary to use a computer that meets the following requirements:

![Minimum requirements for Oculus Rift](./images/min_spec.PNG "Minimum requirements for Oculus Rift")
![Recommened requirements for Oculus Rift](./images/best_spec.PNG "Recommended requirements for Oculus Rift")

Secondly, it is necessary to have an Oculu account. If it is not the case yet, you can create one at this address: [https://auth.oculus.com/login/](https://auth.oculus.com/login/)

### Setup environment

In a first time, it is necessary to download the *Oculus* application that allows you to use the headset on your PC.
This application is available at this address: [https://www.oculus.com/setup/](https://www.oculus.com/setup/)

As soon as the download is finished, it is time to plug in the headset to your computer ! 
You will need to follow these steps:
- Put the sensor (similar to a webcam) on top of your screen in front of you
- Plug in the sennsor to a 2.0 or 3.0 USB port of your computer
- Plug in the headset USB port to a 3.0 USB port of your computer
- Plug in the HDMI cable to the HDMI port of your computer (if your computer have more than one HDMI port, use the one of the graphic card)

In order to check if the headset is well plugged, the lights on the headset and the sensor should be orange/yellow.

It is now time to launch the Oculus Application in order to connect the headset. Log you in on the application with your Oculus ID (if you do not have any account, please create one there: [https://auth.oculus.com/login/](https://auth.oculus.com/login/))
At this stage, the two lights (headset and sensor) should be blue and a menu should be displayed inside the headset.

If everything is working, you have just finish the environment setup, otherwise try again or look for your specific problem on Google or on the Oculus forum.

### Install the CervicalKineRecords Application

In order to install the application on your computer, you just need to get the latest release available on the current git repository. 
This release should contains: 
- The exe file "CervicalKineRecord.exe"
- TODO

### Start application

Starting the application is very simple ! You just need to run the *exe* file called "*CervicalKineRecord.exe*".
Then, the application should start and you should have two distincts windows:
- The window that displays the target seen inside the headset
- The window that allows you to setup the parameters, launch an acquisition and see the results.

*Optionnal:*
To access the app easily, you can create a desktop shortcut with the following operation:
![Create a desktop shortcut](./images/creer_raccourci.png "Create a desktop shorctut")

At this stage, all the preliminary steps is done, you can now go to the next section to learn how to use the application.

# Tutorial

In order to not have unexpected behaviours, be sure to have done all the preliminary steps in the previous section "*Setup environment and start application*".

## Application overview and vocabulary

Here is an screenshot showing how the computer screen should be after the application starting.
![Computer scree after application start](./images/screens/00_desktop.png "Computer scree after application start")

We are now goint to define all the terms we are going to use in this tutorial 

### Vocabulary 

- Unity3D window: this windows allows you to see everythin that is displayed inside the headset and therefore follow the user movements.
![Unity3D window](./images/screens/0_unity.png "Unity3D window")

- Application window: This window allows you to manipulate profiles, set up parameters, launch/stop acquistion and analyse results throught the modelization tab
[Application window](./images/screens/0_python.png "Application window")

- Acquisition tab: This tab allows you to set up parameters, launch/stop acquisition and see the acquired curves (see image above)

- Modelization tabs: TODO
 
- Menu bar: The menu bar is composed of four entries :
-- "Profil": Create, load or opena  recent profile
-- "Courbes": Load saved curves
-- "Modèles": Create or load a model according to selected patients
-- "À propos": Application documentation
![Application menu bar](./img/screens/0_python_menu.png "Application menu bar")

### Functionnalities

##### Create a profile
    
To create a profile, you need to go to the "*Profile*" menu bar entry and then click on "*Nouveau profil*". From there, a new dialog will appear to enter the patient details (last name, first name, age)
These details should follow the following rules:
- **Last name**: text without any space, number, or special characters (~, ", ', (, -, è, \_, ç, @, =, +, \$, ...)
- **First name**: text without any space, number, or special characters (~, ", ', (, -, è, \_, ç, @, =, +, \$, ...)
- **Age**: number greater or equals to zero

**WARNING:** None of this details should be empty ! You should put a value, even without any sense, in each field.
![Create a profile](./img/screens/2_python_create.png "Create a profile")

**WARNING:** At this stage, the app does not accept people with same last name, first name AND age. If you try to create a profile with exact same details as one that already exists, you will face the following window.
![Create an existing profile](./img/screens/2_python_create_already_exists.png "Create an existing profile")

##### Load a profile

To load a profile you need to the "*Profile*" menu bar entry and then click on "*Charger un profil*". From there, a new dialog will appear to select the patient folder you want to load.
This folder name should meet the following requirements: *<NomPatient>*\_*<PrénomPatient>*\_*<ÂgePatient>*
    
![Load a profile](./img/screens/2_python_load.png "Load a profile")

When the patient is loaded well, his details (last name, first name, age) should be displayed in the application window. You can now display his saved curves, set up and launch an acquisition.
![Patient loaded](./img/screens/3_python.png "Patient loaded")
**WARNING:** If you try to load a profile that is already loaded in the application, a dialog will show up to inform you about it and nothing will be done. Indeed, in order to avoid any confusion between profiles, this actions is not possible.
![Load same profile twice](./img/screens/2_python_load_same.png "Load same profile twice)
##### Load a recent profile
\section{Charger un profil récent}

Afin de charger un profil, il vous faut vous rendre dans l'entrée "\textit{Profil}" de la barre des menus, puis de cliquer sur "\textit{Charger un profil récent}". \\
Lorsque le patient est chargé correctement, ses informations personnelles (nom, prénom, âge) sont affichées au milieu de la fenêtre. Vous pouvez donc désormais afficher ses courbes sauvegardées, paramétrer et lancer une acquisition.
    
    \begin{figure}[H]
        \centering
        \subfloat{{\includegraphics[width=8cm]{./img/screens/3_python.png} }}% 
    \end{figure}

\textbf{ATTENTION : Il ne faut sous aucun prétexte modifier le nom de dossier d'un patient ni en créer un soi-même, pour en créer un, utiliser l'option de création de profil décrite plus haut.}

\newpage

##### Load one or more curves 
\section{Charger une (ou des) courbe(s)}

Afin de charger un profil, il vous faut vous rendre dans l'entrée "\textit{Courbes}" de la barre des menus, puis de cliquer sur "\textit{Charger courbes}". À partir de là, la fenêtre ci-dessous apparaît vous demandant de sélectionner la ou les courbe(s) que vous souhaitez afficher. \\
    
    \begin{figure}[H]
        \centering
        \subfloat{{\includegraphics[width=8cm]{./img/screens/7_python_load_plots.png} }}% 
    \end{figure}

Vous pouvez sélectionner autant de courbes que vous le souhaitez, à savoir qu'elles seront toutes affichées sur les trois graphiques de l'onglet "\textit{Acquisition}". D'autre part les commentaires correspondant aux courbes chargées seront affichés dans la zone prévue à cet effet accompagnés de la même légende que celle présente sur le graphique (cf image ci-dessus). Il est peut être judicieux de n'en afficher que 5 à la fois pour une meilleure lisibilité. \\

Si vous souhaitez \textit{modifier les courbes affichées}, il vous suffit de revenir au même menu et de sélectionner et dé-sélectionner les courbes que vous souhaitez afficher. \\

Si vous souhaitez \textit{vider les graphiques de toutes les courbes affichées}, il vous suffit de cliquer sur le bouton "Vider graphiques" et de confirmer (ou infirmer si vous souhaitez annuler) la fenêtre de dialogue qui apparaît. \\

Dans le cas où les couleurs des différentes courbes ne sont pas bien distinguables, il suffit de ré-ouvrir le dialogue de chargement des courbes et de re-valider le chargement des courbes afin de changer les couleurs.


\newpage

##### Do an acquisition

    Afin d'effectuer une acquisition, il est d'abord \textbf{impératif} d'avoir un \textbf{profil ouvert}. Pour cela, il vous suffit d'\textbf{en créer un} (cf \hyperlink{creer_profil}{Créer un profil}) ou d'\textbf{en charger un} (cf \hyperlink{charger_profil}{Charger un profil}, \hyperlink{charger_profil_recent}{Charger un profil récent}. \\
    
    Lorsque le profil est chargé, vous pouvez paramétrer l'acquisition que vous souhaitez effectuer tel qui suit :
    \begin{table}[H]
        \begin{tabular}{|c|c|p{50mm}|c|}\toprule
            \hline
            \textbf{Nom} & \textbf{Type (unité)} & \textbf{Signification} & \textbf{Valeurs idéales}\\
            \midrule
            \hline
            Commentaires & Texte & Informations qui peuvent \newline être nécessaire à avoir sur l'acquisition (conditions d'acquisition, pathologie, etc.) & -  \\
            \hline
            Type de mouvement & Lacet/Roulis/Tangage & Type de mouvement qui sera effectué par le porteur du casque & Lacet \\
            \hline 
            Vitesse de rotation & Nombre (en °/s) & Vitesse de déplacement de la cible dans le casque &  20-40°/s \\
            \hline
            Amplitude maximale de rotation & Nombre (en °) & Angle maximal auquel la cible ira & 60-90° \\
            \hline
            Nombre d'aller retour & Nombre & Nombre d'aller retour que devra effectuer le patient lors de l'acquisition & 3-7 \\
            \hline
            Temps d'attente aux bornes & Nombre (en s) & Temps qu'attendra la cible entre chaque va-et-vient & 0.20-0.35s \\
            \hline            
        \end{tabular}
    \end{table}
    (\textbf{ATTENTION : seul le Lacet est supporté actuellement par l'application dans le casque, vous pouvez sélectionner les autres mouvements mais la cible affichée ne vous aidera pas à effectuer ces mouvements}) \\ 
    
    Après avoir paramétré l'acquisition comme vous le souhaitiez, il ne reste plus qu'à équiper votre patient du casque et cliquer sur le bouton "\textit{Lancer acquisition}". Suite à cela, un compte à rebours est lancé dans la fenêtre de visualisation du casque et l'acquisition se lance. \\

    À la fin de l'acquisition, deux cas sont possibles :
    \begin{itemize}
        \item \textbf{Le patient a bien suivi la cible}, les données récupérées sont affichées sur les trois graphiques de l'onglet acquisition ainsi que sur les trois onglets de modélisation mathématiques.
        \item \textbf{Le patient n'a pas assez bien suivi la cible}. Dans ce cas la fenêtre suivante apparaît afin de vous prévenir du manquement au suivi de la cible et de vous demander si vous souhaitez tout de même conserver les données ou non. \textit{Si vous acceptez} on se retrouve dans le \textit{cas n°1} où les données récupérées sont affichées sur l'ensemble des graphiques.
    \end{itemize}

    Lorsque la courbe est affichée sur l'ensemble des graphes, \textbf{elle n'est pas encore SAUVEGARDÉE}, il est \textit{impératif} de cliquer sur le bouton "\textit{Enregistrer}" \textit{pour enregistrer la courbe} récupérée après l'acquisition.
    
    Vous pouvez par ailleurs, à tout moment, \textit{interrompre l'acquisition en cours} afin de modifier ses paramètres ou tout simplement suite à une mauvaise manipulation. Les \textit{données acquises} ne seront dans ce cas \textit{ni sauvegardées ni affichées}.
    
\newpage


##### Mathematic modelization

##### Create a model

##### Load a model

##### Documentation



