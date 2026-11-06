"""Generate the AnyCompany Air sample: an airline whose customers cannot rebook themselves when flights go wrong.

Writes samples/anycompany-air/discovery/data/, with telemetry in data/telemetry/. Deterministic: the same seed writes byte-identical files.

Usage: python3 scripts/samples/anycompany-air.py
"""

from __future__ import annotations

import csv
import random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

SEED = 20261101
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "samples" / "anycompany-air" / "discovery" / "data"

START, END = date(2026, 5, 1), date(2026, 10, 15)
MONTHS = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

THEMES = ["disruption_rebooking", "bag_tracking", "booking_flow", "cheaper_fares",
          "seat_map_3d", "loyalty_points", "on_time_positive", "other"]

# Records per channel and theme. These counts are quoted in facilitator/anycompany-air.md.
PLAN = {
    "reviews":          {"disruption_rebooking": 12, "bag_tracking": 8, "booking_flow": 14, "cheaper_fares": 8,
                         "seat_map_3d": 6, "loyalty_points": 6, "on_time_positive": 15, "other": 11},
    "call_center":      {"disruption_rebooking": 42, "bag_tracking": 18, "booking_flow": 6, "cheaper_fares": 2,
                         "seat_map_3d": 0, "loyalty_points": 9, "on_time_positive": 0, "other": 33},
    "social":           {"disruption_rebooking": 18, "bag_tracking": 8, "booking_flow": 5, "cheaper_fares": 10,
                         "seat_map_3d": 6, "loyalty_points": 3, "on_time_positive": 10, "other": 10},
    "nps":              {"disruption_rebooking": 22, "bag_tracking": 7, "booking_flow": 6, "cheaper_fares": 8,
                         "seat_map_3d": 2, "loyalty_points": 5, "on_time_positive": 25, "other": 5},
    "account_manager":  {"disruption_rebooking": 9, "bag_tracking": 2, "booking_flow": 8, "cheaper_fares": 3,
                         "seat_map_3d": 2, "loyalty_points": 2, "on_time_positive": 3, "other": 1},
    "travel_agency":    {"disruption_rebooking": 10, "bag_tracking": 2, "booking_flow": 6, "cheaper_fares": 2,
                         "seat_map_3d": 0, "loyalty_points": 2, "on_time_positive": 2, "other": 6},
}

CITIES = ["Lisbon", "Madrid", "Paris", "Frankfurt", "Milan", "Dublin", "Amsterdam", "Vienna", "Zurich",
          "Barcelona", "Munich", "Copenhagen", "Prague", "Brussels", "Rome", "Athens", "Stockholm",
          "Warsaw", "Porto", "Nice", "Seville", "Hamburg", "Oslo", "Budapest"]
TIMES = ["06:10", "06:45", "07:20", "07:40", "08:15", "09:05", "10:30", "11:50", "13:15", "14:40",
         "16:05", "17:25", "18:10", "19:35", "20:50", "21:40"]
INDUSTRIES = ["consulting", "engineering", "pharma", "software", "legal services", "logistics",
              "retail", "banking", "insurance", "energy", "media", "public sector"]


def slots(rng: random.Random) -> dict:
    city, dest = rng.sample(CITIES, 2)
    return {
        "city": city, "dest": dest, "hours": rng.randint(2, 9), "wait": rng.choice(range(35, 185, 5)),
        "time": rng.choice(TIMES), "n": rng.randint(101, 989), "size": rng.choice(range(300, 4100, 100)),
        "pax": rng.randint(6, 48), "kids": rng.randint(2, 3), "days": rng.randint(4, 21),
        "industry": rng.choice(INDUSTRIES), "points": rng.choice(range(1200, 18000, 100)),
        "agency": rng.randint(11, 97), "price": rng.choice(range(89, 640, 10)),
    }


