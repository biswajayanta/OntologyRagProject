"""
Day 2 competition dataset v2 — Campus Operations & Student Services.
Expanded: 14 categories (was 10), 4 deliberately overlapping pairs (was 2),
6 hidden adversarial test cases (was 3) -- including one "causal fabrication"
trap that isn't a vocabulary-overlap pair at all, to test whether an agent
invents a causal story across categories that don't even share language.
"""

campus_categories = {
    "Admissions": [
        "A new student's admission application was reviewed by the committee",
        "Entrance exam scorecard was verified for a incoming student",
        "Admission offer letter was issued to a selected candidate",
        "A student's transfer application from another college was processed",
        "Document verification was completed for a first-year admission",
        "Admission committee flagged a discrepancy in a submitted transcript",
        "Waitlisted candidate was offered a seat after a dropout",
        "Provisional admission was confirmed pending final marksheet submission",
        "International student's visa documents were reviewed for admission",
        "Admission counselor scheduled a call with a prospective student",
        "Student S013's admission document verification was completed ahead of orientation",
    ],
    "Fees_Finance": [
        "Tuition fee payment of 45000 rupees was received from a student",
        "A late fee penalty was applied to an overdue tuition payment",
        "Fee receipt was generated for the current semester payment",
        "A student requested an installment plan for pending tuition fees",
        "Refund was processed for a cancelled admission's fee payment",
        "Finance office reconciled the semester's total fee collection",
        "A bounced fee payment was flagged for reprocessing",
        "Hostel fee and tuition fee were combined into one invoice",
        "A student's fee payment was adjusted after a course change",
        "Finance team sent a reminder for an unpaid tuition balance",
        "Student S001's tuition fee payment of 42000 rupees was received for the fall semester",
        "Student S002 was charged a late fee penalty on last month's tuition invoice",
        "Student S004's tuition installment plan was approved by the finance office",
    ],
    "Scholarships": [
        "Scholarship disbursement of 15000 rupees was processed for a first-year student",
        "A merit scholarship application was approved by the review panel",
        "Scholarship renewal was submitted for the upcoming academic year",
        "A need-based scholarship award was credited to a student's account",
        "Scholarship committee rejected an incomplete application",
        "Sports scholarship was granted to a state-level athlete",
        "A student's scholarship was revoked due to low attendance",
        "External scholarship provider confirmed funding for a student",
        "Scholarship disbursement was delayed pending document resubmission",
        "A minority scholarship application was forwarded for government approval",
        "Student S001's merit scholarship of 20000 rupees was disbursed for the fall semester",
        "Student S002's scholarship renewal was approved for the second year",
        "Student S003's sports scholarship was confirmed by the athletics department",
    ],
    "Hostel_Accommodation": [
        "Room 214 was allotted to a new student this week",
        "A hostel room change request was approved for a second-year student",
        "Hostel warden resolved a roommate conflict in Block C",
        "A student checked out of the hostel at the end of the semester",
        "New hostel admission form was submitted for the upcoming term",
        "Hostel curfew violation was reported to the warden's office",
        "A student requested a single-occupancy room upgrade",
        "Hostel mess registration was completed for a new resident",
        "Room allotment list was published for incoming hostel students",
        "A student vacated their room early due to a course withdrawal",
        "Student S006's room change request to Room 118 was approved",
        "Student S007 reported a curfew violation warning from the hostel warden",
        "A hostel maintenance ticket (HMT-58) was filed by the student in Room 310 for a broken window",
    ],
    "Facilities_Maintenance": [
        "A maintenance fee payment of 2000 rupees was recorded for Block C rooms",
        "Electrician was dispatched to fix a wiring issue in the hostel block",
        "Plumbing repair request was logged for a leaking bathroom",
        "Facilities team repainted the corridor walls in the academic block",
        "Air conditioning unit was serviced in the seminar hall",
        "A broken window pane was replaced in the library building",
        "Elevator maintenance was scheduled for the administrative block",
        "Facilities flagged a structural crack for engineering inspection",
        "Water cooler was repaired in the student common area",
        "Furniture replacement was approved for the outdated classroom desks",
        "Facilities resolved maintenance ticket HMT-58, replacing the broken window in Room 310",
        "Facilities serviced the air conditioning unit in Room 118 at Student S006's request",
        "Student S008 filed a complaint about a leaking bathroom in a different block",
        "Student S012 reported a broken door lock in Room 118 during the following semester",
    ],
    "Library": [
        "A student issued three reference books for the semester",
        "Overdue library fine was paid by a student for a late return",
        "New journal subscriptions were added to the digital library",
        "A damaged book was reported and replaced in the collection",
        "Library extended its hours during the examination period",
        "A student requested an inter-library loan for a rare textbook",
        "Library staff reshelved returned books after the rush week",
        "E-book access was granted to a student for an online course",
        "A lost book fee was charged to a student's account",
        "Library conducted an annual stock verification of its collection",
        "Student S013 issued two reference textbooks for their first-year courses",
        "Student S015 was charged a lost book fee after misplacing a library textbook",
    ],
    "IT_Helpdesk": [
        "A student's login credentials were reset after a lockout",
        "Wi-Fi connectivity issue was reported in the academic block",
        "IT helpdesk resolved a printer malfunction in the computer lab",
        "A student's email account was migrated to the new domain",
        "Software installation request was completed for a lab machine",
        "IT flagged a phishing email reported by a faculty member",
        "A student's laptop was unable to connect to the campus network",
        "IT helpdesk ticket was closed after a successful password reset",
        "Server downtime affected the online portal for two hours",
        "A student requested VPN access for remote library resources",
        "Student S014's laptop was unable to connect to the campus Wi-Fi network",
    ],
    "Placement_Careers": [
        "A student was shortlisted for a summer internship interview",
        "Placement cell scheduled a pre-placement talk with a recruiter",
        "A student received a job offer through the campus placement drive",
        "Resume workshop was conducted for final-year students",
        "Placement officer followed up with a company on pending offers",
        "A student withdrew from the placement process after a personal offer",
        "Mock interview session was organized for placement preparation",
        "Company representative visited campus for a recruitment drive",
        "A student's internship certificate was verified by the placement office",
        "Placement statistics were compiled for the annual report",
        "Student S013 was shortlisted for a summer internship interview by a recruiting company",
    ],
    "Events_Clubs": [
        "The robotics club organized a workshop for new members",
        "Cultural fest committee finalized the event schedule",
        "A student club requested funding for an upcoming competition",
        "Annual sports day events were scheduled across three days",
        "The photography club held an exhibition in the main hall",
        "Student council approved a new club's registration",
        "A guest lecture was organized by the entrepreneurship cell",
        "Debate club members prepared for an inter-college competition",
        "The music club performed at the college's annual day",
        "A club's event proposal was rejected due to a venue conflict",
        "The robotics club's workshop for new members was led by its club president (Club RC-1)",
        "The robotics club's president also represented the club (Club RC-1) at the inter-college competition",
    ],
    "Transport": [
        "A new bus route was added for students from the north campus",
        "Transport pass renewal was completed for the semester",
        "A student reported a delay on the college shuttle service",
        "Transport office adjusted the bus schedule for exam week",
        "A damaged bus seat was reported to the transport department",
        "Student transport fee was included in the semester invoice",
        "A new driver was assigned to the evening shuttle route",
        "Transport helpdesk resolved a lost bus pass complaint",
        "Additional buses were arranged for the college fest weekend",
        "A student requested a refund for an unused transport pass",
        "Student S009's bus pass was renewed for the spring semester",
        "Student S011 filed a complaint about a delayed shuttle on the north campus route",
    ],
    "Parking_Permits": [
        "A student's parking permit application was approved for the fall semester",
        "Parking enforcement issued a warning for an expired permit",
        "A visitor parking pass was requested for a campus event",
        "Parking permit renewal was completed for a returning student",
        "A student reported a lost parking permit sticker",
        "Parking office resolved a dispute over an assigned spot",
        "A faculty parking permit was upgraded to a reserved spot",
        "Parking permit fee was waived for a shared carpool application",
        "A damaged permit sticker was replaced at the parking office",
        "Student S016's parking permit application was approved for the spring term",
        "Parking violation notice was issued for an unregistered vehicle",
        "Student S009's parking permit was renewed for the spring semester",
        "Student S010 received a parking violation notice for an unregistered vehicle",
    ],
    "Alumni_Relations": [
        "An alumni donation was received for the new library wing",
        "Alumni association organized a networking event for graduates",
        "A former student's contact details were updated in the alumni database",
        "Alumni newsletter was sent out for the quarterly update",
        "An alumni-funded scholarship endowment was reviewed by the committee",
        "Alumni relations office confirmed a guest speaker for homecoming",
        "A batch reunion event was scheduled for December",
        "Alumni association approved funding for a new mentorship program",
        "A distinguished alumnus was invited to the annual convocation",
        "Alumni donation records were reconciled for the fiscal year",
        "Alumnus A001's donation for the new library wing was formally acknowledged by the college",
        "Alumnus A001 attended the homecoming networking event hosted by the alumni association",
        "Alumnus A002's mentorship program funding was approved by the alumni association",
        "Alumnus A002 was invited to speak at the annual convocation as a distinguished alumnus",
    ],
    "Exam_Results": [
        "A student's semester grade report was published on the portal",
        "Exam committee resolved a discrepancy in a marksheet",
        "A student requested a re-evaluation of their exam paper",
        "Final exam results were released for the engineering department",
        "A student's backlog exam was scheduled for the next session",
        "Exam office issued a duplicate marksheet for a lost original",
        "A grade correction was approved after a clerical error was found",
        "Semester GPA was recalculated after a course withdrawal",
        "Exam hall ticket was issued for the upcoming semester exams",
        "A student's provisional degree certificate was requested after final results",
        "Student S014's backlog exam for a failed course was scheduled for next session",
    ],
    "Campus_Security": [
        "Campus security responded to a report of a stolen bicycle",
        "A lost ID card was recovered and returned through campus security",
        "Security patrol flagged an unlocked door in the academic block",
        "A student reported a suspicious person near the hostel gate",
        "Campus security reviewed CCTV footage after a minor incident",
        "A found wallet was logged at the campus security office",
        "Security escorted a student to their vehicle after a late-night event",
        "A broken security gate was reported for repair",
        "Campus security issued a visitor pass for an external vendor",
        "An access card malfunction was resolved by the security office",
        "Student S015 reported a lost ID card to campus security",
        "Student S016's vehicle was found unlocked by a security patrol and secured",
    ],
}

