-- Schema do Simulador de Bolão Copa 2026

-- Tabela de participantes
CREATE TABLE IF NOT EXISTS participantes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome_completo TEXT NOT NULL,
  time_favorito TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  senha_hash TEXT NOT NULL,
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

-- Habilitar RLS (Row Level Security)
ALTER TABLE participantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE selecoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE melhores_terceiros ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso (permitir leitura/escrita para todos - projeto educacional)
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

-- Tabela de palpites do bracket (mata-mata)
CREATE TABLE IF NOT EXISTS palpites_bracket (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  participante_id UUID REFERENCES participantes(id) ON DELETE CASCADE,
  palpites JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(participante_id)
);

-- Habilitar RLS
ALTER TABLE palpites_bracket ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir INSERT palpites_bracket" ON palpites_bracket FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT palpites_bracket" ON palpites_bracket FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE palpites_bracket" ON palpites_bracket FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE palpites_bracket" ON palpites_bracket FOR DELETE USING (true);

-- Tabela de palpites da fase de grupos (placar de cada jogo)
CREATE TABLE IF NOT EXISTS palpites_grupos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  participante_id UUID REFERENCES participantes(id) ON DELETE CASCADE,
  rodada INTEGER NOT NULL CHECK (rodada IN (1, 2, 3)),
  grupo TEXT NOT NULL,
  time_casa TEXT NOT NULL,
  time_fora TEXT NOT NULL,
  placar_casa INTEGER NOT NULL DEFAULT 0,
  placar_fora INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(participante_id, rodada, grupo, time_casa, time_fora)
);

-- Habilitar RLS
ALTER TABLE palpites_grupos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir INSERT palpites_grupos" ON palpites_grupos FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT palpites_grupos" ON palpites_grupos FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE palpites_grupos" ON palpites_grupos FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE palpites_grupos" ON palpites_grupos FOR DELETE USING (true);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_selecoes_participante ON selecoes(participante_id);
CREATE INDEX IF NOT EXISTS idx_selecoes_grupo ON selecoes(grupo);
CREATE INDEX IF NOT EXISTS idx_melhores_terceiros_participante ON melhores_terceiros(participante_id);
CREATE INDEX IF NOT EXISTS idx_palpites_bracket_participante ON palpites_bracket(participante_id);
CREATE INDEX IF NOT EXISTS idx_palpites_grupos_participante ON palpites_grupos(participante_id);

-- Tabela de resultados reais (gols dos jogos)
CREATE TABLE IF NOT EXISTS resultados (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  fase TEXT NOT NULL CHECK (fase IN ('grupo', 'R32', 'Oitavas', 'Quartas', 'Semis', 'Terceiro', 'Final')),
  rodada INTEGER,
  grupo TEXT,
  time_casa TEXT NOT NULL,
  time_fora TEXT NOT NULL,
  gols_casa INTEGER NOT NULL DEFAULT 0,
  gols_fora INTEGER NOT NULL DEFAULT 0,
  UNIQUE(fase, rodada, grupo, time_casa, time_fora),
  UNIQUE(fase, time_casa, time_fora)
);

-- Habilitar RLS
ALTER TABLE resultados ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir INSERT resultados" ON resultados FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir SELECT resultados" ON resultados FOR SELECT USING (true);
CREATE POLICY "Permitir UPDATE resultados" ON resultados FOR UPDATE USING (true);
CREATE POLICY "Permitir DELETE resultados" ON resultados FOR DELETE USING (true);

CREATE INDEX IF NOT EXISTS idx_resultados_fase ON resultados(fase);
