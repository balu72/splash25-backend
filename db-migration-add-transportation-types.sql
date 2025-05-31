-- Migration to add individual transportation types for outbound and return journeys
-- This fixes the issue where both journeys were forced to use the same transportation type

-- Add new columns to the transportation table
ALTER TABLE transportation 
ADD COLUMN outbound_type VARCHAR(20),
ADD COLUMN return_type VARCHAR(20);

-- Update existing records to use the main type as default for both outbound and return
UPDATE transportation 
SET outbound_type = type, return_type = type 
WHERE outbound_type IS NULL OR return_type IS NULL;

-- Add comments to document the purpose of these fields
COMMENT ON COLUMN transportation.outbound_type IS 'Individual transportation type for outbound journey (can be different from main type)';
COMMENT ON COLUMN transportation.return_type IS 'Individual transportation type for return journey (can be different from main type)';

-- Verify the migration
SELECT 
    id, 
    type as main_type, 
    outbound_type, 
    return_type,
    outbound_carrier,
    return_carrier
FROM transportation 
LIMIT 5;
