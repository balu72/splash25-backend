-- Migration script to add business_images column to seller_profiles table
-- Run this script to add the new JSONB column for storing business image URLs

-- Add business_images column to seller_profiles table
ALTER TABLE seller_profiles 
ADD COLUMN IF NOT EXISTS business_images JSONB DEFAULT '[]'::jsonb;

-- Add a comment to document the column
COMMENT ON COLUMN seller_profiles.business_images IS 'JSONB array storing business image metadata including URLs, filenames, sizes, and upload timestamps';

-- Create an index on the business_images column for better query performance
CREATE INDEX IF NOT EXISTS idx_seller_profiles_business_images 
ON seller_profiles USING GIN (business_images);

-- Verify the column was added successfully
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'seller_profiles' 
AND column_name = 'business_images';
