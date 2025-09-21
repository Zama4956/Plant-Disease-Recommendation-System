import streamlit as st
from PIL import Image
import io
import time

# Set up the page configuration for a clean layout
st.set_page_config(
    page_title="Plant Disease Recommendation",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state for history and language if they don't exist
if 'history' not in st.session_state:
    st.session_state.history = []
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'last_prediction_time' not in st.session_state:
    st.session_state.last_prediction_time = 0

def predict_disease(image_file):
    """
    This is a placeholder function that simulates a machine learning model.
    In a real application, you would load and use your actual model here.
    """
    diseases = [
        "Rust Fungus", "Bacterial Blight", "Apple Scab",
        "Grape Black Rot", "Potato Late Blight", "Healthy"
    ]
    # Cycle through the diseases to demonstrate a changing output
    current_index = (len(st.session_state.history)) % len(diseases)
    return diseases[current_index]

# Data dictionary with translations for diseases and treatments
disease_data = {
    "Rust Fungus": {
        "en": {
            "name": "Rust Fungus",
            "description": "Rust fungus is a common fungal disease that affects plants. It appears as yellow or orange spots on the leaves and can spread quickly.",
            "medicine": "Apply a copper-based fungicide to the affected areas. Ensure good air circulation around the plants and avoid overhead watering."
        },
        "hi": {
            "name": "रतुआ कवक",
            "description": "रतुआ कवक एक सामान्य फंगल रोग है जो पौधों को प्रभावित करता है। यह पत्तियों पर पीले या नारंगी धब्बों के रूप में दिखाई देता है और तेजी से फैल सकता है।",
            "medicine": "प्रभावित क्षेत्रों पर कॉपर-आधारित फफूंदनाशक लगाएं। पौधों के चारों ओर हवा का अच्छा संचार सुनिश्चित करें और ऊपर से पानी देने से बचें।"
        },
        "ta": {
            "name": "துரு பூஞ்சை",
            "description": "துரு பூஞ்சை என்பது தாவரங்களை பாதிக்கும் ஒரு பொதுவான பூஞ்சை நோய். இது இலைகளில் மஞ்சள் அல்லது ஆரஞ்சு புள்ளிகளாக தோன்றி விரைவாக பரவுகிறது.",
            "medicine": "பாதிக்கப்பட்ட பகுதிகளில் தாமிரம் சார்ந்த பூஞ்சைக்கொல்லியை பயன்படுத்தவும். தாவரங்களைச் சுற்றி நல்ல காற்று சுழற்சியை உறுதி செய்து, மேலே இருந்து தண்ணீர் பாய்ச்சுவதை தவிர்க்கவும்."
        },
        "te": {
            "name": "రస్ట్ ఫంగస్",
            "description": "రస్ట్ ఫంగస్ అనేది మొక్కలను ప్రభావితం చేసే ఒక సాధారణ ఫంగల్ వ్యాధి. ఇది ఆకులపై పసుపు లేదా నారింజ మచ్చలుగా కనిపిస్తుంది మరియు వేగంగా వ్యాపిస్తుంది.",
            "medicine": "ప్రభావిత ప్రాంతాలపై కాపర్ ఆధారిత శిలీంద్రనాశినిని ఉపయోగించండి. మొక్కల చుట్టూ మంచి గాలి ప్రసరణ ఉండేలా చూసుకోండి మరియు పైనుండి నీరు పోయడం మానుకోండి."
        },
        "bn": {
            "name": "রাস্ট ফাঙ্গাস",
            "description": "রাস্ট ফাঙ্গাস একটি সাধারণ ছত্রাক রোগ যা গাছপালাতে হয়। এটি পাতায় হলুদ বা কমলা দাগ হিসাবে দেখা যায় এবং দ্রুত ছড়িয়ে পড়তে পারে।",
            "medicine": "আক্রান্ত স্থানে তামা-ভিত্তিক ছত্রাকনাশক প্রয়োগ করুন। গাছের চারপাশে ভালো বায়ু চলাচল নিশ্চিত করুন এবং উপর থেকে জল দেওয়া থেকে বিরত থাকুন।"
        },
        "mr": {
            "name": "गंजा बुरशी",
            "description": "गंजा बुरशी हा एक सामान्य बुरशीजन्य रोग आहे जो वनस्पतींना प्रभावित करतो. तो पानांवर पिवळ्या किंवा नारंगी ठिपक्यांच्या रूपात दिसतो आणि वेगाने पसरू शकतो.",
            "medicine": "प्रभावित भागांवर तांब्याच्या आधारावर बनवलेले बुरशीनाशक वापरा. वनस्पतींच्या सभोवताली चांगले वायुवीजन असल्याची खात्री करा आणि वरून पाणी देणे टाळा."
        }
    },
    "Bacterial Blight": {
        "en": {
            "name": "Bacterial Blight",
            "description": "Bacterial blight is a disease that causes brown spots with a yellow halo on the leaves. It can lead to wilting and plant death if left untreated.",
            "medicine": "Remove and destroy affected leaves. Use a copper fungicide spray to prevent further spread. Ensure good drainage and avoid overcrowding plants."
        },
        "hi": {
            "name": "जीवाणु झुलसा",
            "description": "जीवाणु झुलसा एक ऐसा रोग है जो पत्तियों पर पीले घेरे के साथ भूरे धब्बे पैदा करता है। अगर इसका इलाज न किया जाए तो इससे पत्तियां मुरझा सकती हैं और पौधा मर सकता है।",
            "medicine": "प्रभावित पत्तियों को हटा दें और नष्ट कर दें। आगे फैलने से रोकने के लिए कॉपर फफूंदनाशक स्प्रे का उपयोग करें। अच्छी जल निकासी सुनिश्चित करें और पौधों को बहुत पास-पास लगाने से बचें।"
        },
        "ta": {
            "name": "பாக்டீரியா பிளைட்",
            "description": "பாக்டீரியா பிளைட் என்பது இலைகளில் மஞ்சள் வளையத்துடன் பழுப்பு புள்ளிகளை ஏற்படுத்தும் ஒரு நோய். சிகிச்சையளிக்கப்படாவிட்டால் இது வாடி, தாவரத்தின் இறப்புக்கு வழிவகுக்கும்.",
            "medicine": "பாதிக்கப்பட்ட இலைகளை நீக்கி அழிக்கவும். மேலும் பரவாமல் தடுக்க தாமிர பூஞ்சைக்கொல்லி ஸ்ப்ரேயை பயன்படுத்தவும். நல்ல வடிகால் இருப்பதை உறுதி செய்து, தாவரங்களை நெருக்கமாக நடுவதைத் தவிர்க்கவும்."
        },
        "te": {
            "name": "బాక్టీరియల్ బ్లైట్",
            "description": "బాక్టీరియల్ బ్లైట్ అనేది ఆకులపై పసుపు రంగు వలయంతో గోధుమ రంగు మచ్చలను కలిగించే వ్యాధి. చికిత్స చేయకపోతే ఇది మొక్క వాడిపోవడం మరియు చనిపోవడానికి దారితీస్తుంది.",
            "medicine": "ప్రభావిత ఆకులను తీసివేసి నాశనం చేయండి. మరింత వ్యాప్తిని నివారించడానికి కాపర్ శిలీంద్రనాశిని స్ప్రేని ఉపయోగించండి. మంచి నీటి ప్రవాహం ఉండేలా చూసుకోండి మరియు మొక్కలను దగ్గరగా నాటడం మానుకోండి."
        },
        "bn": {
            "name": "ব্যাকটেরিয়াল ব্লাইট",
            "description": "ব্যাকটেরিয়াল ব্লাইট একটি রোগ যা পাতায় হলুদ রিং সহ বাদামী দাগ সৃষ্টি করে। চিকিৎসা না করা হলে এটি পাতা শুকিয়ে গাছ মারা যেতে পারে।",
            "medicine": "আক্রান্ত পাতাগুলি সরিয়ে ফেলুন এবং ধ্বংস করুন। আরও ছড়িয়ে পড়া রোধ করতে একটি কপার ছত্রাকনাশক স্প্রে ব্যবহার করুন। ভালো নিষ্কাশন নিশ্চিত করুন এবং গাছপালা খুব ঘন না করে লাগান।"
        },
        "mr": {
            "name": "बॅक्टेरियल ब्लाइट",
            "description": "बॅक्टेरियल ब्लाइट हा एक रोग आहे ज्यामुळे पानांवर पिवळ्या रंगाच्या वलयासह तपकिरी ठिपके येतात. उपचार न केल्यास पाने सुकू शकतात आणि वनस्पती मरू शकते.",
            "medicine": "प्रभावित पाने काढून टाका आणि नष्ट करा. पुढील प्रसार टाळण्यासाठी तांब्याच्या बुरशीनाशकाचा वापर करा. चांगला पाण्याचा निचरा असल्याची खात्री करा आणि झाडे खूप जवळ लावणे टाळा।"
        }
    },
    "Apple Scab": {
        "en": {
            "name": "Apple Scab",
            "description": "Apple scab is a common disease affecting apples and crabapples. It causes olive-green to black spots on leaves and fruit, leading to defoliation.",
            "medicine": "Use a fungicide spray, such as one containing sulfur. Prune trees to improve air circulation and remove fallen leaves to reduce fungal spores."
        },
        "hi": {
            "name": "सेब का स्कैब",
            "description": "सेब का स्कैब सेब और क्रैबएप्पल को प्रभावित करने वाला एक सामान्य रोग है। यह पत्तियों और फलों पर जैतून-हरे से काले धब्बे पैदा करता है, जिससे पत्तियां गिर जाती हैं।",
            "medicine": "सल्फर युक्त फफूंदनाशक स्प्रे का उपयोग करें। हवा के संचार को बेहतर बनाने के लिए पेड़ों की छंटाई करें और फंगल बीजाणुओं को कम करने के लिए गिरी हुई पत्तियों को हटा दें।"
        },
        "ta": {
            "name": "ஆப்பிள் ஸ்கேப்",
            "description": "ஆப்பிள் ஸ்கேப் என்பது ஆப்பிள்கள் மற்றும் கிராபாப்பிள்களை பாதிக்கும் ஒரு பொதுவான நோய். இது இலைகள் மற்றும் பழங்களில் ஆலிவ்-பச்சை முதல் கருப்பு புள்ளிகளை ஏற்படுத்துகிறது, இதனால் இலைகள் உதிர்ந்துவிடும்.",
            "medicine": "கந்தகம் கொண்ட பூஞ்சைக்கொல்லி ஸ்ப்ரேயை பயன்படுத்தவும். நல்ல காற்று சுழற்சிக்காக மரங்களை கத்தரித்து, பூஞ்சை வித்துக்களை குறைக்க கீழே விழுந்த இலைகளை அகற்றவும்."
        },
        "te": {
            "name": "ఆపిల్ స్కాబ్",
            "description": "ఆపిల్ స్కాబ్ అనేది ఆపిల్ మరియు క్రాబాపిల్‌లను ప్రభావితం చేసే ఒక సాధారణ వ్యాధి. ఇది ఆకులు మరియు పండ్లపై ఆలివ్-ఆకుపచ్చ నుండి నలుపు రంగు మచ్చలను కలిగిస్తుంది, దీనివల్ల ఆకులు రాలిపోతాయి.",
            "medicine": "సల్ఫర్ ఉన్న శిలీంద్రనాశిని స్ప్రేని ఉపయోగించండి. గాలి ప్రసరణను మెరుగుపరచడానికి చెట్లను కత్తిరించండి మరియు శిలీంద్రాల స్పోర్స్‌ను తగ్గించడానికి రాలిపోయిన ఆకులను తొలగించండి."
        },
        "bn": {
            "name": "অ্যাপল স্ক্যাব",
            "description": "অ্যাপল স্ক্যাব হল আপেল এবং ক্র্যাবঅ্যাপেলকে প্রভাবিত করে এমন একটি সাধারণ রোগ। এটি পাতা ও ফলের উপর জলপাই-সবুজ থেকে কালো দাগ সৃষ্টি করে, যা পাতা ঝরিয়ে দেয়।",
            "medicine": "সালফারযুক্ত ছত্রাকনাশক স্প্রে ব্যবহার করুন। বায়ু চলাচল উন্নত করতে গাছের ডালপালা ছাঁটা উচিত এবং ছত্রাক স্পোর কমাতে ঝরা পাতাগুলি সরিয়ে ফেলুন।"
        },
        "mr": {
            "name": "ॲपल स्कॅब",
            "description": "ॲपल स्कॅब हा सफरचंद आणि क्रॅबॲपलला प्रभावित करणारा एक सामान्य रोग आहे. यामुळे पाने आणि फळांवर ऑलिव्ह-हिरव्या ते काळ्या रंगाचे ठिपके येतात, ज्यामुळे पाने गळून पडतात.",
            "medicine": "सल्फर असलेले बुरशीनाशक स्प्रे वापरा. चांगल्या वायुवीजनासाठी झाडांची छाटणी करा आणि बुरशीचे बीजाणू कमी करण्यासाठी गळून पडलेली पाने काढून टाका."
        }
    },
    "Grape Black Rot": {
        "en": {
            "name": "Grape Black Rot",
            "description": "Grape black rot is a fungal disease that severely affects grapes. It appears as reddish-brown spots on leaves and causes the grapes to shrivel and turn black.",
            "medicine": "Apply fungicides containing captan or mancozeb. Prune out infected canes and clean up plant debris to reduce the spread of the disease."
        },
        "hi": {
            "name": "अंगूर का ब्लैक रोट",
            "description": "अंगूर का ब्लैक रोट एक फंगल रोग है जो अंगूर को बुरी तरह प्रभावित करता है। यह पत्तियों पर लाल-भूरे धब्बे के रूप में दिखाई देता है और अंगूर को सिकुड़कर काला कर देता है।",
            "medicine": "कैप्टन या मैनकोजेब युक्त फफूंदनाशकों का उपयोग करें। रोग के प्रसार को कम करने के लिए संक्रमित टहनियों की छंटाई करें और पौधों के मलबे को साफ करें।"
        },
        "ta": {
            "name": "திராட்சை கருப்பு அழுகல்",
            "description": "திராட்சை கருப்பு அழுகல் என்பது திராட்சைகளை கடுமையாக பாதிக்கும் ஒரு பூஞ்சை நோய். இது இலைகளில் சிவந்த-பழுப்பு புள்ளிகளாக தோன்றி, திராட்சையை சுருங்கி கருப்பாக மாற்றுகிறது.",
            "medicine": "கேப்டன் அல்லது மேன்கோசெப் கொண்ட பூஞ்சைக்கொல்லிகளை பயன்படுத்தவும். நோயின் பரவலை குறைக்க பாதிக்கப்பட்ட தண்டுகளை கத்தரித்து, தாவரக் கழிவுகளை சுத்தம் செய்யவும்."
        },
        "te": {
            "name": "ద్రాక్ష బ్లాక్ రాట్",
            "description": "ద్రాక్ష బ్లాక్ రాట్ అనేది ద్రాక్షను తీవ్రంగా ప్రభావితం చేసే ఒక శిలీంద్ర వ్యాధి. ఇది ఆకులపై ఎర్రటి-గోధుమ రంగు మచ్చలుగా కనిపిస్తుంది మరియు ద్రాక్షను ముడుచుకొని నల్లగా మారేలా చేస్తుంది.",
            "medicine": "కాప్టాన్ లేదా మాంకోజెబ్ ఉన్న శిలీంద్రనాశినులను ఉపయోగించండి. వ్యాధి వ్యాప్తిని తగ్గించడానికి ప్రభావితమైన రెమ్మలను కత్తిరించండి మరియు మొక్కల శిథిలాలను శుభ్రం చేయండి."
        },
        "bn": {
            "name": "আঙ্গুর ব্ল্যাক রট",
            "description": "আঙ্গুর ব্ল্যাক রট একটি ছত্রাকজনিত রোগ যা আঙ্গুরকে মারাত্মকভাবে প্রভাবিত করে। এটি পাতায় লালচে-বাদামী দাগ হিসাবে দেখা যায় এবং আঙ্গুরকে শুকিয়ে কালো করে দেয়।",
            "medicine": "ক্যাপ্টান বা ম্যানকোজেব ধারণকারী ছত্রাকনাশক ব্যবহার করুন। রোগের বিস্তার কমাতে আক্রান্ত শাখাগুলি ছাঁটুন এবং গাছের আবর্জনা পরিষ্কার করুন।"
        },
        "mr": {
            "name": "द्राक्ष काळा कुजवा",
            "description": "द्राक्ष काळा कुजवा हा एक बुरशीजन्य रोग आहे जो द्राक्षांना गंभीरपणे प्रभावित करतो. तो पानांवर लालसर-तपकिरी ठिपके म्हणून दिसतो आणि द्राक्षे सुकवून काळी पडतात.",
            "medicine": "कॅप्टन किंवा मॅन्कोझेब असलेले बुरशीनाशक स्प्रे वापरा. रोगाचा प्रसार कमी करण्यासाठी संक्रमित फांद्या छाटा आणि वनस्पतींचा कचरा साफ करा."
        }
    },
    "Potato Late Blight": {
        "en": {
            "name": "Potato Late Blight",
            "description": "Potato late blight is a devastating disease that causes dark, water-soaked spots on leaves and stems. It can rapidly destroy entire potato crops.",
            "medicine": "Apply a fungicidal spray containing chlorothalonil or mancozeb. Ensure proper spacing between plants and avoid watering leaves directly."
        },
        "hi": {
            "name": "आलू का लेट ब्लाइट",
            "description": "आलू का लेट ब्लाइट एक विनाशकारी रोग है जो पत्तियों और तनों पर गहरे, पानी से भीगे हुए धब्बे पैदा करता है। यह पूरे आलू की फसल को तेजी से नष्ट कर सकता है।",
            "medicine": "क्लोरोथैलोनिल या मैनकोजेब युक्त फफूंदनाशक स्प्रे का उपयोग करें। पौधों के बीच उचित दूरी सुनिश्चित करें और पत्तियों पर सीधे पानी देने से बचें।"
        },
        "ta": {
            "name": "உருளைக்கிழங்கு தாமத பிளைட்",
            "description": "உருளைக்கிழங்கு தாமத பிளைட் ஒரு அழிவுகரமான நோய். இது இலைகள் மற்றும் தண்டுகளில் இருண்ட, நீர் தேங்கிய புள்ளிகளை ஏற்படுத்துகிறது. இது உருளைக்கிழங்கு பயிர்களை விரைவாக அழிக்கக்கூடும்.",
            "medicine": "குளோரோதலோனில் அல்லது மேன்கோசெப் கொண்ட பூஞ்சைக்கொல்லி ஸ்ப்ரேயை பயன்படுத்தவும். தாவரங்களுக்கு இடையில் சரியான இடைவெளியை உறுதி செய்து, இலைகளில் நேரடியாக தண்ணீர் பாய்ச்சுவதை தவிர்க்கவும்."
        },
        "te": {
            "name": "బంగాళాదుంప లేట్ బ్లైట్",
            "description": "బంగాళాదుంప లేట్ బ్లైట్ అనేది ఒక వినాశకరమైన వ్యాధి. ఇది ఆకులు మరియు కాండాలపై నల్లని, నీటితో తడిసిన మచ్చలను కలిగిస్తుంది. ఇది బంగాళాదుంప పంటలను వేగంగా నాశనం చేయగలదు.",
            "medicine": "క్లోరోథలోనిల్ లేదా మాంకోజెబ్ ఉన్న శిలీంద్రనాశిని స్ప్రేని ఉపయోగించండి. మొక్కల మధ్య సరైన దూరం ఉండేలా చూసుకోండి మరియు ఆకులపై నేరుగా నీరు పోయడం మానుకోండి."
        },
        "bn": {
            "name": "আলু লেট ব্লাইট",
            "description": "আলু লেট ব্লাইট একটি বিধ্বংসী রোগ যা পাতা এবং ডালপালায় কালো, জল-ডোবা দাগ সৃষ্টি করে। এটি দ্রুত আলুর পুরো ফসল ধ্বংস করতে পারে।",
            "medicine": "ক্লোरोথ্যালোনিল বা ম্যানকোজেব ধারণকারী ছত্রাকনাশক স্প্রে ব্যবহার করুন। গাছের মধ্যে সঠিক দূরত্ব নিশ্চিত করুন आणि সরাসরি পাতায় जल দেওয়া এড়িয়ে চলুন।"
        },
        "mr": {
            "name": "बटाटा उशिरा बुरशी",
            "description": "बटाटा उशिरा बुरशी हा एक विनाशकारी रोग आहे. ज्यामुळे पाने आणि फांद्यांवर काळे, पाण्याने भरलेले ठिपके येतात. तो संपूर्ण बटाट्याचे पीक वेगाने नष्ट करू शकतो.",
            "medicine": "क्लोरोथॅलोनिल किंवा मॅन्कोझेब असलेले बुरशीनाशक स्प्रे वापरा. वनस्पतींमध्ये योग्य अंतर ठेवा आणि पानांवर थेट पाणी देणे टाळा."
        }
    },
    "Healthy": {
        "en": {
            "name": "Healthy",
            "description": "This plant shows no signs of disease. Keep up the good care!",
            "medicine": "No treatment needed. Continue to provide adequate water, sunlight, and nutrients."
        },
        "hi": {
            "name": "स्वस्थ",
            "description": "इस पौधे में रोग का कोई लक्षण नहीं है। अच्छी देखभाल जारी रखें!",
            "medicine": "किसी भी उपचार की आवश्यकता नहीं है। पर्याप्त पानी, धूप और पोषक तत्व देना जारी रखें।"
        },
        "ta": {
            "name": "ஆரோக்கியமானது",
            "description": "இந்த தாவரத்தில் நோய்க்கான எந்த அறிகுறியும் இல்லை. நல்ல கவனிப்பைத் தொடரவும்!",
            "medicine": "சிகிச்சை தேவையில்லை. போதுமான தண்ணீர், சூரிய ஒளி மற்றும் ஊட்டச்சத்துக்களை தொடர்ந்து வழங்குங்கள்।"
        },
        "te": {
            "name": "ఆరోగ్యమైనది",
            "description": "ఈ మొక్కలో వ్యాధి సంకేతాలు కనిపించలేదు. మంచి సంరక్షణను కొనసాగించండి!",
            "medicine": "చికిత్స అవసరం లేదు. తగినంత నీరు, సూర్యరశ్మి మరియు పోషకాలను అందించడం కొనసాగించండి।"
        },
        "bn": {
            "name": "স্বাস্থ্যবান",
            "description": "এই গাছে রোগের কোন লক্ষণ নেই। ভালো যত্ন চালিয়ে যান!",
            "medicine": "কোনো চিকিৎসার প্রয়োজন নেই। পর্যাপ্ত জল, সূর্যালোক এবং পুষ্টি সরবরাহ চালিয়ে যান।"
        },
        "mr": {
            "name": "निरोगी",
            "description": "या वनस्पतीत रोगाचे कोणतेही लक्षण नाही. चांगली काळजी घेत राहा!",
            "medicine": "उपचारांची गरज नाही. पुरेसे पाणी, सूर्यप्रकाश आणि पोषक तत्वे देणे सुरू ठेवा."
        }
    }
}

# --- Streamlit UI Components ---

st.title("🌱 Plant Disease Recommendation")

st.markdown("""
Upload an image of a plant leaf and get a diagnosis and treatment recommendation.
""")

# Language selection
language_options = {
    'en': 'English', 'hi': 'हिन्दी', 'ta': 'தமிழ்',
    'te': 'తెలుగు', 'bn': 'বাংলা', 'mr': 'मराठी'
}
st.session_state.language = st.selectbox(
    "Select Language",
    options=list(language_options.keys()),
    format_func=lambda x: language_options[x]
)

# File uploader section
uploaded_file = st.file_uploader(
    "Choose an image of a plant leaf...",
    type=["jpg", "jpeg", "png"]
)

# Layout for image and results
col1, col2 = st.columns(2)

with col1:
    if uploaded_file is not None:
        try:
            # Use a context manager to handle file stream
            with uploaded_file as f:
                image = Image.open(f)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        except Exception:
            st.error("Error processing the image file. Please upload a valid image.")
    else:
        st.image("https://placehold.co/400x300/e2e8f0/4a5568?text=Click+to+upload+a+leaf+image", use_container_width=True)

with col2:
    if uploaded_file is not None:
        # Simulate prediction with a loading spinner
        with st.spinner('Analyzing image...'):
            time.sleep(2)  # Simulate delay for prediction
            disease_name = predict_disease(uploaded_file)
        
        # Get the recommendation in the selected language
        rec = disease_data.get(disease_name, disease_data["Healthy"]).get(st.session_state.language, disease_data["Healthy"]["en"])
        
        st.subheader("Recommendation")
        st.markdown(f"**Disease Name:** {rec['name']}")
        st.markdown(f"**Description:** {rec['description']}")
        st.markdown(f"**Recommended Medicine:** {rec['medicine']}")

        # Add to history
        st.session_state.history.append({
            "disease_name": rec['name'],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "image_name": uploaded_file.name,
            "image_size": f"{uploaded_file.size / 1024:.2f} KB"
        })

# --- History Section ---
st.markdown("---")
st.subheader("Scan History")
if st.session_state.history:
    history_df = st.session_state.history
    # Displaying history in a table
    st.table(history_df)
else:
    st.info("No scan history yet.")