# Hand-written phrasings, by theme and channel. {slots} vary per record.
BANK: dict[str, dict[str, list[str]]] = {
    "disruption_rebooking": {
        "reviews": [
            "Flight to {dest} cancelled at the gate. The app just said 'please contact us'. {wait} minutes on hold to get moved to a flight the next afternoon. The flight itself was fine; the cancellation handling was a disaster.",
            "Delayed {hours} hours in {city}. There was a later flight with empty seats and no way to move myself onto it in the app. I queued at the desk behind what felt like the whole plane.",
            "Missed my connection in {city} because the first leg was late. The app knew. I got a push notification and then nothing: no new flight, no button, just 'call us'.",
            "Cancelled flight, and the automatic rebooking put me on a flight {days} days later. Changing it meant calling. Why can't I choose from the options myself?",
            "Good crew, comfortable seats, but when something goes wrong you are on your own. My {city} flight was cancelled and it took {wait} minutes on the phone to sort out.",
            "The app is fine for booking and check-in. The moment a flight is disrupted it becomes useless and everything goes through the call centre.",
            "Two hours stuck at {city} airport after a cancellation, and the website still showed my old flight as confirmed.",
            "Our family got split across two flights after a cancellation and we couldn't fix it online. One star for the disruption handling only.",
            "They cancelled my return from {city} by text at 23:00 and the phone line opened at 07:00. By then the next flights were full.",
            "Delays happen, I get it. What I don't get is why I can see alternative flights on the website but can't move myself onto one.",
            "Flight delayed {hours} hours, I missed the meeting I was flying for. Getting a new flight meant two calls and an email.",
            "Got a meal voucher after the {city} cancellation but no new flight. The app had nothing for me to choose.",
            "The 'manage booking' page shows an error when your flight is cancelled. Of all the moments for that to happen.",
            "Rebooking after a delay should take a minute. It took me the whole evening and three phone calls.",
            "Fourth time this year a {city} flight was moved, and every time the only option is the hotline. I have started booking another airline for that route.",
        ],
        "call_center": [
            "Customer: My {time} to {dest} was cancelled. The app tells me to call you and I've been waiting {wait} minutes. Agent: I'm sorry about the wait. I can see two options tomorrow morning. Customer: I saw those in the app too, why couldn't I just pick one?",
            "Customer: I'm at {city} airport, my connection has gone because the first flight was {hours} hours late. Agent: Let me look at alternatives. Customer: The desk queue is huge, please just put me on anything today.",
            "Customer: You rebooked me automatically onto a flight in {days} days. I need to be in {dest} tomorrow. Agent: I can move you to the {time} if you don't mind a connection. Customer: Yes. Why does this need a phone call?",
            "Customer: Our flight to {dest} is delayed again and we'll miss the onward train. Can we change to the earlier flight? Agent: The {time} has seats, I can move all {kids} of you. Customer: Thank you, I tried doing it on the website for an hour.",
            "Customer: The text says my flight is cancelled and 'we will contact you'. Nobody has. Agent: I can see you were rebooked for the day after tomorrow. Customer: That's no good, I fly back for work.",
            "Customer: I want a refund, not a voucher, for the cancelled {city} flight. Agent: You're entitled to a refund, I'll process it. Customer: The app only offered the voucher.",
            "Customer: My boss is on the {time} from {city} that was just cancelled. Can I rebook her from here? Agent: I can do it if you have the booking. Customer: The online tool just says to call.",
            "Customer: I've been on hold {wait} minutes. Delay of {hours} hours on {dest}, and I need a hotel. Agent: I'll issue a hotel voucher and rebook you on the first flight. Customer: Can't the app do the voucher?",
            "Customer: Second call today. The first agent rebooked me but the app still shows the cancelled flight and won't let me check in. Agent: I'll reissue the ticket now.",
            "Customer: Missed connection in {city}, I'm travelling with a wheelchair user and we need a new flight with assistance. Agent: I'll rebook and add assistance. It may take a few minutes.",
            "Customer: Is my flight to {dest} actually going? The app says delayed, the board says cancelled. Agent: It's cancelled, I'm sorry. I'll find you an alternative.",
            "Customer: Group of {pax} colleagues on the cancelled {city} flight. Can we all move to the evening one? Agent: I can only see nine seats. I'll split the group.",
            "Customer: I picked a new flight on your website after the cancellation and it charged me a change fee. Agent: That shouldn't happen after a cancellation, I'll refund the fee.",
            "Customer: The delay means I'll land after the last bus. Can I move to tomorrow morning instead? Agent: Yes, the {time} has space. Customer: I'd have done this myself if the app let me.",
            "Customer: Why did I get rebooked through {city} with a five-hour layover when there's a direct flight? Agent: The system picks automatically. I can change it to the direct one.",
            "Customer: I'm calling from the gate in {city}. The flight just got cancelled and there are 150 of us. Agent: I'm checking the next flights now. Customer: Please hurry, everyone is on the phone to you.",
            "Customer: The app offered me a new flight but the 'accept' button does nothing. Agent: I'll confirm it from here. Customer: I've tapped it twenty times.",
            "Customer: My {time} was delayed {hours} hours and now the hotel won't hold my room. Agent: I can move you to tomorrow and add a hotel voucher for tonight in {city}.",
            "Customer: I travel for work every week and this is the third disruption this month. I just want to choose my own flight. Agent: I understand. I've put you on the {time}.",
            "Customer: The rebooking text says to go to the transfer desk in {city}, but it's closed. Agent: I'll rebook you now, I'm sorry.",
            "Customer: Can I take a train instead after the cancellation and get a refund? Agent: Yes, I'll refund the unused flight. Customer: I couldn't find that option anywhere online.",
            "Customer: We're a family of {kids} adults and two children. The new flight split us across two days. Agent: Let me find a flight where you can travel together.",
            "Customer: I don't want the flight you rebooked me on, I want my money back. Agent: I'll process the refund now; it takes up to seven days.",
            "Customer: I've called four times, each time a different answer about my cancelled {dest} flight. Agent: I'm sorry. I'll fix the booking and note it so it stays fixed.",
            "Customer: The board in {city} says my flight is delayed to {time}. Will I make my connection to {dest}? Agent: Probably not. I'll protect you on the later connection.",
            "Customer: I'm a frequent flyer, is there a priority line for rebooking? Agent: You're through to it now. The wait was {wait} minutes for everyone today, I'm sorry.",
            "Customer: Your text said I'd been rebooked, but there's no new booking in the app. Agent: The new ticket wasn't issued. I'll issue it now.",
        ],
        "social": [
            "Flight to {dest} cancelled, app says call, hold time {wait} min and counting. Come on @AnyCompanyAir",
            "Stuck in {city}. {hours}h delay, missed connection, no rebooking option anywhere online. Desk queue goes round the terminal.",
            "@AnyCompanyAir your app tells me my flight is cancelled and then has no buttons. What am I supposed to do with that",
            "Third cancellation on the {city} route this summer. Every time: call the hotline. Every time: {wait} minutes on hold.",
            "Love how I can book a flight in 30 seconds but rebooking a cancelled one takes an afternoon",
            "Got rebooked automatically to a flight {days} days from now. I have a job. @AnyCompanyAir",
            "Sat on the floor at {city} for {hours} hours, there's a flight leaving at {time} with seats and nobody at the desk can move me",
            "Pro tip if your AnyCompany Air flight gets cancelled: don't bother with the app, call immediately before the good flights fill up",
            "Cancelled at midnight by text, hotline closed until 7. Thanks @AnyCompanyAir",
            "The disruption experience is the whole product. Everything else is fine until it isn't.",
            "Delay notification at {time}, then nothing. No new times, no options, no humans. {city} gate is chaos",
            "@AnyCompanyAir why does the website show me alternative flights after a cancellation but won't let me pick one",
            "My parents are stuck in {city} after a cancellation and can't get through on the phone. They don't know how to use the app, and the app can't help anyway",
            "Spent my holiday's first evening on hold with the airline instead of at dinner. {wait} minutes for a rebooking.",
            "Flight cancelled. App: 'Something went wrong.' Yes. Yes it did.",
            "Rebooking queue at {city} is longer than the security queue",
            "Cancelled again on the {city} route. I'm switching airlines for this one.",
            "Hold music for {wait} minutes so far. It's a good song the first 30 times.",
        ],
        "nps": [
            "Flight was cancelled and I had to call to rebook. {wait} minutes waiting.",
            "The delay wasn't the problem. Not being able to change my flight myself was.",
            "Cancelled, rebooked to a terrible time, and the only way to fix it was the phone.",
            "Missed my connection in {city} and nobody helped until I found a desk.",
            "Nothing in the app when the flight was disrupted. Just a message to call.",
            "Flight moved twice, no way to choose another option online.",
            "The crew were lovely. The cancellation process was not.",
            "I waited {hours} hours with no clear information and no way to rebook.",
            "Would have given 8 if the rebooking had worked in the app.",
            "Being stuck on hold while the good flights filled up.",
            "Cancelled late at night, phone line closed, we slept at the airport.",
            "Rebooked automatically onto a flight that didn't work for us and changing it was a nightmare.",
            "When it goes wrong you are completely alone.",
            "I could see empty seats on a later flight and couldn't get on it.",
            "Spent the evening on hold instead of with my family.",
            "The flight was cancelled and the app was no help at all.",
            "Rebooking took longer than the flight.",
            "No information during a {hours}-hour delay.",
            "Nobody at the desk and nothing in the app after the cancellation.",
            "I had to sort out my own hotel after the cancellation.",
            "The airline didn't care once the flight was cancelled.",
            "We missed our connection and lost a day of our holiday.",
            "I had no control over my new flight.",
            "Three calls to fix one cancellation.",
        ],
        "account_manager": [
            "QBR with Customer 0{n} ({industry}, about {size} travellers). Travel manager raised four cancellations on the {city} route last quarter where travellers could not rebook themselves and waited on hold. She said plainly that the renewal in Q1 depends on how we handle disruption.",
            "Renewal call with Customer 0{n} ({industry}). Their CFO missed a board meeting after a {city} cancellation and spent an hour on the phone. They are trialling a competitor on two routes. The ask is simple: let travellers rebook themselves in the app.",
            "Customer 0{n} ({industry}, about {size} travellers) sent their disruption report: 61 disrupted trips in the summer, average time to rebook over two hours. They want self-service rebooking and real-time updates to their travel management company.",
            "Quarterly review with Customer 0{n}. Price and network are fine, and they like the lounges. The one complaint is disruption: travellers stranded at {city} with no way to change flights. Flagged the account as at risk.",
            "Customer 0{n} ({industry}) asked whether we can give their travel desk a tool to rebook disrupted travellers in bulk. Today their agents call our corporate line one traveller at a time.",
            "Escalation from Customer 0{n}'s travel manager after the {city} cancellations: 23 travellers, 9 of them rebooked only the next day. She compared us unfavourably with the airline they use on long-haul.",
            "Customer 0{n} renewal is on track commercially, but their duty-of-care team wants to know where travellers are during disruptions and how fast they get rebooked. We can't give them either today.",
            "Visit to Customer 0{n} ({industry}). Their travellers have stopped calling us and book the next flight with any airline at their own cost, then claim it back. They call it 'the AnyCompany tax'.",
            "Customer 0{n} raised that our app tells travellers to call during disruptions while the corporate line is overloaded. They asked for a written plan before their tender in February.",
            "Customer 0{n}: travel manager said the booking experience is 'fine, nobody complains', but disruption is 'the reason we get calls from the CEO's office'.",
        ],
        "travel_agency": [
            "Agency {agency} escalation: group of {pax} travellers on the cancelled {city} flight. We could not rebook them through the agency portal and the airline desk line had a {wait}-minute wait.",
            "Agency {agency}: after the {city} delays our agents rebooked 31 passengers by phone, one at a time. The portal shows the disruption but has no rebooking action.",
            "Agency {agency} reports customers are choosing other airlines for {dest} after two summers of cancellations handled by phone only.",
            "Agency {agency}: the automatic rebooking moved a wedding party of {pax} onto a flight {days} days later. Fixing it took most of a working day.",
            "Agency {agency} asks for a disruption feed and the ability to rebook in the portal. Today they learn about cancellations from their own customers.",
            "Agency {agency}: corporate client threatened to move their account to us exclusively for another airline after travellers were stranded in {city}.",
            "Agency {agency} escalation: school group of {pax} stranded overnight in {city}, rebooking only possible through the call centre, which closed at 22:00.",
            "Agency {agency}: our out-of-hours team spent the night on hold to rebook travellers after the {city} cancellations. We will charge clients a disruption fee from next season.",
            "Agency {agency} notes that refunds after cancellations are fine, it's getting people onto a new flight quickly that fails.",
            "Agency {agency}: the portal let us see the new automatic flight but not change it. Every change after a disruption is a phone call for us too.",
            "Agency {agency}: tour operator partner is reconsidering AnyCompany Air for {dest} packages because disruption handling costs them staff time every week.",
        ],
    },
    "bag_tracking": {
        "reviews": [
            "Bag didn't arrive in {dest}. The app has no tracking, the desk gave me a paper form and a phone number that never answers.",
            "Five days and my suitcase is still 'being traced'. I have no idea where it is and no way to find out.",
            "My bag missed the connection in {city}. Fine, it happens. But I had to call three times to learn it was on the next flight.",
            "Delayed bag, and the online claim form timed out twice. Had to start again each time.",
            "Other airlines show you where your bag is. Here you get a reference number and silence.",
            "Arrived in {dest}, bag stayed in {city}. Took {days} days to get it back and nobody told me anything in between.",
            "Damaged suitcase and the claim process wants receipts I don't have for a bag I bought six years ago.",
            "The bag tag has a barcode, so somebody knows where it is. Why can't I?",
            "Lost bag on a family holiday, kids' clothes and medicines inside. No updates for three days.",
        ],
        "call_center": [
            "Customer: My bag didn't arrive in {dest}, I filed a report at the airport. Can you tell me where it is? Agent: It's showing as traced in {city}, it should be on tomorrow's flight. Customer: Can I see that somewhere myself?",
            "Customer: Third time calling about my suitcase. Agent: I'm sorry. It was delivered to the airport this morning and the courier will bring it today. Customer: Nobody told me.",
            "Customer: The claim form keeps timing out. Agent: I can take the details over the phone. Customer: It's 20 items, that'll take ages.",
            "Customer: My bag came back broken, the wheel is gone. Agent: I'll open a damage claim. Customer: Do I need to keep the bag? Agent: Yes, please keep it for inspection.",
            "Customer: Bag missed the connection in {city}. When will it get to my hotel? Agent: Within 48 hours. Customer: I fly home in 48 hours.",
            "Customer: The tracing reference you gave me doesn't work on the website. Agent: The site has been having issues, I'll check it here.",
            "Customer: I need my medication from my checked bag. Where is it? Agent: It's in {city}, I'll mark it urgent.",
            "Customer: My bag arrived but the bottle inside broke and ruined everything. Agent: I'll register the damage. Customer: How long does that take? Agent: Around {days} days.",
            "Customer: The courier left my bag outside the hotel and now it's gone again. Agent: I'll check with the courier company.",
            "Customer: Can you just tell me if my bag is on the plane before I take off? Agent: I can see it was loaded, yes. Customer: Why isn't that in the app?",
            "Customer: Delayed bag, I've bought clothes. How do I claim? Agent: Upload receipts through the claims page. Customer: The page says the reference is invalid.",
            "Customer: My golf bag didn't arrive in {dest}. Agent: Oversized items sometimes go on a later flight. It's showing in {city}.",
            "Customer: It's day {days} and my suitcase is still lost. Agent: It's still being traced. Customer: What does that actually mean?",
        ],
        "social": [
            "Day {days} without my bag. @AnyCompanyAir tracing reference leads to an error page.",
            "My bag is having a better holiday in {city} than I am in {dest}",
            "Every airline in 2026 has bag tracking except @AnyCompanyAir apparently",
            "Filed a lost bag report in {dest}, no update since. Do I just buy new everything?",
            "Bag finally arrived after {days} days. Nobody told me it was coming, the courier just turned up at 23:00",
            "Put an AirTag in my suitcase because the airline won't tell me where it is. It's in {city}. The airline says it's 'being traced'.",
            "Claim form for my damaged bag has crashed twice. Giving up.",
            "Missed connection, bag missing, no information. Great combo @AnyCompanyAir",
            "Waiting at the belt in {dest}, belt stopped, my bag never came. Desk had a queue of 40 people with the same problem.",
        ],
        "nps": [
            "My bag was lost for {days} days with no updates.",
            "Bag didn't arrive and the claim process is a mess.",
            "No way to track my delayed suitcase.",
            "Suitcase damaged and the claim is still open.",
            "Flight fine, bag missing, information zero.",
            "Had to call three times to find my luggage.",
            "Bag came {days} days late and nobody told me it was coming.",
            "The lost luggage desk was closed when we landed.",
        ],
        "account_manager": [
            "Customer 0{n} raised delayed bags for their equipment cases on the {city} route. Not a renewal issue, but they asked whether we offer tracking.",
            "Customer 0{n} ({industry}) mentioned two travellers who arrived without luggage for a client event. They asked how to escalate bag cases faster.",
        ],
        "travel_agency": [
            "Agency {agency}: tour group of {pax} with four delayed bags in {dest}. We cannot see bag status, so we pass calls to the airline.",
            "Agency {agency} asks whether bag tracing references can be shared with agents. Customers call us first.",
        ],
    },
    "booking_flow": {
        "reviews": [
            "Booking works but it takes too many steps. Every page tries to sell me insurance, a hotel and a car.",
            "The website looks a bit dated compared to other airlines. Gets the job done though.",
            "Search is slow when you change dates. Minor thing, but annoying.",
            "Would love to book multi-city in one go. Today I have to do two separate bookings.",
            "The seat selection step comes before you see the final price, which feels sneaky.",
            "The calendar view with prices is hard to read on a phone.",
            "Booking flow is OK. I wish it remembered my passport details.",
            "Took me 12 minutes to book a simple return because of all the upsell pages.",
            "Fine app for booking, nothing special. Could be simpler.",
            "Paying with my company card fails about half the time and I have to retry.",
            "The new design is prettier but the 'continue' button keeps moving around.",
            "I'd like to see the baggage rules before I choose a fare, not after.",
            "Booking for my elderly mother was confusing, too many options on one page.",
            "Couldn't apply my voucher during booking; it only works through the call centre.",
            "Booking on the website is fine, I'd just like Apple Pay.",
        ],
        "call_center": [
            "Customer: The payment page failed but I think you charged my card. Agent: I can see one booking and one failed attempt; the hold will be released in a few days.",
            "Customer: I can't find where to add my frequent flyer number in the booking. Agent: It's on the passenger details page, under the name. I'll add it for you.",
            "Customer: The website won't let me book for a child travelling alone. Agent: That needs to be booked by phone, I can do it now.",
            "Customer: I tried to book multi-city and it only lets me do return trips. Agent: Multi-city is only available by phone at the moment.",
            "Customer: The site keeps showing a higher price at the last step. Agent: That's the bag and seat you selected. I can remove them.",
            "Customer: My voucher code doesn't work online. Agent: Vouchers from cancellations can only be used here, I'll apply it.",
            "Customer: The booking page froze after payment. Did it go through? Agent: Yes, your booking is confirmed, I'll resend the email.",
        ],
        "social": [
            "Booking a flight on @AnyCompanyAir: 1 page for the flight, 6 pages of upsells",
            "Why does every airline website still look like 2012",
            "Payment failed twice, worked the third time. Classic.",
            "The booking site is fine but multi-city would be nice @AnyCompanyAir",
            "Upsell pages longer than the flight",
            "Booked in 4 minutes on the app, honestly painless",
        ],
        "nps": [
            "Booking took longer than it should with all the extras.",
            "Website feels old but works.",
            "Payment failed the first time.",
            "Too many upsell screens when booking.",
            "Booking was OK, could be simpler.",
            "Would like to book multi-city online.",
            "Booking page was confusing for adding bags.",
        ],
        "account_manager": [
            "Customer 0{n} asked about the roadmap for the booking flow. Nice to have, not a factor in the renewal.",
            "Customer 0{n} ({industry}) mentioned a competitor's booking flow looks more modern, but said their travellers book through the travel management company anyway.",
            "Leadership asked me to check with Customer 0{n} whether a booking redesign would help retention. Their answer: 'Booking is fine. Fix what happens when flights get cancelled.'",
            "Customer 0{n} would like the corporate fare to show automatically when travellers book directly. Low priority for them.",
            "Customer 0{n}'s travellers use our app to book about 20% of trips. The travel manager has no complaints about booking itself.",
            "Customer 0{n} asked whether we will support booking through their new travel platform. Integration question, not a booking design one.",
            "Customer 0{n} said the booking pages are slow on hotel Wi-Fi. Mentioned it in passing.",
            "Customer 0{n} ({industry}) asked for receipts to show the cost centre field automatically after booking.",
            "Pitched the idea of a redesigned booking flow to Customer 0{n}. They were polite, but their questions were all about disruptions.",
        ],
        "travel_agency": [
            "Agency {agency}: the agency portal booking is slow but it works. Not urgent.",
            "Agency {agency} would like group bookings above nine passengers in the portal. Today it's by email.",
            "Agency {agency} asks for fare rules to show before selecting a fare in the portal.",
            "Agency {agency}: portal times out on long sessions, agents lose half-finished bookings.",
            "Agency {agency} suggested a cleaner booking page for their less technical customers who book directly.",
            "Agency {agency}: commission statements don't match bookings made through the new web flow.",
            "Agency {agency} would like to save passenger profiles in the portal for repeat travellers.",
        ],
    },
    "cheaper_fares": {
        "reviews": [
            "Prices to {dest} have gone up a lot this year. Low-cost carriers are half the price.",
            "Decent airline but too expensive for what you get in economy.",
            "The fare looks cheap until you add a bag and a seat.",
            "Paid {price} euros for a short flight. Hard to justify.",
            "Prices jump the moment you search twice. Feels like they track you.",
            "Would fly more often if the fares were more reasonable.",
            "Good service, but the competition is cheaper on the {city} route.",
            "Family of four, the bags alone cost more than one ticket.",
            "Last-minute prices are absurd.",
        ],
        "call_center": [
            "Customer: The price went up between searching and booking. Can you give me the earlier fare? Agent: I'm afraid fares change with availability.",
            "Customer: Is there a cheaper fare to {dest} if I travel midweek? Agent: Tuesday and Wednesday are cheaper, I can show you.",
        ],
        "social": [
            "{price} euros to {dest} @AnyCompanyAir. For a two-hour flight. Seriously.",
            "Low-cost to {dest}: 49 euros. AnyCompany Air: {price}. Same airport.",
            "Bag fee more than the ticket. Every time.",
            "Why are fares on the {city} route so high this summer",
            "Love the airline, hate the prices",
            "Searched twice and the price went up 40 euros. Not booking.",
            "AnyCompany Air sale is the same price as everyone else's normal price",
            "Flew AnyCompany Air because the low-cost flight was cancelled. Paid {price} euros. At least it left on time.",
            "Fares to {dest} doubled since last year",
            "Can't afford to take the family on AnyCompany Air anymore",
            "Business class prices are wild",
        ],
        "nps": [
            "Too expensive compared to other airlines.",
            "Price is the only reason I'd go elsewhere.",
            "Good flight, high price.",
            "Bag fees are too high.",
            "Fares keep going up.",
            "I'd recommend it if it were cheaper.",
            "Expensive for short flights.",
            "Price went up while I was booking.",
            "Fine, but overpriced.",
        ],
        "account_manager": [
            "Customer 0{n} asked for a better corporate discount at renewal. Standard negotiation, they accepted the current terms.",
            "Customer 0{n} ({industry}) is benchmarking fares on the {city} route against a competitor as part of their tender.",
            "Customer 0{n}: price came up, but the travel manager said disruption costs them more than the fare difference.",
        ],
        "travel_agency": [
            "Agency {agency}: price-sensitive leisure customers are moving to low-cost carriers on short routes.",
            "Agency {agency} asks for more competitive group fares for school trips.",
        ],
    },
    "seat_map_3d": {
        "reviews": [
            "Would be cool to see a 3D view of the cabin when choosing a seat.",
            "Seat map is fine. A 3D view would be a nice touch like some other airlines have.",
            "Love the app. Only wish: a 3D seat preview so I can see the legroom.",
            "I'd like to see photos or a 3D view of the seat before paying extra for it.",
            "Seat selection works. It would be fun to see the view from the window seat in 3D.",
            "A 3D seat map would make choosing extra legroom seats easier to justify.",
        ],
        "social": [
            "@AnyCompanyAir please add a 3D seat map, it would be so cool",
            "Other airline's app has a 3D cabin view and honestly it's great. AnyCompany Air next?",
            "Not a complaint, but a 3D seat preview would be amazing",
            "Feature request: show me the actual seat in 3D before I pay 35 euros for it",
            "3D seat map when, @AnyCompanyAir",
            "Saw a 3D seat map demo at a conference, would love that in the AnyCompany Air app",
            "3D seat maps are the future. Just saying.",
        ],
        "nps": [
            "Great flight. A 3D seat map would make it perfect.",
            "All good. Would like a better seat preview.",
        ],
        "account_manager": [
            "Customer 0{n}'s travel manager saw a 3D seat map at a trade fair and asked if we plan one. Curiosity, not a requirement.",
            "Customer 0{n} asked about a 3D seat view for executives choosing business class seats. Mentioned once, not raised again.",
        ],
    },
    "loyalty_points": {
        "reviews": [
            "Points from my last three flights never appeared on my account.",
            "Hard to see how many points I need for the next status level.",
            "The loyalty section of the app is confusing. I never know what my points are worth.",
            "Booked through a partner and got no points. Nobody explains why.",
            "Status expired without any warning email.",
            "I can't use points for seats or bags, only flights. Feels limited.",
            "Took {days} days for my points to show up after the flight.",
        ],
        "call_center": [
            "Customer: My points from the {city} flight are missing. Agent: Partner flights can take up to six weeks. I'll add a claim.",
            "Customer: How many points do I need for silver? Agent: You need 1,800 more tier points. Customer: The app shows a different number.",
            "Customer: My status expired, I didn't get a warning. Agent: I can see it expired last month. I'll check if there's a grace period.",
            "Customer: Can I use my {points} points for a bag? Agent: Points can only be used for flights at the moment.",
            "Customer: I booked with my company and didn't get points. Agent: You need to add your number at booking; I'll add it retroactively.",
            "Customer: Points disappeared from my account. Agent: They expired after 36 months of inactivity. Customer: I fly every month.",
            "Customer: The app says I have {points} points, the website says less. Agent: The app may not have refreshed. The website is correct.",
            "Customer: I want to transfer points to my partner. Agent: Transfers are possible for a fee, I can do that now.",
            "Customer: Why did I earn so few points on this fare? Agent: Light fares earn 25%. Customer: That's not clear when booking.",
            "Customer: Can I buy status? Agent: No, but there's a fast-track challenge I can enrol you in.",
        ],
        "social": [
            "Points from 3 flights still missing @AnyCompanyAir",
            "Is there a single person who understands the AnyCompany Air loyalty programme",
            "Status expired with zero warning. Thanks for the loyalty.",
            "Loyalty app shows {points} points, website shows something else",
        ],
        "nps": [
            "Missing points again.",
            "Loyalty programme is confusing.",
            "Points take too long to appear.",
            "Status benefits aren't clear.",
            "I can't redeem points for anything useful.",
            "Lost my status without a warning.",
        ],
        "account_manager": [
            "Customer 0{n} asked whether travellers can earn points on corporate fares. They can, travellers just don't add their number.",
            "Customer 0{n} wants a report of points earned by their travellers. Not available today.",
        ],
        "travel_agency": [
            "Agency {agency}: customers complain points are missing when booked through the agency. The number isn't passed through the portal.",
            "Agency {agency} asks for a way to add loyalty numbers after booking in the portal.",
        ],
    },
    "on_time_positive": {
        "reviews": [
            "On time both ways, friendly crew, clean cabin. No complaints.",
            "Flight to {dest} left and arrived early. Smooth boarding.",
            "Best short-haul airline I've used this year when everything runs to plan.",
            "Check-in in the app was quick and the flight was on time.",
            "Comfortable seats, good coffee, on time. Will fly again.",
            "Crew handled a full flight brilliantly. Arrived ten minutes early.",
            "Easy app, mobile boarding pass worked first time, on time departure.",
            "Very professional crew, punctual, and the lounge in {city} was great.",
            "Third trip this year, all on time. Reliable airline.",
            "Lovely flight, the crew helped with my kids without being asked.",
            "Everything worked: app, bag drop, boarding, on time landing in {dest}.",
            "Quiet cabin, good legroom for economy, on schedule.",
            "No drama, no delays, that's all I want from an airline.",
            "Flew {city} to {dest} and back, both flights on time, bags first off the belt.",
            "Good value for the service when it all goes to plan.",
            "Clean plane, friendly staff, on time. Exactly what it says.",
            "Boarding was organised by groups and actually worked. On time.",
        ],
        "social": [
            "Shout out to the @AnyCompanyAir crew on the {time} to {dest}, absolute pros",
            "On time, coffee was good, landed early. Rare these days",
            "Smoothest airport experience I've had in ages flying @AnyCompanyAir out of {city}",
            "AnyCompany Air on time again. Five for five this year",
            "Mobile boarding pass, no queue, on time. Love it",
            "Window seat, on time, sunset over {dest}. Can't complain",
            "@AnyCompanyAir crew made my nervous flyer daughter feel so safe today",
            "Early arrival in {dest}! Never happens",
            "Honestly when AnyCompany Air runs on time it's my favourite airline",
            "Boarding in {city} took ten minutes flat. Impressive",
            "Easy flight, friendly crew, bags fast. Nice one @AnyCompanyAir",
        ],
        "nps": [
            "On time and friendly crew.",
            "Everything went smoothly.",
            "Punctual and comfortable.",
            "Easy check-in and on time.",
            "Great crew, early arrival.",
            "No problems at all.",
            "The app made boarding easy.",
            "Reliable as always.",
            "Clean plane and on time.",
            "Smooth trip from start to finish.",
            "Friendly service, no delays.",
            "Quick boarding, arrived early.",
            "The crew were excellent.",
            "Good flight, will book again.",
            "Comfortable and punctual.",
            "Hassle-free trip.",
            "Bags arrived fast and the flight was on time.",
            "Nice crew and good coffee.",
            "Very well organised boarding.",
            "Flight was exactly as expected, on time.",
            "Lounge was great and the flight was on time.",
            "Easy from booking to landing.",
            "Kind crew who helped with my mother's wheelchair.",
            "All on schedule, no stress.",
            "Smooth, simple, on time.",
            "On time, quiet cabin, good seat.",
            "Would recommend for business trips, always punctual.",
        ],
        "account_manager": [
            "Customer 0{n} ({industry}) is happy with punctuality on their main routes this year and with the lounge access.",
            "Customer 0{n}: travel manager praised the crew on the {city} route. No issues reported this quarter.",
            "Customer 0{n} renewal agreed. Network and on-time performance are why they stay.",
        ],
        "travel_agency": [
            "Agency {agency}: customers rate AnyCompany Air highly on punctuality on the {city} route.",
            "Agency {agency} notes very few complaints on flights that operate as planned.",
        ],
    },
    "other": {
        "reviews": [
            "Sandwich was dry and overpriced.",
            "Legroom is tight on the older planes.",
            "App crashed when I tried to download my boarding pass.",
            "Ok.",
            "Wi-Fi didn't work the whole flight.",
            "Cabin was too cold.",
            "The lounge in {city} was overcrowded.",
            "Fine.",
            "Couldn't add my special meal online.",
            "The check-in kiosk at {city} rejected my passport twice.",
            "Too many announcements on a night flight.",
            "Average airline.",
        ],
        "call_center": [
            "Customer: I need to correct a spelling mistake in my surname. Agent: I can do that, one letter is free of charge.",
            "Customer: I need wheelchair assistance at {city}. Agent: I've added it to your booking.",
            "Customer: Can I bring my dog in the cabin? Agent: Pets up to 8 kg in a carrier, I'll add it.",
            "Customer: I need an invoice with my company's tax number. Agent: I'll email it within 24 hours.",
            "Customer: Can I choose a seat next to my son? Agent: I've seated you together.",
            "Customer: I can't check in online, it says 'passport required'. Agent: I'll add the passport details now.",
            "Customer: Can I order a vegetarian meal? Agent: Yes, added to both flights.",
            "Customer: I'm pregnant, do I need a certificate? Agent: After 28 weeks, yes.",
            "Customer: I was charged twice for my seat. Agent: I can see the duplicate, I'll refund it.",
            "Customer: I want to bring a surfboard. Agent: That's sports equipment, I'll add it for a fee.",
            "Customer: My son is flying alone, what do I need? Agent: The unaccompanied minor service, I'll book it.",
            "Customer: Can I upgrade with money at the airport? Agent: Yes, if seats are available.",
            "Customer: I lost my boarding pass email. Agent: I'll resend it.",
            "Customer: Is there a lounge in {city}? Agent: Yes, after security near gate 12.",
            "Customer: I need to add infant to my booking. Agent: I can do that now.",
            "Customer: How early should I arrive at {city}? Agent: Two hours for international flights.",
            "Customer: My e-ticket shows the wrong date of birth. Agent: I'll correct it.",
            "Customer: Can I carry my insulin? Agent: Yes, with the prescription.",
            "Customer: I want to change the name on the ticket to my wife. Agent: Name changes aren't possible, but I can rebook with a change fee.",
            "Customer: The app won't log me in. Agent: I'll send you a password reset.",
            "Customer: Is my flight to {dest} operated by you or a partner? Agent: By a partner airline.",
            "Customer: Can I bring a stroller? Agent: Yes, free of charge, at the gate.",
            "Customer: I need a receipt for my extra bag. Agent: I'll send it.",
            "Customer: Can I pay with points and cash? Agent: Not at the moment.",
            "Customer: Is my visa valid for the transit in {city}? Agent: I can't advise on visas, please check with the embassy.",
            "Customer: I need to cancel my booking for medical reasons. Agent: I'll open a refund request; please send the certificate.",
            "Customer: Can I bring a musical instrument as cabin baggage? Agent: Small instruments yes; a cello needs its own seat.",
            "Customer: The airport parking we booked through your site isn't working. Agent: I'll give you the partner's number.",
            "Customer: Can I get a window seat? Agent: Done.",
            "Customer: My company needs a VAT invoice for last month. Agent: I'll send it to the address on file.",
            "Customer: The check-in reminder email had the wrong time. Agent: Let me check. The flight time is correct in your booking.",
            "Customer: Can I check in for my partner too? Agent: Yes, if you're on the same booking.",
            "Customer: Do you have a lost and found? I left my headphones on the plane. Agent: I'll open a report.",
            "Customer: Can I get a copy of my travel history for expenses? Agent: Yes, from the website, or I can email it.",
            "Customer: How do I complain about the crew's behaviour? Agent: I'm sorry, I'll log a formal complaint.",
        ],
        "social": [
            "Why is plane coffee always like this",
            "Window seat, wing view. Classic.",
            "Anyone know if AnyCompany Air has Wi-Fi on the {city} flights?",
            "That landing in {dest} was spicy",
            "Who chooses the music during boarding",
            "Middle seat again lol",
            "Kid kicked my seat for two hours, not the airline's fault I guess",
            "The new uniforms look sharp @AnyCompanyAir",
            "Lounge pancakes in {city} are elite",
            "Missed the flight because of security at {city}, my own fault",
            "Flying to {dest} for a wedding, wish me luck",
            "Turbulence over the Alps was something else",
        ],
        "nps": [
            "Food could be better.",
            "Legroom is tight.",
            "Wi-Fi didn't work.",
            "Average.",
            "Cabin was cold.",
            "The app logged me out.",
        ],
        "account_manager": [
            "Customer 0{n} asked for a single monthly invoice across all travellers. Finance request, passed to billing.",
        ],
        "travel_agency": [
            "Agency {agency} asks for updated commission terms for next year.",
            "Agency {agency}: request for brochure material for the winter season.",
            "Agency {agency} asks whether infants can be added in the portal.",
            "Agency {agency}: login to the portal fails for new staff accounts.",
            "Agency {agency} requests training for two new agents on the portal.",
            "Agency {agency} asks for the new baggage policy in writing.",
            "Agency {agency}: invoice format changed and our accounting software rejects it.",
        ],
    },
}

