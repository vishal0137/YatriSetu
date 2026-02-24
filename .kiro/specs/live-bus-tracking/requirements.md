# Live Bus Tracking System - Requirements Document

## Feature Name
Live Bus Tracking with Real-time GPS Mapping

## Overview
Implement a real-time bus tracking system similar to the government's "Where is my train" service, allowing passengers to track DTC buses on a live map, see estimated arrival times, and get real-time location updates.

## Problem Statement
Currently, passengers have no way to know:
- Where their bus is in real-time
- How long until the bus arrives at their stop
- If the bus is running on schedule
- Alternative buses nearby

This leads to:
- Uncertainty and anxiety at bus stops
- Wasted time waiting for buses
- Poor passenger experience
- Difficulty in planning journeys

## Target Users
1. **Passengers**: Want to track buses and plan their journey
2. **Admin/Operators**: Need to monitor fleet in real-time
3. **Drivers**: May need to share their location (optional)

## User Stories

### US-1: View Live Bus Location
**As a** passenger  
**I want to** see the real-time location of my bus on a map  
**So that** I can know exactly where it is and when it will arrive

**Acceptance Criteria**:
- AC-1.1: Map displays current location of all active buses
- AC-1.2: Bus markers show bus number and route
- AC-1.3: Location updates every 10-30 seconds
- AC-1.4: Map is interactive (zoom, pan, center)
- AC-1.5: Bus markers are color-coded by status (on-time, delayed, stopped)

### US-2: Track Specific Bus
**As a** passenger  
**I want to** search for and track a specific bus by number  
**So that** I can focus on the bus I need to take

**Acceptance Criteria**:
- AC-2.1: Search bar to find bus by number
- AC-2.2: Map centers on selected bus
- AC-2.3: Selected bus is highlighted with different marker
- AC-2.4: Shows bus details (route, next stops, ETA)
- AC-2.5: Can follow bus as it moves

### US-3: View Estimated Arrival Time
**As a** passenger  
**I want to** see when the bus will arrive at my stop  
**So that** I can plan when to leave for the bus stop

**Acceptance Criteria**:
- AC-3.1: Select a stop on the route
- AC-3.2: System calculates ETA based on current location and speed
- AC-3.3: ETA updates in real-time
- AC-3.4: Shows distance remaining to stop
- AC-3.5: Displays "Arriving soon" when within 2 minutes

### US-4: View Route Path
**As a** passenger  
**I want to** see the complete route path on the map  
**So that** I can understand the bus's journey

**Acceptance Criteria**:
- AC-4.1: Route path drawn on map as a line
- AC-4.2: All stops marked along the route
- AC-4.3: Completed portion shown in different color
- AC-4.4: Upcoming stops highlighted
- AC-4.5: Can click stops to see details

### US-5: View Nearby Buses
**As a** passenger  
**I want to** see all buses near my current location  
**So that** I can find the nearest available bus

**Acceptance Criteria**:
- AC-5.1: "Near Me" button to find nearby buses
- AC-5.2: Shows buses within 2km radius
- AC-5.3: Lists buses sorted by distance
- AC-5.4: Shows walking distance to each bus
- AC-5.5: Can filter by route/destination

### US-6: Admin Fleet Monitoring
**As an** admin/operator  
**I want to** monitor all buses in real-time  
**So that** I can manage the fleet effectively

**Acceptance Criteria**:
- AC-6.1: Dashboard showing all active buses
- AC-6.2: Filter by route, status, or region
- AC-6.3: View bus statistics (speed, stops, delays)
- AC-6.4: Identify buses that are off-route
- AC-6.5: Export tracking data for analysis

### US-7: Historical Tracking
**As an** admin  
**I want to** view historical bus movement data  
**So that** I can analyze patterns and optimize routes

**Acceptance Criteria**:
- AC-7.1: Select date/time range for playback
- AC-7.2: Replay bus movements on map
- AC-7.3: View speed and stop duration analytics
- AC-7.4: Generate reports on route efficiency
- AC-7.5: Identify problem areas (frequent delays)

### US-8: Offline Support
**As a** passenger  
**I want to** see last known location when offline  
**So that** I can still get some information without internet

