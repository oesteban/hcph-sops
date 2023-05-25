
!!! info "Cohort I"

	Recruitment, screening and informed consent do not apply to Cohort I because the participant is the Principal Investigator himself.

!!! info "Cohort III"

	Recruitment, screening and informed consent do not apply to Cohort III because the sessions have already been acquired.

## Recruitment shortlist

- [ ] Distribute the [recruitment flyers](../assets/files/flyer_FR.pdf) at CHUV, as well as on EPFL and UNIL campuses, both physically and electronically (e.g., e-mail lists).
- [ ] Insert any new potential participant who shows interest by calling {{ secrets.phones.study | default("███") }}, whatsapp, SMS, email, etc. in [our recruits spreadsheet]({{ secrets.data.recruits_url | default("/redacted.html") }}). Make sure you get **an e-mail contact** to send documents.

!!!warning "Recruits shortlist"

	- [ ] Remove all flyers and indicate that recruitment is not open anymore once the shortlist quotas have been reached (5 males and 5 females for Cohort II).

## First contact

!!!warning "Important"
	
	- [ ] Write an email to them within **the next 24h**.
	- [ ] Use [the email template](#first-contact-email-fr) and make sure you attach the MRI Safety and Screening Questionnaire and the Informed Consent Form.
	- [ ] Confirm the reception of the email AND the documents over the phone.

## Phone call

!!!info

	The study coordinator ({{ secrets.people.study_coordinator | default("███") }}, Assistante doctorante) will call the potential participant **after at least three days** of having sent the information in the case of cohort II ([HRA, art. 16-3][1]).

- [ ] Use the [phone script](#first-contact-call-fr) to drive the conversation and record participant responses to questions.
- [ ] If participant consents to the phone screen, conduct it and mark the results (screener date, if responded "yes" to any medical questions, whether or not passed screener) in the appropriate columns of the recruitment spreadsheet.
- [ ] Confirm whether the potential participant understood the MRI Safety & Screening Questionnaire, and discuss with them any questions or potential reasons that may disqualify them to participate.

!!!danger "Carefully screen the subject"
    - [ ] In case of any doubts emerging from the MRI safety screening, indicate the potential participant that you will call them back **within three days**, after contacting the responsible physician.
    - [ ] Collect as much information as possible about their case.
    - [ ] Contact {{ secrets.people.medical_contact | default("███") }} with all the information.
    - [ ] In case of negative assessment by the medical contact, the volunteer **MUST NOT** participate in the study.
    - [ ] Otherwise, call back the participant as soon as possible to confirm participation.

- [ ] Female participants will be informed and must acknowledge that they must take a pregnancy test before the first scanning session.
- [ ] If the candidate participant does not pass the phone screen, then end the interview, informing them that they do not meet our inclusion criteria, and mark the screen fail in the recruitment spreadsheet.
- [ ] Make sure that the participant's questions about the study are all addressed and answered.
- [ ] Request the potential participant to confirm they are willing to continue.
	- [ ] Indicate in the shortlist of recruits that the participant is ready to schedule the first session.
	- [ ] Tell the participant that they will be called back to set up the first session.
	- [ ] Remind them that they can ask further questions at any time before the MRI scan session.

## Templates

### First contact email (FR)

!!! warning "Remember to attach the MRI Safety and Screening Questionnaire and the ICF."

!!! note "Objet: Invitation à participer à une étude d'acquisition IRM du cerveau : informations et documents joints"

	Cher/Chère **[nom]**,

	Nous vous remercions vivement pour l'intérêt que vous portez à notre étude de recherche sur l'imagerie IRM du cerveau.

	Notre équipe mène actuellement une étude visant à mieux comprendre les différentes sources de variabilité lors d'un examen IRM.
	
	Nous recherchons des participants·tes âgés de 24 à 55 ans, en bonne santé et sans antécédents de maladies neurologiques.
	Les participants·tes doivent consentir à la publication de leurs données dans le cadre du projet.
	Des mesures de confidentialité sont rigoureusement mises en place pour garantir l'anonymat des données.
	Elles impliquent notamment la suppression de toute information permettant l'identification des participants, telles que la date de naissance ou le nom.
	
	Participer à cette étude implique une présence à 12 séances d'acquisition IRM du cerveau, d'environ 1h30 chacune.
	Ceci représente un temps de participation total d'environ 18 heures.
	Vous recevrez une indemnité financière pour votre participation.
	Veuillez noter que si des découvertes fortuites concernant votre santé étaient faites au cours de l'expérience, vous consentez à en être informé·e.

	Nous vous invitons à prendre connaissance des documents joints afin d'obtenir un aperçu de l'étude.
	Le premier document détaille les implications d'une participation à l'étude, l'organisation des séances d'acquisition et fourni un résumé des objectifs du projet.
	Le second document concerne les éventuelles contre-indications à passer un examen IRM.
	Veuillez le remplir soigneusement et nous le retourner.
	
	Si après lecture des informations ci-dessus vous acceptez de participer, nous souhaiterions convenir d'un entretien téléphonique avec vous afin de récapituler les points importants de votre participation. 
	Cet entretien nous permettra également de vérifier votre éligibilité à participer à l'étude et de répondre à toutes vos éventuelles questions. 
	Nous vous prions de nous retourner votre réponse dans un délai de 3 jours ouvrables.
	Afin que nous puissions planifier l'entretien téléphonique, veuillez également nous indiquer les plages horaires dans lesquelles nous pourrions vous contacter.

	Entre-temps, si vous avez des questions, n'hésitez pas à nous contacter par e-mail ou par téléphone au {{ secrets.phones.study | default("███") }}.
	Nous serons ravis de répondre à toutes vos questions.

	Nous vous remercions encore une fois pour votre intérêt.

	Cordialement, <br />
	Céline PROVINS <br />
	Assistante-doctorante

### First contact call (FR)

!!! note "First contact call script in French"

	Bonjour ici Céline Provins,

	Je vous appelle concernant l'étude d'acquisition IRM du cerveau.
	Le but de cet appel est de vous répéter les éléments importants concernant le projet.
	Ensuite nous allons vérifier ensemble que vous êtes d’accord avec toutes les exigences pour participer à ce projet et nous allons vérifier que vous n’avez pas de contre-indications qui vous empêchent de passer des sessions IRM.
	De plus, je suis aussi là pour répondre à toutes vos questions, donc n'hésitez pas à m'interrompre si vous comprenez pas quelque chose ou si vous avez des doutes.

	Est-ce que vous avez des questions jusque là ?

	Je vais maintenant vous présenter les éléments essentiels concernant votre participation à notre étude.
	La participation à ce projet comprend 12 séances d'environ 1h30 qui se dérouleront au CHUV.
	Chaque séance durera environ 1h30.
	On commencera par remplir un bref questionnaire pour assurer la sécurité de la procédure, ça prendra environ 15 minutes ensuite, nous vous prépareront, nous vous expliquerons l’examen et nous nous assurerons que vous ne portez rien qui puisse causer des perturbations magnétiques.
	Nous vérifierons également avec une liste de contrôle que toutes les mesures de sécurité sont prises et que vous n'avez pas un élément métalliques sur vous.
	Ensuite vous passerez environ 1h15 dans le scanner.

	Dans chaque séance nous allons non seulement acquérir des images IRM mais nous allons aussi enregistrer des signaux physiologiques au moyen de quatres appareils supplémentaires.
	Ces appareils sont compatibles avec l’IRM et ils n'affectent pas votre santé.

	Le premier appareil est une ceinture respiratoire pour suivre votre respiration.
	C'est simplement une ceinture autour de votre ventre ou autour de votre thorax qui mesure le déplacement de votre ventre.

	Ensuite nous allons placer trois d’électrodes au sommet de votre thorax.
	Ceux-ci sont placés avec un gel conducteur sur la peau pour mesurer vos pulsations cardiaques.
	

	Le troisième appareil est une canule respiratoire pour mesurer la concentration de dioxyde de carbone expiré.
	Une canule respiratoire c'est le tube que les personnes âgées ont pour respirer de l'oxygène.
	La différence c’est que nous n’allons pas vous donner du gaz, mais simplement que vous expirez pendant votre respiration.

	Le 4ème appareil est un appareil pour mesurer le mouvement de vos pupilles.
	Cet appareil ne sera pas sur vous et n'a aucun effet ni sur votre santé ni sur votre confort.
	Durant toute la séance d'IRM, vous tiendrez un bouton alarme dans votre main, c'est-à-dire qu'à n'importe quel moment si vous avez un problème vous pouvez appuyer sur ce bouton d'alarme et nous interrompons l’examen immédiatement et venons vous chercher à l'intérieur du scanner pour voir avec vous ce qui ne va pas.
	Vous pouvez interrompre une session à tout moment sans explication.

	Est-ce que vous avez des questions? Non, alors continuous.

	Les risques liés à l'IRM sont les suivants.

	l’IRM est un fort champ magnétique, il est donc dangereux de rentrer dans la salle avec des objets à susceptibilité magnétique.
	C'est pourquoi plus tard nous allons minutieusement vérifier ensemble la liste du questionnaire de sécurité IRM.
	Toutefois en l’absence d’object à susceptibilité magnétique, l’IRM est complètement sans danger car il n’utilise pas de rayonnement ionisant.
	 Il n'y a pas de danger même si on fait beaucoup de séances.

	Sachez que le tunnel est relativement étroit donc on peut se sentir un peu claustrophobique.

	Si vous êtes une femme, je dois vous informer qu’avant la première session vous allez devoir faire un test de grossesse.
	C'est pour vérifier que vous n'êtes pas enceinte, car éthiquement nous n'avons pas le droit de scanner des femmes enceintes car les effets des IRM sur le fœtus n'ont pas encore été étudiés en détail.
	Avant chaque séance vous devrez également de donner des informations sur vos règles comme le dernier jour des règles ainsi que la régularité de vos règles ceci est important car le cycle menstruel a un effet sur le cerveau et pour la fiabilité de notre étude nous avons besoin de savoir ces informations.
	Toutefois sachez que vous pouvez décider d’exclure les informations sur vos règles quand nous allons publier les données publiquement.

	Les séances IRM seront programmées en fonction de la disponibilité des appareils et des préférences et de votre agenda.
	La durée de participation maximale est de 20 semaines consécutive, c'est-à-dire 5 mois, mais idéalement les sessions seront programmées à un interval régulier 
	Est-ce que vous avez des questions jusque-là ?

	Ok donc maintenant je veux juste vérifier avec vous que vous êtes d'accord avec toutes les exigences concernant la participation à ce projet.
	Est-ce que vous êtes âgés entre 24 et 55 ans ?
	Vous n'êtes pas diagnostiquer avec un trouble ou une maladie neurologique ?
	Vous acceptez d'être informé des découvertes fortuites concernant votre santé? Parce que on a l'obligation éthique d'envoyer les images de la première session à un radiologue qui va vérifier ces images et vous informer s'il découvre quelque chose d'anormal dans votre cerveau.
	Ensuite un élément très important, c'est que vous devez accepter que vos données soient publier ouvertement, mais bien sûr après que nous ayons appliqué des mesures adéquates de protection de la confidentialité des données.
	Par exemple, nous allons enlever toute informations qui permettraient de vous reconnaitre comme votre nom, votre date de naissance ou la date de l’examen afin de protéger votre confidentialité.
	Etes-vous d'accord avec ce terme ?
	Un autre élément important est que la participation à cette étude implique de nombreuses sessions IRM.
	Comme je vous ai dit 12 sessions d'environ 1h30.
	Donc s'il vous plaît, veuillez vous demander si l'engagement pour le projet n'est pas excessif ou pourrait devenir lourd avec le temps et que vous avez amplement le temps pour finir le projet.
	Vous devez aussi accepter de nous informer si vous prenez des médicaments, si vous consommez de l’alcool ou de la drogue car ces substances ont un effet important sur le cerveau et nous avons besoin de savoir pour pouvoir quantifier ces effets.
	
	Une autre contrainte c'est que vous devez éviter de boire du café 4h avant les séances car le café aussi est connu pour avoir des effets notables sur le cerveau.

	Maintenant qu’on a confirmé que vous êtes d'accord avec toutes ces exigences, je vous rappelle que votre participation est entièrement libre et que vous pouvez vous retirer à tout moment sans explication.
	Toutefois pour nous c'est important que les participants finissent les 12 sessions pour la complétude de nos données et donc pour nous c'est mieux si vous êtes déterminés à finir les 12 sessions et que c'est seulement si il y a quelque chose d'urgent ou d’imprévu que vous interrompez votre participation.

	Chaque séance sera rémunéré 45 francs plus les frais de transport.

	Des questions ?

	OK maintenant nous pouvons regarder ensemble le questionnaire de contrôle de sécurité et vérifier que vous avez répondu non à toutes les questions.
	
	Avez-vous répondu oui à une des questions ? Non ok parfait.
	
	Je veux juste revérifier avec vous que vous n’avez bien pas d'aide auditive.
	
	Vous n'avez pas de bac dentaire, de prothèse dentaire, de fausses dents etc.
	Vous n'avez pas non plus de piercing de tatouage ou de maquillage permanent ni d’implant capillaire
	Vous n'avez jamais été blessé par un objet métallique.
	Vous n'avez pas subi des opérations dans lesquelles il y aurait des métaux qui restent dans votre corps comme des clips chirurgicaux, des agrafes, des fixations vertébrale, un stimulateur de la moelle épinière, des extendeurs de tissu
	Vous ne portez pas de valve cardiaque.
	Vous portez pas de biostimulateur, de pompe à médicament interne ou externe, de cathéters ou d'articulation artificielle.

	C’est parfait, vous êtes éligible à participer.

	Encore quelques instructions à suivre avant chaque la séance.
	Il faut retirer tous les bijoux, piercing compris, et tous les accessoires de cheveux.
	Veuillez aussi retirer vos prothèses dentaires, les fausses dents etc.
	Il faut également retirer les aides auditives et les lunettes.
	Si vous êtes un homme, veuillez s'il vous plaît vous raser la partie supérieure du torse car nous avons besoin de placer les électrodes à même la peau pour bien enregistrer le signal.

	Voilà c’est toutes les informations que j’ai à vous partager.
	Est-ce que vous avez des questions?

	En tout cas merci beaucoup pour votre participation!
	Si vous avez des questions, des doutes, n'hésitez pas à me rappeler à ce numéro et je vous rappelle dans quelques jours afin de fixer la première session.

	Bonne journée.
	
	Au revoir.

[1]: https://www.fedlex.admin.ch/eli/cc/2013/642/en "The Swiss Federal Council, Federal Act of 30 September 2011 on Research involving Human Beings (Human Research Act, HRA). 2011. Accessed: Nov. 29, 2021."
