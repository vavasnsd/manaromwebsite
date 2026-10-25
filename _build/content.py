# -*- coding: utf-8 -*-
"""Real content for the Manarom site, taken from www.manarom.com (Oct 2026)
and the Sitemap (revise 22.9.69). Thai first, English second."""

PHONE_1 = "02-032-9595"
PHONE_2 = "02-725-9595"
PHONE_REG = "02-725-9592"
FAX = "02-725-9599"
EMAIL = "manarom@manarom.com"
ADDR_TH = "เลขที่ 9 ถนนสุขุมวิท 70/3 แขวงบางนาใต้ เขตบางนา กรุงเทพฯ 10260"
ADDR_EN = "9 Sukhumvit 70/3, Bang Na Tai, Bang Na, Bangkok 10260"
HOURS_TH = "ผู้ป่วยนอก 07:00–20:00 น. · ฉุกเฉิน 24 ชั่วโมง"
HOURS_EN = "Outpatient 07:00–20:00 · Emergency 24 hours"
MAPS = "https://www.google.com/maps/search/?api=1&query=Manarom+Hospital+Sukhumvit+70%2F3"

PHOTO = {
    "dining": "assets/img/photos/dining",
    "activity": "assets/img/photos/activity-room",
    "lounge": "assets/img/photos/lounge",
    "garden": "assets/img/photos/garden-lounge",
    "common": "assets/img/photos/common-room",
}