SEGMENT_WEIGHTS = {
    "disruption_rebooking": {"leisure": 4, "frequent_flyer": 3, "corporate": 3},
    "bag_tracking": {"leisure": 6, "frequent_flyer": 3, "corporate": 1},
    "booking_flow": {"leisure": 6, "frequent_flyer": 3, "corporate": 1},
    "cheaper_fares": {"leisure": 8, "frequent_flyer": 1, "corporate": 1},
    "seat_map_3d": {"leisure": 5, "frequent_flyer": 5, "corporate": 0},
    "loyalty_points": {"leisure": 1, "frequent_flyer": 8, "corporate": 1},
    "on_time_positive": {"leisure": 5, "frequent_flyer": 3, "corporate": 2},
    "other": {"leisure": 6, "frequent_flyer": 2, "corporate": 2},
}

# Disruption peaks in July and August.
MONTH_WEIGHTS = {
    "disruption_rebooking": [1, 2, 4, 4, 2, 1],
    "default": [2, 2, 2, 2, 2, 1],
}


def pick_date(rng: random.Random, theme: str) -> str:
    weights = MONTH_WEIGHTS.get(theme, MONTH_WEIGHTS["default"])
    month = rng.choices(range(6), weights=weights)[0]
    first = date(2026, 5 + month, 1)
    last = END if month == 5 else (date(2026, 6 + month, 1) - timedelta(days=1))
    return (first + timedelta(days=rng.randint(0, (last - first).days))).isoformat()


