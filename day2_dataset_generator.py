"""
Day 2 competition dataset v4 -- Campus Operations & Student Services.

v4 CHANGES (competition reframed as "Complete the grounding"):
  * 179 records (was 172). New records add Kind 2 traps -- shared amounts (46000, 500),
    a shared semester ("spring semester"), a shared room (Room 214) -- plus an S009 tuition record.
  * Teams get a working pipeline with ONE pattern (Student ID) and extend a PATTERN REGISTRY.
  * Two question packs:
      PUBLIC_ADVERSARIAL (8) + PUBLIC_POSITIVE (3)   -> shipped inside the starter notebook
      HIDDEN_ADVERSARIAL (9) + HIDDEN_POSITIVE (4)   -> JUDGES ONLY, never shared
  * Every question carries the two records it is about (trap_records / shared_records) so
    the structural graph verdict can be checked without an LLM (see day2_offline_check.py).

Kind 1 identifiers (one per real event): Student S0xx, Alumnus A0xx, Club RC-n, ticket codes (HMT-58).
Kind 2 incidental fields (reused across unrelated events): room, block, amount, semester.
"""

campus_categories = {
    'Admissions': [
        "A new student's admission application was reviewed by the committee",
        'Entrance exam scorecard was verified for a incoming student',
        'Admission offer letter was issued to a selected candidate',
        "A student's transfer application from another college was processed",
        'Document verification was completed for a first-year admission',
        'Admission committee flagged a discrepancy in a submitted transcript',
        'Waitlisted candidate was offered a seat after a dropout',
        'Provisional admission was confirmed pending final marksheet submission',
        "International student's visa documents were reviewed for admission",
        'Admission counselor scheduled a call with a prospective student',
        "Student S013's admission document verification was completed ahead of orientation",
    ],
    'Fees_Finance': [
        'Tuition fee payment of 45000 rupees was received from a student',
        'A late fee penalty was applied to an overdue tuition payment',
        'Fee receipt was generated for the current semester payment',
        'A student requested an installment plan for pending tuition fees',
        "Refund was processed for a cancelled admission's fee payment",
        "Finance office reconciled the semester's total fee collection",
        'A bounced fee payment was flagged for reprocessing',
        'Hostel fee and tuition fee were combined into one invoice',
        "A student's fee payment was adjusted after a course change",
        'Finance team sent a reminder for an unpaid tuition balance',
        "Student S001's tuition fee payment of 42000 rupees was received for the fall semester",
        "Student S002 was charged a late fee penalty on last month's tuition invoice",
        "Student S004's tuition installment plan was approved by the finance office",
        "Student S009's tuition fee payment of 46000 rupees was received for the spring semester",
        "A refund of 46000 rupees was processed for a cancelled admission's fee payment",
    ],
    'Scholarships': [
        'Scholarship disbursement of 15000 rupees was processed for a first-year student',
        'A merit scholarship application was approved by the review panel',
        'Scholarship renewal was submitted for the upcoming academic year',
        "A need-based scholarship award was credited to a student's account",
        'Scholarship committee rejected an incomplete application',
        'Sports scholarship was granted to a state-level athlete',
        "A student's scholarship was revoked due to low attendance",
        'External scholarship provider confirmed funding for a student',
        'Scholarship disbursement was delayed pending document resubmission',
        'A minority scholarship application was forwarded for government approval',
        "Student S001's merit scholarship of 20000 rupees was disbursed for the fall semester",
        "Student S002's scholarship renewal was approved for the second year",
        "Student S003's sports scholarship was confirmed by the athletics department",
    ],
    'Hostel_Accommodation': [
        'Room 214 was allotted to a new student this week',
        'A hostel room change request was approved for a second-year student',
        'Hostel warden resolved a roommate conflict in Block C',
        'A student checked out of the hostel at the end of the semester',
        'New hostel admission form was submitted for the upcoming term',
        "Hostel curfew violation was reported to the warden's office",
        'A student requested a single-occupancy room upgrade',
        'Hostel mess registration was completed for a new resident',
        'Room allotment list was published for incoming hostel students',
        'A student vacated their room early due to a course withdrawal',
        "Student S006's room change request to Room 118 was approved",
        'Student S007 reported a curfew violation warning from the hostel warden',
        'A hostel maintenance ticket (HMT-58) was filed by the student in Room 310 for a broken window',
    ],
    'Facilities_Maintenance': [
        'A maintenance fee payment of 2000 rupees was recorded for Block C rooms',
        'Electrician was dispatched to fix a wiring issue in the hostel block',
        'Plumbing repair request was logged for a leaking bathroom',
        'Facilities team repainted the corridor walls in the academic block',
        'Air conditioning unit was serviced in the seminar hall',
        'A broken window pane was replaced in the library building',
        'Elevator maintenance was scheduled for the administrative block',
        'Facilities flagged a structural crack for engineering inspection',
        'Water cooler was repaired in the student common area',
        'Furniture replacement was approved for the outdated classroom desks',
        'Facilities resolved maintenance ticket HMT-58, replacing the broken window in Room 310',
        "Facilities serviced the air conditioning unit in Room 118 at Student S006's request",
        'Student S008 filed a complaint about a leaking bathroom in a different block',
        'Student S012 reported a broken door lock in Room 118 during the following semester',
        'Plumbing repair in Room 214 was completed after a leak was reported',
    ],
    'Library': [
        'A student issued three reference books for the semester',
        'Overdue library fine was paid by a student for a late return',
        'New journal subscriptions were added to the digital library',
        'A damaged book was reported and replaced in the collection',
        'Library extended its hours during the examination period',
        'A student requested an inter-library loan for a rare textbook',
        'Library staff reshelved returned books after the rush week',
        'E-book access was granted to a student for an online course',
        "A lost book fee was charged to a student's account",
        'Library conducted an annual stock verification of its collection',
        'Student S013 issued two reference textbooks for their first-year courses',
        'Student S015 was charged a lost book fee after misplacing a library textbook',
        'A library fine of 500 rupees was collected from a student for a damaged book',
        'Library extended its seating for the spring semester exam preparation',
    ],
    'IT_Helpdesk': [
        "A student's login credentials were reset after a lockout",
        'Wi-Fi connectivity issue was reported in the academic block',
        'IT helpdesk resolved a printer malfunction in the computer lab',
        "A student's email account was migrated to the new domain",
        'Software installation request was completed for a lab machine',
        'IT flagged a phishing email reported by a faculty member',
        "A student's laptop was unable to connect to the campus network",
        'IT helpdesk ticket was closed after a successful password reset',
        'Server downtime affected the online portal for two hours',
        'A student requested VPN access for remote library resources',
        "Student S014's laptop was unable to connect to the campus Wi-Fi network",
    ],
    'Placement_Careers': [
        'A student was shortlisted for a summer internship interview',
        'Placement cell scheduled a pre-placement talk with a recruiter',
        'A student received a job offer through the campus placement drive',
        'Resume workshop was conducted for final-year students',
        'Placement officer followed up with a company on pending offers',
        'A student withdrew from the placement process after a personal offer',
        'Mock interview session was organized for placement preparation',
        'Company representative visited campus for a recruitment drive',
        "A student's internship certificate was verified by the placement office",
        'Placement statistics were compiled for the annual report',
        'Student S013 was shortlisted for a summer internship interview by a recruiting company',
    ],
    'Events_Clubs': [
        'The robotics club organized a workshop for new members',
        'Cultural fest committee finalized the event schedule',
        'A student club requested funding for an upcoming competition',
        'Annual sports day events were scheduled across three days',
        'The photography club held an exhibition in the main hall',
        "Student council approved a new club's registration",
        'A guest lecture was organized by the entrepreneurship cell',
        'Debate club members prepared for an inter-college competition',
        "The music club performed at the college's annual day",
        "A club's event proposal was rejected due to a venue conflict",
        "The robotics club's workshop for new members was led by its club president (Club RC-1)",
        "The robotics club's president also represented the club (Club RC-1) at the inter-college competition",
    ],
    'Transport': [
        'A new bus route was added for students from the north campus',
        'Transport pass renewal was completed for the semester',
        'A student reported a delay on the college shuttle service',
        'Transport office adjusted the bus schedule for exam week',
        'A damaged bus seat was reported to the transport department',
        'Student transport fee was included in the semester invoice',
        'A new driver was assigned to the evening shuttle route',
        'Transport helpdesk resolved a lost bus pass complaint',
        'Additional buses were arranged for the college fest weekend',
        'A student requested a refund for an unused transport pass',
        "Student S009's bus pass was renewed for the spring semester",
        'Student S011 filed a complaint about a delayed shuttle on the north campus route',
        'Transport office added extra shuttle trips for the spring semester',
    ],
    'Parking_Permits': [
        "A student's parking permit application was approved for the fall semester",
        'Parking enforcement issued a warning for an expired permit',
        'A visitor parking pass was requested for a campus event',
        'Parking permit renewal was completed for a returning student',
        'A student reported a lost parking permit sticker',
        'Parking office resolved a dispute over an assigned spot',
        'A faculty parking permit was upgraded to a reserved spot',
        'Parking permit fee was waived for a shared carpool application',
        'A damaged permit sticker was replaced at the parking office',
        "Student S016's parking permit application was approved for the spring term",
        'Parking violation notice was issued for an unregistered vehicle',
        "Student S009's parking permit was renewed for the spring semester",
        'Student S010 received a parking violation notice for an unregistered vehicle',
        'A parking fine of 500 rupees was collected from a student for an unregistered vehicle',
    ],
    'Alumni_Relations': [
        'An alumni donation was received for the new library wing',
        'Alumni association organized a networking event for graduates',
        "A former student's contact details were updated in the alumni database",
        'Alumni newsletter was sent out for the quarterly update',
        'An alumni-funded scholarship endowment was reviewed by the committee',
        'Alumni relations office confirmed a guest speaker for homecoming',
        'A batch reunion event was scheduled for December',
        'Alumni association approved funding for a new mentorship program',
        'A distinguished alumnus was invited to the annual convocation',
        'Alumni donation records were reconciled for the fiscal year',
        "Alumnus A001's donation for the new library wing was formally acknowledged by the college",
        'Alumnus A001 attended the homecoming networking event hosted by the alumni association',
        "Alumnus A002's mentorship program funding was approved by the alumni association",
        'Alumnus A002 was invited to speak at the annual convocation as a distinguished alumnus',
    ],
    'Exam_Results': [
        "A student's semester grade report was published on the portal",
        'Exam committee resolved a discrepancy in a marksheet',
        'A student requested a re-evaluation of their exam paper',
        'Final exam results were released for the engineering department',
        "A student's backlog exam was scheduled for the next session",
        'Exam office issued a duplicate marksheet for a lost original',
        'A grade correction was approved after a clerical error was found',
        'Semester GPA was recalculated after a course withdrawal',
        'Exam hall ticket was issued for the upcoming semester exams',
        "A student's provisional degree certificate was requested after final results",
        "Student S014's backlog exam for a failed course was scheduled for next session",
    ],
    'Campus_Security': [
        'Campus security responded to a report of a stolen bicycle',
        'A lost ID card was recovered and returned through campus security',
        'Security patrol flagged an unlocked door in the academic block',
        'A student reported a suspicious person near the hostel gate',
        'Campus security reviewed CCTV footage after a minor incident',
        'A found wallet was logged at the campus security office',
        'Security escorted a student to their vehicle after a late-night event',
        'A broken security gate was reported for repair',
        'Campus security issued a visitor pass for an external vendor',
        'An access card malfunction was resolved by the security office',
        'Student S015 reported a lost ID card to campus security',
        "Student S016's vehicle was found unlocked by a security patrol and secured",
    ],
}