# ------------------------------------------------------------------ services
# slug, icon, main(circle)?, th, en, photo-or-illustration, short th, short en,
# intro th, intro en, sections [(h_th, h_en, [(th, en), ...])], extra key
SERVICES = [
 dict(slug="opd", icon="doctor", main=True, th="ผู้ป่วยนอก", en="Outpatient (OPD)", img="photo:common",
      s_th="ตรวจรักษากับจิตแพทย์ ให้คำปรึกษา และจิตบำบัด", s_en="Psychiatrist care, counselling and psychotherapy",
      i_th="บริการตรวจรักษาโดยจิตแพทย์ ทั้งการรักษาด้วยยาที่เหมาะสม การให้คำปรึกษา จิตบำบัดแบบรายบุคคล กลุ่ม ครอบครัว และคู่สมรส พฤติกรรมบำบัด และกิจกรรมบำบัด เน้นการรักษาและป้องกันการกลับเป็นซ้ำ พร้อมติดตามประเมินผลอย่างต่อเนื่อง",
      i_en="Psychiatrist-led outpatient care: the right medication when needed, counselling, psychotherapy for individuals, groups, families and couples, behavioural therapy and occupational therapy. We focus on treatment, preventing relapse and steady follow-up.",
      sec=[("กลุ่มโรคที่ให้การรักษา", "Conditions we treat", [("จิตเภท", "Schizophrenia"), ("ไบโพลาร์", "Bipolar disorder"), ("ซึมเศร้า", "Depression"), ("วิตกกังวล", "Anxiety"), ("แพนิค", "Panic disorder"), ("ย้ำคิดย้ำทำ (OCD)", "OCD"), ("กลัวการเข้าสังคม", "Social phobia"), ("PTSD", "PTSD"), ("สมองเสื่อม ความจำถดถอย", "Dementia and memory decline"), ("ปัญหาการนอน", "Sleep problems"), ("สมาธิสั้น", "ADHD"), ("แอลดี", "Learning disabilities"), ("ออทิสติก", "Autism"), ("หูแว่ว หวาดระแวง", "Hearing voices, paranoia")]),
           ("เรื่องที่ให้คำปรึกษา", "Concerns we help with", [("ติดเกมและคอมพิวเตอร์", "Gaming and screen addiction"), ("พฤติกรรมเด็ก", "Children's behaviour"), ("พัฒนาการล่าช้าและการพูด", "Development and speech delays"), ("ปัญหาการกิน", "Eating problems"), ("ความสัมพันธ์และครอบครัว", "Relationships and family"), ("การเลี้ยงลูก", "Parenting"), ("การปรับตัวและการจัดการอารมณ์", "Adjustment and managing emotions"), ("สารเสพติดและการพนัน", "Substance use and gambling")])],
      extra="opd"),
 dict(slug="ipd", icon="bed", main=True, th="ผู้ป่วยใน", en="Inpatient (IPD)", img="photo:garden",
      s_th="ดูแลใกล้ชิดในบรรยากาศอบอุ่นเหมือนบ้าน", s_en="Close care in a warm, home-like setting",
      i_th="สำหรับผู้ป่วยที่ต้องการการดูแลใกล้ชิด ในบรรยากาศอบอุ่นเหมือนบ้าน รักษาด้วยยาควบคู่การฟื้นฟูแบบนิเวศน์บำบัด (Milieu Therapy) โดยทีมสหวิชาชีพ ทั้งพยาบาลจิตเวช นักจิตวิทยาคลินิก และนักกิจกรรมบำบัด ฝึกระเบียบวินัย ความเข้าใจอารมณ์ การสื่อสาร การจัดการความเครียด และการเห็นคุณค่าในตนเอง",
      i_en="For patients who need close care, in a warm, home-like setting. Medication goes together with milieu therapy led by psychiatric nurses, clinical psychologists and occupational therapists, building routine, emotional understanding, communication, stress management and self-worth.",
      sec=[("ประเภทห้องพัก", "Room types", [("ห้องเตียงคู่", "Twin room"), ("ห้องเตียงเดี่ยว", "Single room"), ("ห้องพิเศษ", "Private room"), ("ห้องพิเศษมีสวนหย่อม", "Private room with garden"), ("ห้องสังเกตอาการ", "Close observation room")]),
           ("ข้อปฏิบัติในการเยี่ยม", "Visiting rules", [("เยี่ยมได้เฉพาะรายชื่อที่ได้รับอนุญาต", "Only approved visitors on the list"), ("ไม่อนุญาตเด็กอายุต่ำกว่า 7 ปี", "No children under 7"), ("งดถ่ายภาพและวิดีโอ", "No photos or video"), ("งดนำของมีค่า โทรศัพท์ และกระเป๋าเข้า", "No valuables, phones or bags"), ("ห้ามนำแอลกอฮอล์ ยา บุหรี่ และของมีคม", "No alcohol, drugs, cigarettes or sharp objects"), ("อาหารและของฝากต้องผ่านการอนุมัติจากทีมรักษา", "Food and gifts need the care team's approval")])],
      extra="ipd"),
 dict(slug="daycenter", icon="sun", main=True, th="ศูนย์กิจกรรมกลางวัน", en="Day Activity Center", img="photo:activity",
      s_th="โปรแกรมฟื้นฟูแบบไป–กลับ 1–5 วันต่อสัปดาห์", s_en="A day program, 1–5 days a week",
      i_th="สำหรับผู้ที่ต้องการปรับตัวในการใช้ชีวิตประจำวัน พัฒนาการจัดการอารมณ์ ความเครียด การเข้าสังคม และการดูแลตนเอง เข้าร่วมกิจกรรม 1–5 วันต่อสัปดาห์ตามการประเมินของนักบำบัด ดูแลโดยจิตแพทย์ นักกิจกรรมบำบัด นักจิตวิทยา และนักกายภาพบำบัด",
      i_en="For people rebuilding everyday life: managing emotions and stress, getting along with others and caring for themselves. Join 1–5 days a week, as assessed by our therapists. Run by psychiatrists, occupational therapists, psychologists and physical therapists.",
      sec=[("เหมาะกับใคร", "Who it's for", [("ผู้สูงอายุที่อยู่ลำพัง หรือดูแลตนเองไม่ได้", "Older adults living alone or unable to self-care"), ("ครอบครัวที่ดูแลใกล้ชิดไม่ได้", "Families who can't provide close supervision"), ("ผู้ที่รู้สึกเหงา แยกตัว", "People feeling lonely or isolated"), ("ผู้ที่ต้องการพัฒนาพฤติกรรมและทักษะชีวิต", "Anyone building behaviour and life skills")]),
           ("กิจกรรมในโปรแกรม", "Activities", [("ฝึกกิจวัตรประจำวัน", "Daily living skills"), ("การรับรู้ ความรู้สึก และการเคลื่อนไหว", "Perception, sensation and movement"), ("ทักษะทางสังคม", "Social skills"), ("จัดการความเครียดและปัญหา", "Stress and problem management"), ("จัดการเวลาและการเงิน", "Time and money management"), ("ดนตรีบำบัดและการทำสวน", "Music therapy and gardening"), ("ฝึกทักษะการใช้มือ", "Hand skills"), ("เตรียมตัวก่อนเกษียณ", "Preparing for retirement"), ("ออกกำลังกาย ความยืดหยุ่น และการทรงตัว", "Exercise, flexibility and balance")])],
      extra="day"),
 dict(slug="child", icon="child", main=False, th="จิตเวชเด็กและวัยรุ่น", en="Child & Adolescent Psychiatry", img="ill:child",
      s_th="พัฒนาการ การเรียนรู้ อารมณ์ และพฤติกรรม", s_en="Development, learning, emotions and behaviour",
      i_th="คลินิกสุขภาพจิตเด็กและวัยรุ่น ส่งเสริมพัฒนาการสุขภาพจิตที่ดี และเสริมสร้างครอบครัวที่มีความสุขและอบอุ่น ดูแลทั้งเด็ก ครอบครัว โรงเรียน และองค์กร พร้อมอบรม สัมมนา และให้ความรู้แก่ผู้ปกครอง",
      i_en="Our child and adolescent clinic supports healthy development and warm, happy families. We work with children, parents, schools and organisations, and run training and talks for parents.",
      sec=[("ปัญหาที่ดูแล", "What we help with", [("พัฒนาการล่าช้า", "Developmental delay"), ("ปัญหาการเรียน", "Learning problems"), ("ปัญหาเชาวน์ปัญญา", "Intellectual difficulties"), ("ปัญหาพฤติกรรม", "Behaviour problems"), ("ปัญหาการกิน", "Eating problems"), ("สมาธิสั้น", "ADHD"), ("ออทิสติก", "Autism")]),
           ("บริการ", "Services", [("ให้คำปรึกษาเชิงป้องกัน", "Preventive counselling"), ("ตรวจรักษารายบุคคลและครอบครัว", "Individual and family treatment"), ("ฝึกปรับเปลี่ยนพฤติกรรม", "Behaviour modification"), ("กิจกรรมบำบัด", "Occupational therapy"), ("กลุ่มฝึกทักษะสังคม", "Social skills groups"), ("ฝึกพูด", "Speech training"), ("สัมมนาผู้ปกครองและครู", "Talks for parents and teachers"), ("เยี่ยมโรงเรียนและสอนเสริม", "School visits and tutoring")])]),
 dict(slug="adult", icon="person", main=False, th="จิตเวชผู้ใหญ่", en="Adult Psychiatry", img="ill:adult",
      s_th="ความเครียด ซึมเศร้า วิตกกังวล การนอน", s_en="Stress, depression, anxiety and sleep",
      i_th="ดูแลผู้ที่อายุ 18 ปีขึ้นไป เป้าหมายคือการใช้ชีวิตเป็นส่วนหนึ่งในสังคมได้อย่างมีคุณภาพ ให้บริการทั้งผู้ป่วยนอก ผู้ป่วยใน และศูนย์กิจกรรมกลางวัน",
      i_en="Care for adults aged 18 and over, with one goal: a good-quality life as part of the community. Available as outpatient, inpatient and day-program care.",
      sec=[("กลุ่มโรคและปัญหา", "Conditions and concerns", [("ความเครียด", "Stress"), ("ซึมเศร้า", "Depression"), ("ปัญหาการนอน", "Sleep problems"), ("ปัญหาการกิน", "Eating problems"), ("จิตเภท", "Schizophrenia"), ("ไบโพลาร์", "Bipolar disorder"), ("โรคกลัวต่าง ๆ", "Phobias"), ("ปัญหาครอบครัว", "Family problems"), ("ความสัมพันธ์และความรัก", "Relationships and love"), ("สารเสพติด", "Substance use")]),
           ("การบำบัดเสริม", "Supporting therapies", [("กิจกรรมบำบัด", "Occupational therapy"), ("กายภาพบำบัด", "Physical therapy"), ("ศิลปะบำบัด", "Art therapy"), ("การเต้นบำบัด", "Dance therapy"), ("ดนตรีบำบัด", "Music therapy")])]),
 dict(slug="elderly", icon="cane", main=False, th="จิตเวชผู้สูงอายุ", en="Elderly Psychiatry", img="ill:elderly",
      s_th="ความจำ การนอน สมองเสื่อม และอารมณ์", s_en="Memory, sleep, dementia and mood",
      i_th="ดูแลผู้ที่อายุ 55 ปีขึ้นไปที่มีปัญหาระบบประสาทและสุขภาพจิต ครอบคลุมการป้องกัน ประเมิน รักษา และพัฒนาสภาพจิตใจ ทั้งผู้ป่วย ผู้ดูแล และครอบครัว",
      i_en="Care for people aged 55 and over with neurological and mental health concerns: prevention, assessment, treatment and support for patients, carers and families.",
      sec=[("ปัญหาที่ดูแล", "What we help with", [("ปัญหาความจำ", "Memory problems"), ("ปัญหาการนอน", "Sleep problems"), ("ภาวะสมองเสื่อม", "Dementia"), ("ปัญหาอารมณ์ เช่น ซึมเศร้า", "Mood problems such as depression")]),
           ("โปรแกรม", "Programs", [("โปรแกรมผู้สูงอายุ (Geriatric day care)", "Geriatric day care program"), ("โปรแกรมฝึกสมอง (Brain rehabilitation)", "Brain rehabilitation program"), ("ประเมินการทำงานของสมอง", "Brain function assessment"), ("ปรับสภาพแวดล้อมในบ้าน", "Home environment advice"), ("อบรมผู้ดูแล", "Carer training")])]),
 dict(slug="ot", icon="hand", main=False, th="กิจกรรมบำบัด", en="Occupational Therapy", img="ill:ot",
      s_th="ใช้กิจกรรมที่มีเป้าหมายช่วยให้ใช้ชีวิตได้ตามศักยภาพ", s_en="Purposeful activity for everyday independence",
      i_th="การนำกิจกรรมที่มีจุดมุ่งหมาย รวมทั้งวิธีการและอุปกรณ์ที่เหมาะสม มาใช้บำบัดผู้ที่มีปัญหาด้านร่างกาย จิตใจ การเรียนรู้ พัฒนาการเด็ก และผู้สูงอายุ เพื่อให้ดำเนินชีวิตได้ตามศักยภาพของตน",
      i_en="Purposeful activities, methods and equipment that help people with physical, mental, learning or developmental difficulties, and older adults, live as independently as they can.",
      sec=[("ด้านสุขภาพจิต", "Mental health", [("ให้คำปรึกษา", "Counselling"), ("ฝึกกิจวัตรประจำวัน", "Daily living skills"), ("ทักษะทางสังคม", "Social skills"), ("จัดการความเครียด เวลา และการเงิน", "Managing stress, time and money")]),
           ("ผู้สูงอายุและเด็ก", "Older adults and children", [("ประเมินและบำบัดด้านการรับรู้", "Perception assessment and therapy"), ("ดัดแปลงอุปกรณ์ช่วย", "Adapted equipment"), ("คัดกรองและกระตุ้นพัฒนาการเด็ก", "Developmental screening and stimulation"), ("กลุ่มกิจกรรมสำหรับเด็ก", "Group activities for children")])]),
 dict(slug="pt", icon="walk", main=False, th="กายภาพบำบัด", en="Physical Therapy", img="ill:ot",
      s_th="ป้องกัน รักษา และฟื้นฟูการเคลื่อนไหว", s_en="Preventing, treating and restoring movement",
      i_th="วิชาชีพด้านวิทยาศาสตร์สุขภาพที่เกี่ยวข้องกับการป้องกัน รักษา และจัดการการเคลื่อนไหวที่ผิดปกติ ดูแลตั้งแต่ผู้ป่วยระบบประสาท ปัญหากล้ามเนื้อและข้อต่อ จนถึงผู้สูงอายุ",
      i_en="A health profession that prevents, treats and manages movement problems, from neurological conditions and muscle or joint pain to the needs of older adults.",
      sec=[("บริการ", "Services", [("กายภาพบำบัดระบบประสาท (อัมพฤกษ์ อัมพาต บาดเจ็บทางสมอง)", "Neurological physiotherapy (paralysis, brain injury)"), ("ระบบกล้ามเนื้อ กระดูก และข้อ (ปวดคอ บ่า หลัง เข่า)", "Muscles, bones and joints (neck, shoulder, back, knee pain)"), ("กายภาพบำบัดในผู้สูงวัย", "Physiotherapy for older adults"), ("ออกกำลังกายควบคุมน้ำหนัก ร่วมกับนักโภชนาการ", "Weight-control exercise with a nutritionist")])]),
 dict(slug="art", icon="palette", main=False, th="ศิลปะบำบัด", en="Art Therapy", img="ill:daycenter",
      s_th="สื่อสารความรู้สึกผ่านงานศิลปะ", s_en="Expressing feelings through art",
      i_th="ใช้ศิลปะเป็นเครื่องมือหลักในการเยียวยาทั้งกายและใจ ให้ผู้รับการบำบัดสำรวจภายในจิตใจและสื่อสารผ่านงานศิลปะได้อย่างอิสระ ไม่เน้นความสวยงาม แต่เน้นกระบวนการสำรวจอารมณ์และความรู้สึก",
      i_en="Art used as the main tool for healing body and mind. People explore their inner world and express themselves freely. It isn't about making something beautiful; it's about the process of exploring feelings.",
      sec=[("เหมาะกับใคร", "Who it's for", [("เด็กและวัยรุ่นที่มีปัญหาการเรียนรู้ ออทิสติก อารมณ์ หรือการเข้าสังคม", "Children and teens with learning, autism, emotional or social difficulties"), ("ผู้ที่เศร้า วิตกกังวล หรือเก็บตัว", "People who feel low, anxious or withdrawn"), ("ผู้ใหญ่และผู้สูงอายุที่มีปัญหาการนอนหรืออัลไซเมอร์", "Adults and older adults with sleep problems or Alzheimer's")]),
           ("ประโยชน์", "Benefits", [("สมาธิดีขึ้น จดจ่อได้นานขึ้น", "Better focus and attention"), ("เห็นคุณค่าในตนเอง", "Stronger self-worth"), ("จินตนาการและความคิดสร้างสรรค์", "Imagination and creativity"), ("ผ่อนคลาย ฟื้นฟูพลังชีวิต", "Relaxation and renewed energy"), ("ทักษะทางสังคม", "Social skills")])]),
 dict(slug="dance", icon="dance", main=False, th="การเต้นบำบัด", en="Dance Therapy", img="ill:daycenter",
      s_th="แสดงอารมณ์ผ่านร่างกายและการเคลื่อนไหว", s_en="Expressing emotion through movement",
      i_th="การเต้นและการเคลื่อนไหวบำบัด เป็นรูปแบบหนึ่งของ Expressive Therapy ที่ให้ผู้เข้าร่วมสื่อสารและแสดงอารมณ์ผ่านร่างกาย ท่าเต้น และการเคลื่อนไหว ใช้เกมและกิจกรรมกลุ่มเพื่อเชื่อมโยงกับร่างกายตนเองและผู้อื่น",
      i_en="Dance and movement therapy is a form of expressive therapy. People communicate and express emotion through the body, dance and movement, using games and group activities to connect with themselves and others.",
      sec=[("เหมาะกับใคร", "Who it's for", [("ผู้ที่มีปัญหาสังคมและอารมณ์ เช่น ซึมเศร้า วิตกกังวล เหงา", "People struggling with mood or social life: depression, anxiety, loneliness"), ("ผู้ที่ขาดแรงจูงใจ เฉื่อยชา", "People lacking motivation"), ("ผู้ที่ต้องการฟื้นฟูร่างกาย", "People recovering physically"), ("ผู้ที่ต้องการดูแลสมองและชะลอความเสื่อม", "Anyone keeping their brain active")]),
           ("ประโยชน์", "Benefits", [("ออกกำลังกายในบรรยากาศผ่อนคลาย", "Exercise in a relaxed setting"), ("เชื่อมโยงอารมณ์และจิตใจ", "Connecting emotions and mind"), ("สร้างปฏิสัมพันธ์ทางสังคม", "Building social connection"), ("ส่งเสริมความจำระยะสั้นและระยะยาว", "Supporting short and long-term memory")])]),
 dict(slug="music", icon="music", main=False, th="ดนตรีบำบัด", en="Music Therapy", img="ill:daycenter",
      s_th="ใช้ดนตรีช่วยผ่อนคลาย สื่อสาร และฟื้นฟู", s_en="Music for relaxation, communication and recovery",
      i_th="การนำดนตรีมาใช้ทางการแพทย์ เพื่อรักษาหรือพัฒนาศักยภาพด้านร่างกาย จิตใจ ความคิด และทักษะทางสังคม ทำได้ทั้งแบบเดี่ยวและกลุ่มในทุกช่วงวัย มีทั้งแบบฟัง (Receptive) และแบบเล่น (Active)",
      i_en="Music used in healthcare to treat and to build physical, emotional, thinking and social skills, one-to-one or in groups, at any age. Sessions can be listening (receptive) or playing (active).",
      sec=[("ประโยชน์", "Benefits", [("เพิ่มคุณภาพชีวิต", "Better quality of life"), ("จัดการความเครียด", "Stress management"), ("บรรเทาอาการเจ็บปวด", "Pain relief"), ("แสดงความรู้สึก", "Expressing feelings"), ("กระตุ้นความจำ", "Memory stimulation"), ("เพิ่มทักษะการสื่อสาร", "Communication skills")]),
           ("เหมาะกับใคร", "Who it's for", [("ผู้มีปัญหาพัฒนาการร่างกายและสมอง", "People with developmental needs"), ("ผู้สูงอายุ และผู้มีภาวะสมองเสื่อม", "Older adults and people with dementia"), ("ผู้ที่แยกตัวหรือขาดทักษะการสื่อสาร", "People who are withdrawn or find communication hard"), ("ผู้ที่มีภาวะซึมเศร้า", "People with depression")])]),
 dict(slug="sleep", icon="moon", main=False, th="ปัญหาการนอน", en="Sleep Disorders", img="ill:adult",
      s_th="ตรวจ วินิจฉัย และรักษาปัญหาการนอนหลับ", s_en="Diagnosis and treatment of sleep problems",
      i_th="ตรวจ วินิจฉัย และรักษาผู้ที่มีปัญหาการนอนหลับ โดยแพทย์ที่มีความรู้ความชำนาญด้านปัญหาการนอน ร่วมกับนักจิตวิทยาที่ฝึกการผ่อนคลายเพื่อส่งเสริมการนอนหลับ",
      i_en="Diagnosis and treatment of sleep problems by doctors experienced in sleep medicine, with psychologists who teach relaxation techniques for better sleep.",
      sec=[("ปัญหาที่ดูแล", "What we treat", [("นอนไม่หลับ หลับยาก หลับไม่สนิท", "Insomnia and restless sleep"), ("ง่วงนอนตอนกลางวัน", "Daytime sleepiness"), ("หยุดหายใจขณะหลับและนอนกรน", "Sleep apnea and snoring"), ("ขาอยู่ไม่สุข (Restless legs)", "Restless legs syndrome"), ("ขากระตุกขณะหลับ (PLMD)", "Periodic limb movement disorder"), ("โรคลมหลับ (Narcolepsy)", "Narcolepsy"), ("ปัญหาการใช้ยานอนหลับ", "Sleeping-pill problems")])]),
 dict(slug="special-ed", icon="book", main=False, th="การศึกษาพิเศษ", en="Special Education", img="ill:child",
      s_th="แผนการเรียนเฉพาะบุคคลสำหรับเด็กที่มีความต้องการพิเศษ", s_en="Individual education plans for children",
      i_th="การฟื้นฟูสมรรถภาพทางการศึกษาและทักษะวิชาการ ควบคู่กับการเพิ่มทักษะทางสังคม จัดทำแผนการศึกษาเฉพาะบุคคล (IEP) ช่วยเด็กที่มีปัญหาการเรียนรู้ การอ่าน การเขียน และเด็กที่มีความต้องการพิเศษ เช่น แอลดี สมาธิสั้น ออทิสติก",
      i_en="Rebuilding learning and academic skills alongside social skills, with an Individualized Education Program (IEP) for children with reading, writing or learning difficulties and special needs such as LD, ADHD or autism.",
      sec=[("สิ่งที่ครูการศึกษาพิเศษทำ", "What our special educators do", [("ประเมินทักษะและหาวิธีเรียนที่เหมาะสม", "Assess skills and find the right way to learn"), ("วางแผนการศึกษาเฉพาะบุคคล (IEP)", "Plan an individual education program (IEP)"), ("เสริมความมั่นใจในการเรียน", "Build confidence in learning"), ("เรียนผ่านประสาทสัมผัสทั้ง 5", "Learning through all five senses")])]),
 dict(slug="psych-test", icon="brain", main=False, th="การทดสอบทางจิตวิทยา", en="Psychological Testing", img="ill:consult",
      s_th="แบบทดสอบมาตรฐานโดยนักจิตวิทยา", s_en="Standardised testing by psychologists",
      i_th="ประเมินด้วยแบบทดสอบมาตรฐานโดยนักจิตวิทยา นำผลไปเปรียบเทียบกับคนในวัยเดียวกัน เพื่อช่วยวินิจฉัยโรค วางแผนการบำบัด และค้นหาจุดเด่นจุดด้อยในการเรียน",
      i_en="Standardised tests run by psychologists. Results are compared with people of the same age to support diagnosis, therapy planning and understanding learning strengths and weaknesses.",
      sec=[("ประเภทการทดสอบ", "Types of testing", [("ความสามารถทางปัญญา (IQ)", "Cognitive ability (IQ)"), ("ผลสัมฤทธิ์ทางการศึกษา", "Academic achievement"), ("ความสามารถทางภาษาไทยและอังกฤษ", "Thai and English language skills"), ("พฤติกรรมการปรับตัว", "Adaptive behaviour"), ("การประเมินบุคลิกภาพ", "Personality assessment"), ("การประเมินทางจิตวิทยาคลินิก", "Clinical psychological assessment"), ("การประเมินทางจิตประสาท", "Neuropsychological assessment")])]),
]

