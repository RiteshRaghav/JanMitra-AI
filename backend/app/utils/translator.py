# -*- coding: utf-8 -*-
from typing import Dict, Any, List

HINDI_TRANSLATION_MAP = {
    # Documents
    "Aadhaar Card": "आधार कार्ड",
    "Ration Card": "राशन कार्ड",
    "Ration Card (PHH or AAY)": "राशन कार्ड (PHH या AAY)",
    "Bank Passbook": "बैंक पासबुक",
    "Bank Passbook (linked with Aadhaar)": "बैंक पासबुक (आधार से लिंक)",
    "Land Record / Land Ownership Certificate": "भूमि रिकॉर्ड / भूमि स्वामित्व प्रमाणपत्र",
    "Samagra ID": "समग्र आईडी",
    "Samagra ID (Family & Individual)": "समग्र आईडी (परिवार और व्यक्तिगत)",
    "Domicile Certificate": "मूल निवासी प्रमाण पत्र",
    "Domicile Certificate of Madhya Pradesh": "मध्य प्रदेश का मूल निवासी प्रमाण पत्र",
    "Domicile Certificate of Uttar Pradesh": "उत्तर प्रदेश का मूल निवासी प्रमाण पत्र",
    "Income Certificate": "आय प्रमाण पत्र",
    "Income Certificate (showing household income <= ₹1.2 Lakhs)": "आय प्रमाण पत्र (पारिवारिक आय ₹1.2 लाख से कम दर्शाने वाला)",
    "Income Certificate (showing household income <= ₹2 Lakhs)": "आय प्रमाण पत्र (पारिवारिक आय ₹2 लाख से कम दर्शाने वाला)",
    "Income Certificate of parents (annual income <= ₹2.5 Lakhs)": "माता-पिता का आय प्रमाण पत्र (वार्षिक आय ₹2.5 लाख से कम)",
    "Caste Certificate": "जाति प्रमाण पत्र",
    "Caste Certificate (if applicable)": "जाति प्रमाण पत्र (यदि लागू हो)",
    "Caste Certificate (issued by competent authority)": "जाति प्रमाण पत्र (सक्षम अधिकारी द्वारा जारी)",
    "Disability Certificate": "विकलांगता प्रमाण पत्र",
    "Disability Certificate (40% or more disability)": "विकलांगता प्रमाण पत्र (40% या अधिक विकलांगता)",
    "Student ID": "छात्र आईडी",
    "Student ID Card / Proof of Admission": "छात्र आईडी कार्ड / प्रवेश का प्रमाण",
    "Mobile Number linked with Aadhaar": "आधार से लिंक मोबाइल नंबर",
    "PAN Card": "पैन कार्ड",
    "GSTIN Number (for micro/small enterprises)": "GSTIN नंबर (सूक्ष्म/लघु उद्यमों के लिए)",
    "Business Address details": "व्यापारिक पते का विवरण",
    "Marriage Certificate": "विवाह प्रमाण पत्र",
    "Joint Bank Account Passbook": "संयुक्त बैंक खाता पासबुक",
    "Age Proof (Birth Certificate or School Leaving Certificate)": "आयु प्रमाण (जन्म प्रमाण पत्र या स्कूल छोड़ने का प्रमाण पत्र)",
    "BPL Card (Below Poverty Line) or Income Certificate": "बीपीएल कार्ड (गरीबी रेखा से नीचे) या आय प्रमाण पत्र",
    "Passport Size Photograph": "पासपोर्ट आकार की तस्वीर",
    "Affidavit stating that you do not own any pucca house anywhere in India": "शपथ पत्र कि भारत में कहीं भी आपका कोई पक्का घर नहीं है",
    "Bank Account Statement": "बैंक खाता विवरण",
    "Mobile number linked with Samagra": "समग्र से लिंक मोबाइल नंबर",

    # Scheme Names & Ministries
    "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)",
    "Ministry of Agriculture and Farmers Welfare": "कृषि एवं किसान कल्याण मंत्रालय",
    "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
    "Ministry of Health and Family Welfare": "स्वास्थ्य एवं परिवार कल्याण मंत्रालय",
    "Pradhan Mantri Awas Yojana - Urban (PMAY-U)": "प्रधानमंत्री आवास योजना - शहरी (PMAY-U)",
    "Ministry of Housing and Urban Affairs": "आवास और शहरी मामलों के मंत्रालय",
    "Post Matric Scholarship for OBC / SC / ST Students": "ओबीसी / एससी / एसटी छात्रों के लिए पोस्ट मैट्रिक छात्रवृत्ति",
    "Ministry of Social Justice and Empowerment": "सामाजिक न्याय और अधिकारिता मंत्रालय",
    "Mukhyamantri Ladli Behna Yojana (MP)": "मुख्यमंत्री लाड़ली बहना योजना (MP)",
    "Women and Child Development Department, Madhya Pradesh": "महिला एवं बाल विकास विभाग, मध्य प्रदेश",
    "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)": "इन्दिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना (IGNOAPS)",
    "Ministry of Rural Development": "ग्रामीण विकास मंत्रालय",
    "Udyam MSME Registration & Support Portal": "उद्यम एमएसएमई पंजीकरण और सहायता पोर्टल",
    "Ministry of Micro, Small and Medium Enterprises": "सूक्ष्म, लघु और मध्यम उद्यम मंत्रालय",
    "Divyangjan Shadi Protsahan Yojana (UP)": "दिव्यांगजन शादी प्रोत्साहन योजना (UP)",
    "Empowerment of Persons with Disabilities Department, Uttar Pradesh": "दिव्यांगजन सशक्तिकरण विभाग, उत्तर प्रदेश",

    # Benefits
    "Guaranteed income support of ₹6,000 per year paid in three equal installments of ₹2,000 directly into the bank accounts of farmers.": "किसानों के बैंक खातों में सीधे ₹2,000 की तीन समान किश्तों में प्रति वर्ष ₹6,000 की गारंटीकृत आय सहायता।",
    "Access to credit card facilities (Kisan Credit Card) with subsidized interest rates.": "रियायती ब्याज दरों पर क्रेडिट कार्ड सुविधाओं (किसान क्रेडिट कार्ड) तक पहुंच।",
    "Cashless health cover of up to ₹5 Lakhs per family per year for secondary and tertiary care hospitalization.": "माध्यमिक और तृतीयक देखभाल अस्पताल में भर्ती के लिए प्रति परिवार प्रति वर्ष ₹5 लाख तक का कैशलेस स्वास्थ्य कवर।",
    "Covers pre-existing conditions from day one of enrollment.": "नामांकन के पहले दिन से ही पहले से मौजूद बीमारियों को कवर करता है।",
    "No restriction on family size, age, or gender.": "परिवार के आकार, आयु या लिंग पर कोई प्रतिबंध नहीं है।",
    "Interest subsidy up to 6.5% on home loans under CLSS for EWS/LIG categories.": "EWS/LIG श्रेणियों के लिए CLSS के तहत गृह ऋण पर 6.5% तक ब्याज सब्सिडी।",
    "Financial assistance up to ₹1.5 Lakhs for construction of new houses or enhancement of existing ones.": "नए घरों के निर्माण या मौजूदा घरों के विस्तार के लिए ₹1.5 लाख तक की वित्तीय सहायता।",
    "Empowerment: The house must be owned or co-owned by a female head of the family.": "सशक्तिकरण: घर का स्वामित्व परिवार की महिला मुखिया के नाम या संयुक्त नाम पर होना चाहिए।",
    "100% reimbursement of compulsory non-refundable fees charged by educational institutions.": "शैक्षणिक संस्थानों द्वारा लिए जाने वाले अनिवार्य गैर-वापसी योग्य शुल्कों की 100% प्रतिपूर्ति।",
    "Monthly maintenance allowance ranging from ₹300 to ₹1,200 depending on course groups and hostel status.": "कोर्स समूहों और हॉस्टल स्थिति के आधार पर ₹300 से ₹1,200 प्रति माह तक का रखरखाव भत्ता।",
    "Monthly direct benefit transfer (DBT) of ₹1,250 into the beneficiary woman's bank account.": "लाभार्थी महिला के बैंक खाते में ₹1,250 का मासिक प्रत्यक्ष लाभ हस्तांतरण (DBT)।",
    "Monthly pension of ₹200 for citizens aged 60-79 years.": "60-79 वर्ष की आयु के नागरिकों के लिए ₹200 मासिक पेंशन।",
    "Increased monthly pension of ₹500 for senior citizens aged 80 years and above.": "80 वर्ष और उससे अधिक आयु के वरिष्ठ नागरिकों के लिए बढ़ाकर ₹500 मासिक पेंशन।",
    "States usually add matching contributions, bringing total pension up to ₹1,000 - ₹3,000 depending on the state.": "राज्य आमतौर पर अपना हिस्सा भी जोड़ते हैं, जिससे राज्य के आधार पर कुल पेंशन ₹1,000 - ₹3,000 तक हो जाती है।",
    "Free permanent registration number and digital certificate.": "मुफ़्त स्थायी पंजीकरण संख्या और डिजिटल प्रमाणपत्र।",
    "Collateral-free loans under CGTMSE and sub-vention on loan interest rates.": "CGTMSE के तहत संपार्श्विक-मुक्त (बिना गारंटी) ऋण और ऋण ब्याज दरों पर छूट।",
    "Exemption in government tenders, energy bills, and patent filing costs.": "सरकारी निविदाओं, बिजली बिलों और पेटेंट फाइलिंग लागतों में छूट।",
    "Financial incentive up to ₹35,000 for disabled couples upon marriage (₹15,000 if husband is disabled, ₹20,000 if wife is disabled, and ₹35,000 if both are disabled).": "विवाह पर विकलांग जोड़ों के लिए ₹35,000 तक का वित्तीय प्रोत्साहन (यदि पति विकलांग है तो ₹15,000, यदि पत्नी विकलांग है तो ₹20,000, और यदि दोनों विकलांग हैं तो ₹35,000)।",

    # Application Steps
    "Visit the official PM-KISAN portal (pmkisan.gov.in).": "आधिकारिक पीएम-किसान पोर्टल (pmkisan.gov.in) पर जाएं।",
    "Click on 'New Farmer Registration' and enter your Aadhaar Number and Captcha.": "'New Farmer Registration' पर क्लिक करें और अपना आधार नंबर और कैप्चा दर्ज करें।",
    "Select State, District, Block, and Village, then enter land details and upload land records.": "राज्य, जिला, ब्लॉक और गांव का चयन करें, फिर भूमि का विवरण दर्ज करें और भूमि दस्तावेज अपलोड करें।",
    "Submit the form. State government authorities will verify and approve details.": "फॉर्म जमा करें। राज्य सरकार के अधिकारी विवरणों को सत्यापित और स्वीकृत करेंगे।",
    "Funds will be disbursed once verification is successful.": "सत्यापन सफल होने के बाद धनराशि वितरित की जाएगी।",
    "Check eligibility on the PMJAY portal (mera.pmjay.gov.in) using your mobile number or Ration Card.": "अपने मोबाइल नंबर या राशन कार्ड का उपयोग करके PMJAY पोर्टल (mera.pmjay.gov.in) पर पात्रता की जांच करें।",
    "Visit an empanelled government or private hospital or a CSC center.": "किसी सूचीबद्ध सरकारी या निजी अस्पताल या सीएससी (CSC) केंद्र पर जाएं।",
    "Present your Aadhaar Card and Ration Card to the Ayushman Mitra.": "आयुष्मान मित्र के समक्ष अपना आधार कार्ड और राशन कार्ड प्रस्तुत करें।",
    "Get your Ayushman Golden Card generated after biometrics verification.": "बायोमेट्रिक्स सत्यापन के बाद अपना आयुष्मान गोल्डन कार्ड जनरेट करवाएं।",
    "Avail cashless treatments directly at empanelled healthcare facilities.": "सूचीबद्ध स्वास्थ्य सुविधाओं पर सीधे कैशलेस उपचार का लाभ उठाएं।",
    "Log in to the official PMAY portal (pmaymis.gov.in).": "आधिकारिक PMAY पोर्टल (pmaymis.gov.in) पर लॉग इन करें।",
    "Select 'Citizen Assessment' and choose 'Benefit under other 3 components' or 'Slum Dwellers'.": "'Citizen Assessment' चुनें और 'Benefit under other 3 components' या 'Slum Dwellers' का चयन करें।",
    "Enter Aadhaar details and fill out the detailed application form containing income, family, and contact details.": "आधार विवरण दर्ज करें और आय, परिवार और संपर्क विवरण वाला विस्तृत आवेदन फॉर्म भरें।",
    "Save the system-generated application number for tracking.": "ट्रैकिंग के लिए सिस्टम द्वारा जनरेट की गई आवेदन संख्या को सुरक्षित रखें।",
    "Wait for physical verification by local municipal authorities.": "स्थानीय नगर निकायों द्वारा भौतिक सत्यापन की प्रतीक्षा करें।",
    "Register on the National Scholarship Portal (scholarships.gov.in).": "राष्ट्रीय छात्रवृत्ति पोर्टल (scholarships.gov.in) पर पंजीकरण करें।",
    "Complete registration and log in using the Student Application ID.": "पंजीकरण पूरा करें और छात्र आवेदन आईडी का उपयोग करके लॉग इन करें।",
    "Fill out course, academic, and basic profiling details.": "पाठ्यक्रम, शैक्षणिक और बुनियादी प्रोफाइल विवरण भरें।",
    "Upload scanned copies of required documents including Fee Receipt, Caste/Income certificates.": "फीस रसीद, जाति/आय प्रमाण पत्र सहित आवश्यक दस्तावेजों की स्कैन की गई प्रतियां अपलोड करें।",
    "Submit and forward the digital copy to your school/college institute for verification.": "जमा करें और सत्यापन के लिए डिजिटल कॉपी को अपने स्कूल/कॉलेज संस्थान में भेजें।",
    "Visit the designated Gram Panchayat / Ward Office or Camp in MP.": "मध्य प्रदेश में मनोनीत ग्राम पंचायत / वार्ड कार्यालय या शिविर में जाएं।",
    "Get the application form printed out, fill in your Samagra ID and Aadhaar.": "आवेदन पत्र का प्रिंट आउट लें, उसमें अपनी समग्र आईडी और आधार भरें।",
    "Provide biometrics at the registration counter setup by the municipal officials.": "नगर निगम के अधिकारियों द्वारा स्थापित पंजीकरण काउंटर पर बायोमेट्रिक्स प्रदान करें।",
    "Get a printed acknowledgment receipt with a unique application ID.": "एक अद्वितीय आवेदन आईडी के साथ मुद्रित पावती रसीद प्राप्त करें।",
    "Verify that your bank account has e-KYC and active DBT status.": "सत्यापित करें कि आपका बैंक खाता ई-केवाईसी और सक्रिय डीबीटी स्थिति में है।",
    "Obtain the application form from the Social Welfare Department, Gram Panchayat, or Block Development Office.": "समाज कल्याण विभाग, ग्राम पंचायत या ब्लॉक विकास कार्यालय से आवेदन पत्र प्राप्त करें।",
    "Attach required documents, including age proof and BPL card verification.": "आयु प्रमाण और बीपीएल कार्ड सत्यापन सहित आवश्यक दस्तावेज संलग्न करें।",
    "Submit the application to the Gram Panchayat or Ward Office.": "आवेदन ग्राम पंचायत या वार्ड कार्यालय में जमा करें।",
    "Social Welfare inspectors will verify eligibility through field visits.": "समाज कल्याण निरीक्षक फील्ड दौरों के माध्यम से पात्रता का सत्यापन करेंगे।",
    "Once approved, the pension is deposited monthly in the Aadhaar-linked bank account.": "एक बार स्वीकृत होने के बाद, पेंशन मासिक रूप से आधार-लिंक्ड बैंक खाते में जमा की जाती है।",
    "Go to the official Udyam Registration portal (udyamregistration.gov.in).": "आधिकारिक उद्यम पंजीकरण पोर्टल (udyamregistration.gov.in) पर जाएं।",
    "Enter Aadhaar number and name, click on Validate and Generate OTP.": "आधार संख्या और नाम दर्ज करें, 'Validate and Generate OTP' पर क्लिक करें।",
    "Enter PAN card details and specify organization type.": "पैन कार्ड विवरण दर्ज करें और संगठन का प्रकार निर्दिष्ट करें।",
    "Provide plant location, investment figures, and annual turnover details.": "संयंत्र का स्थान, निवेश के आंकड़े और वार्षिक टर्नओवर का विवरण प्रदान करें।",
    "Submit the form and instantly download the Udyam Registration Certificate.": "फॉर्म जमा करें और तुरंत उद्यम पंजीकरण प्रमाणपत्र डाउनलोड करें।",
    "Visit the UP Divyangjan Shadi portal (divyangjan.upsdc.gov.in).": "यूपी दिव्यांगजन शादी पोर्टल (divyangjan.upsdc.gov.in) पर जाएं।",
    "Fill the online registration form within one year of marriage.": "विवाह के एक वर्ष के भीतर ऑनलाइन पंजीकरण फॉर्म भरें।",
    "Upload Aadhaar, Marriage certificate, Domicile certificate, and Disability certificate.": "आधार, विवाह प्रमाण पत्र, मूल निवासी प्रमाण पत्र और विकलांगता प्रमाण पत्र अपलोड करें।",
    "Submit the hard copy along with documents to the District Disabled Welfare Office within 15 days.": "दस्तावेजों के साथ हार्ड कॉपी 15 दिनों के भीतर जिला विकलांग कल्याण कार्यालय में जमा करें।",
    "Approved incentive is directly transferred to the joint bank account.": "स्वीकृत प्रोत्साहन सीधे संयुक्त बैंक खाते में स्थानांतरित कर दिया जाता है।",

    # FAQs
    "Is there any income limit for PM Kisan?": "क्या पीएम किसान के लिए कोई आय सीमा है?",
    "No specific income limit, but institutional landholders, government employees, and income tax payers are excluded.": "कोई विशिष्ट आय सीमा नहीं है, लेकिन संस्थागत भूमि धारक, सरकारी कर्मचारी और आयकर दाता बाहर हैं।",
    "Can joint landholders apply?": "क्या संयुक्त भूमि धारक आवेदन कर सकते हैं?",
    "Yes, joint landholders can also apply for the benefits proportionally as per government rules.": "हाँ, संयुक्त भूमि धारक भी सरकारी नियमों के अनुसार आनुपातिक रूप से लाभ के लिए आवेदन कर सकते हैं।",
    "Does Ayushman Bharat cover private hospitals?": "क्या आयुष्मान भारत निजी अस्पतालों को कवर करता है?",
    "Yes, it covers cashless treatment in both empanelled public and private hospitals across India.": "हाँ, यह पूरे भारत में सूचीबद्ध सार्वजनिक और निजी दोनों अस्पतालों में कैशलेस उपचार को कवर करता है।",
    "Is there a limit on family members?": "क्या परिवार के सदस्यों की कोई सीमा है?",
    "No, all family members listed in the household database can use the card. There is no size limit.": "नहीं, घरेलू डेटाबेस में सूचीबद्ध सभी परिवार के सदस्य कार्ड का उपयोग कर सकते हैं। इसकी कोई सीमा नहीं है।",
    "Can I apply if my family owns a home in my native village?": "यदि मेरे परिवार के पास मेरे मूल गाँव में घर है तो क्या मैं आवेदन कर सकता हूँ?",
    "No, the applicant and their family members must not own a pucca house in any part of India to be eligible.": "नहीं, पात्र होने के लिए आवेदक और उनके परिवार के सदस्यों के पास भारत के किसी भी हिस्से में पक्का घर नहीं होना चाहिए।",
    "Can general category students apply?": "क्या सामान्य श्रेणी के छात्र आवेदन कर सकते हैं?",
    "No, this scholarship is specifically for students belonging to SC, ST, and OBC categories. General category students with low income should explore EBC scholarships.": "नहीं, यह छात्रवृत्ति विशेष रूप से एससी, एसटी और ओबीसी श्रेणियों के छात्रों के लिए है। कम आय वाले सामान्य श्रेणी के छात्रों को ईबीसी छात्रवृत्ति का पता लगाना चाहिए।",
    "Can unmarried women apply for Ladli Behna?": "क्या अविवाहित महिलाएं लाड़ली बहना के लिए आवेदन कर सकती हैं?",
    "No, this scheme is currently only for married, widowed, divorced, or abandoned women aged 21-60.": "नहीं, यह योजना वर्तमान में केवल 21-60 वर्ष की विवाहित, विधवा, तलाकशुदा या परित्यक्त महिलाओं के लिए है।",
    "Do I need a BPL card for IGNOAPS?": "क्या मुझे IGNOAPS के लिए बीपीएल कार्ड की आवश्यकता है?",
    "Yes, applicants must belong to a household living below the poverty line (BPL) to qualify under central guidelines.": "हाँ, केंद्रीय दिशानिर्देशों के तहत अर्हता प्राप्त करने के लिए आवेदकों का गरीबी रेखा से नीचे (बीपीएल) रहने वाले परिवार से होना आवश्यक है।",
    "Is registration free?": "क्या पंजीकरण मुफ्त है?",
    "Yes, government registration is completely free of charge. Do not pay any private portals.": "हाँ, सरकारी पंजीकरण पूरी तरह से निःशुल्क है। किसी भी निजी पोर्टल को भुगतान न करें।",
    "What is the minimum percentage of disability required?": "विकलांगता का न्यूनतम आवश्यक प्रतिशत क्या है?",
    "The applicant must possess a valid Disability Certificate certifying at least 40% or higher disability.": "आवेदक के पास कम से कम 40% या उससे अधिक विकलांगता प्रमाणित करने वाला वैध विकलांगता प्रमाणपत्र होना चाहिए।",

    # Document guidelines steps
    "Visit the nearest Aadhaar Enrolment Centre (UIDAI).": "निकटतम आधार नामांकन केंद्र (UIDAI) पर जाएं।",
    "Fill out the Aadhaar Enrolment Form.": "आधार नामांकन फॉर्म भरें।",
    "Submit biometric details (fingerprints and iris scan) and identity/address proofs.": "बायोमेट्रिक विवरण (उंगलियों के निशान और आईरिस स्कैन) और पहचान/पते के प्रमाण जमा करें।",
    "Aadhaar is generated and dispatched within 10-15 days. E-Aadhaar can be downloaded online.": "आधार 10-15 दिनों के भीतर जनरेट और डिस्पैच किया जाता है। ई-आधार ऑनलाइन डाउनलोड किया जा सकता है।",
    "Apply online through your State Food and Civil Supplies portal or visit the nearest Circle Office.": "अपने राज्य के खाद्य और नागरिक आपूर्ति पोर्टल के माध्यम से ऑनलाइन आवेदन करें या निकटतम सर्कल कार्यालय पर जाएं।",
    "Submit Application Form along with Aadhaar card copies, Income Certificate, and gas connection details.": "आधार कार्ड की प्रतियों, आय प्रमाण पत्र और गैस कनेक्शन विवरण के साथ आवेदन पत्र जमा करें।",
    "Physical verification of residence will be done by a food inspector.": "खाद्य निरीक्षक द्वारा निवास का भौतिक सत्यापन किया जाएगा।",
    "Ration card is issued after verification.": "सत्यापन के बाद राशन कार्ड जारी किया जाता है।",
    "Visit the nearest branch of any commercial bank (SBI, PNB, etc.) or post office.": "किसी भी वाणिज्यिक बैंक (SBI, PNB, आदि) या डाकघर की निकटतम शाखा पर जाएं।",
    "Ask to open a 'Pradhan Mantri Jan Dhan Yojana' (PMJDY) zero-balance account.": "'प्रधानमंत्री जन धन योजना' (PMJDY) शून्य-बैलेंस खाता खोलने के लिए कहें।",
    "Submit Aadhaar Card and PAN card (or Form 60) along with 2 passport photographs.": "2 पासपोर्ट तस्वीरों के साथ आधार कार्ड और पैन कार्ड (या फॉर्म 60) जमा करें।",
    "Passbook is issued instantly, and Rupay debit card will arrive by post.": "पासबुक तुरंत जारी की जाती है, और रुपे डेबिट कार्ड डाक से आएगा।",
    "Access your State Bhulekh (Land Records) portal online.": "अपने राज्य के भूलेख (भूमि अभिलेख) पोर्टल पर ऑनलाइन जाएं।",
    "Select your District, Tehsil, and Village, then enter your Khasra or Khatauni number.": "अपने जिले, तहसील और गांव का चयन करें, फिर अपना खसरा या खतौनी नंबर दर्ज करें।",
    "Download/print the digitally signed copy of your land records.": "अपने भूमि रिकॉर्ड की डिजिटल रूप से हस्ताक्षरित प्रति डाउनलोड/प्रिंट करें।",
    "Alternatively, visit the local Tehsil office and request the Patwari or Lekhpal for an official copy.": "वैकल्पिक रूप से, स्थानीय तहसील कार्यालय जाएं और आधिकारिक प्रति के लिए पटवारी या लेखपाल से अनुरोध करें।",
    "Go to the official Samagra Portal (samagra.gov.in) (Madhya Pradesh residents only).": "आधिकारिक समग्र पोर्टल (samagra.gov.in) पर जाएं (केवल मध्य प्रदेश के निवासियों के लिए)।",
    "Click on 'Register Family / Member' under the Samagra Profile section.": "समग्र प्रोफाइल अनुभाग के तहत 'Register Family / Member' पर क्लिक करें।",
    "Enter details of family members, upload Aadhaar card, and perform Aadhaar OTP e-KYC.": "परिवार के सदस्यों का विवरण दर्ज करें, आधार कार्ड अपलोड करें, और आधार ओटीपी ई-केवाईसी करें।",
    "Samagra ID will be generated and approved by the local municipal/block office.": "समग्र आईडी जनरेट की जाएगी और स्थानीय नगर/ब्लॉक कार्यालय द्वारा अनुमोदित की जाएगी।",
    "Log in to the e-District portal of your respective State Government.": "अपने संबंधित राज्य सरकार के ई-डिस्ट्रिक्ट (e-District) पोर्टल पर लॉग इन करें।",
    "Register as a new citizen and fill out the Domicile Certificate Application Form.": "नए नागरिक के रूप में पंजीकरण करें और मूल निवासी प्रमाण पत्र आवेदन फॉर्म भरें।",
    "Upload utility bills, Aadhaar card, school leaving certificate, and self-declaration form.": "उपयोगिता बिल, आधार कार्ड, स्कूल छोड़ने का प्रमाण पत्र और स्व-घोषणा पत्र अपलोड करें।",
    "Pay the nominal fee (usually ₹15-30) and download the signed certificate once approved.": "नाममात्र शुल्क (आमतौर पर ₹15-30) का भुगतान करें और स्वीकृत होने पर हस्ताक्षरित प्रमाण पत्र डाउनलोड करें।",
    "Apply online via your State e-District portal or visit the local SDM/Tehsildar/CSC office.": "अपने राज्य के ई-डिस्ट्रिक्ट पोर्टल के माध्यम से ऑनलाइन आवेदन करें या स्थानीय एसडीएम/तहसीलदार/सीएससी कार्यालय पर जाएं।",
    "Provide proof of salary (salary slips / Form 16) or an affidavit of agricultural/business income.": "वेतन का प्रमाण (वेतन पर्ची / फॉर्म 16) या कृषि/व्यवसाय आय का शपथ पत्र प्रदान करें।",
    "Submit identity and residence proof along with a self-declaration statement.": "स्व-घोषणा पत्र के साथ पहचान और निवास का प्रमाण जमा करें।",
    "The Patwari/Revenue officer will conduct verification before issuing the certificate.": "प्रमाण पत्र जारी करने से पहले पटवारी/राजस्व अधिकारी सत्यापन करेंगे।",
    "Apply online through the State e-District portal or the Social Welfare Office.": "राज्य के ई-डिस्ट्रिक्ट पोर्टल या समाज कल्याण कार्यालय के माध्यम से ऑनलाइन आवेदन करें।",
    "Submit proof of caste (father's or close blood relative's caste certificate), identity proof, and affidavit.": "जाति का प्रमाण (पिता या करीबी रक्त संबंधी का जाति प्रमाण पत्र), पहचान प्रमाण और शपथ पत्र जमा करें।",
    "Local inquiry will be conducted by the revenue inspector.": "राजस्व निरीक्षक द्वारा स्थानीय जांच की जाएगी।",
    "Download the digital certificate or collect it from the local block office.": "डिजिटल प्रमाण पत्र डाउनलोड करें या स्थानीय ब्लॉक कार्यालय से एकत्र करें।",
    "Register on the Unique Disability ID (UDID) portal (swavlambancard.gov.in).": "विशिष्ट विकलांगता आईडी (UDID) पोर्टल (swavlambancard.gov.in) पर पंजीकरण करें।",
    "Fill in personal, medical, and employment details, and upload identity/address proofs.": "व्यक्तिगत, चिकित्सा और रोजगार विवरण भरें, और पहचान/पते के प्रमाण अपलोड करें।",
    "Select the nearest government hospital for medical assessment.": "चिकित्सा मूल्यांकन के लिए निकटतम सरकारी अस्पताल का चयन करें।",
    "Visit the hospital on the scheduled date for assessment by the medical board. The digital card will be dispatched after approval.": "चिकित्सा बोर्ड द्वारा मूल्यांकन के लिए निर्धारित तिथि पर अस्पताल जाएं। अनुमोदन के बाद डिजिटल कार्ड भेज दिया जाएगा।",
    "Visit the administrative block or registrar's office of your school/college.": "अपने स्कूल/कॉलेज के प्रशासनिक ब्लॉक या रजिस्ट्रार कार्यालय पर जाएं।",
    "Present your Admission Fee Receipt and passport-sized photographs.": "अपनी प्रवेश शुल्क रसीद और पासपोर्ट आकार की तस्वीरें प्रस्तुत करें।",
    "Collect your student identity card once printed and signed by the principal/dean.": "प्रधानाचार्य/डीन द्वारा मुद्रित और हस्ताक्षरित होने के बाद अपना छात्र पहचान पत्र एकत्र करें।",

    # Timelines
    "10-15 Days": "10-15 दिन",
    "15-30 Days": "15-30 दिन",
    "1-2 Days": "1-2 दिन",
    "2-5 Days": "2-5 दिन",
    "2-3 Days": "2-3 दिन",
    "7-10 Days": "7-10 दिन",
    "15-20 Days": "15-20 दिन",
    "1-3 Days": "1-3 दिन",

    # Statuses
    "Highly Eligible": "अत्यधिक पात्र",
    "Eligible": "पात्र",
    "Potentially Eligible": "संभावित रूप से पात्र",
    "Ineligible": "अपात्र",
}

