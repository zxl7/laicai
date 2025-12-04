import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://jkggoicvyyvrujjgfaxd.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImprZ2dvaWN2eXl2cnVqamdmYXhkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ4NTUyNTksImV4cCI6MjA4MDQzMTI1OX0.SORvrjnI-hhx42zJdD2we1lHUFypsHZaIfftlMncC4Q'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)