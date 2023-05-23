
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

	Nous vous remercions vivement pour l'intérêt que vous portez à notre étude de recherche sur l'imagerie IRM du cerveau.

	Notre équipe mène actuellement une étude visant à mieux comprendre les différentes sources de variabilité lors d'un examen IRM.
	
	Dans le cadre de cette étude, nous recherchons des participants·tes âgés de 24 à 55 ans, en bonne santé et sans antécédents de maladies neurologiques. Les participants·tes doivent consentir à la publication de leurs données dans le cadre du projet. Des mesures de confidentialité sont rigoureusement mises en place pour garantir l'anonymat des données. Elles impliquent notamment la suppression de toute information permettant l'identification des participants, telles que la date de naissance ou le nom.
	
	Participer à cette étude implique une présence à 12 séances d'acquisition IRM du cerveau, d'environ 1h30 chacune. Ceci représente un temps de participation total d'environ 18 heures.
	Vous recevrez une indemnité financière pour votre participation.
	Veuillez noter que si des découvertes fortuites concernant votre santé étaient faites au cours de l'expérience, vous consentez à en être informé·e.

	Nous vous invitons à prendre connaissance des documents joints afin d'obtenir un aperçu détaillé de l'étude.
	Le premier document détaille les implications d'une participation à l'étude, l'organisation des séances d'acquisition et fournit un résumé des objectifs du projet.
	Le second document concerne les éventuelles contre-indications à passer un examen IRM. Veuillez le remplir soigneusement et nous le retourner.
	
	Si après lecture des informations ci-dessus vous acceptez de participer, nous souhaiterions convenir d'un entretien téléphonique avec vous afin de récapituler les points importants de la participation à l'étude. 
	Cet entretien nous permettra également de vérifier votre éligibilité à participer à l'étude et de répondre à toutes vos éventuelles questions. 
	Nous vous prions de nous retourner votre réponse dans un délai de 3 jours ouvrables. Afin que nous puissions planifier l'entretien téléphonique, veuillez également nous indiquer les plages horaires dans lesquelles nous pourrions vous contacter.

	Entre-temps, si vous avez des questions, n'hésitez pas à nous contacter par e-mail ou par téléphone au {{ secrets.phones.study | default("███") }}.
	Nous serons ravis de répondre à toutes vos questions.

	Nous vous remercions encore une fois pour votre intérêt.

	Cordialement, <br />
	Céline PROVINS <br />
	Assistante-doctorante