def pick_segment(rng: random.Random, theme: str, channel: str) -> str:
    if channel == "account_manager":
        return "corporate"
    w = SEGMENT_WEIGHTS[theme]
    return rng.choices(list(w), weights=list(w.values()))[0]


def rating(rng: random.Random, theme: str) -> int:
    ranges = {"disruption_rebooking": (1, 2), "bag_tracking": (1, 3), "booking_flow": (2, 4), "cheaper_fares": (2, 4),
              "seat_map_3d": (4, 5), "loyalty_points": (2, 3), "on_time_positive": (4, 5), "other": (1, 5)}
    return rng.randint(*ranges[theme])


def nps_score(rng: random.Random, theme: str) -> int:
    ranges = {"disruption_rebooking": (0, 4), "bag_tracking": (2, 6), "booking_flow": (5, 8), "cheaper_fares": (4, 8),
              "seat_map_3d": (8, 10), "loyalty_points": (4, 8), "on_time_positive": (9, 10), "other": (6, 9)}
    return rng.randint(*ranges[theme])


def flight_outcome(rng: random.Random, theme: str) -> str:
    if theme == "disruption_rebooking":
        return rng.choices(["delayed", "cancelled"], weights=[11, 9])[0]
    if theme == "on_time_positive":
        return "on_time"
    if theme == "bag_tracking":
        return rng.choices(["on_time", "delayed"], weights=[3, 1])[0]
    return rng.choices(["on_time", "delayed"], weights=[9, 1])[0]


