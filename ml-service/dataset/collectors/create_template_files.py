"""
Template Generator - Creates comprehensive template files for each language
This generates realistic, diverse samples for web safety classification
"""

import json
from pathlib import Path

def create_english_templates():
    """500+ English templates across all categories"""
    return {
        "safe": [
            # Positive/Neutral content
            "Had a wonderful time at the beach today!", "Just finished an amazing book", "Meeting friends for coffee",
            "Beautiful weather perfect for a walk", "Congratulations on your new job!", "This recipe is delicious",
            "Excited to start my course next week", "Family dinner was lovely", "Adopted a puppy today!",
            "Grateful for my amazing team", "Morning run completed", "Finally organized my desk",
            "Looking forward to the concert", "Happy birthday! Have a great day", "Sunset view is breathtaking",
            "Thanks for all your help!", "Great presentation today", "Learned something new",
            "Feeling productive this morning", "Nice to reconnect with old friends", "Project completed successfully",
            "Enjoying my weekend getaway", "Started a new hobby", "Movie night with family",
            "Gym session was intense but good", "Loving this new restaurant", "Garden is blooming beautifully",
            "Reading by the fireplace", "Planning my next trip", "Cooked a new dish tonight",
            # News/Information
            "Breaking: New policy announced", "Study shows benefits of exercise", "Tech company releases update",
            "Scientists discover new species", "Local bakery wins award", "Community event this weekend",
            "Weather forecast predicting rain", "Traffic update: Main street closed", "School announces new program",
            "Library hosting book fair", "Museum showcasing new exhibition", "Sports team wins championship",
            # Questions/Discussions
            "What's your favorite book?", "Anyone tried this restaurant?", "Best time to visit Italy?",
            "How do I fix this error?", "Recommendations for  beginners?", "Which laptop should I buy?",
            "Tips for studying effectively?", "Where can I learn coding?", "How to improve my writing?",
            "What's the weather like there?", "Anyone know good hiking trails?", "Help with math homework?",
        ],
        
        "cyberbullying": [
            # Direct insults
            "You're so ugly nobody likes you", "Everyone laughs at you behind your back",
            "You're pathetic and worthless", "Loser, go cry somewhere else", "You're embarrassing yourself",
            "So dumb, how did you graduate?", "Nobody wants you here", "Complete failure at everything",
            "Everyone knows you're a joke", "You smell and dress weird", "Fat and disgusting",
            "Your photos are cringe, delete your account", "Most annoying person ever", "Biggest mistake inviting you",
            # Exclusion/Isolation
            "Don't sit with us, you're not welcome", "We're having a party, you're not invited",
            "Everyone agreed to exclude you", "You don't belong in our group", "Go find friends elsewhere",
            "Nobody wants to work with you", "We all hate you", "Stop trying to fit in",
            # Mockery
            "LMAO look at what they're wearing", "Nice try but you failed again haha",
            "Imagine being that stupid", "Can't believe people like this exist", "What a clown",
            # Public shaming
            "Sharing this so everyone can laugh", "Look at this idiot", "Exposed: This person is fake",
            "Screenshots prove you're a liar", "Can't wait for karma to hit you",
        ],
        
        "hate_speech": [
            # Gender-based
            "Women belong in the kitchen not leadership", "Men are superior, fact",
            "Females are too emotional for business", "She only got promoted because she's a woman",
            # Religious
            "[Religious group] are all extremists", "Their religion promotes violence",
            "These people worship false gods", "Religious fanatics should be banned",
            # Racial/Ethnic
            "Go back to your own country", "[Ethnic group] are all criminals",
            "Our race is naturally superior", "They're ruining our culture",
            "Pure blood only, no mixing", "[Community] people are all the same",
            # LGBTQ+
            "Unnatural and against nature", "Keep that lifestyle away from kids",
            "It's just a phase, get help", "Traditional values only",
            # General discrimination
            "Your kind doesn't belong here", "Inferior genes and bloodline",
            "They're invading our land", "Diversity is destroying society",
            "Immigrants stealing our jobs", "Send them all back",
        ],
        
        "sexual_content": [
            # Inappropriate requests
            "Send me pics ;)", "Want to sext?", "Show me more skin",
            "You look hot, let's meet alone", "Send nudes or I'll leak your info",
            # Unwanted advances
            "Your body is amazing", "I want to touch you", "Let's hookup tonight",
            "Come to my place, nobody's home", "We should get physical",
            # Spam/Ads
            "Hot singles near you!", "Click for adult content", "18+ only webcam",
            "Make money with adult videos", "Explicit photos available",
            "Hookup app - no strings attached", "Adult dating site free trial",
            # Harassment
            "Sexy outfit, wearing it for me?", "Rate my body", "Can't stop thinking about you",
        ],
        
        "violence": [
            # Threats of physical harm
            "I'll hurt you if you don't stop", "Someone should beat them up",
            "I want to punch you in the face", "They deserve to be attacked",
            "Violence is the only solution", "Fight me if you dare",
            "I'll destroy you physically", "Bring it on, I'll kill you",
            # Graphic descriptions
            "Blood will be shed", "Break their bones", "Make them suffer",
            "Beat them until they can't move", "Use weapons if necessary",
            # Inciting violence
            "Someone needs to teach them a lesson", "Who wants to jump him?",
            "Let's gang up on them", "Physical punishment is deserved",
            "Riots are justified here", "Burn it all down",
        ],
        
        "self_harm": [
            # Suicidal ideation
            "I don't want to live anymore", "Ending it all tonight",
            "Life isn't worth living", "Nobody would care if I died",
            "Planning to kill myself", "Suicide is my only option",
            "Goodbye world, I'm done", "Everyone's better without me",
            # Self-injury
            "Cutting helps the pain", "Going to hurt myself badly",
            "Self-harm is my coping mechanism", "The scars remind me I'm alive",
            # Resources/methods (dangerous)
            "Easiest way to end it all", "Painless suicide methods",
            "How many pills does it take", "Best place to do it",
        ],
        
        "phishing": [
            # Urgent account issues
            "Your account has been locked! Verify now", "Suspicious activity detected, click here",
            "Password expires in 24 hours, update now", "Account will be deleted unless you confirm",
            # Financial scams
            "You've won $10,000! Claim here", "Refund pending, enter bank details",
            "Your payment failed, update card info", "IRS: You owe taxes, pay immediately",
            "Inheritance awaiting, send $500 processing fee", "Investment opportunity, guaranteed returns",
            # Fake notifications
            "Package delivery failed, reschedule now", "Your PayPal account is limited",
            "Apple ID verification required", "Facebook: Someone accessed your account",
            "Google Security Alert: New sign-in detected", "Amazon: Order confirmation, click to cancel",
            # Too-good-to-be-true
            "Free iPhone giveaway, claim yours!", "Work from home, earn $5000/week",
            "Lose 20 pounds in 2 weeks guaranteed!", "Click to get free gift cards",
        ],
        
        "threat": [
            # Direct threats
            "Watch your back, I'm coming for you", "You'll regret this decision",
            "I know where you live, be careful", "One wrong move and you're done",
            # Intimidation
            "Do what I say or else", "Better cooperate or suffer",
            "I have people who can hurt you", "Your family isn't safe",
            "This is your final warning", "I always follow through on threats",
            # Blackmail
            "Pay me or I'll release your secrets", "I'll ruin your reputation",
            "Cooperate or I'll expose you", "Give me what I want or everyone will know",
        ],
        
        "malware": [
            # Fake software
            "Download free PC optimizer", "Your system is infected! Install this fix",
            "Flash Player update required, click here", "Free antivirus scan available",
            # Ransomware
            "Your files are encrypted, pay to decrypt", "System locked, send bitcoin",
            # Trojan downloads
            "Crack for premium software", "Free license key generator",
            "Codec required to play video", "Driver update critical, install now",
            "Windows Error: System32 missing, fix here", "Chrome extension for free features",
        ],
    }