GROUPS = [("main", "บริการหลัก", "Core services"), ("care", "ดูแลตามช่วงวัย", "Care by age"),
          ("therapy", "บำบัดและฟื้นฟู", "Therapy & rehabilitation"), ("special", "บริการเฉพาะทาง", "Specialised services")]
GROUP_OF = {"opd": "main", "ipd": "main", "daycenter": "main", "child": "care", "adult": "care", "elderly": "care",
            "ot": "therapy", "pt": "therapy", "art": "therapy", "dance": "therapy", "music": "therapy",
            "sleep": "special", "special-ed": "special", "psych-test": "special"}
CARD_ORDER = ["child", "adult", "elderly", "ot", "pt", "art", "dance", "music", "sleep", "special-ed", "psych-test"]

# ------------------------------------------------------------------ articles (real, manarom.com/blog)
B = "https://www.manarom.com/blog/"
ART = {
 "path": ("เส้นทางแห่งความสุข", "The path to happiness", B + "path_to_happiness.html", "garden"),
 "compare": ("มีความสุขง่ายขึ้น ถ้าเปรียบเทียบน้อยลง", "Compare less, feel happier", B + "comparisons_reduce_happiness.html", "lounge"),
 "seven": ("7 วิธี ดูแลสุขภาพจิต เริ่มได้เลย ไม่ต้องรอให้ป่วย", "7 ways to care for your mental health", B + "7_Ways_to_Take_Care_of_Your_Mental_Health.html", "dining"),
 "dead": ("Dead Inside รับมืออย่างไรกับ “ภาวะสิ้นยินดี”", "Dead inside: coping with anhedonia", B + "dead_inside.html", "common"),
 "fatigue": ("สมองล้า (Mental Fatigue) คืออะไร ทำไมพักแล้วไม่หาย?", "Mental fatigue: why rest doesn't fix it", B + "mental_fatigue.html", "activity"),
 "procrast": ("How to หยุดนิสัยผัดวันประกันพรุ่ง", "How to stop procrastinating", B + "how_to_stop_procrastinating.html", "dining"),
 "heal": ("การเยียวยาจิตใจตัวเองเมื่อเป็นโรคซึมเศร้า", "Healing yourself through depression", B + "Heal_yourself_when_suffering_from_depression.html", "garden"),
 "hope": ("HOPE เรายังมีหวังแม้วันฟ้าหม่น", "HOPE: still hopeful on grey days", B + "hope.html", "lounge"),
 "lonely": ("อยู่อย่างคนเหงา ๆ รับมือแบบไหน ดูแลตัวเองยังไง", "Living with loneliness", B + "how_to_deal_with_loneliness.html", "common"),
 "desk": ("คลายเครียดง่าย ๆ ที่โต๊ะทำงาน", "Easy stress relief at your desk", B + "Stress_relief_at_your_desk.html", "dining"),
 "breath": ("ฝึกหายใจแบบ “Slow motion” พร้อมรับปัญหา สร้างความสงบ", "Slow-motion breathing for calm", B + "slow_breathing_helps_problem_solving.html", "garden"),
 "overthink": ("คิดมากจนปวดหัว คิดเยอะจนเหนื่อยใจ คิดอย่างไรให้พอดี", "Overthinking: how to think just enough", B + "stop_overthinking.html", "activity"),
 "burnout": ("Burnout สภาวะหมดไฟจากการทำงาน", "Burnout at work", B + "burnout.html", "common"),
 "imposter": ("Imposter Syndrome ทำไมฉันไม่เคยเก่งพอ", "Imposter syndrome", B + "Imposter_Syndrome.html", "lounge"),
 "childsign": ("สังเกตพฤติกรรมลูก เมื่อไหร่ต้องไปพบจิตแพทย์", "When should your child see a psychiatrist?", B + "Signs_your_child_may_need_psychiatrist.html", "activity"),
 "discipline": ("10 วิธี สร้างวินัยให้ลูกรัก", "10 ways to build discipline in your child", B + "Discipline_for_children.html", "dining"),
 "teentalk": ("5 เทคนิค คุยกับพ่อแม่อย่างไร เมื่อลูกวัยรุ่นอยากพบจิตแพทย์", "Telling your parents you want to see a psychiatrist", B + "how_to_tell_your_parents_that_you_need_a_psychiatrist_for_teen.html", "lounge"),
 "bully": ("STOP BULLYING หยุดแกล้งกัน ก่อนซึมเศร้าถามหา", "Stop bullying before depression sets in", B + "stop_bullying.html", "common"),
 "memory": ("กิจกรรมส่งเสริมความจำ สำหรับผู้สูงอายุที่มีภาวะสมองเสื่อม", "Memory activities for older adults with dementia", B + "Brain_boosting_activities_for_seniors.html", "garden"),
 "retire": ("วางแผนจิตใจให้พร้อมก่อนวัยเกษียณ", "Preparing your mind for retirement", B + "Retirement_preparations.html", "activity"),
 "panic": ("โรคแพนิก (Panic Disorder) ทุกข์ทรมานแค่ไหน", "Panic disorder: what it feels like", B + "panic_disorder.html", "common"),
 "bipolar": ("เดี๋ยวดี เดี๋ยวร้าย ใช่ไบโพลาร์หรือเปล่านะ?", "Up one day, down the next: is it bipolar?", B + "BipolarDisorder.html", "lounge"),
 "cbti": ("CBT-I ปรับความคิด พฤติกรรม บำบัดรักษาโรคนอนไม่หลับ", "CBT-I: treating insomnia", B + "CBT-I_Cognitive_Behavioral_Therapy_for_Insomnia.html", "dining"),
}
ALL_ARTICLES_URL = B + "article_thai.html"