REASON_KEYWORDS = {
    "disruption_rebooking": [("refund", "Refund request"), ("hotel|voucher", "Hotel and meal voucher"),
                             ("connection|connect", "Missed connection"), ("cancel", "Cancellation"),
                             ("delay|late", "Schedule change")],
    "bag_tracking": [("broke|damage|wheel|bottle", "Damaged baggage"), ("claim|form|receipt|reference", "Baggage claim status")],
    "booking_flow": [("payment|charged|froze|price", "Payment failed")],
    "loyalty_points": [("status|silver", "Status query")],
    "other": [("spelling|surname|date of birth|name on the ticket", "Name correction"),
              ("wheelchair|assistance|pregnant|insulin|alone|infant|stroller", "Special assistance"),
              ("dog", "Pet travel"), ("invoice|receipt|vat|travel history", "Invoice request"),
              ("charged twice", "Duplicate charge"), ("seat|window|upgrade", "Seat request"),
              ("check in|passport|boarding pass|log me in|reminder", "Check-in problem"),
              ("meal|vegetarian", "Special meal")],
}
REASON_DEFAULT = {"disruption_rebooking": "Rebooking", "bag_tracking": "Delayed baggage",
                  "booking_flow": "Website booking problem", "cheaper_fares": "Fare query",
                  "loyalty_points": "Missing points", "other": "General enquiry"}


