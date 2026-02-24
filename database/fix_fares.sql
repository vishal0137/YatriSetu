-- Fix fare amounts to be in increments of 5, 10, 15, 25, 35, 45, etc.
-- Based on distance ranges

-- Update fares based on distance
-- 0-5 km: ₹5
UPDATE routes SET fare = 5.00 WHERE distance_km <= 5 AND is_active = true;

-- 5-10 km: ₹10
UPDATE routes SET fare = 10.00 WHERE distance_km > 5 AND distance_km <= 10 AND is_active = true;

-- 10-15 km: ₹15
UPDATE routes SET fare = 15.00 WHERE distance_km > 10 AND distance_km <= 15 AND is_active = true;

-- 15-20 km: ₹20
UPDATE routes SET fare = 20.00 WHERE distance_km > 15 AND distance_km <= 20 AND is_active = true;

-- 20-25 km: ₹25
UPDATE routes SET fare = 25.00 WHERE distance_km > 20 AND distance_km <= 25 AND is_active = true;

-- 25-30 km: ₹30
UPDATE routes SET fare = 30.00 WHERE distance_km > 25 AND distance_km <= 30 AND is_active = true;

-- 30-35 km: ₹35
UPDATE routes SET fare = 35.00 WHERE distance_km > 30 AND distance_km <= 35 AND is_active = true;

-- 35-40 km: ₹40
UPDATE routes SET fare = 40.00 WHERE distance_km > 35 AND distance_km <= 40 AND is_active = true;

-- 40-45 km: ₹45
UPDATE routes SET fare = 45.00 WHERE distance_km > 40 AND distance_km <= 45 AND is_active = true;

-- 45-50 km: ₹50
UPDATE routes SET fare = 50.00 WHERE distance_km > 45 AND distance_km <= 50 AND is_active = true;

-- 50+ km: ₹55
UPDATE routes SET fare = 55.00 WHERE distance_km > 50 AND is_active = true;

-- Verify the changes
SELECT 
    CASE 
        WHEN distance_km <= 5 THEN '0-5 km'
        WHEN distance_km <= 10 THEN '5-10 km'
        WHEN distance_km <= 15 THEN '10-15 km'
        WHEN distance_km <= 20 THEN '15-20 km'
        WHEN distance_km <= 25 THEN '20-25 km'
        WHEN distance_km <= 30 THEN '25-30 km'
        WHEN distance_km <= 35 THEN '30-35 km'
        WHEN distance_km <= 40 THEN '35-40 km'
        WHEN distance_km <= 45 THEN '40-45 km'
        WHEN distance_km <= 50 THEN '45-50 km'
        ELSE '50+ km'
    END as distance_range,
    COUNT(*) as route_count,
    MIN(fare) as min_fare,
    MAX(fare) as max_fare
FROM routes
WHERE is_active = true
GROUP BY distance_range
ORDER BY MIN(distance_km);