# knowledge page list: (category, key)
KNOW = [("work", "burnout"), ("work", "imposter"), ("work", "desk"), ("family", "childsign"), ("family", "discipline"),
        ("teen", "teentalk"), ("teen", "bully"), ("elder", "memory"), ("elder", "retire"), ("cond", "panic"),
        ("cond", "bipolar"), ("cond", "cbti"), ("cond", "fatigue"), ("work", "overthink"), ("cond", "heal")]

MOODS = [
 ("good", "สบายดี", "Good", "ดีใจด้วยนะคะ เก็บพลังใจดี ๆ แบบนี้ไว้ใช้ในวันที่เหนื่อย ลองอ่านบทความเหล่านี้ดูค่ะ", "So glad to hear it! Keep that good energy for harder days. Here's some reading for you.", ["path", "compare", "seven"]),
 ("ok", "เฉย ๆ", "So-so", "บางวันก็แค่เรื่อย ๆ ไม่เป็นไรเลยค่ะ ลองหาสิ่งเล็ก ๆ ที่ช่วยเติมไฟให้ใจดูนะคะ", "Some days are just so-so, and that's okay. Here are small things that can lift you a little.", ["dead", "fatigue", "procrast"]),
 ("sad", "เศร้า", "Low", "ขอบคุณที่บอกน้องใจดีนะคะ ความรู้สึกนี้ผ่านไปได้ ถ้าเป็นติดต่อกันหลายวัน คุยกับผู้เชี่ยวชาญได้เสมอค่ะ", "Thank you for telling me. This feeling can pass. If it lasts several days, a specialist is always here to talk.", ["heal", "hope", "lonely"]),
 ("tense", "เครียด", "Stressed", "หายใจลึก ๆ ก่อนนะคะ ความเครียดจัดการได้ ลองวิธีง่าย ๆ จากบทความนี้ หรือเช็กระดับความเครียดใน 1 นาทีค่ะ", "Take a deep breath first. Stress can be managed: try these simple ideas, or check your stress level in one minute.", ["desk", "breath", "overthink"]),
]

