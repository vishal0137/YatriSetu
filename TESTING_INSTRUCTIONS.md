# YatriSetu Testing Instructions

## Server Status

✅ All models successfully reorganized and tested  
✅ Import errors fixed  
✅ Server ready for testing  

## Quick Start

### 1. Start the Server

```bash
python run.py
```

You should see:

```
======================================================================
YatriSetu - Smart Transit Platform
======================================================================
Starting server...

Available Endpoints:
  • Home Page:          http://localhost:5000/
  • AI Chatbot:         http://localhost:5000/chatbot
  • Admin Dashboard:    http://localhost:5000/admin
  • Data Import:        http://localhost:5000/admin/data-import

Testing Features:
  ✓ Chatbot - Natural language route queries
  ✓ Data Extractor - CSV/PDF file processing
  ✓ Admin Panel - Complete dashboard access

Press CTRL+C to quit
======================================================================
```

## Testing Checklist

### Test 1: Chatbot Functionality

**URL:** http://localhost:5000/chatbot

**Test Cases:**

| Test | Input | Expected Output |
|------|-------|----------------|
| Greeting | "Hello" | Welcome message with system stats |
| Route Search | "Route from Connaught Place to Dwarka" | Route suggestions with details |
| Direct Route | "Route DS-1" | Complete route information |
| Bus Info | "Bus DTC-078" | Bus details and current route |
| Fare Query | "Fare to Nehru Place" | Fare breakdown by category |

**What to Verify:**
- ✓ Chat interface loads properly
- ✓ Messages send and receive correctly
- ✓ Typing indicators appear
- ✓ Quick suggestions work
- ✓ Route cards display properly
- ✓ No console errors

### Test 2: Data Extractor (Data Import Feature)

**URL:** http://localhost:5000/admin/data-import

**Test Cases:**

#### A. CSV File Upload

1. Navigate to Data Import page
2. Click "Choose File"
3. Select a CSV file from `processed_data/`:
   - `routes_final.csv`
   - `stops_final.csv`
   - `fares_final.csv`
4. Click "Analyze File"

**Expected Results:**
- File analysis shows:
  - Total rows and columns
  - Column names
  - Detected category
  - Sample data preview
  - Validation status

#### B. PDF File Processing

1. Click "Choose File"
2. Select: `destination_bus_services_nov_2025_1_0.pdf`
3. Click "Analyze File"

**Expected Results:**
- PDF analysis shows:
  - Total pages
  - Tables found
  - Text extraction status

#### C. Data Extraction

1. After analysis, select category (Routes/Stops/Fares)
2. Click "Extract Data"

**Expected Results:**
- Extracted data preview
- Record count
- Validation report
- No errors

#### D. Database Import

1. After extraction, click "Import to Database"

**Expected Results:**
- Success message
- Number of records imported
- No validation errors

**What to Verify:**
- ✓ File upload works
- ✓ Analysis completes successfully
- ✓ Category detection is accurate
- ✓ Validation catches errors
- ✓ Data preview displays correctly
- ✓ Import completes without errors

### Test 3: Admin Dashboard

**URL:** http://localhost:5000/admin

**What to Verify:**
- ✓ Dashboard loads
- ✓ Statistics display
- ✓ Navigation works
- ✓ All sections accessible

### Test 4: CLI Tool (process_dtc_data.py)

**Command:**

```bash
python process_dtc_data.py destination_bus_services_nov_2025_1_0.pdf test_output
```

**Expected Output:**

```
======================================================================
YatriSetu Data Processing Tool
======================================================================
Input File: destination_bus_services_nov_2025_1_0.pdf
Output Directory: test_output
Category: routes
Timestamp: 2026-02-25 XX:XX:XX
======================================================================

Processing PDF file...
✓ PDF processing completed successfully

Exporting processed data to CSV files...

✓ Routes exported: test_output/routes_final.csv
✓ Stops exported: test_output/stops_final.csv
✓ Fares exported: test_output/fares_final.csv

======================================================================
PROCESSING SUMMARY
======================================================================

Exported Files:
  • Routes: 41 records → routes_final.csv
  • Stops: 82 records → stops_final.csv
  • Fares: 205 records → fares_final.csv

Validation Results:
  • Total Errors: 0
  • Total Warnings: 0
  • Status: ✓ PASSED

======================================================================
Processing completed successfully!
======================================================================
```

**What to Verify:**
- ✓ PDF processing completes
- ✓ CSV files generated
- ✓ Validation passes
- ✓ Record counts match

## Model Testing

### Run Model Tests

```bash
python test_models.py
```

**Expected Output:**

```
======================================================================
YatriSetu Models Test
======================================================================

Test 1: Importing models...
✓ Successfully imported: chatbot, DataExtractor, SamparkChatbot

Test 2: Testing chatbot instance...
✓ Chatbot instance is valid

Test 3: Testing DataExtractor class...
✓ DataExtractor class is valid

Test 4: Testing chatbot greeting...
✓ Chatbot greeting works

Test 5: Testing database models import...
✓ Successfully imported all database models

======================================================================
Test Summary
======================================================================
All critical imports are working correctly!
Server is ready for testing.
======================================================================
```

## Common Issues and Solutions

### Issue 1: Import Error

**Error:** `ImportError: cannot import name 'Chatbot'`

**Solution:** Already fixed! The models `__init__.py` now correctly exports `SamparkChatbot` and `chatbot` instance.

### Issue 2: Database Connection Error

**Error:** `Database initialization failed`

**Solution:** This is expected if PostgreSQL is not running. The server will run without database connection for testing the UI.

### Issue 3: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in run.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Testing Workflow

### Recommended Testing Order

1. **Model Tests** (5 minutes)
   ```bash
   python test_models.py
   ```

2. **Start Server** (1 minute)
   ```bash
   python run.py
   ```

3. **Test Chatbot** (10 minutes)
   - Open http://localhost:5000/chatbot
   - Try various queries
   - Test route search
   - Test direct lookups

4. **Test Data Import** (15 minutes)
   - Open http://localhost:5000/admin/data-import
   - Upload CSV files
   - Test PDF processing
   - Verify validation

5. **Test CLI Tool** (5 minutes)
   ```bash
   python process_dtc_data.py destination_bus_services_nov_2025_1_0.pdf test_output
   ```

6. **Verify Admin Dashboard** (5 minutes)
   - Open http://localhost:5000/admin
   - Check all sections

## Success Criteria

### ✅ All Tests Pass When:

- [ ] Server starts without errors
- [ ] All models import successfully
- [ ] Chatbot responds to queries
- [ ] Data import analyzes files correctly
- [ ] CSV files can be uploaded and processed
- [ ] PDF files can be analyzed
- [ ] CLI tool generates CSV files
- [ ] No console errors in browser
- [ ] All pages load correctly

## Performance Benchmarks

| Operation | Expected Time |
|-----------|--------------|
| Server startup | < 5 seconds |
| Chatbot response | < 1 second |
| CSV analysis | < 2 seconds |
| PDF processing | 5-10 seconds |
| Data extraction | 2-5 seconds |

## Next Steps After Testing

1. ✅ Verify all features work
2. ✅ Document any issues found
3. ✅ Test with real database connection
4. ✅ Import processed data to database
5. ✅ Test end-to-end workflows
6. ✅ Performance testing with larger datasets

## Support

If you encounter any issues:

1. Check console output for errors
2. Review browser console (F12)
3. Check `test_models.py` output
4. Verify all dependencies installed: `pip install -r requirements.txt`
5. Ensure virtual environment is activated

---

**Status:** Ready for Testing  
**Last Updated:** February 25, 2026  
**Version:** 1.0.0
