# Pickleball Court Reserver Bot

## Overview
The **Pickleball Court Reserver Bot** is a Python automation tool that helps players secure pickleball court reservations as soon as they open. Many facilities release slots at fixed times, and they fill up within minutes (or seconds). This bot reduces the stress of manual booking by handling login, navigating to reservation pages, and attempting to book available slots automatically.

---

## Problem Statement
Pickleball courts are in high demand, and reservations often open at a set time each day. Players who can’t log in exactly at release time frequently miss out. This creates a frustrating experience for casual and competitive players alike.  

---

## Solution
This bot automates the reservation process ethically:  

- Automates login and navigates to the court reservation page.  
- Selects desired time slots within allowed limits.  
- Retries bookings if the system is temporarily unavailable.  
- Handles errors gracefully.  

**Note:** This bot is designed strictly for **personal use and testing**, following facility rules. It is not meant for abuse or unfair exploitation.

---

## Features
- **Automated login** with credential handling.  
- **Court slot selection** with configurable times.  
- **Retry logic** for failed attempts or busy servers.  
- **Error handling** for missing UI elements or network issues.  
- Designed for **end-to-end testing** of the reservation workflow.  

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/zabu24/pickleball_court_reserver_bot.git
cd pickleball_court_reserver_bot