FAQ = [
 ("มาใช้บริการครั้งแรกต้องทำอย่างไร", "What do I do for my first visit?",
  f"กรุณานัดหมายล่วงหน้า ติดต่อแผนกเวชระเบียน โทร {PHONE_REG} นำบัตรประชาชนมาด้วย และมาก่อนเวลานัดอย่างน้อย 15 นาที",
  f"Please book ahead with our medical records team on {PHONE_REG}. Bring your ID card or passport and arrive at least 15 minutes early."),
 ("มาโดยไม่นัดหมาย (Walk in) ได้ไหม", "Can I walk in without an appointment?",
  "ได้ค่ะ แต่อาจได้รับบริการช้ากว่าผู้ที่นัดหมายล่วงหน้า", "Yes, but you may wait longer than patients with an appointment."),
 ("โรงพยาบาลเปิดให้บริการเวลาใด", "What are your opening hours?",
  "แผนกผู้ป่วยนอก เปิด 07:00–20:00 น. แผนกฉุกเฉิน เปิด 24 ชั่วโมง", "Outpatient: 07:00–20:00. Emergency: open 24 hours."),
 ("กังวลเรื่องค่าใช้จ่าย ต้องทำอย่างไร", "I'm worried about the cost. What should I do?",
  f"ค่ารักษาผู้ป่วยนอกโดยประมาณครั้งละ 1,000–3,000 บาท สอบถามค่าใช้จ่ายเบื้องต้นได้ที่ {PHONE_2}", f"Outpatient visits are roughly 1,000–3,000 baht each. Call {PHONE_2} for an estimate."),
 ("ใช้สิทธิประกันได้หรือไม่", "Can I use insurance or government schemes?",
  "โรงพยาบาลไม่ได้เปิดรับสิทธิประกันสังคม สิทธิข้าราชการ หรือสิทธิประกันสุขภาพกับบริษัทประกันใด ๆ", "The hospital does not accept social security, civil-servant schemes or direct billing with insurance companies."),
 ("ขอสำเนาใบเสร็จรับเงินได้ไหม", "Can I get a copy of my receipt?",
  "ติดต่อแผนกการเงิน หรือขอให้จัดส่งทางไปรษณีย์ได้ (ไม่สามารถเปลี่ยนวันที่ในเอกสารการเงินได้)", "Contact our finance department, or ask us to post it. Dates on financial documents can't be changed."),
 ("ต้องการขอข้อมูลการรักษาของผู้ป่วย", "How do I request treatment records?",
  "ผู้ป่วยต้องกรอกเอกสารขอข้อมูลการรักษาด้วยตนเองที่โรงพยาบาลเท่านั้น", "Patients must fill in the request form in person at the hospital."),
 ("ขอซื้อยาได้หรือไม่", "Can I buy medication?",
  "ผู้ป่วยติดต่อขอซื้อยาได้ กรณีอยู่ต่างประเทศ ให้ญาติมาติดต่อรับยาที่โรงพยาบาลได้", "Yes. If the patient is abroad, a relative can collect medication at the hospital."),
]