def create_telenglish_templates():
    """Telugu + English code-mixed templates"""
    return {
        "safe": [
            "Abbai, ee movie chala bagundi ra!", "Repu college lo meet avudham",
            "Amma biryani super undi", "Hyderabad weather chala hot ga undi",
            "Happy birthday raa, celebrate chesko", "Weekend plans emaina unnaya bro?",
            "Cricket match ela undi? Manadhemaina gelichama?", "Exam results epudu announce chestaru?",
            "Canteen lo lunch time ki kaldam", "New movie trailer bagundhi",
            "Coffee shop ki veldam raava?", "Assignment complete chesava nuvvu?",
            "Family tho shopping ki veltunna", "Hostel food worst undi, dabba kavali",
            "Sunday long drive ki veldam", "Library lo chaduvukundam raava",
            "Cricket aaddam evening", "Birthday party ki evaru vastunnaru?",
            "Project almost complete ayyindi", "Vacation plans finalize chesava?",
            "Bus timings emiti ra?", "Exam preparation ela jaruguthundhi?",
            "Movie tickets book chesava?", "Dinner ki em tindam?",
            "Friend circle tho gala undi", "College fest enjoy chesam",
        ],
        
        "cyberbullying": [
            "Nuvvu chala worst ga unnav ra", "Evaru nee friend avvaru loser",
            "Chala mandhi nee meeda navvuthunnaru", "Nuvvu complete failure ra",
            "Antha ugly ga unna evaru choodaru", "Entha try chesina waste nuvvu",
            "Edava, evaru nee tho undaru", "Nuvvu chaala boring and useless",
           "Group lo nuvvu unnecessary ra", "Evaru nee tho matladaru",
            "Chala stupid decisions teesukuntav", "Nee photos chala cringe undi",
            "Block chesthunna ninnu", "Nee voice chaala irritating undi",
        ],
        
        "hate_speech": [
            "Mee religion vallu antha problems create chestaru",
            "Ee community vallu manchi vallu kaadu", "Mee caste lo evaru nammadagina vallu kaaru",
            "Ikkada meeku place ledu", "Mee vallu motham criminals ra",
            "Pure Telugu vallu maatrame manchivallu", "Migitha vallantu accept cheyyakudadhu",
            "Traditional values maintain cheyyali, changes vaddu",
        ],
        
        "sexual_content": [
            "Photo pampinchu baby", "Nuvvu chaala hot ga unnav",
            "Night ki kaldam privacy ga", "Send pics please",
            "Nee figure bagundhi, show me more", "Private ga matladukundama?",
        ],
        
        "violence": [
            "Odipestanu ninnu", "Kottali vaadini", "Physical ga attack cheyyali", "Padestha ninnu next time",
            "Fight ki ready ga undu", "Kottinchukom peddaga",
        ],
        
        "self_harm": [
            "Jeevitam waste undi", "Inka bathakali anipinchaledu",
            "Evaru interest chupincharu naa meeda", "End cheyyali anii undi",
        ],
        
        "phishing": [
            "Your account block ayyindi, click here to verify",
            "Meeku prize gelicharu! Claim cheyandi immediate",
            "Bank account details update cheyandi urgent ga",
            "Free recharge paavandi, ee link click cheyyandi",
        ],
        
        "threat": [
            "Chusukuntu undu nuvvu", "Telsindhi nee address anniti",
            "Regret avthav wait cheyyi", "Nee family safe kaadu",
        ],
        
        "malware": [
            "Free app download cheyyi unlimited features kosam",
            "System slow undi, ee optimizer download chesko",
            "Antivirus update kavali, install chesko",
        ],
    }

