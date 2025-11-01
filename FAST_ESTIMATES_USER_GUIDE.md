# Eagle Eye Fast Estimates: Complete User Journey

**Document**: Quick Reference Guide  
**Audience**: Construction Firms Transitioning from Excel  
**Time to Estimate**: 5-10 minutes from upload

---

## THE SIMPLE STORY

### Before Eagle Eye (Typical Firm)
```
Construction firm receives plan PDF
        ↓
Estimator manually reviews (3-4 hours)
        ↓
Hand-enters component data into Excel (2-3 hours)
        ↓
Manually checks against code standards (4-5 hours)
        ↓
Looks up pricing in spreadsheets (1-2 hours)
        ↓
Hand-writes proposal in Word/PDF (2-3 hours)
        ↓
TOTAL: 10-14 HOURS per project
```

### After Eagle Eye (New Workflow)
```
Construction firm uploads:
  • PDF construction plans
  • Excel input template (optional, AI fills it in)
  • Engineering drawings (optional)
        ↓
Eagle Eye AI analyzes everything automatically
        ↓
User receives email with results (5-10 MINUTES)
  • Updated Excel (findings + estimate populated)
  • Professional PDF proposal (ready to send)
  • Xactimate CSV (ready for GC)
  • Compliance report (detailed findings)
        ↓
TOTAL: 5-10 MINUTES per project
        ↓
TIME SAVED: 10-14 hours → 5-10 minutes = 60X FASTER
```

---

## STEP-BY-STEP USER GUIDE

### Step 1: Download Template (1 minute)

```
User goes to: https://app.eagleeye.ai/templates

Downloads: eagle_eye_input_template.xlsx

This is a simple Excel file with 5 sheets:
  1. PROJECT_INFO - Basic project details
  2. COMPONENTS_SCHEDULE - What needs to be estimated
  3. REGIONAL_FACTORS - Auto-populated by ZIP code
  4. FINDINGS_OUTPUT - (Empty now, AI will fill)
  5. ESTIMATE_OUTPUT - (Empty now, AI will fill)
```

### Step 2: Fill Project Info (2 minutes)

User opens Excel and fills in basic info:

```excel
PROJECT_INFO Sheet

Project Name              → "Smith Residence Addition"
Client Name              → "John Smith"
Client Email             → "john@smith.com"
Property Address         → "123 Oak Street"
City, State, ZIP         → "Madison, GA 30601"
Jurisdiction             → "Georgia"
Building Year            → "2025"
Scope Summary            → "800 SF addition + new HVAC"
Budget (optional)        → "$50,000"
Special Conditions       → "Flood prone area, slope"
Notes                    → "Existing home built 1995"
```

Optional: User can fill in components they KNOW:

```excel
COMPONENTS_SCHEDULE Sheet

Component Type    | Qty | Unit | Size      | Location   | Notes
─────────────────────────────────────────────────────────────────
Windows           | 12  | Each | 3'x5'     | Exterior   | NEW
Exterior Doors    | 2   | Each | 3'x6'8"   | Front/Back | NEW
HVAC Unit         | 1   | Each | 2.5 Ton   | Attic      | REPLACE
(Leave rest blank - AI will fill from PDF)
```

### Step 3: Upload Everything (2 minutes)

```
User navigates to: https://app.eagleeye.ai/new-analysis

Uploads:
  • Drag Excel file here ✓
  • Drag PDF plans here ✓
  • Drag engineering drawings here (optional)
  • Drag site photos here (optional)

Clicks: "START ANALYSIS"
```

### Step 4: Watch Progress (5-10 minutes)

User sees real-time progress updates:

```
🔄 Analyzing Your Project
[████████░░░░░░░░░░] 50%

Stage 1: Extracting from PDFs (COMPLETE)
  ✓ Downloaded 3 PDF files
  ✓ Converted to images (48 pages)
  ✓ Found component schedule
  ✓ Recognized components:
    - 12 windows
    - 2 doors
    - 1 HVAC unit
    - 4,200 SF drywall
    - Roofing 2,400 SF

Stage 2: Checking Compliance (IN PROGRESS)
  🔄 Running IRC 2018 rules...
  🔄 Running IECC 2015 rules...
  🔄 Running NEC 2017 rules...
  🔄 Checking Georgia amendments...

  Findings so far: 3 issues found
    1 RED (critical)
    1 ORANGE (important)
    1 YELLOW (nice-to-know)

Estimated time remaining: 2 minutes...
```

### Step 5: Get Results (Download)

User receives email:

