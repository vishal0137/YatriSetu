# Duplicate Detection Guide

## Overview

The enhanced data import feature includes comprehensive duplicate detection that helps you identify and manage duplicate entries before importing data to the database.

## How Duplicate Detection Works

### Detection Process

1. **File Upload**: Upload CSV/PDF file with data
2. **Data Extraction**: System extracts all records from file
3. **Database Check**: Each record is checked against existing database entries
4. **Comparison**: System compares new data with existing data field-by-field
5. **Preview**: Duplicates are highlighted in the preview table
6. **Action Selection**: Admin decides what to do with each duplicate

### Duplicate Identification

| Category | Duplicate Check Criteria |
|----------|-------------------------|
| Buses | bus_number (must be unique) |
| Routes | route_number (must be unique) |
| Stops | route_id + stop_name + sequence (combination must be unique) |
| Fares | route_id + passenger_type (combination must be unique) |

## Visual Indicators

### In Preview Table

| Indicator | Meaning |
|-----------|---------|
| Yellow row background | Duplicate entry found |
| Green row background | New entry (no duplicate) |
| Red row background | Validation error |
| Yellow cell background | Field value differs from existing |
| Bold text in cell | Changed field |

### Status Badges

| Badge | Color | Meaning |
|-------|-------|---------|
| New | Green | No duplicate found |
| Duplicate | Yellow | Duplicate entry exists |
| Error | Red | Validation failed |

## Duplicate Details Modal

### Accessing Details

1. Click on the yellow "Duplicate" badge in the Status column
2. Or click the "View Details" button in the Duplicate Info column

### Information Displayed

The modal shows:

1. **Duplicate Identification**
   - Which field caused the duplicate
   - The duplicate value
   - Database ID of existing record

2. **Existing Database Record**
   - All fields from the current database record
   - Shows what data is already stored

3. **Field Differences Table**
   - Side-by-side comparison
   - Existing value vs New value
   - Only shows fields that differ
   - New values highlighted in yellow

4. **Recommended Actions**
   - Skip: Keep existing data, don't import
   - Update: Replace existing data with new values
   - Insert: Force insert (may cause error)

## Example Scenarios

### Scenario 1: Identical Duplicate

**Situation**: New data is exactly the same as existing data

**Visual Indicator**: 
- Yellow row
- No yellow cells (no differences)
- Modal shows "No differences found"

**Recommended Action**: Skip

**Why**: No need to update if data is identical

### Scenario 2: Duplicate with Changes

**Situation**: Same bus_number but different capacity or type

**Visual Indicator**:
- Yellow row
- Yellow cells for changed fields (e.g., capacity)
- Bold text in changed cells

**Differences Table**:
```
Field      | Existing Value | New Value
-----------|----------------|----------
capacity   | 50             | 60
bus_type   | AC             | Non-AC
```

**Recommended Action**: Update or Skip

**Why**: 
- Update if new data is more accurate
- Skip if existing data is correct

### Scenario 3: Duplicate Route with Different Locations

**Situation**: Same route_number but different start/end locations

**Visual Indicator**:
- Yellow row
- Yellow cells for start_location and end_location
- Bold text in location fields

**Differences Table**:
```
Field           | Existing Value    | New Value
----------------|-------------------|------------------
start_location  | Connaught Place   | CP Metro Station
end_location    | Dwarka Sector 21  | Dwarka Sec-21
```

**Recommended Action**: Review carefully

**Why**: Could be:
- Same route with updated location names
- Different route with same number (error)
- Typo in existing or new data

## Action Options

### Skip (Default for Duplicates)

**What it does**: 
- Does not import the record
- Keeps existing database data unchanged
- Counts as "skipped" in statistics

**When to use**:
- Data is identical
- Existing data is correct
- New data is incorrect or outdated

**Example**:
```
Existing: Bus DL-1234, Capacity: 50, Type: AC
New:      Bus DL-1234, Capacity: 50, Type: AC
Action:   Skip (identical data)
```

### Update

**What it does**:
- Updates existing database record
- Replaces old values with new values
- Preserves database ID and relationships
- Updates timestamp

**When to use**:
- New data is more accurate
- Data has been corrected
- Information has changed (e.g., capacity increased)

**Example**:
```
Existing: Bus DL-1234, Capacity: 50, Type: AC
New:      Bus DL-1234, Capacity: 60, Type: AC
Action:   Update (capacity changed)
Result:   Database record updated to capacity 60
```

### Insert (Force)

