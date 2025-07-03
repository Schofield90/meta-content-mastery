-- Supabase Database Schema for Meta Content Manager
-- Run these SQL commands in your Supabase SQL Editor

-- 1. Business Profiles Table
CREATE TABLE business_profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    business_name TEXT NOT NULL,
    industry TEXT,
    location TEXT,
    target_audience TEXT,
    brand_voice TEXT,
    services TEXT,
    usp TEXT,
    goals TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Content Library Table
CREATE TABLE content_library (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    business_id UUID REFERENCES business_profiles(id) ON DELETE CASCADE,
    post_content TEXT NOT NULL,
    platform TEXT,
    performance TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Training Images Table
CREATE TABLE training_images (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    business_id UUID REFERENCES business_profiles(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    source TEXT DEFAULT 'upload',
    file_size INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Enable Row Level Security (RLS) for multi-tenancy
ALTER TABLE business_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_library ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_images ENABLE ROW LEVEL SECURITY;

-- 5. Create policies for public access (you can make these more restrictive later)
CREATE POLICY "Allow all access to business_profiles" ON business_profiles FOR ALL USING (true);
CREATE POLICY "Allow all access to content_library" ON content_library FOR ALL USING (true);
CREATE POLICY "Allow all access to training_images" ON training_images FOR ALL USING (true);

-- 6. Create storage bucket for images
INSERT INTO storage.buckets (id, name, public) VALUES ('training-images', 'training-images', true);

-- 7. Storage policy for images
CREATE POLICY "Allow all access to training images bucket" ON storage.objects FOR ALL USING (bucket_id = 'training-images');