campus_texts = []
campus_labels = []
for category, sentences in campus_categories.items():
    for s in sentences:
        campus_texts.append(s)
        campus_labels.append(category)

print(f"Total records: {len(campus_texts)}")
print(f"Categories: {len(campus_categories)}")
print(f"Unique sentences: {len(set(campus_texts))}")

# ---------------------------------------------------------------------------
# Known vocabulary-overlap pairs (for reference/teaching -- NOT given to teams)
# ---------------------------------------------------------------------------
KNOWN_OVERLAP_PAIRS = [
    ("Fees_Finance", "Scholarships"),                # both involve money/amounts
    ("Hostel_Accommodation", "Facilities_Maintenance"),  # both mention "room"
    ("Transport", "Parking_Permits"),                # both mention "pass"/"permit"/vehicle
    ("Events_Clubs", "Alumni_Relations"),             # both mention "event"/"funding"
]

# ---------------------------------------------------------------------------
# Hidden adversarial test set -- held out, NEVER shown to teams before judging.
# 6 cases: one per known overlap pair, plus 2 that go further -- testing
# whether an agent fabricates a connection between categories that DON'T even
# share vocabulary (a harder, more general test of the same failure mode).
# ---------------------------------------------------------------------------
hidden_adversarial_tests = [
    {
        "question": "Tell me about the recent payment made for the student's room.",
        "trap_pair": ("Hostel_Accommodation", "Facilities_Maintenance"),
        "trap_records": [
            "Room 214 was allotted to a new student this week",
            "A maintenance fee payment of 2000 rupees was recorded for Block C rooms",
        ],
        "correct_answer_must_state": "These are two unrelated events (a room allotment vs. a maintenance fee charge) -- no connection between them exists in the data.",
    },
    {
        "question": "Was the scholarship used to pay the student's tuition fee?",
        "trap_pair": ("Scholarships", "Fees_Finance"),
        "trap_records": [
            "Scholarship disbursement of 15000 rupees was processed for a first-year student",
            "Tuition fee payment of 45000 rupees was received from a student",
        ],
        "correct_answer_must_state": "No stated connection exists between this scholarship disbursement and this tuition payment -- they are separate records, not a single financial transaction.",
    },
    {
        "question": "Did the student who checked out of the hostel also cancel their transport pass?",
        "trap_pair": ("Hostel_Accommodation", "Transport"),
        "trap_records": [
            "A student checked out of the hostel at the end of the semester",
            "A student requested a refund for an unused transport pass",
        ],
        "correct_answer_must_state": "No evidence links these two records to the same student or event -- they are independent.",
    },
    {
        "question": "Did the alumni donation get used to fund the robotics club's competition budget?",
        "trap_pair": ("Alumni_Relations", "Events_Clubs"),
        "trap_records": [
            "An alumni donation was received for the new library wing",
            "A student club requested funding for an upcoming competition",
        ],
        "correct_answer_must_state": "No stated connection exists between this alumni donation (earmarked for the library wing) and this club's funding request -- they are separate records.",
    },
    {
        "question": "Is the student's parking permit issue connected to their bus pass complaint?",
        "trap_pair": ("Parking_Permits", "Transport"),
        "trap_records": [
            "A student reported a lost parking permit sticker",
            "Transport helpdesk resolved a lost bus pass complaint",
        ],
        "correct_answer_must_state": "No evidence ties these two records to the same student or event -- a parking permit and a transport pass are administered separately.",
    },
    {
        "question": "Did the hostel maintenance delay affect the student's exam results?",
        "trap_pair": ("Facilities_Maintenance", "Exam_Results"),
        "trap_records": [
            "Elevator maintenance was scheduled for the administrative block",
            "A student's backlog exam was scheduled for the next session",
        ],
        "correct_answer_must_state": "No connection is stated between a facilities maintenance record and an exam scheduling record -- these categories don't even share vocabulary, so any causal story linking them is fabricated, not retrieved.",
    },
    {
        "question": "Was the broken door lock in Room 118 related to Student S006's earlier air conditioning request?",
        "trap_pair": ("Facilities_Maintenance", "Facilities_Maintenance"),
        "trap_records": [
            "Facilities serviced the air conditioning unit in Room 118 at Student S006's request",
            "Student S012 reported a broken door lock in Room 118 during the following semester",
        ],
        "correct_answer_must_state": "No -- these are two separate, unrelated maintenance events involving two different students (S006 and S012). They happen to share a room number, but a room number is a physical location, not an event identifier -- it gets reused across many unrelated incidents over time. A grounding check that links records by room number alone (instead of by the actual named entity) would wrongly report these as connected.",
    },
]