OPD_PRICES = [("ตรวจรักษาครั้งแรก (ไม่รวมค่ายา)", "First consultation (excl. medication)", "1,800 – 4,000"),
              ("ตรวจรักษาครั้งต่อไป", "Follow-up consultation", "1,000 – 4,000"),
              ("จิตบำบัดรายบุคคล", "Individual psychotherapy", "1,600 – 4,000"),
              ("ครอบครัวบำบัด", "Family therapy", "3,200 – 4,500")]
IPD_PRICES = [  # room th, en, room, nursing, therapy, service, total
 ("ห้องเตียงคู่", "Twin room", "3,500", "3,300", "2,000", "1,200", "10,000"),
 ("ห้องเตียงเดี่ยว", "Single room", "5,000", "3,300", "2,000", "1,500", "11,800"),
 ("ห้องพิเศษ", "Private room", "7,000", "3,300", "2,000", "1,800", "14,100"),
 ("ห้องพิเศษมีสวนหย่อม", "Private room with garden", "8,000", "3,300", "2,000", "2,000", "15,300"),
 ("ห้องสังเกตอาการ", "Close observation room", "6,500", "5,800", "–", "2,000", "14,300"),
]

PSYCHOTESTS = [
 ("BCA", "Basic Competency Assessment", "คัดกรองผู้สมัครได้ทันทีที่มาสมัครงาน ใช้ได้ทุกระดับตำแหน่งและการศึกษา", "Screens applicants on the spot. Works for every position and education level."),
 ("MCA", "Manarom Cognitive Ability Assessment", "วัดระดับสติปัญญาและความถนัด แบบทดสอบที่สัมพันธ์สูงสุดกับความสำเร็จในการทำงาน", "Measures intelligence and aptitude, the test most closely linked to success at work."),
 ("MPI", "Manarom Personality Inventory", "ประเมินบุคลิกภาพในการทำงาน ความคิดสร้างสรรค์ ภาวะผู้นำ และความพร้อมเรียนรู้สิ่งใหม่", "Assesses work personality, creativity, leadership and openness to learning."),
 ("MRT", "Manarom Resilience Psychotest", "ประเมินความสามารถในการจัดการอารมณ์และจิตใจ เมื่อเจอเหตุการณ์ไม่คาดฝัน", "Assesses how well people manage emotions and pressure when the unexpected happens."),
]
PSYCHO_BENEFITS = [("ได้บุคลากรที่เหมาะกับตำแหน่ง", "Hire people who fit the role"), ("ลดอคติจากผู้สัมภาษณ์", "Reduce interviewer bias"),
                   ("ลดปัญหาพนักงานดีลาออก", "Keep good employees longer"), ("พัฒนาศักยภาพบุคลากรที่มีอยู่", "Develop the people you already have")]
TRAININGS = [("การจัดการความเครียด", "Stress management"), ("การสื่อสารในองค์กร", "Workplace communication"), ("การเจรจาต่อรอง", "Negotiation"),
             ("เตรียมตัวก่อนเกษียณ", "Preparing for retirement"), ("ภาวะผู้นำ", "Leadership"), ("Executive Coaching Program", "Executive Coaching Program"),
             ("หลักสูตรตามความต้องการขององค์กร (Customized)", "Customised programs")]
