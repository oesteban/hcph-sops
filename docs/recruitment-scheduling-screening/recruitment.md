
!!! info "Cohort I"

	Recruitment, screening and informed consent do not apply to Cohort I because the participant is the Principal Investigator himself.

## Recruitment shortlist

- [ ] Distribute the [recruitment flyers](../assets/files/flyer_FR.pdf) at CHUV, as well as on EPFL and UNIL campuses, both physically and electronically (e.g., e-mail lists).
- [ ] Insert any new potential participant who shows interest by calling {{ secrets.phones.study | default("███") }}, whatsapp, SMS, email, etc. in [our recruits spreadsheet]({{ secrets.data.recruits_url | default("/redacted.html") }}). Make sure you get **an e-MAIL CONTACT**.

!!!warning "Recruits shortlist"

	- [ ] Remove all flyers and indicate that recruitment is not open anymore once the shortlist quotas have been reached (5 males and 5 females for Cohort II; 10M/10F for Cohort III)
	- [ ] Participants can be enrolled for both Cohorts II and III.

## First contact

!!!warning "Important"
	
	- [ ] Write an email to them within **the next 24h**.
	- [ ] Use [the email template](#first-contact-email-fr) and make sure you attach the MRI Safety and Screening Questionnaire and the Informed Consent Form.
	- [ ] Confirm the reception of the email AND the documents over the phone.

## Phone call

!!!info

	The study coordinator ({{ secrets.people.study_coordinator | default("███") }}, Assistente doctorant) will call the potential participant **after at least three days** of having sent the information in the case of cohort II, and **one day** in the case of cohort III (HRA, art. 16-3; [24]).

- [ ] Use the phone script [WRITE!] to drive the conversation and record participant responses to questions.
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

	Nous avons bien reçu votre intérêt pour participer à notre étude de recherche sur les images IRM du cerveau et nous vous en remercions.

	Notre équipe de chercheurs de renom dans le domaine de la neuroimagerie mène actuellement un projet passionnant visant à mieux comprendre les différentes sources de variabilité d'un examen IRM.
	Nous recherchons des participants âgés de 24 à 55 ans en bonne santé, sans antécédents de maladies neurologiques, et qui acceptent que leurs données soient publiées après que des mesures adéquates de protection de la confidentialité des données ont été prises.
	Celles-ci inclusent notamment la suppression de données qui pourraient vous identifier comme votre date de naissance ou votre nom.
	De plus, vous devez accepter d'être informé(e) des découvertes fortuites concernant votre santé.

	L'étude implique 12 séances d'acquisition IRM du cerveau, qui dureront environ 1h30 chacune.
	Vous recevrez une indemnité financière pour votre participation.

	Veuillez lire attentivement les documents en pièce jointe pour avoir un aperçu du projet.
	Le premier document détaille ce que votre participation implique, comment les séances d'acquisition seront organisées et donne un aperçu des objectifs du projet.
	Le second document est à remplir soigneusement afin de déterminer si vous possédez des contre-indications qui vous empêcheraient de passer un examen IRM.
	 
	Lors d’un entretien téléphonique, nous vous répéterons les éléments essentiels et répondrons à vos questions. 
	De plus, nous vérifierons également ensemble si vous etes éligibles à participer à l'étude.

	Nous vous accordons une période de trois jours pour examiner attentivement les informations fournies et réfléchir si vous êtes certain(e) que vous voulez et que vous êtes en mesure de consacrer les 18 heures que votre participation à cette étude exige.
	Pour que nous puissions planifier notre entretien téléphonique dans environ trois jours (jours ouvrables seulement), pourriez-vous s'il vous plaît me communiquer une date et une heure à laquelle je peux vous contacter ?

	Entre temps, si vous avez des questions ou hésitations, n'hésitez pas à me contacter par e-mail ou par téléphone au {{ secrets.phones.study | default("███") }}.
	Nous serions ravis de répondre à toutes vos questions et de discuter davantage de cette opportunité de recherche passionnante.

	Nous vous remercions encore une fois pour votre intérêt.

	Cordialement, <br />
	Céline PROVINS <br />
	Assistente doctoral