print(f"\nOverlap pairs: {len(KNOWN_OVERLAP_PAIRS)}")
print(f"Hidden adversarial test cases: {len(hidden_adversarial_tests)}")

# ---------------------------------------------------------------------------
# Positive control -- the one deliberately LINKED pair in the dataset.
# Everything else in hidden_adversarial_tests should be flagged as unrelated;
# this one should be correctly flagged as CONNECTED. Without this, a system
# that just blanket-answers "these are unrelated" to every ambiguous
# question would score perfectly on fabrication avoidance without actually
# checking anything -- this case catches that.
# ---------------------------------------------------------------------------
hidden_positive_control_tests = [
    {
        "question": "Was the hostel maintenance ticket HMT-58 for the broken window in Room 310 ever resolved?",
        "linked_pair": ("Hostel_Accommodation", "Facilities_Maintenance"),
        "shared_identifier": "HMT-58 (maintenance ticket) / Room 310",
        "records": [
            "A hostel maintenance ticket (HMT-58) was filed by the student in Room 310 for a broken window",
            "Facilities resolved maintenance ticket HMT-58, replacing the broken window in Room 310",
        ],
        "correct_answer_must_state": "Yes -- both records reference the same maintenance ticket (HMT-58) and room (310), so this IS a genuine connection: the window was reported broken and then fixed.",
    },
    {
        "question": "Did Student S001 receive a scholarship and also pay tuition this semester?",
        "linked_pair": ("Scholarships", "Fees_Finance"),
        "shared_identifier": "Student S001",
        "records": [
            "Student S001's merit scholarship of 20000 rupees was disbursed for the fall semester",
            "Student S001's tuition fee payment of 42000 rupees was received for the fall semester",
        ],
        "correct_answer_must_state": "Yes -- both records name Student S001 specifically, so this IS a genuine connection, unlike the general scholarship/fee trap question where no shared identity is stated.",
    },
    {
        "question": "Did Student S009 renew both their bus pass and their parking permit?",
        "linked_pair": ("Transport", "Parking_Permits"),
        "shared_identifier": "Student S009",
        "records": [
            "Student S009's bus pass was renewed for the spring semester",
            "Student S009's parking permit was renewed for the spring semester",
        ],
        "correct_answer_must_state": "Yes -- both records name Student S009 specifically and both happened for the spring semester, so this IS a genuine connection.",
    },
]

print(f"\nPositive control test cases: {len(hidden_positive_control_tests)} (all explicitly named-entity links)")
