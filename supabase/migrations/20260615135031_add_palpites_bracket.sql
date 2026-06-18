-- Tabela de palpites do bracket (mata-mata)
CREATE TABLE IF NOT EXISTS palpites_bracket (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  participante_id UUID REFERENCES participantes(id) ON DELETE CASCADE,
  palpites JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(participante_id)
);

ALTER TABLE palpites_bracket ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir INSERT palpites_bracket" ON palpites_bracket FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT palpites_bracket" ON palpites_bracket FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE palpites_bracket" ON palpites_bracket FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE palpites_bracket" ON palpites_bracket FOR DELETE USING (true);

CREATE INDEX IF NOT EXISTS idx_palpites_bracket_participante ON palpites_bracket(participante_id);