**Acceptance Criteria**:
- AC-8.1: Cache last known bus locations
- AC-8.2: Show "Last updated" timestamp
- AC-8.3: Indicate when data is stale
- AC-8.4: Auto-refresh when connection restored
- AC-8.5: Store route maps for offline viewing

## Technical Requirements

### TR-1: GPS Data Collection
- TR-1.1: GPS coordinates collected every 10-30 seconds
- TR-1.2: Accuracy within 10-20 meters
- TR-1.3: Include speed, heading, and timestamp
- TR-1.4: Handle GPS signal loss gracefully
- TR-1.5: Validate coordinates (within service area)

### TR-2: Real-time Updates
- TR-2.1: Use WebSocket for live updates
- TR-2.2: Fallback to polling if WebSocket unavailable
- TR-2.3: Update frequency: 10-30 seconds
- TR-2.4: Batch updates for multiple buses
- TR-2.5: Compress data for mobile networks

### TR-3: Map Integration
- TR-3.1: Use Leaflet.js or Google Maps API
- TR-3.2: Support for custom markers and polylines
- TR-3.3: Responsive design (mobile + desktop)
- TR-3.4: Smooth marker animation between updates
- TR-3.5: Clustering for many buses

### TR-4: Performance
- TR-4.1: Map loads in < 3 seconds
- TR-4.2: Smooth animations at 60fps
- TR-4.3: Handle 150+ buses simultaneously
- TR-4.4: Efficient database queries (< 100ms)
- TR-4.5: Optimize for mobile data usage

### TR-5: Data Storage
- TR-5.1: Store location history for 90 days
- TR-5.2: Efficient time-series database (TimescaleDB/InfluxDB)
- TR-5.3: Index by bus_id, timestamp, route_id
- TR-5.4: Automatic data archival/cleanup
- TR-5.5: Backup and recovery procedures

### TR-6: Security & Privacy
- TR-6.1: Encrypt GPS data in transit (HTTPS/WSS)
- TR-6.2: Rate limiting on API endpoints
- TR-6.3: Authentication for admin features
- TR-6.4: No personal driver information exposed
- TR-6.5: GDPR compliance for location data

## GPS Data Sources (Implementation Options)

### Option 1: GPS Tracking Devices (Hardware)
**Description**: Install GPS devices in each bus
- **Pros**: Most accurate, reliable, professional
- **Cons**: Expensive, requires hardware installation
- **Cost**: ₹5,000-15,000 per device
- **Examples**: Teltonika, Queclink, Concox GPS trackers

### Option 2: Mobile App for Drivers
**Description**: Drivers use smartphone app to share location
- **Pros**: Low cost, easy deployment, no hardware
- **Cons**: Depends on driver cooperation, battery drain
- **Cost**: App development only
- **Examples**: Similar to Uber driver app

### Option 3: Simulated GPS (Development/Demo)
**Description**: Generate realistic GPS data for testing
- **Pros**: No hardware needed, perfect for development
- **Cons**: Not real data, only for demo
- **Cost**: Free
- **Implementation**: Algorithm to move buses along routes

### Option 4: Government API Integration
**Description**: Integrate with existing DTC/government GPS system
- **Pros**: Official data, no hardware needed
- **Cons**: May not exist, requires partnership
- **Cost**: Depends on API access
- **Examples**: Similar to GTFS Realtime feeds

### Recommended Approach
**Phase 1 (MVP)**: Option 3 - Simulated GPS for demo and development
**Phase 2 (Pilot)**: Option 2 - Mobile app for 10-20 buses
**Phase 3 (Production)**: Option 1 - Professional GPS devices for full fleet

## Data Flow Architecture

```
GPS Source → Data Collection → Validation → Database → WebSocket Server → Client App
                                                    ↓
                                            Historical Storage
```

### Components:
1. **GPS Data Collector**: Receives location updates
2. **Validation Service**: Validates and enriches data
3. **Real-time Database**: Current locations (Redis/PostgreSQL)
4. **Historical Database**: Time-series data (TimescaleDB)
5. **WebSocket Server**: Pushes updates to clients
6. **REST API**: For queries and historical data
7. **Web Client**: Interactive map interface