campus_texts = []
campus_labels = []
for category, sentences in campus_categories.items():
    for s in sentences:
        campus_texts.append(s)
        campus_labels.append(category)

KNOWN_OVERLAP_PAIRS = [
    ("Fees_Finance", "Scholarships"),
    ("Hostel_Accommodation", "Facilities_Maintenance"),
    ("Transport", "Parking_Permits"),
    ("Events_Clubs", "Alumni_Relations"),
]

# ---------------------------------------------------------------------------
# JUDGES' ANSWER KEY for the pattern registry
# ---------------------------------------------------------------------------
KIND1_PATTERNS = {   # real per-event identifiers -- adopting these is correct
    "Student": r"\bStudent\s+(S\d{3})\b",
    "Alumnus": r"\bAlumnus\s+(A\d{3})\b",
    "Club":    r"\bClub\s+([A-Z]{2,4}-\d)\b",
    "Ticket":  r"\b([A-Z]{2,5}-\d{2,4})\b",
}
KIND2_PATTERNS = {   # incidental fields -- adopting these creates false links
    "Room":     r"\bRoom\s+(\d+)\b",
    "Block":    r"\bBlock\s+([A-Z])\b",
    "Amount":   r"\b(\d{3,6})\s+rupees\b",
    "Semester": r"\b((?:fall|spring|summer)\s+(?:semester|term))\b",
}