```
Subject: ✅ Your Eagle Eye Analysis is Ready!

Hi John,

Your analysis is complete in just 8 minutes!

📊 QUICK SUMMARY
Project: Smith Residence Addition
Address: 123 Oak Street, Madison, GA 30601
Components Found: 8 major items
Code Issues: 3 findings
Estimated Cost: $45,226

🎁 YOUR DOWNLOADS (Click to download)

1. 📄 Updated_Excel.xlsx
   → All findings and costs now populated
   → Ready to share with team

2. 📋 Proposal_SmithResidence_Nov2025.pdf
   → Professional format
   → Ready to send to client

3. 📊 Xactimate_Export.csv
   → Ready for your GC/contractor
   → Import directly into estimating software

4. 📑 Compliance_Report_Detailed.pdf
   → All code references with locations
   → Insurance/lender documentation

🚨 CODE ISSUES

RED (Must fix):
  • Truss design missing documentation
    Location: Sheet A2.1, Detail 4
    Fix: Obtain from manufacturer

ORANGE (Should fix):
  • Air sealing inadequate
    Location: Exterior walls
    Fix: Add caulk/sealant

YELLOW (Optional):
  • GFCI receptacles needed
    Location: Kitchen/bathroom
    Fix: Upgrade outlets
```

### Step 6: Share Results (2 minutes)

```
User opens PDF proposal

Sees professional document:
  • Client name & address
  • Project scope
  • Component list
  • Code compliance summary (with citations)
  • Cost breakdown
  • Code issues & recommendations
  • Payment schedule
  • Professional signatures/terms

User can:
  ✓ Send directly to client (it's ready!)
  ✓ Export to Word for customization
  ✓ Email to contractor for bidding
  ✓ Submit to lender for approval
  ✓ Share with GC on job site
```

---

## REAL-WORLD EXAMPLE: From Start to Finish

### Scenario: Madison, GA General Contractor
```
Project: Addition to residential home
Plans: 3 PDF files (floor plan, elevations, details)
Team: Estimator (non-technical)

TIMELINE:

09:00 AM  - Receive project inquiry from client
09:05 AM  - Download Excel template (1 min)
09:07 AM  - Fill in project info (2 min)
           Name: "Anderson Renovation"
           Address: "456 Peach Road, Madison GA 30601"
           Scope: "1,200 SF addition, new roof, HVAC"
           
09:10 AM  - Upload files (2 min)
           - anderson_floor_plans.pdf
           - anderson_elevations.pdf
           - anderson_details.pdf
           
09:10 AM  - Click "START ANALYSIS"
           
09:12 AM  - Receive progress update email
           "Your analysis is 25% complete..."
           
09:17 AM  - Receive completion email
           "Your analysis is ready!"
           
09:18 AM  - Download all files
           - Updated Excel (with findings + estimate)
           - PDF proposal ($62,500 estimate)
           - Xactimate export
           
09:20 AM  - Review findings
           Read 4 code issues (2 critical, 2 minor)
           
09:22 AM  - Customize proposal in Word (optional)
           Add company logo, change terms
           
09:25 AM  - Send to client
           "Here's your estimate..."
           
CLIENT RESPONSE: 09:45 AM
"Wow! How did you get this done so fast? 
 Usually takes 3-4 days."

RESULT: Won bid vs. competitor (faster turnaround = more professional)
```

---

## WHAT CHANGES FOR YOUR TEAM

### For Estimators
```
❌ BEFORE:
  • Spend 3-4 hours manually extracting data from PDFs
  • Hunt through multiple spreadsheets for pricing
  • Cross-check against building codes manually (error-prone)
  • Hand-type into proposal templates
  • Result: Lots of mistakes, slow delivery

✅ AFTER:
  • Upload PDF + done (2 minutes)
  • AI extracts all data automatically
  • Pricing auto-populated by region
  • Code compliance built-in
  • Result: Accurate estimates in 5-10 minutes
  • Bonus: Spend 90% less time on data entry
```

### For Project Managers
```
❌ BEFORE:
  • Can't commit to turnaround time
  • Bottleneck: waiting for estimates
  • Lots of back-and-forth with estimators
  • No visibility into what's taking time

✅ AFTER:
  • Promise: "You'll have estimate by tomorrow"
  • Reality: Estimate in 5-10 minutes
  • No bottlenecks
  • Instant visibility (real-time status updates)
  • Can take on 3x more projects
```

### For Office Manager
```
❌ BEFORE:
  • Hire 1-2 full-time estimators ($40K-$60K/year each)
  • Still have 2-3 week backlog
  • Staff turnover (job is tedious)
  • Excel spreadsheets everywhere (messy, error-prone)

✅ AFTER:
  • Same team handles 3x more projects
  • No backlog (estimates in 5-10 min)
  • Staff happier (spend time on valuable work)
  • Centralized system (no more lost files)
  • Cost: ~$500-$2000/month subscription
  • ROI: 2-3 months (payback period)
```

---

## THE NUMBERS: ROI FOR YOUR FIRM

### Before Eagle Eye
```
Estimate per project:
  • Time: 10-14 hours
  • Cost: 10-14 hrs × $50/hr labor = $500-$700 per estimate
  • Typical firm: 50 projects/year
  • Total cost: 50 × $600 (avg) = $30,000/year on estimating
  
Backlog:
  • Can handle ~50-75 estimates per year per person
  • If higher demand, must hire more estimators
  • Typical firm: 1-2 FTE estimators @ $45K-$60K/year
```

