import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY
let client: any

if (typeof supabaseUrl === 'string' && supabaseUrl && typeof supabaseAnonKey === 'string' && supabaseAnonKey) {
  client = createClient(String(supabaseUrl), String(supabaseAnonKey))
} else {
  client = {
    auth: {
      async getSession() {
        return { data: { session: null }, error: null }
      },
      onAuthStateChange() {
        return { data: { subscription: { unsubscribe() {} } } }
      },
      async signInWithPassword() {
        return { error: { message: 'Auth disabled' } }
      },
      async signUp() {
        return { error: { message: 'Auth disabled' } }
      },
      async signOut() {
        return { error: null }
      }
    }
  }
}

export const supabase = client