def translate_str(text: str) -> str:
    if not text:
        return text
    stripped = text.strip()
    if stripped in HINDI_TRANSLATION_MAP:
        return HINDI_TRANSLATION_MAP[stripped]
    return text

def translate_results_to_hindi(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates the results structure to Hindi.
    """
    if not results:
        return results

    translated = {}

    # Translate Profile
    if "profile" in results:
        prof = results["profile"]
        translated_prof = {}
        for k, v in prof.items():
            if k == "occupation":
                translated_prof[k] = "किसान" if v == "Farmer" else "छात्र" if v == "Student" else "व्यवसायी" if v == "Business Owner" else "बेरोजगार" if v == "Unemployed" else "नौकरीपेशा" if v == "Salaried" else v
            elif k == "gender":
                translated_prof[k] = "पुरुष" if v == "Male" else "महिला" if v == "Female" else "अन्य" if v == "Other" else v
            elif k == "social_category":
                translated_prof[k] = v
            elif k == "state":
                translated_prof[k] = translate_str(v)
            elif k == "available_documents" and isinstance(v, list):
                translated_prof[k] = [translate_str(d) for d in v]
            else:
                translated_prof[k] = v
        translated["profile"] = translated_prof
    else:
        translated["profile"] = results.get("profile")

    # Translate Eligibility Results
    if "eligibility_results" in results:
        elig = results["eligibility_results"]
        translated_elig = {}
        for status_key, scheme_list in elig.items():
            # Status keys are: "Highly Eligible", "Eligible", "Potentially Eligible", "Ineligible"
            translated_scheme_list = []
            for s in scheme_list:
                translated_scheme = {
                    "scheme_id": s.get("scheme_id"),
                    "scheme_name": translate_str(s.get("scheme_name")),
                    "ministry": translate_str(s.get("ministry")),
                    "state": "केंद्र" if s.get("state") == "Central" else translate_str(s.get("state")),
                    "benefits": [translate_str(b) for b in s.get("benefits", [])],
                    "required_documents": [translate_str(d) for d in s.get("required_documents", [])],
                    "application_steps": [translate_str(step) for step in s.get("application_steps", [])],
                    "official_link": s.get("official_link"),
                    "faqs": [
                        {
                            "question": translate_str(faq.get("question")),
                            "answer": translate_str(faq.get("answer"))
                        } for faq in s.get("faqs", [])
                    ],
                    "match_percentage": s.get("match_percentage"),
                    "reasons": [translate_str(r) for r in s.get("reasons", [])],
                    "status": translate_str(s.get("status")),
                    "missing_profile_fields": s.get("missing_profile_fields")
                }
                translated_scheme_list.append(translated_scheme)
            
            # Map status key
            translated_status_key = status_key # Keep the key name in English so the frontend code results['Highly Eligible'] continues to work!
            translated_elig[translated_status_key] = translated_scheme_list
        translated["eligibility_results"] = translated_elig

    # Translate Document Analysis
    if "document_analysis" in results:
        doc_an = results["document_analysis"]
        translated_doc_an = {
            "required": [translate_str(d) for d in doc_an.get("required", [])],
            "available": [translate_str(d) for d in doc_an.get("available", [])],
            "missing": [translate_str(d) for d in doc_an.get("missing", [])],
            "readiness_score": doc_an.get("readiness_score", 0)
        }
        translated["document_analysis"] = translated_doc_an

    # Translate Action Plan
    if "action_plan" in results:
        act = results["action_plan"]
        translated_steps = []
        for step in act.get("steps", []):
            title = step.get("title")
            # Step titles: "Obtain [doc_name]" or "Apply for [scheme_name]"
            if title.startswith("Obtain "):
                doc_part = title[7:]
                translated_title = f"प्राप्त करें: {translate_str(doc_part)}"
            elif title.startswith("Apply for "):
                scheme_part = title[10:]
                translated_title = f"आवेदन करें: {translate_str(scheme_part)}"
            else:
                translated_title = translate_str(title)

            desc = step.get("description")
            if "To apply for your eligible schemes, you first need to obtain your" in desc:
                doc_part = desc.split("obtain your ")[-1].replace(".", "").strip()
                translated_desc = f"अपने योग्य योजनाओं के लिए आवेदन करने के लिए, आपको पहले अपना {translate_str(doc_part)} प्राप्त करना होगा।"
            elif "Once all documents are ready, submit your application for the scheme" in desc:
                translated_desc = "एक बार सभी दस्तावेज तैयार हो जाने के बाद, योजना के लिए अपना आवेदन जमा करें।"
            else:
                translated_desc = translate_str(desc)

            translated_step = {
                "step_number": step.get("step_number"),
                "title": translated_title,
                "description": translated_desc,
                "actions": [translate_str(a) for a in step.get("actions", [])],
                "estimated_time": translate_str(step.get("estimated_time")),
                "official_link": step.get("official_link"),
                "status": step.get("status")
            }
            translated_steps.append(translated_step)

        # Summary translation
        summary = act.get("summary")
        # "Your plan contains X document preparation steps and Y scheme application steps. Total estimated readiness: Z days."
        # We can construct a translated summary dynamically
        doc_count = len(results.get("document_analysis", {}).get("missing", []))
        scheme_count = len(results.get("eligibility_results", {}).get("Highly Eligible", [])) + \
                       len(results.get("eligibility_results", {}).get("Eligible", [])) + \
                       len(results.get("eligibility_results", {}).get("Potentially Eligible", []))
        days = act.get("estimated_completion_days", 0)
        translated_summary = f"आपकी योजना में {doc_count} दस्तावेज़ तैयारी चरण और {scheme_count} योजना आवेदन चरण शामिल हैं। कुल अनुमानित तैयारी: {days} दिन।"

        translated["action_plan"] = {
            "steps": translated_steps,
            "estimated_completion_days": days,
            "summary": translated_summary
        }

    return translated