HIDDEN_ADVERSARIAL = [{'question': "Tell me about the recent payment made for the student's room.",
  'trap_records': ['Room 214 was allotted to a new student this week',
                   'A maintenance fee payment of 2000 rupees was recorded for Block C rooms'],
  'correct_answer_must_state': 'These are two unrelated events (a room allotment vs. a maintenance '
                               'fee charge) -- no connection between them exists in the data.',
  'id': 'H1',
  'expect_connected': False,
  'kind2_trap': None},
 {'question': "Was the scholarship used to pay the student's tuition fee?",
  'trap_records': ['Scholarship disbursement of 15000 rupees was processed for a first-year '
                   'student',
                   'Tuition fee payment of 45000 rupees was received from a student'],
  'correct_answer_must_state': 'No stated connection exists between this scholarship disbursement '
                               'and this tuition payment -- they are separate records, not a '
                               'single financial transaction.',
  'id': 'H2',
  'expect_connected': False,
  'kind2_trap': None},
 {'question': 'Did the student who checked out of the hostel also cancel their transport pass?',
  'trap_records': ['A student checked out of the hostel at the end of the semester',
                   'A student requested a refund for an unused transport pass'],
  'correct_answer_must_state': 'No evidence links these two records to the same student or event '
                               '-- they are independent.',
  'id': 'H3',
  'expect_connected': False,
  'kind2_trap': None},
 {'question': "Did the alumni donation get used to fund the robotics club's competition budget?",
  'trap_records': ['An alumni donation was received for the new library wing',
                   'A student club requested funding for an upcoming competition'],
  'correct_answer_must_state': 'No stated connection exists between this alumni donation '
                               "(earmarked for the library wing) and this club's funding request "
                               '-- they are separate records.',
  'id': 'H4',
  'expect_connected': False,
  'kind2_trap': None},
 {'question': "Is the student's parking permit issue connected to their bus pass complaint?",
  'trap_records': ['A student reported a lost parking permit sticker',
                   'Transport helpdesk resolved a lost bus pass complaint'],
  'correct_answer_must_state': 'No evidence ties these two records to the same student or event -- '
                               'a parking permit and a transport pass are administered separately.',
  'id': 'H5',
  'expect_connected': False,
  'kind2_trap': None},
 {'question': "Did the hostel maintenance delay affect the student's exam results?",
  'trap_records': ['Elevator maintenance was scheduled for the administrative block',
                   "A student's backlog exam was scheduled for the next session"],
  'correct_answer_must_state': 'No connection is stated between a facilities maintenance record '
                               "and an exam scheduling record -- these categories don't even share "
                               'vocabulary, so any causal story linking them is fabricated, not '
                               'retrieved.',
  'id': 'H6',
  'expect_connected': False,
  'kind2_trap': None},
 {'question': "Was the broken door lock in Room 118 related to Student S006's earlier air "
              'conditioning request?',
  'trap_records': ["Facilities serviced the air conditioning unit in Room 118 at Student S006's "
                   'request',
                   'Student S012 reported a broken door lock in Room 118 during the following '
                   'semester'],
  'correct_answer_must_state': 'No -- these are two separate, unrelated maintenance events '
                               'involving two different students (S006 and S012). They happen to '
                               'share a room number, but a room number is a physical location, not '
                               'an event identifier -- it gets reused across many unrelated '
                               'incidents over time. A grounding check that links records by room '
                               'number alone (instead of by the actual named entity) would wrongly '
                               'report these as connected.',
  'id': 'H7',
  'expect_connected': False,
  'kind2_trap': 'Room number (Room 118)'},
 {'question': 'Was the fees of 46000 paid and then refunded for Student S009?',
  'kind2_trap': 'Amount (46000)',
  'trap_records': ["Student S009's tuition fee payment of 46000 rupees was received for the spring "
                   'semester',
                   "A refund of 46000 rupees was processed for a cancelled admission's fee "
                   'payment'],
  'correct_answer_must_state': "Student S009's 46000 tuition payment is recorded, and a 46000 "
                               'refund exists -- but the refund record names no student, and '
                               'nothing ties it to S009 or to that payment. The matching amount is '
                               'an incidental value, not an event identifier, so the data does not '
                               'say this payment was refunded.',
  'id': 'H8',
  'expect_connected': False},
 {'question': "Were the extra shuttle trips added so that students could get to the library's "
              'spring exam seating?',
  'kind2_trap': 'Semester (spring semester)',
  'trap_records': ['Library extended its seating for the spring semester exam preparation',
                   'Transport office added extra shuttle trips for the spring semester'],
  'correct_answer_must_state': 'No stated connection -- both records mention the spring semester, '
                               'but a semester is a time period shared by thousands of unrelated '
                               'events, not an identifier of one event. Nothing says the shuttle '
                               'trips were added for the library seating.',
  'id': 'H9',
  'expect_connected': False}]

