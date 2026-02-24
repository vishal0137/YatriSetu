# Sampark Chatbot - Conversational Flow Guide

## Overview
The Sampark chatbot now features a conversational flow similar to DMRC WhatsApp chatbot, where users can enter start and end locations step by step instead of typing complete commands.

## Conversational Flow Features

### 1. Step-by-Step Route Search

**User Flow**:
```
User: Find Route
Bot: Let's find your route!
     Where are you starting from?
     Please enter your starting location:
     [Suggestions: Connaught Place, IGI Airport, Kashmere Gate, Anand Vihar, Dwarka, Noida]

User: Connaught Place
Bot: Starting from: Connaught Place
     Where do you want to go?
     Please enter your destination:
     [Suggestions: Connaught Place, IGI Airport, Kashmere Gate, Anand Vihar, Dwarka, Noida]

User: Dwarka
Bot: [Shows route results from Connaught Place to Dwarka]
     [Suggestions: Book Ticket, Cheapest Route, Fastest Route, New Search]
```

### 2. Step-by-Step Fare Check

**User Flow**:
```
User: Check Fare
Bot: I can help you check fares!
     Where are you starting from?
     Please enter your starting location:
     [Suggestions: Connaught Place, IGI Airport, Kashmere Gate, Anand Vihar, Dwarka, Noida]

User: IGI Airport
Bot: Starting from: IGI Airport
     Where do you want to go?
     Please enter your destination:
     [Suggestions: Connaught Place, IGI Airport, Kashmere Gate, Anand Vihar, Dwarka, Noida]

User: Kashmere Gate
Bot: [Shows fare breakdown from IGI Airport to Kashmere Gate]
     [Suggestions: Book Ticket, Find Route, New Search]
```

## Backend State Management

### User Context States

```python
user_context = {
    'state': 'initial',  # or 'awaiting_source', 'awaiting_destination', 'awaiting_source_fare', 'awaiting_destination_fare'
    'source': None,      # Stores source location
    'destination': None  # Stores destination location
}
```

### State Transitions

1. **initial** → User types "Find Route" → **awaiting_source**
2. **awaiting_source** → User enters location → **awaiting_destination**
3. **awaiting_destination** → User enters location → **initial** (with results)

4. **initial** → User types "Check Fare" → **awaiting_source_fare**
5. **awaiting_source_fare** → User enters location → **awaiting_destination_fare**
6. **awaiting_destination_fare** → User enters location → **initial** (with fare)

## Commands

### Conversational Commands
- `Find Route` - Start route search flow
- `Check Fare` - Start fare check flow
- `New Search` - Reset context and start over

### Direct Commands (Still Available)
- `Route 001` - Get route details directly
- `Bus DTC-078` - Get bus information directly
- `Route from CP to Dwarka` - Search with full command
- `Fare from CP to Airport` - Check fare with full command
- `Stats` - Get statistics
- `Help` - Get help
- `Popular Routes` - See popular routes
- `Track bus DTC-001` - Track a bus

## Frontend Context Detection

### Location Input Detection
The frontend detects when the bot is asking for location input by checking for these phrases in the response:
- "starting from"
- "where do you want to go"
- "enter your"

When detected, it shows location suggestions:
- Connaught Place
- IGI Airport
- Kashmere Gate
- Anand Vihar
- Dwarka
- Noida

### Context Switching
The frontend automatically switches contexts based on:
1. Response type (greeting, help, statistics, etc.)
2. Message content (asking for location, showing results, etc.)
3. Presence of routes array (route search results)

## User Experience Benefits

### 1. Simpler Input
- Users don't need to remember command syntax
- Just click "Find Route" and follow prompts
- Natural conversation flow

### 2. Guided Experience
- Bot asks specific questions
- Clear instructions at each step
- Helpful location suggestions

### 3. Error Prevention
- Users can't make syntax mistakes
- Location matching handles typos
- Clear feedback at each step

### 4. Flexibility
- Can use conversational flow OR direct commands
- Both methods work seamlessly
- Users choose their preferred method

## Example Conversations

### Example 1: First-Time User
```
User: hi
Bot: Namaste! I'm Sampark...
     [Suggestions: Find Route, Route 001, Bus DTC-078, Help]

User: [Clicks "Find Route"]
Bot: Let's find your route!
     Where are you starting from?
     [Suggestions: Connaught Place, IGI Airport, ...]

User: [Clicks "Connaught Place"]
Bot: Starting from: Connaught Place
     Where do you want to go?
     [Suggestions: Connaught Place, IGI Airport, ...]

User: [Types "dwarka"]
Bot: [Shows routes from Connaught Place to Dwarka]
     [Suggestions: Book Ticket, Cheapest Route, Fastest Route, New Search]
```