## Non-Functional Requirements

### NFR-1: Scalability
- Support 150 buses initially
- Scale to 500+ buses in future
- Handle 10,000+ concurrent users

### NFR-2: Availability
- 99.5% uptime during service hours
- Graceful degradation if GPS unavailable
- Automatic recovery from failures

### NFR-3: Latency
- Location updates within 30 seconds
- Map interactions < 100ms response
- ETA calculations < 500ms

### NFR-4: Mobile Optimization
- Works on 3G networks
- Minimal data usage (< 5MB/hour)
- Battery efficient

### NFR-5: Accessibility
- WCAG 2.1 AA compliance
- Screen reader support
- Keyboard navigation
- High contrast mode

## Success Metrics

### User Engagement
- 60% of users check bus location before leaving
- Average session duration > 2 minutes
- 40% return users within 7 days

### Accuracy
- GPS accuracy within 20 meters 95% of time
- ETA accuracy within ±3 minutes 80% of time
- 95% uptime for tracking service

### Performance
- Map load time < 3 seconds
- Location update latency < 30 seconds
- Support 150 buses with smooth performance

## Out of Scope (Future Enhancements)

1. Push notifications for bus arrival
2. Crowdsourced bus occupancy data
3. Integration with ticket booking
4. Multi-modal journey planning
5. Driver communication features
6. Predictive arrival times using ML
7. Traffic integration
8. Bus delay alerts

## Dependencies

### External Services
- Map provider (Leaflet.js with OpenStreetMap or Google Maps)
- GPS data source (hardware or mobile app)
- WebSocket infrastructure (Socket.io or native WebSocket)

### Internal Systems
- Existing bus and route database
- User authentication system
- Admin dashboard

### Infrastructure
- WebSocket server (Node.js or Python)
- Time-series database (TimescaleDB extension for PostgreSQL)
- Redis for caching current locations
- CDN for map tiles (optional)

## Risks & Mitigations

### Risk 1: GPS Data Unavailable
**Impact**: High  
**Mitigation**: 
- Start with simulated data for MVP
- Implement fallback to last known location
- Show clear indicators when data is stale

### Risk 2: Poor GPS Accuracy
**Impact**: Medium  
**Mitigation**:
- Implement map-matching algorithms
- Filter out invalid coordinates
- Use Kalman filtering for smoothing

### Risk 3: High Server Load
**Impact**: Medium  
**Mitigation**:
- Use Redis for caching
- Implement efficient WebSocket broadcasting
- Use CDN for static assets
- Horizontal scaling capability

### Risk 4: Mobile Data Costs
**Impact**: Low  
**Mitigation**:
- Compress WebSocket messages
- Implement smart update frequency
- Cache map tiles
- Provide data usage settings

## Timeline Estimate

### Phase 1: MVP (4-6 weeks)
- Week 1-2: Database schema, simulated GPS generator
- Week 3-4: WebSocket server, REST API
- Week 5-6: Map interface, basic tracking

### Phase 2: Enhanced Features (3-4 weeks)
- Week 7-8: ETA calculations, route visualization
- Week 9-10: Admin dashboard, historical data

### Phase 3: Production Ready (2-3 weeks)
- Week 11-12: Performance optimization, testing
- Week 13: Deployment, monitoring

**Total**: 9-13 weeks for full implementation

## Glossary

- **GPS**: Global Positioning System
- **ETA**: Estimated Time of Arrival
- **WebSocket**: Protocol for real-time bidirectional communication
- **GTFS**: General Transit Feed Specification
- **Map Matching**: Algorithm to snap GPS points to road network
- **Geofencing**: Virtual boundary around geographic area
- **Kalman Filter**: Algorithm for smoothing noisy GPS data

## References

1. "Where is my train" - Indian Railways live tracking
2. Google Maps Live Transit
3. Moovit - Public transit app
4. GTFS Realtime specification
5. Leaflet.js documentation
6. WebSocket protocol specification

---

**Document Version**: 1.0  
**Created**: February 23, 2026  
**Status**: Draft - Awaiting Review  
**Next Steps**: Design document with technical architecture
