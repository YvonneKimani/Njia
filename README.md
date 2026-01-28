# Njia 🚍
Bridging the Transit Information Gap

Njia (Swahili for “The Way”) is a USSD-powered navigation and safety engine designed to empower commuters in Nairobi. It provides real-time access to boarding stages, dynamic fare estimates, and safety resources without requiring a smartphone or an internet connection.

## The Problem
Nairobi’s public transport (Matatu) ecosystem is dynamic but fragmented. Commuters face three core challenges:
- Information asymmetry due to fluctuating fares
- Navigation complexity when identifying correct boarding stages and Saccos
- The digital divide created by smartphone- and data-dependent solutions

## The Solution
Njia digitizes the last mile of public transport access using USSD and SMS. By leveraging Africa’s Talking APIs, Njia works on any GSM phone, ensuring accessibility and inclusivity.

## Core Features
- Dynamic route discovery with boarding stage, route number, and Sacco details
- Three-tiered fare intelligence (live, scheduled, and community-driven)
- Crowdsourced fare reporting
- Safety and emergency access including police and Sacco hotlines
- SMS summaries for session continuity

## Technical Stack
- Backend: Python / Django 5.0
- Database: SQLite
- Communication: Africa’s Talking (USSD & SMS)
- Logic: Custom time-slot engine synchronized with East Africa Time

## Installation & Setup
Clone the repository, set up a virtual environment, install dependencies, run migrations, seed Nairobi data, configure Africa’s Talking credentials, and expose the server using Ngrok for USSD callbacks.

## Vision
Njia aims to become the digital backbone of informal transport systems—starting in Nairobi and scaling across African cities—bringing transparency, safety, and accessibility to millions of commuters.

## Monetisation
First, Transactional Service Fees (Lost & Found).
Reporting a lost item is free. If the user wants recovery and dispatch, we charge a small convenience fee (about KES 50–200). People are willing to pay because it’s a small fraction of the value of items like phones or laptops. We take a commission (around 20%) and the rest goes to the Sacco or driver as an incentive for honesty.

Second, Sacco Insights Dashboard (B2B SaaS).
Saccos pay a monthly subscription to access a premium admin portal. They receive safety and harassment reports, fare compliance data to detect overcharging, and performance benchmarks compared to other Saccos. This gives them visibility and accountability they currently lack.

Third, Hyper-Local USSD Advertising.
After showing fare or route information, we include a short text ad in the USSD menu. The ads are contextual because we know the user’s destination, allowing nearby businesses to advertise directly to commuters heading to that stage.