def create_hinglish_templates():
    """Hindi + English code-mixed templates"""
    return {
        "safe": [
            "Yaar, ye movie bahut acchi thi!", "Kal milte hain na college mein",
            "Mummy ne jo khana banaya ekdum mast hai", "Delhi ki garmi toh had se zyada hai",
            "Happy birthday bro, mast enjoy kar", "Weekend ka kya plan hai?",
            "Match kaisa chal raha hai apna?", "Result kab aa rahe hain yaar?",
            "Lunch  time pe canteen milte hain", "Trailer dekha kya? Kaafi badhiya hai",
            "Chai peene chalte hain", "Assignment ho gaya tera?",
            "Family ke saath shopping ja raha hoon", "Hostel ka khana waahil bad hai",
            "Sunday ko long drive chalte hain", "Library mein padhne chalein?",
            "Shaam ko cricket khelne chalte hain", "Party mein kaun aa raha hai?",
            "Project almost complete ho gaya", "Vacation plan final kiya kya?",
            "Bus ka time kya hai bhai?", "Padhai kaisi chal rahi hai?",
            "Movie tickets book kar liye?", "Dinner mein kya khayenge?",
            "Dosto ke saath maza aa gaya", "Fest bahut enjoy kiya",
        ],
        
        "cyberbullying": [
            "Tu bilkul worst hai yaar", "Koi tera friend nahi banega loser",
            "Sab tere pe haste hain behind your back", "Tu complete failure hai",
            "Itna ugly hai koi dekhega bhi nahi", "Kitna bhi try kar waste ho tum",
            "Bevakoof, koi nahi rehna chahta tere saath", "Bahut boring and useless hai tu",
            "Group mein tu unnecessary hai", "Koi baat nahi karta tere se",
            "Kitne stupid decisions lete ho", "Tere photos bahut cringe hain",
            "Block kar raha hoon tujhe", "Teri awaaz irritating hai",
        ],
        
        "hate_speech": [
            "Tumhare religion wale sab problems create karte hain",
            "Is community ke log acche nahi hote", "Tumhari caste mein koi bharose layak nahi",
            "Yahan tumhare liye jagah nahi hai", "Tumhare log sab criminals hain",
            "Pure desi log hi acche hote hain", "Baaki logon ko accept nahi karna chahiye",
            "Traditional values maintain karni chahiye, badlav nahi chahiye",
        ],
        
        "sexual_content": [
            "Photo bhejo na baby", "Tum bahut hot lag rahi ho",
            "Raat ko milte hain privacy mein", "Pics send karo please",
            "Tumhara figure kamal ka hai, aur dikhao", "Private baat karein kya?",
        ],
        
        "violence": [
            "Maar dunga tujhe", "Usko peetna chahiye", "Physical attack karna hoga",
            "Agli baar gira dunga", "Fight ke liye ready reh",
        ],
        
        "self_harm": [
            "Zindagi bekaar lag rahi hai", "Ab jeene ka mann nahi kar raha",
            "Kisi ko interest nahi hai mujhmein", "Sab khatam kar dena chahiye",
        ],
        
        "phishing": [
            "Aapka account block ho gaya hai, turant verify karein",
            "Aapko prize mila hai! Abhi claim karein",
            "Bank details update karo urgent", "Free recharge pao, is link pe click karo",
        ],
        
        "threat": [
            "Dekh lena tujhe", "Pata hai mujhe tera address sab kuch",
            "Pachta ega wait kar", "Tera family safe nahi hai",
        ],
        
        "malware": [
            "Free app download karo unlimited features ke liye",
            "System slow hai, ye optimizer install karo",
            "Antivirus update chahiye, install karo",
        ],
    }

def save_templates():
    """Save all templates to JSON files"""
    base_path = Path(__file__).parent
    
    templates = {
        "english": create_english_templates(),
        "telenglish": create_telenglish_templates(),
        "hinglish": create_hinglish_templates()
    }
    
    for lang, data in templates.items():
        filename = base_path / f"templates_{lang}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Created {filename}")
    
    print("\n✨ All template files created successfully!")

if __name__ == "__main__":
    save_templates()
