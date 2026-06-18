-- Tabela de participantes
CREATE TABLE IF NOT EXISTS participantes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome_completo TEXT NOT NULL,
  time_favorito TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de seleções do bolão (1º e 2º lugar por grupo)
CREATE TABLE IF NOT EXISTS selecoes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  participante_id UUID REFERENCES participantes(id) ON DELETE CASCADE,
  grupo TEXT NOT NULL CHECK (grupo IN ('A','B','C','D','E','F','G','H','I','J','K','L')),
  primeiro_lugar TEXT NOT NULL,
  segundo_lugar TEXT NOT NULL,
  UNIQUE(participante_id, grupo)
);

-- Tabela dos 8 melhores terceiros lugares
CREATE TABLE IF NOT EXISTS melhores_terceiros (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  participante_id UUID REFERENCES participantes(id) ON DELETE CASCADE,
  terceiros_selecionados TEXT[] NOT NULL CHECK (array_length(terceiros_selecionados, 1) = 8),
  UNIQUE(participante_id)
);

-- Habilitar RLS
ALTER TABLE participantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE selecoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE melhores_terceiros ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso
CREATE POLICY "Permitir INSERT participantes" ON participantes FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT participantes" ON participantes FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE participantes" ON participantes FOR UPDATE USING (true);

CREATE POLICY "Permitir INSERT selecoes" ON selecoes FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT selecoes" ON selecoes FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE selecoes" ON selecoes FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE selecoes" ON selecoes FOR DELETE USING (true);

CREATE POLICY "Permitir INSERT melhores_terceiros" ON melhores_terceiros FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT melhores_terceiros" ON melhores_terceiros FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE melhores_terceiros" ON melhores_terceiros FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE melhores_terceiros" ON melhores_terceiros FOR DELETE USING (true);

-- Índices
CREATE INDEX IF NOT EXISTS idx_selecoes_participante ON selecoes(participante_id);
CREATE INDEX IF NOT EXISTS idx_selecoes_grupo ON selecoes(grupo);
CREATE INDEX IF NOT EXISTS idx_melhores_terceiros_participante ON melhores_terceiros(participante_id);