def contact_reason(theme: str, text: str) -> str:
    customer = text.split("Agent:")[0].lower()
    for pattern, reason in REASON_KEYWORDS.get(theme, []):
        if any(word in customer for word in pattern.split("|")):
            return reason
    return REASON_DEFAULT[theme]


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def qualitative(rng: random.Random) -> tuple[dict[str, list[dict]], Counter]:
    seen: set[str] = set()
    files: dict[str, list[dict]] = {c: [] for c in PLAN}
    tally: Counter = Counter()
    for channel, themes in PLAN.items():
        for theme, count in themes.items():
            bank = BANK[theme].get(channel, [])
            if count and not bank:
                raise ValueError(f"no phrasings for {theme} on {channel}")
            order = list(range(len(bank)))
            rng.shuffle(order)
            for i in range(count):
                for attempt in range(400):
                    idx = order[i % len(order)] if attempt == 0 else rng.randrange(len(bank))
                    text = bank[idx].format(**slots(rng))
                    if text not in seen:
                        break
                else:
                    raise ValueError(f"could not find a unique text for {theme} on {channel}")
                seen.add(text)
                row: dict[str, object] = {"date": pick_date(rng, theme), "channel": channel,
                       "segment": pick_segment(rng, theme, channel), "text": text, "_theme": theme}
                if channel == "reviews":
                    row["channel"] = rng.choice(["app_store", "google_play", "web_review"])
                    row["rating"] = rating(rng, theme)
                elif channel == "call_center":
                    row["contact_reason"] = contact_reason(theme, text)
                    row["handle_time_min"] = rng.randint(18, 55) if theme == "disruption_rebooking" else rng.randint(4, 24)
                elif channel == "nps":
                    row["flight_outcome"] = flight_outcome(rng, theme)
                    row["score"] = nps_score(rng, theme)
                elif channel == "account_manager":
                    row["account_tier"] = rng.choice(["gold", "silver", "silver", "bronze"])
                files[channel].append(row)
                tally[(channel, theme)] += 1
    for rows in files.values():
        rows.sort(key=lambda r: (r["date"], r["text"]))
    return files, tally


def ids(rows: list[dict], prefix: str) -> None:
    for i, r in enumerate(rows, 1):
        r["id"] = f"{prefix}-{i:04d}"