### Example 2: Experienced User
```
User: Route from CP to Airport
Bot: [Shows routes directly]
     [Suggestions: Book Ticket, Cheapest Route, Fastest Route, New Search]
```

### Example 3: Fare Check
```
User: Check Fare
Bot: Where are you starting from?
     [Suggestions: Connaught Place, IGI Airport, ...]

User: Kashmere Gate
Bot: Starting from: Kashmere Gate
     Where do you want to go?
     [Suggestions: Connaught Place, IGI Airport, ...]

User: Anand Vihar
Bot: [Shows fare breakdown]
     [Suggestions: Book Ticket, Find Route, New Search]
```

## Implementation Details

### Backend Handler
```python
def process_message(self, user_id, message):
    context = self.user_context[user_id]
    
    # Handle conversational flow states
    if context['state'] == 'awaiting_source':
        # User provided source location
        source_match = self.location_handler.find_best_location_match(message)
        context['source'] = source_match
        context['state'] = 'awaiting_destination'
        return {
            'message': f"Starting from: {source_match}\n\nWhere do you want to go?",
            'suggestions': ['Connaught Place', 'IGI Airport', ...]
        }
    
    elif context['state'] == 'awaiting_destination':
        # User provided destination
        dest_match = self.location_handler.find_best_location_match(message)
        source = context['source']
        context['state'] = 'initial'
        
        # Search for routes
        routes = self.route_search.find_routes(source, dest_match)
        return self.route_search.generate_recommendations(routes, source, dest_match)
```

### Frontend Detection
```javascript
function updateContextSuggestionsFromResponse(response) {
    const message = response.message.toLowerCase();
    
    // Detect location input request
    if (message.includes('starting from') || 
        message.includes('where do you want to go') || 
        message.includes('enter your')) {
        updateContextSuggestions('', 'location');
    }
    // ... other conditions
}
```

## Suggestions Mapping

### Conversational Flow Suggestions

| State | Suggestions |
|-------|-------------|
| Initial | Find Route, Route 001, Check Fare, Track Bus |
| Awaiting Source | Connaught Place, IGI Airport, Kashmere Gate, Anand Vihar, Dwarka, Noida |
| Awaiting Destination | Connaught Place, IGI Airport, Kashmere Gate, Anand Vihar, Dwarka, Noida |
| Route Results | Book Ticket, Cheapest Route, Fastest Route, New Search |
| No Routes Found | Popular Routes, New Search, Help |

## Testing the Flow

### Test Case 1: Complete Flow
1. Type "Find Route"
2. Click "Connaught Place"
3. Type "dwarka"
4. Verify routes are shown
5. Click "New Search"
6. Verify context is reset

### Test Case 2: Fare Flow
1. Type "Check Fare"
2. Click "IGI Airport"
3. Click "Kashmere Gate"
4. Verify fare is shown

### Test Case 3: Mixed Usage
1. Type "Route 001" (direct command)
2. Verify route details shown
3. Click "New Search"
4. Click "Find Route" (conversational)
5. Follow prompts
6. Verify both methods work

## Troubleshooting

### Issue: Context Not Resetting
**Solution**: Use "New Search" command or type "reset"

### Issue: Wrong Location Detected
**Solution**: Type the location name more clearly or select from suggestions

### Issue: Stuck in Conversational Flow
**Solution**: Type "New Search" or use a direct command like "Route 001"

## Future Enhancements

### Potential Improvements
1. **Location Autocomplete**: Show suggestions as user types
2. **Recent Locations**: Remember user's recent searches
3. **Favorite Routes**: Save frequently used routes
4. **Voice Input**: Allow voice commands for locations
5. **Map Integration**: Show locations on map
6. **Multi-language**: Support Hindi and other languages

## Comparison with DMRC WhatsApp Bot

### Similarities
- Step-by-step location input
- Clear prompts at each step
- Location suggestions
- Simple, guided flow

### Enhancements in Sampark
- Direct commands still available
- More context-aware suggestions
- Richer route information
- Multiple search options (cheapest, fastest)
- Real-time bus tracking
- Comprehensive help system

---

**Last Updated**: February 23, 2026  
**Version**: 3.0  
**Status**: Production Ready  
**Flow Type**: Conversational + Direct Commands