**What it does**:
- Attempts to insert as new record
- May cause database constraint error
- Not recommended for true duplicates

**When to use**:
- You're certain it's not a duplicate
- Database check was incorrect
- Testing purposes only

**Warning**: May fail with database error if unique constraint exists

## Workflow Example

### Step-by-Step: Handling 100 Routes with 10 Duplicates

1. **Upload File**
   - Upload routes.csv with 100 routes
   - Click "Analyze & Preview Data"

2. **Review Statistics**
   ```
   Total Records: 100
   To Insert: 90
   Duplicates: 10
   Errors: 0
   ```

3. **Filter Duplicates**
   - Click "Duplicates" filter button
   - See only the 10 duplicate records

4. **Review Each Duplicate**
   - Click "View Details" for first duplicate
   - Check differences table
   - Decide action (Skip/Update)
   - Repeat for all 10 duplicates

5. **Example Decisions**:
   ```
   Route DS-1: No changes → Skip
   Route DS-2: Updated distance → Update
   Route DS-3: Typo in new data → Skip
   Route DS-4: Corrected location → Update
   Route DS-5: Identical → Skip
   Route DS-6: New fare info → Update
   Route DS-7: Old data better → Skip
   Route DS-8: Updated duration → Update
   Route DS-9: Identical → Skip
   Route DS-10: Corrected name → Update
   ```

6. **Final Statistics**:
   ```
   To Insert: 90 new routes
   To Update: 4 existing routes
   To Skip: 6 duplicates
   Total: 100 records processed
   ```

7. **Proceed to Import**
   - Review summary
   - Confirm import
   - Execute

8. **Results**:
   ```
   Inserted: 90 records
   Updated: 4 records
   Skipped: 6 records
   Errors: 0
   ```

## Best Practices

### Before Import

1. **Review All Duplicates**
   - Don't skip this step
   - Check each duplicate carefully
   - Verify data accuracy

2. **Use Filters**
   - Filter by "Duplicates" to focus
   - Review changed fields
   - Compare with existing data

3. **Check Differences**
   - Look at yellow highlighted cells
   - Read differences table
   - Understand what changed

### During Review

1. **Ask Questions**
   - Is the new data more accurate?
   - Is this a real update or error?
   - Should I keep existing data?

2. **Verify Sources**
   - Check source of new data
   - Verify existing data accuracy
   - Consult with data owner if unsure

3. **Document Decisions**
   - Note why you chose Skip/Update
   - Keep track of data changes
   - Maintain audit trail

### After Import

1. **Verify Results**
   - Check import statistics
   - Review updated records
   - Test with chatbot queries

2. **Validate Data**
   - Query updated routes
   - Check bus information
   - Verify stop sequences

3. **Monitor Issues**
   - Watch for user reports
   - Check data consistency
   - Fix any problems quickly

## Troubleshooting

### Issue: Too Many Duplicates

**Cause**: File contains mostly existing data

**Solution**:
- Filter to show only new records
- Consider if import is necessary
- Check if file is outdated

### Issue: Can't See Differences

**Cause**: Data is identical or very similar

**Solution**:
- Check modal for "No differences found"
- Skip these records
- Focus on records with changes

### Issue: Wrong Duplicate Detection

**Cause**: Database check criteria too broad

**Solution**:
- Review duplicate criteria
- Check if records are truly different
- Contact support if needed

### Issue: Update Not Working

**Cause**: Database permissions or constraints

**Solution**:
- Check database connection
- Verify user permissions
- Review error messages

## Tips for Efficient Review

1. **Use Keyboard Shortcuts**
   - Tab: Move between cells
   - Enter: Save cell edit
   - Esc: Cancel edit

2. **Batch Actions**
   - Review all duplicates first
   - Make decisions together
   - Apply consistent logic

3. **Focus on Changes**
   - Look for yellow cells
   - Ignore identical fields
   - Prioritize important changes

4. **Save Time**
   - Skip identical duplicates quickly
   - Update only when necessary
   - Don't overthink minor differences

## Security Considerations

- All duplicate checks are read-only
- No data is modified until import
- Changes can be reviewed before commit
- Database transactions ensure data integrity
- Rollback available if import fails

## Related Documentation

- [DATA_IMPORT_ENHANCED.md](DATA_IMPORT_ENHANCED.md) - Complete import guide
- [app/models/README.md](../app/models/README.md) - Data extractor documentation
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures

---

**Last Updated:** February 25, 2026  
**Version:** 2.0  
**Status:** Production Ready