HIDDEN_POSITIVE = [{'question': 'Was the hostel maintenance ticket HMT-58 for the broken window in Room 310 ever '
              'resolved?',
  'shared_identifier': 'HMT-58 (maintenance ticket) / Room 310',
  'correct_answer_must_state': 'Yes -- both records reference the same maintenance ticket (HMT-58) '
                               'and room (310), so this IS a genuine connection: the window was '
                               'reported broken and then fixed.',
  'id': 'HP1',
  'expect_connected': True,
  'shared_records': ['A hostel maintenance ticket (HMT-58) was filed by the student in Room 310 '
                     'for a broken window',
                     'Facilities resolved maintenance ticket HMT-58, replacing the broken window '
                     'in Room 310']},
 {'question': 'Did Student S001 receive a scholarship and also pay tuition this semester?',
  'shared_identifier': 'Student S001',
  'correct_answer_must_state': 'Yes -- both records name Student S001 specifically, so this IS a '
                               'genuine connection, unlike the general scholarship/fee trap '
                               'question where no shared identity is stated.',
  'id': 'HP2',
  'expect_connected': True,
  'shared_records': ["Student S001's merit scholarship of 20000 rupees was disbursed for the fall "
                     'semester',
                     "Student S001's tuition fee payment of 42000 rupees was received for the fall "
                     'semester']},
 {'question': "Did the robotics club's president both lead the new-member workshop and represent "
              'the club at the inter-college competition?',
  'shared_identifier': 'Club RC-1',
  'shared_records': ["The robotics club's workshop for new members was led by its club president "
                     '(Club RC-1)',
                     "The robotics club's president also represented the club (Club RC-1) at the "
                     'inter-college competition'],
  'correct_answer_must_state': 'Yes -- both records carry the same club code (Club RC-1), so the '
                               'same president did both.',
  'id': 'HP3',
  'expect_connected': True},
 {'question': "Was Alumnus A001's library-wing donation acknowledged, and did the same alumnus "
              'also attend homecoming?',
  'shared_identifier': 'Alumnus A001',
  'shared_records': ["Alumnus A001's donation for the new library wing was formally acknowledged "
                     'by the college',
                     'Alumnus A001 attended the homecoming networking event hosted by the alumni '
                     'association'],
  'correct_answer_must_state': 'Yes -- both records name Alumnus A001, so it is the same alumnus.',
  'id': 'HP4',
  'expect_connected': True}]

