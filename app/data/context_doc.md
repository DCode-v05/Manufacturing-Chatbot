# Factory Knowledge Base — Manufacturing Operations AI Assistant

## 1. Factory Overview
This factory manufactures mechanical components and operates multiple production lines with CNC machines, milling machines, robotic arms, conveyors, and inspection systems.

The factory runs in three shifts per day:
- Shift A: 6:00 AM – 2:00 PM
- Shift B: 2:00 PM – 10:00 PM
- Shift C: 10:00 PM – 6:00 AM

Departments:
- Production
- Maintenance
- Quality Control (QC)
- Packaging
- Safety Compliance
- Logistics

## 2. Machine Directory & Status Rules

### Machine Types
- A1: CNC Cutting Machine
- A2: Lathe Machine
- A3: CNC Milling Machine
- B5: Robotic Arm
- B7: Packing Conveyor
- C2: QC Scanner

### Machine Status Codes
- RUNNING
- IDLE
- DOWN
- MAINTENANCE
- CHANGEOVER
- WARMUP

### Common Machine Issues
- Motor overheating
- Low lubrication
- Tool misalignment
- Sensor failure
- Material feed jam
- Safety guard open
- Power fluctuation

## 3. Shop Floor Workflow Procedures

### Start-of-Shift Procedure
1. Check PPE.
2. Review shift handover notes.
3. Inspect workstation.
4. Confirm machines are OK.
5. Clear scrap.
6. Warm-up cycle.

### End-of-Shift Procedure
1. Stop production.
2. Log output.
3. Report issues.
4. Clean area.
5. Update shift book.

### Production Reporting
Operators log:
- Output
- Uptime
- Scrap
- Downtime reason
- Material usage

## 4. Safety Guidelines & SOPs

### General Safety Rules
- PPE required.
- Don’t bypass interlocks.
- Report spills.
- No loose clothing.
- Only trained operators.

### Hazard Categories
- Mechanical
- Electrical
- Thermal
- Chemical
- Slip hazards

### SOP: Emergency Machine Shutdown
1. Emergency STOP.
2. Inform supervisor.
3. Disconnect power.
4. Log incident.
5. Restart only after clearance.

### SOP: Fire Response
1. Alert.
2. Raise alarm.
3. Use correct extinguisher.
4. Evacuate.
5. Call emergency team.

## 5. Order & Inventory

### Order Status
- Received
- In Production
- QC
- Packed
- Dispatched
- Delayed

### Inventory Categories
- Raw
- WIP
- Finished
- Rejected

Low stock threshold: 20%.

## 6. Maintenance Procedures

### Breakdown Maintenance
1. Operator reports.
2. Engineer inspects.
3. Diagnose issue.
4. Repair/replace.
5. Trial run.
6. Mark RUNNING.

### Preventive Maintenance
- Lubrication
- Bolt tightening
- Sensor cleaning
- Filter replacement
- Calibration

## 7. Quality Control

### Common Defects
- Scratches
- Dimensional mismatch
- Burrs
- Misalignment

### QC Acceptance
- ±0.05 mm tolerance
- Clean finish
- No structural defects

## 8. Escalation Matrix

### Machine Breakdown
Operator → Maintenance Engineer → Lead → Plant Manager

### Safety Violation
Operator → Safety Officer → HR (if repeated)

## 9. AI Usage Rules
- Use only this document.
- If unsure: “This info is not in the knowledge base.”
- Respond clearly and structured.