### After Eagle Eye
```
Estimate per project:
  • Time: 5-10 minutes
  • Cost: $0 (included in subscription)
  • Typical firm: 50 projects/year
  • Total cost: 0 labor cost

Capacity increase:
  • Same team can now handle 300+ estimates/year
  • No need to hire more staff
  • Or: Existing staff can take on more complex work

Annual ROI:
  Old cost (50 projects @ $600 ea):        $30,000/year
  Eagle Eye subscription:                  $1,500/year
  Savings:                                 $28,500/year
  Payback period:                          ~6 weeks
```

---

## WHAT DATA EAGLE EYE ANALYZES

### From PDFs, Eagle Eye Automatically Extracts:

```
✓ Component Schedule (windows, doors, HVAC, etc.)
✓ Dimensions (from drawing notation)
✓ Material specifications (grade, type, model)
✓ Quantities (from tables/schedules)
✓ Structural details (beam sizes, spacing, etc.)
✓ Mechanical/electrical specs (if shown)
✓ Site conditions (from notes/callouts)
✓ Any handwritten notes or annotations
```

### Analysis Eagle Eye Performs:

```
✓ Code Compliance Checking
  - IRC 2018 (residential code)
  - IECC 2015 (energy code)
  - NEC 2017 (electrical code)
  - Local amendments (Georgia, etc.)

✓ Cost Estimation
  - Regional labor rates
  - Material costs by ZIP code
  - O&P calculation
  - Contingency assessment
  - Permit cost estimation

✓ Risk Assessment
  - Severity coding (RED/ORANGE/YELLOW)
  - Consequences of non-compliance
  - Recommended fixes

✓ Document Generation
  - Professional PDF proposal (A-I sections)
  - Xactimate-ready CSV
  - Compliance report
  - Payment schedule
```

---

## TECHNICAL SPECS (What Happens Behind the Scenes)

```
Pipeline: Extract → Analyze → Generate (5-10 minutes)

Stage 1: Extract (2-3 min)
  • Convert PDFs to images
  • Run OCR (Tesseract) for text
  • Find tables with SAM (Segment Anything Model)
  • Recognize components with vision models
  • Merge with Excel data (if provided)

Stage 2: Analyze (1-2 min, parallel)
  • IRC 2018 rules checking
  • IECC 2015 rules checking
  • NEC 2017 rules checking
  • Jurisdiction amendments
  • Regional factor lookup

Stage 3: Generate (1 min)
  • Calculate costs (TradeBase + regional factors)
  • Generate Excel with findings/estimate
  • Generate PDF proposal
  • Generate Xactimate CSV
  • Generate compliance report

Stage 4: Deliver (30 sec)
  • Send email with download links
  • Update project status
```

---

## SUPPORT & CUSTOMIZATION

### If Excel Template Doesn't Match Your Workflow
```
✓ We can customize the template for your firm
✓ Add your company logo to proposals
✓ Change payment terms/schedule
✓ Add custom code sets (if you have local standards)
✓ Integrate with your existing tools
  (QuickBooks, Xactimate, CRM, etc.)
```

### If You Need Custom Rules
```
✓ Add your own code standards
✓ Create firm-specific checklists
✓ Add company-specific pricing adjustments
✓ Create custom proposal templates
```

### Training
```
✓ 30-minute onboarding (via Zoom)
✓ Video library (how-to guides)
✓ Email support (24 hour response)
✓ Dedicated account manager (for Enterprise plans)
```

---

## SUCCESS METRICS: How to Measure

```
Week 1:
  ✓ All team members trained
  ✓ 10 pilot projects completed
  ✓ Average time: 8 minutes ✓
  ✓ 100% accuracy on components ✓
  ✓ Team feedback: Positive

Month 1:
  ✓ 50+ estimates generated
  ✓ Average turnaround: 6 minutes
  ✓ Client satisfaction: High
  ✓ Zero delays (all on-time delivery)
  ✓ Cost savings: $2,500/month labor

Month 3:
  ✓ 150+ estimates generated
  ✓ Can take on 3x more projects
  ✓ No staff additions needed
  ✓ Cumulative savings: $7,500+
  ✓ ROI: 5x return on Eagle Eye subscription

Year 1:
  ✓ 500+ estimates generated
  ✓ Team throughput increased 300%
  ✓ Annual savings: $28,500
  ✓ Total ROI: 19x
```

---

## CONCLUSION: THE SIMPLE PROMISE

**Old Way**: Excel + PDFs + manual work = 10-14 hours per estimate

**New Way**: Upload + AI magic = 5-10 minutes per estimate

**Your Benefit**: 60x faster estimates, same accuracy, better compliance

**Your Cost**: ~$1,500/year (pays for itself in 2 weeks)

**Your Result**: Win more bids, happier clients, more profit

---
