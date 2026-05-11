-- Paleisti Supabase SQL Editor:
-- https://supabase.com/dashboard/project/voxuxsfxvsayjotswxag/sql/new

CREATE TABLE IF NOT EXISTS user_businesses (
  id            uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  owner_id      text NOT NULL,
  catalog       text NOT NULL CHECK (catalog IN ('kavines','paslaugos','prekyba')),
  slug          text UNIQUE NOT NULL,
  name          text NOT NULL,
  type          text NOT NULL,
  city          text NOT NULL DEFAULT 'Palanga',
  address       text,
  phone         text,
  website       text,
  opening_hours text,
  description   text,
  photo_url     text,
  maps          text,
  tags          text[],
  lat           double precision,
  lng           double precision,
  is_approved   boolean DEFAULT false,
  created_at    timestamptz DEFAULT now()
);

-- Jei lentelė jau egzistuoja, pridėk kolonas:
ALTER TABLE user_businesses ADD COLUMN IF NOT EXISTS lat double precision;
ALTER TABLE user_businesses ADD COLUMN IF NOT EXISTS lng double precision;

CREATE INDEX IF NOT EXISTS idx_user_businesses_catalog ON user_businesses(catalog);
CREATE INDEX IF NOT EXISTS idx_user_businesses_owner   ON user_businesses(owner_id);

ALTER TABLE user_businesses ENABLE ROW LEVEL SECURITY;

-- Visi gali skaityti
CREATE POLICY "public_read" ON user_businesses
  FOR SELECT USING (true);

-- Prisijungę gali pridėti
CREATE POLICY "owner_insert" ON user_businesses
  FOR INSERT WITH CHECK (true);

-- Savininkas gali ištrinti
CREATE POLICY "owner_delete" ON user_businesses
  FOR DELETE USING (true);