PUBLIC_ADVERSARIAL = [{'id': 'P1',
  'kind': 'Vocabulary overlap (money)',
  'question': 'When the scholarship was applied to the tuition fee, how much of the fee was left '
              'to pay?',
  'trap_records': ["A need-based scholarship award was credited to a student's account",
                   'Finance team sent a reminder for an unpaid tuition balance'],
  'correct_answer_must_state': 'Nothing links this scholarship record to that unpaid balance, so '
                               'the remaining fee cannot be worked out from the data.',
  'expect_connected': False},
 {'id': 'P2',
  'kind': 'Vocabulary overlap (room)',
  'question': 'Did the student who vacated their room early leave because of the leaking bathroom?',
  'trap_records': ['A student vacated their room early due to a course withdrawal',
                   'Plumbing repair request was logged for a leaking bathroom'],
  'correct_answer_must_state': 'No stated connection: the room vacated and the bathroom leak are '
                               'separate records and name no shared student.',
  'expect_connected': False},
 {'id': 'P3',
  'kind': 'Vocabulary overlap (pass/permit)',
  'question': "Was the returning student's parking permit renewed together with their transport "
              'pass?',
  'trap_records': ['Transport pass renewal was completed for the semester',
                   'Parking permit renewal was completed for a returning student'],
  'correct_answer_must_state': 'No evidence these two renewals belong to the same student; they '
                               'are separate records.',
  'expect_connected': False},
 {'id': 'P4',
  'kind': 'Vocabulary overlap (event)',
  'question': 'Was the alumni networking event part of the cultural fest schedule?',
  'trap_records': ['Alumni association organized a networking event for graduates',
                   'Cultural fest committee finalized the event schedule'],
  'correct_answer_must_state': 'No stated connection: both mention an event, but nothing ties them '
                               'to the same event.',
  'expect_connected': False},
 {'id': 'P5',
  'kind': 'Kind 2 trap: room number',
  'question': 'Did the new student allotted Room 214 cause the plumbing leak in that room?',
  'trap_records': ['Room 214 was allotted to a new student this week',
                   'Plumbing repair in Room 214 was completed after a leak was reported'],
  'correct_answer_must_state': 'No stated connection: both mention Room 214, but a room number is '
                               'a location reused over time, not an event identifier.',
  'expect_connected': False},
 {'id': 'P6',
  'kind': 'Kind 2 trap: block',
  'question': 'Did the roommate conflict in Block C lead to the Block C maintenance fee?',
  'trap_records': ['Hostel warden resolved a roommate conflict in Block C',
                   'A maintenance fee payment of 2000 rupees was recorded for Block C rooms'],
  'correct_answer_must_state': 'No stated connection: sharing a block name is not sharing an '
                               'event.',
  'expect_connected': False},
 {'id': 'P7',
  'kind': 'Kind 2 trap: amount',
  'question': 'Was the 500 rupee library fine paid to cover the parking fine?',
  'trap_records': ['A library fine of 500 rupees was collected from a student for a damaged book',
                   'A parking fine of 500 rupees was collected from a student for an unregistered '
                   'vehicle'],
  'correct_answer_must_state': 'No stated connection: the two fines happen to be the same amount, '
                               'which is a coincidence of value, not a shared event.',
  'expect_connected': False},
 {'id': 'P8',
  'kind': 'Cross-category causal',
  'question': 'Did the server downtime affect the pending placement offers?',
  'trap_records': ['Server downtime affected the online portal for two hours',
                   'Placement officer followed up with a company on pending offers'],
  'correct_answer_must_state': 'No stated connection between an IT outage and a placement '
                               'follow-up; any causal story is invented.',
  'expect_connected': False}]