def quantitative(rng: random.Random) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    ops, funnel = [], []
    for m in MONTHS:
        days = 15 if m == "2026-10" else 30
        flights = int(rng.randint(285, 315) * days)
        peak = m in ("2026-07", "2026-08")
        delayed = int(flights * rng.uniform(0.050, 0.062) if peak else flights * rng.uniform(0.028, 0.036))
        cancelled = int(flights * rng.uniform(0.013, 0.017) if peak else flights * rng.uniform(0.006, 0.009))
        disrupted = (delayed + cancelled) * rng.randint(118, 132)
        rate = rng.uniform(0.106, 0.128)
        self_service = int(disrupted * rate)
        calls = int(disrupted * rng.uniform(0.39, 0.43))
        ops.append({"month": m, "flights_operated": flights, "flights_delayed_over_2h": delayed,
                    "flights_cancelled": cancelled, "disrupted_passengers": disrupted,
                    "rebooked_self_service": self_service,
                    "self_service_rebooking_rate": f"{self_service / disrupted:.3f}",
                    "rebooking_calls": calls, "calls_per_1000_disrupted": round(calls / disrupted * 1000)})
        sessions = int(rng.uniform(1.9e6, 2.2e6) * days / 30)
        searches = int(sessions * rng.uniform(0.58, 0.61))
        bookings = int(sessions * rng.uniform(0.0305, 0.0318))
        funnel.append({"month": m, "sessions": sessions, "searches": searches, "bookings": bookings,
                       "conversion_rate": f"{bookings / sessions:.4f}",
                       "industry_benchmark": "0.0300"})
    nps_rows = []
    targets = {"on_time": (0.58, 0.28), "delayed": (0.20, 0.38), "cancelled": (0.10, 0.25)}
    for m in MONTHS:
        for outcome, (prom, pas) in targets.items():
            n = {"on_time": rng.randint(5200, 6100), "delayed": rng.randint(700, 1400), "cancelled": rng.randint(160, 420)}[outcome]
            p = int(n * (prom + rng.uniform(-0.02, 0.02)))
            pa = int(n * (pas + rng.uniform(-0.02, 0.02)))
            d = n - p - pa
            nps_rows.append({"month": m, "flight_outcome": outcome, "responses": n, "promoters": p,
                             "passives": pa, "detractors": d, "nps": round((p - d) / n * 100)})
    channel_rows = []
    for channel, (n, prom, det) in {"self_service_app": (410, 0.34, 0.30), "self_service_web": (260, 0.31, 0.33),
                                     "call_center": (1630, 0.10, 0.68), "airport_desk": (980, 0.09, 0.71)}.items():
        p, d = int(n * prom), int(n * det)
        channel_rows.append({"rebooking_channel": channel, "responses": n, "promoters": p,
                             "passives": n - p - d, "detractors": d, "nps": round((p - d) / n * 100)})
    return ops, nps_rows, channel_rows, funnel



# Telemetry: what the systems record, aggregated by day and journey step, as a team would export it
# from RUM, traces, and logs. Its own seed, so the files above stay byte-identical.
TELEMETRY_SEED = SEED + 7
JOURNEY_MAP = [
    # journey, step, order, source, rum_view, backend_route, description
    ("disruption_rebooking", "alert_opened", 1, "rum", "push:disruption-alert", "", "Opens the disruption alert in the app or the email link on the web"),
    ("disruption_rebooking", "trip_viewed", 2, "rum+trace", "/trips/{id}", "GET /trips/{id}", "Sees the disrupted trip"),
    ("disruption_rebooking", "alternatives_viewed", 3, "rum+trace", "/trips/{id}/alternatives", "GET /trips/{id}/alternatives", "Sees the other flights, without a way to choose one"),
    ("disruption_rebooking", "suggestion_kept", 4, "rum+trace", "/trips/{id}/keep", "POST /trips/{id}/keep-suggestion", "Keeps the flight the airline chose: today's only self-service action"),
    ("disruption_rebooking", "contact_us_tapped", 4, "rum", "/help/contact", "", "Taps Contact us; the call that follows is not in the app's telemetry"),
    ("booking", "search", 1, "rum+trace", "/search", "GET /search", "Searches for flights"),
    ("booking", "results", 2, "rum+trace", "/results", "GET /offers", "Sees the results"),
    ("booking", "fare_selected", 3, "rum", "/fares", "", "Chooses a fare"),
    ("booking", "extras", 4, "rum+trace", "/extras", "GET /ancillaries", "Sees seats, bags, and other extras"),
    ("booking", "payment", 5, "rum+trace", "/payment", "POST /payments", "Pays"),
    ("booking", "confirmed", 6, "rum", "/confirmation", "", "Sees the booking confirmation"),
]


def days_in(month: str) -> list[date]:
    first = date(int(month[:4]), int(month[5:]), 1)
    out, d = [], first
    while d.month == first.month and d <= END:
        out.append(d)
        d += timedelta(days=1)
    return out


def split(total: int, days: list[date], rng: random.Random, weekend: float = 1.0) -> list[int]:
    weights = [rng.uniform(0.75, 1.25) * (weekend if d.weekday() >= 4 else 1.0) for d in days]
    scale = total / sum(weights)
    return [max(0, int(w * scale)) for w in weights]


