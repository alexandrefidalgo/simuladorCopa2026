-- Tabela de palpites da fase de grupos (placar de cada jogo)
CREATE TABLE IF NOT EXISTS palpites_grupos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  participante_id UUID REFERENCES participantes(id) ON DELETE CASCADE,
  grupo TEXT NOT NULL,
  time_casa TEXT NOT NULL,
  time_fora TEXT NOT NULL,
  placar_casa INTEGER NOT NULL DEFAULT 0,
  placar_fora INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(participante_id, grupo, time_casa, time_fora)
);

-- Habilitar RLS
ALTER TABLE palpites_grupos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir INSERT palpites_grupos" ON palpites_grupos FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT palpites_grupos" ON palpites_grupos FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE palpites_grupos" ON palpites_grupos FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE palpites_grupos" ON palpites_grupos FOR DELETE USING (true);

-- Índice para performance
CREATE INDEX IF NOT EXISTS idx_palpites_grupos_participante ON palpites_grupos(participante_id);
