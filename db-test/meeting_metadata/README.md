# Meeting Metadata Management

This directory contains scripts and documentation for managing meeting metadata settings in the Splash25 application.

## Overview

The Meeting Metadata functionality allows administrators to configure:
- Meeting duration (10-60 minutes)
- Interval between meeting slots (0-30 minutes)
- Day start and end times (12-hour format)
- Multiple breaks with custom names and times

## Database Storage

Meeting metadata is stored in the `system_settings` table with the following keys:
- `meeting_duration` - Meeting duration in minutes (string)
- `meeting_interval` - Interval between slots in minutes (string)
- `day_start_time` - Day start time (e.g., "9:00 AM")
- `day_end_time` - Day end time (e.g., "5:00 PM")
- `meeting_breaks` - JSON array of break objects

## API Endpoints

### GET /api/system/meeting-metadata
Retrieve current meeting metadata configuration.

**Response:**
```json
{
  "metadata": {
    "meeting_duration": 10,
    "meeting_interval": 5,
    "day_start_time": "9:00 AM",
    "day_end_time": "5:00 PM",
    "meeting_breaks": [
      {
        "id": 1,
        "label": "Lunch Break",
        "startTime": "12:00 PM",
        "endTime": "1:00 PM"
      }
    ]
  }
}
```

### PUT /api/system/meeting-metadata
Update meeting metadata configuration (admin only).

**Request:**
```json
{
  "meetingDuration": 10,
  "intervalBetweenSlots": 5,
  "dayStartTime": "9:00",
  "dayStartPeriod": "AM",
  "dayEndTime": "5:00",
  "dayEndPeriod": "PM",
  "breaks": [
    {
      "id": 1,
      "label": "Lunch Break",
      "startTime": "12:00",
      "startPeriod": "PM",
      "endTime": "1:00",
      "endPeriod": "PM"
    }
  ]
}
```

### POST /api/system/meeting-metadata/initialize
Initialize default meeting metadata settings (admin only).

## Scripts

### initialize_meeting_metadata.py

Initialize or reset meeting metadata settings to defaults.

**Usage:**
```bash
# Initialize with defaults
cd splash25-backend
python db-test/meeting_metadata/initialize_meeting_metadata.py

# Verify existing settings
python db-test/meeting_metadata/initialize_meeting_metadata.py verify
```

**Default Settings:**
- Meeting Duration: 10 minutes
- Interval Between Slots: 5 minutes
- Day Start Time: 9:00 AM
- Day End Time: 5:00 PM
- Breaks: Lunch Break (12:00 PM - 1:00 PM)

## Frontend Integration

### Admin Interface

The Meeting Metadata configuration is accessible through:
1. Admin Dashboard → Meetings Tab
2. Click "Meeting Metadata" button
3. Configure settings in the modal dialog

### Validation Rules

- **Meeting Duration**: 10-60 minutes
- **Interval**: 0-30 minutes
- **Day Times**: End time must be after start time
- **Breaks**: Must be within day hours, end time after start time
- **Multiple Breaks**: Supported with add/remove functionality

### Features

- Real-time form validation
- 12-hour time format with AM/PM selection
- Dynamic break management
- API integration with loading states
- Error handling and user feedback

## Development

### Adding New Validation Rules

1. Update backend validation in `splash25-backend/app/routes/system.py`
2. Update frontend validation in `splash25-ui/src/components/admin/MeetingManagement.tsx`

### Extending Break Functionality

To add new break properties:
1. Update `MeetingBreak` interface in `splash25-ui/src/services/system.service.ts`
2. Update break form fields in the MeetingManagement component
3. Update backend processing in system routes

### Database Migration

If you need to modify the meeting metadata structure:
1. Create a new migration script in this directory
2. Update the API endpoints accordingly
3. Update the frontend interfaces

## Troubleshooting

### Common Issues

1. **Settings not loading**: Check database connection and system_settings table
2. **Validation errors**: Ensure all time values are within valid ranges
3. **API errors**: Verify admin authentication and proper request format

### Debug Commands

```bash
# Check if settings exist
python db-test/meeting_metadata/initialize_meeting_metadata.py verify

# Reset to defaults
python db-test/meeting_metadata/initialize_meeting_metadata.py

# Check database directly
docker exec -it splash25-postgres psql -U splash25user -d splash25 -c "SELECT * FROM system_settings WHERE key LIKE 'meeting_%';"
```

## Security

- All meeting metadata endpoints require admin authentication
- Input validation on both frontend and backend
- SQL injection protection through SQLAlchemy ORM
- XSS protection through proper data sanitization

## Future Enhancements

- Time zone support
- Recurring break patterns
- Meeting room assignments
- Calendar integration
- Bulk time slot generation
- Meeting conflict detection