PUBLIC_POSITIVE = [{'id': 'PP1',
  'question': 'Was Student S002 charged a late fee and also approved for scholarship renewal?',
  'shared_identifier': 'Student S002',
  'shared_records': ["Student S002 was charged a late fee penalty on last month's tuition invoice",
                     "Student S002's scholarship renewal was approved for the second year"],
  'correct_answer_must_state': 'Yes -- both records name Student S002.',
  'expect_connected': True},
 {'id': 'PP2',
  'question': 'Did Student S009 renew both their bus pass and their parking permit?',
  'shared_identifier': 'Student S009',
  'shared_records': ["Student S009's bus pass was renewed for the spring semester",
                     "Student S009's parking permit was renewed for the spring semester"],
  'correct_answer_must_state': 'Yes -- both records name Student S009.',
  'expect_connected': True},
 {'id': 'PP3',
  'question': "Was Alumnus A002's mentorship funding approved, and was the same alumnus invited to "
              'speak at convocation?',
  'shared_identifier': 'Alumnus A002',
  'shared_records': ["Alumnus A002's mentorship program funding was approved by the alumni "
                     'association',
                     'Alumnus A002 was invited to speak at the annual convocation as a '
                     'distinguished alumnus'],
  'correct_answer_must_state': 'Yes -- both records name Alumnus A002.',
  'expect_connected': True}]

# backwards-compatible names used by earlier notebooks
hidden_adversarial_tests = HIDDEN_ADVERSARIAL
hidden_positive_control_tests = HIDDEN_POSITIVE

if __name__ == "__main__":
    print(f"Records: {len(campus_texts)} | categories: {len(campus_categories)}")
    print(f"Hidden: {len(HIDDEN_ADVERSARIAL)} adversarial, {len(HIDDEN_POSITIVE)} positive")
    print(f"Public: {len(PUBLIC_ADVERSARIAL)} adversarial, {len(PUBLIC_POSITIVE)} positive")