def telemetry(ops: list[dict], funnel: list[dict]) -> dict:
    rng = random.Random(TELEMETRY_SEED)
    out = OUT / "telemetry"
    out.mkdir(parents=True, exist_ok=True)
    rum, spans, stats = [], [], Counter()
    for op, fn in zip(ops, funnel):
        m = op["month"]
        days = days_in(m)
        peak = m in ("2026-07", "2026-08")
        disrupted = split(op["disrupted_passengers"], days, rng)
        kept = split(op["rebooked_self_service"], days, rng)
        calls = split(op["rebooking_calls"], days, rng)
        web_sessions = split(fn["sessions"], days, rng, weekend=1.12)
        bookings = split(fn["bookings"], days, rng, weekend=1.12)
        busiest = set(sorted(range(len(days)), key=lambda i: -web_sessions[i])[:6]) if m == "2026-08" else set()
        for i, d in enumerate(days):
            day = d.isoformat()
            # Disruption rebooking journey: most people look, few can act, most of those who look tap Contact us.
            for channel, share in (("app", 0.74), ("web", 0.26)):
                opened = int(disrupted[i] * rng.uniform(0.70, 0.74) * share)
                trip = int(opened * rng.uniform(0.86, 0.90))
                alts = int(opened * rng.uniform(0.58, 0.62))
                keep = int(kept[i] * share)
                contact = int(alts * rng.uniform(0.66, 0.70))
                for step, n, secs in (("alert_opened", opened, rng.randint(4, 7)), ("trip_viewed", trip, rng.randint(18, 26)),
                                      ("alternatives_viewed", alts, rng.randint(70, 95)), ("suggestion_kept", keep, rng.randint(30, 45)),
                                      ("contact_us_tapped", contact, rng.randint(5, 9))):
                    rum.append({"date": day, "journey": "disruption_rebooking", "step": step, "channel": channel,
                                "sessions": n, "median_seconds_on_step": secs})
                stats["alerts_opened"] += opened
                stats["alternatives_viewed"] += alts
                stats["contact_us"] += contact
            # Booking journey, web: healthy, with a small dip at payment on the August peak days.
            s = web_sessions[i]
            search = int(s * rng.uniform(0.585, 0.605))
            results = int(search * rng.uniform(0.91, 0.93))
            fare = int(results * rng.uniform(0.105, 0.115))
            extras = int(fare * rng.uniform(0.84, 0.86))
            payment = int(extras * rng.uniform(0.71, 0.73))
            confirmed = min(bookings[i], payment)
            if i in busiest:
                confirmed = int(confirmed * rng.uniform(0.975, 0.985))
            for step, n, secs in (("search", search, rng.randint(9, 14)), ("results", results, rng.randint(25, 40)),
                                  ("fare_selected", fare, rng.randint(15, 25)), ("extras", extras, rng.randint(55, 80)),
                                  ("payment", payment, rng.randint(40, 60) + (25 if i in busiest else 0)), ("confirmed", confirmed, rng.randint(6, 10))):
                rum.append({"date": day, "journey": "booking", "step": step, "channel": "web", "sessions": n,
                            "median_seconds_on_step": secs})
            # Spans and metrics per service: requests, errors, and latency.
            alerts = int(disrupted[i] * rng.uniform(0.94, 0.97))
            delay_p50 = rng.randint(480, 600) if peak else rng.randint(120, 180)
            delay_p95 = rng.randint(2280, 2640) if peak else rng.randint(540, 720)
            pay_p95 = rng.randint(4200, 5200) if i in busiest else rng.randint(780, 980)
            pay_err = rng.uniform(0.015, 0.021) if i in busiest else rng.uniform(0.0015, 0.003)
            reissue = int(calls[i] * rng.uniform(0.85, 0.92))
            reissue_err = rng.uniform(0.052, 0.061) if peak else rng.uniform(0.040, 0.048)
            trips_total = sum(r["sessions"] for r in rum[-16:] if r["step"] == "trip_viewed")
            alts_total = sum(r["sessions"] for r in rum[-16:] if r["step"] == "alternatives_viewed")
            keep_total = sum(r["sessions"] for r in rum[-16:] if r["step"] == "suggestion_kept")
            for svc, span, route, n, err, p50, p95 in (
                ("notifications", "disruption.alert.send", "", alerts, rng.uniform(0.001, 0.003), rng.randint(180, 260), rng.randint(600, 900)),
                ("notifications", "disruption.alert.delay_from_event", "", alerts, 0.0, delay_p50 * 1000, delay_p95 * 1000),
                ("trips-api", "GET /trips/{id}", "/trips/{id}", int(trips_total * 1.3), rng.uniform(0.0005, 0.0012), rng.randint(60, 90), rng.randint(240, 320)),
                ("trips-api", "GET /trips/{id}/alternatives", "/trips/{id}/alternatives", int(alts_total * 1.2), 0.0, rng.randint(110, 150), rng.randint(380, 470)),
                ("trips-api", "POST /trips/{id}/keep-suggestion", "/trips/{id}/keep-suggestion", keep_total, rng.uniform(0.002, 0.004), rng.randint(300, 400), rng.randint(900, 1200)),
                ("booking-api", "GET /offers", "/offers", int(results * 1.6), rng.uniform(0.001, 0.002), rng.randint(250, 330), rng.randint(900, 1150)),
                ("payments-api", "POST /payments", "/payments", int(payment * 1.05), pay_err, rng.randint(320, 420), pay_p95),
                ("reissue-service", "POST /tickets/reissue", "/tickets/reissue", reissue, reissue_err, rng.randint(800, 1100), rng.randint(2300, 2900)),
            ):
                spans.append({"date": day, "service_name": svc, "span_name": span, "http_route": route, "requests": n,
                              "errors": int(n * err), "p50_ms": p50, "p95_ms": p95})
                if svc == "reissue-service":
                    stats["reissue"] += n
                    stats["reissue_errors"] += int(n * err)
                if svc == "payments-api" and i in busiest:
                    stats["payment_peak_errors"] += int(n * err)
    errors = []
    for svc, code, msg, share, first, last in (
        ("reissue-service", "FARE_RULE_MISMATCH", "Reissue rejected: the new flight's fare rules do not match the original ticket", 0.62, "2026-05-01", "2026-10-15"),
        ("reissue-service", "TICKET_LOCKED", "Reissue rejected: the ticket is locked by another change in progress", 0.17, "2026-05-02", "2026-10-15"),
        ("reissue-service", "EMD_NOT_REASSOCIATED", "Extras on the original ticket (seat, bag) were not moved to the new ticket", 0.13, "2026-05-03", "2026-10-14"),
        ("reissue-service", "TIMEOUT_GDS", "Timed out waiting for the reservations system", 0.08, "2026-05-06", "2026-10-13"),
    ):
        errors.append({"service_name": svc, "error_code": code, "message": msg, "count": int(stats["reissue_errors"] * share),
                       "first_seen": first, "last_seen": last})
    for svc, code, msg, count, first, last in (
        ("payments-api", "GATEWAY_TIMEOUT", "Payment gateway did not answer within 4 seconds", int(stats["payment_peak_errors"] * 0.8), "2026-08-01", "2026-08-30"),
        ("payments-api", "3DS_CHALLENGE_TIMEOUT", "Card authentication challenge expired", int(stats["payment_peak_errors"] * 0.2) + 410, "2026-05-01", "2026-10-15"),
        ("notifications", "PROVIDER_THROTTLED", "Push and SMS provider throttled the send rate; messages queued", 0, "2026-07-01", "2026-08-31"),
        ("notifications", "DEVICE_TOKEN_EXPIRED", "Push token no longer valid; email sent instead", 0, "2026-05-01", "2026-10-15"),
        ("trips-api", "UPSTREAM_SLOW", "Reservations lookup slower than 2 seconds", 0, "2026-05-04", "2026-10-15"),
    ):
        errors.append({"service_name": svc, "error_code": code, "message": msg, "count": count or rng.randint(900, 4200),
                       "first_seen": first, "last_seen": last})
    write_csv(out / "journey-map.csv", ["journey", "step", "order", "source", "rum_view", "backend_route", "description"],
              [dict(zip(["journey", "step", "order", "source", "rum_view", "backend_route", "description"], row)) for row in JOURNEY_MAP])
    write_csv(out / "rum-journeys-daily.csv", list(rum[0]), rum)
    write_csv(out / "spans-daily.csv", list(spans[0]), spans)
    write_csv(out / "errors-top.csv", list(errors[0]), errors)
    stats["rum_rows"], stats["span_rows"] = len(rum), len(spans)
    return stats

def main() -> None:
    rng = random.Random(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    files, tally = qualitative(rng)
    layout = {
        "reviews": ("app-and-web-reviews.csv", "REV", ["id", "date", "channel", "segment", "rating", "text"]),
        "call_center": ("call-center-contacts.csv", "CALL", ["id", "date", "channel", "segment", "contact_reason", "handle_time_min", "text"]),
        "social": ("social-posts.csv", "SOC", ["id", "date", "channel", "segment", "text"]),
        "nps": ("nps-verbatims.csv", "NPS", ["id", "date", "channel", "segment", "flight_outcome", "score", "text"]),
        "account_manager": ("corporate-account-notes.csv", "ACC", ["id", "date", "channel", "segment", "account_tier", "text"]),
        "travel_agency": ("travel-agency-escalations.csv", "AGY", ["id", "date", "channel", "segment", "text"]),
    }
    for channel, (name, prefix, fields) in layout.items():
        rows = files[channel]
        ids(rows, prefix)
        write_csv(OUT / name, fields, [{k: r.get(k, "") for k in fields} for r in rows])
    ops, nps_rows, channel_rows, funnel = quantitative(rng)
    write_csv(OUT / "operations-monthly.csv", list(ops[0]), ops)
    write_csv(OUT / "nps-by-flight-outcome.csv", list(nps_rows[0]), nps_rows)
    write_csv(OUT / "disruption-nps-by-rebooking-channel.csv", list(channel_rows[0]), channel_rows)
    write_csv(OUT / "web-booking-funnel-monthly.csv", list(funnel[0]), funnel)
    tel = telemetry(ops, funnel)

    total = sum(len(v) for v in files.values())
    print(f"Wrote {total} qualitative records to {OUT.relative_to(ROOT)}")
    for channel, (name, _, _) in layout.items():
        print(f"  {name}: {len(files[channel])}")
    print("By theme:")
    for theme in THEMES:
        per = ", ".join(f"{c} {tally[(c, theme)]}" for c in PLAN if tally[(c, theme)])
        print(f"  {theme}: {sum(tally[(c, theme)] for c in PLAN)} ({per})")
    disrupted = sum(r["disrupted_passengers"] for r in ops)
    selfs = sum(r["rebooked_self_service"] for r in ops)
    calls = sum(r["rebooking_calls"] for r in ops)
    print(f"Operations: {disrupted} disrupted passengers, self-service rate {selfs / disrupted:.3f}, "
          f"{round(calls / disrupted * 1000)} calls per 1,000 disrupted")
    print(f"Telemetry: {tel['rum_rows']} RUM rows, {tel['span_rows']} span rows; "
          f"{tel['alternatives_viewed'] / tel['alerts_opened']:.0%} of opened alerts reach the alternatives, "
          f"{tel['contact_us'] / tel['alternatives_viewed']:.0%} of those tap Contact us, "
          f"{tel['contact_us'] / calls:.0%} of rebooking calls; reissue errors {tel['reissue_errors'] / tel['reissue']:.1%}")
    for outcome in ("on_time", "delayed", "cancelled"):
        rows = [r for r in nps_rows if r["flight_outcome"] == outcome]
        n = sum(r["responses"] for r in rows)
        print(f"NPS {outcome}: {round((sum(r['promoters'] for r in rows) - sum(r['detractors'] for r in rows)) / n * 100)} ({n} responses)")
    for r in channel_rows:
        print(f"Disrupted NPS via {r['rebooking_channel']}: {r['nps']} ({r['responses']} responses)")
    conv = sum(r["bookings"] for r in funnel) / sum(r["sessions"] for r in funnel)
    print(f"Web booking conversion: {conv:.4f} (benchmark 0.0300)")


if __name__ == "__main__":
    main()
