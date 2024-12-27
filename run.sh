#!/bin/bash

export DB_URL="postgresql+psycopg://user:postgres@localhost:5432/postgres"
export DB_ECHO="True"

export SUPABASE_URL=""
export SUPABASE_KEY=""
export JWT_SECRET=""

fastapi dev main.py