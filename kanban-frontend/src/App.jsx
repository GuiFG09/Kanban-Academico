import { useState, useEffect, useCallback } from "react";

// ─── Config ───────────────────────────────────────────────────────────────────
const API = "http://localhost:8000";

// ─── Types ────────────────────────────────────────────────────────────────────
const STATUS_MAP = {
  A_FAZER: { label: "A Fazer", icon: "◻", color: "#6366f1" },
  FAZENDO: { label: "Fazendo", icon: "◈", color: "#f59e0b" },
  PRONTO:  { label: "Feito",   icon: "◼", color: "#10b981" },
};

const PRIORIDADE_MAP = {
  alta:  { label: "Alta",  color: "#ef4444", bg: "#ef444415", glow: "#ef444450" },
  media: { label: "Média", color: "#f59e0b", bg: "#f59e0b15", glow: "#f59e0b50" },
  baixa: { label: "Baixa", color: "#10b981", bg: "#10b98115", glow: "#10b98150" },
};

// ─── API helpers ──────────────────────────────────────────────────────────────
async function apiFetch(path, opts = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Erro ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

// ─── Hooks ────────────────────────────────────────────────────────────────────
function useKanban() {
  const [usuarios,    setUsuarios]    = useState([]);
  const [disciplinas, setDisciplinas] = useState([]);
  const [atividades,  setAtividades]  = useState([]);
  const [progressos,  setProgressos]  = useState([]);
  const [loading,     setLoading]     = useState(true);
  const [error,       setError]       = useState(null);

  const [alunoLogado, setAlunoLogado] = useState(null);

  const reload = useCallback(async () => {
    try {
      setLoading(true); setError(null);
      const [us, ds, as_] = await Promise.all([
        apiFetch("/usuarios"),
        apiFetch("/disciplinas"),
        apiFetch("/atividades"),
      ]);
      setUsuarios(us); setDisciplinas(ds); setAtividades(as_);

      // Carrega progressos de todos os alunos
      const alunos = us.filter(u => u.tipo === "aluno");
      const progs = await Promise.all(
        alunos.map(a => apiFetch(`/progresso/aluno/${a.id}`).catch(() => []))
      );
      setProgressos(progs.flat());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { reload(); }, [reload]);

  return { usuarios, disciplinas, atividades, progressos, loading, error, reload, alunoLogado, setAlunoLogado };
}

// ─── Componentes de UI ────────────────────────────────────────────────────────
function Toast({ msg, onClose }) {
  useEffect(() => {
    if (!msg) return;
    const t = setTimeout(onClose, 3000);
    return () => clearTimeout(t);
  }, [msg, onClose]);
  if (!msg) return null;
  return (
    <div style={{
      position: "fixed", bottom: 28, left: "50%", transform: "translateX(-50%)",
      background: "rgba(10,15,28,0.97)", border: "1px solid rgba(99,102,241,0.4)",
      borderRadius: 14, padding: "13px 28px", color: "#a5b4fc",
      fontSize: 13, fontWeight: 700, fontFamily: "'DM Mono', monospace",
      boxShadow: "0 12px 40px rgba(0,0,0,0.6), 0 0 0 1px rgba(99,102,241,0.15)",
      backdropFilter: "blur(24px)", zIndex: 9999,
      animation: "toastIn .25s cubic-bezier(.34,1.56,.64,1)",
    }}>
      {msg}
    </div>
  );
}

function Spinner() {
  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: 200 }}>
      <div style={{
        width: 36, height: 36, borderRadius: "50%",
        border: "3px solid rgba(99,102,241,0.2)",
        borderTopColor: "#6366f1",
        animation: "spin .7s linear infinite",
      }} />
    </div>
  );
}

function Badge({ text, color, bg }) {
  return (
    <span style={{
      fontSize: 10, fontWeight: 700, letterSpacing: ".08em",
      textTransform: "uppercase", fontFamily: "'DM Mono', monospace",
      color, background: bg, border: `1px solid ${color}40`,
      padding: "2px 8px", borderRadius: 20,
    }}>{text}</span>
  );
}

function Modal({ title, onClose, children }) {
  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)",
      backdropFilter: "blur(6px)", zIndex: 1000,
      display: "flex", alignItems: "center", justifyContent: "center", padding: 16,
    }} onClick={e => e.target === e.currentTarget && onClose()}>
      <div style={{
        background: "#0d1420", border: "1px solid rgba(99,102,241,0.25)",
        borderRadius: 20, padding: "28px 32px", width: "100%", maxWidth: 480,
        boxShadow: "0 32px 80px rgba(0,0,0,0.7)",
        animation: "modalIn .2s cubic-bezier(.34,1.56,.64,1)",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h3 style={{ margin: 0, fontFamily: "'Cabinet Grotesk', 'Syne', sans-serif", fontSize: 18, fontWeight: 800, color: "#e2e8f0" }}>
            {title}
          </h3>
          <button onClick={onClose} style={{
            background: "rgba(255,255,255,0.06)", border: "none", color: "#94a3b8",
            width: 32, height: 32, borderRadius: 8, cursor: "pointer", fontSize: 16,
          }}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <label style={{ display: "block", fontSize: 11, fontWeight: 700, letterSpacing: ".1em",
        textTransform: "uppercase", color: "#64748b", fontFamily: "'DM Mono', monospace", marginBottom: 6 }}>
        {label}
      </label>
      {children}
    </div>
  );
}

const inputStyle = {
  width: "100%", padding: "10px 14px", borderRadius: 10,
  background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.1)",
  color: "#e2e8f0", fontSize: 13, fontFamily: "'DM Mono', monospace",
  outline: "none", boxSizing: "border-box",
  transition: "border-color .2s",
};

const btnPrimary = {
  padding: "10px 24px", borderRadius: 10, fontWeight: 700, fontSize: 13,
  background: "linear-gradient(135deg,#6366f1,#818cf8)", border: "none",
  color: "#fff", cursor: "pointer", fontFamily: "'Cabinet Grotesk','Syne',sans-serif",
  transition: "opacity .2s, transform .1s",
};

// ─── KanbanCard ───────────────────────────────────────────────────────────────
function KanbanCard({ progresso, atividade, aluno, onTransition }) {
  const [hov, setHov] = useState(false);
  const prio = PRIORIDADE_MAP[atividade?.prioridade] || PRIORIDADE_MAP.media;
  const disc = atividade?.disciplina_nome || `Disciplina #${atividade?.disciplina_id}`;

  const nextAction = {
    A_FAZER: { label: "👉 Iniciar",  next: "FAZENDO" },
    FAZENDO: { label: "✅ Concluir", next: "PRONTO"  },
    PRONTO:  null,
  }[progresso.status];

  const due = atividade?.data_entrega;
  const overdue = due && new Date(due) < new Date() && progresso.status !== "PRONTO";

  return (
    <div
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        background: hov ? "rgba(15,23,42,0.98)" : "rgba(13,20,32,0.85)",
        border: `1px solid ${hov ? prio.color + "60" : "rgba(255,255,255,0.07)"}`,
        borderLeft: `3px solid ${prio.color}`,
        borderRadius: 12, padding: "14px 16px", marginBottom: 10,
        transition: "all .2s cubic-bezier(.4,0,.2,1)",
        transform: hov ? "translateY(-2px)" : "none",
        boxShadow: hov ? `0 8px 32px rgba(0,0,0,.5), 0 0 20px ${prio.glow}` : "0 2px 8px rgba(0,0,0,.3)",
        cursor: "default",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
        <span style={{
          width: 7, height: 7, borderRadius: "50%", flexShrink: 0,
          background: prio.color, boxShadow: `0 0 6px ${prio.color}`,
        }} />
        <Badge text={prio.label} color={prio.color} bg={prio.bg} />
        {overdue && <span style={{ marginLeft: "auto", fontSize: 10, color: "#f87171", fontWeight: 700, fontFamily: "'DM Mono',monospace" }}>⚠ ATRASADO</span>}
      </div>

      {/* Título */}
      <p style={{ margin: "0 0 4px", fontSize: 14, fontWeight: 700, color: "#e2e8f0",
        lineHeight: 1.3, fontFamily: "'Cabinet Grotesk','Syne',sans-serif" }}>
        {atividade?.titulo || "Atividade"}
      </p>
      {atividade?.descricao && (
        <p style={{ margin: "0 0 8px", fontSize: 11, color: "rgba(255,255,255,.38)", lineHeight: 1.5 }}>
          {atividade.descricao}
        </p>
      )}

      {/* Tags */}
      <div style={{ display: "flex", gap: 6, marginBottom: 12, flexWrap: "wrap" }}>
        <span style={{
          fontSize: 10, padding: "2px 8px", borderRadius: 20, fontFamily: "'DM Mono',monospace",
          background: "rgba(99,102,241,0.12)", color: "#818cf8", border: "1px solid rgba(99,102,241,0.2)",
        }}>{disc}</span>
        {due && (
          <span style={{
            fontSize: 10, padding: "2px 8px", borderRadius: 20, fontFamily: "'DM Mono',monospace",
            background: overdue ? "rgba(248,113,113,0.1)" : "rgba(255,255,255,0.04)",
            color: overdue ? "#f87171" : "rgba(255,255,255,.3)",
            border: `1px solid ${overdue ? "rgba(248,113,113,0.25)" : "rgba(255,255,255,0.08)"}`,
          }}>📅 {new Date(due + "T00:00:00").toLocaleDateString("pt-BR")}</span>
        )}
      </div>

      {/* Footer */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div style={{
            width: 24, height: 24, borderRadius: "50%",
            background: `linear-gradient(135deg,${prio.color},${prio.color}99)`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 10, fontWeight: 700, color: "#0d1420",
          }}>{aluno?.nome?.[0]?.toUpperCase() || "A"}</div>
          <span style={{ fontSize: 11, color: "rgba(255,255,255,.4)", fontFamily: "'DM Mono',monospace" }}>
            {aluno?.nome || `Aluno #${progresso.aluno_id}`}
          </span>
        </div>

        {nextAction ? (
          <button
            onClick={() => onTransition(progresso.aluno_id, progresso.atividade_id, nextAction.next)}
            style={{
              fontSize: 11, padding: "5px 13px", borderRadius: 20, cursor: "pointer",
              background: hov ? `linear-gradient(135deg,${prio.color},${prio.color}cc)` : "rgba(255,255,255,.06)",
              border: `1px solid ${hov ? "transparent" : "rgba(255,255,255,0.1)"}`,
              color: hov ? "#0d1420" : "rgba(255,255,255,.7)",
              fontWeight: 700, transition: "all .2s", whiteSpace: "nowrap",
              fontFamily: "'Cabinet Grotesk','Syne',sans-serif",
            }}
          >{nextAction.label}</button>
        ) : (
          <span style={{ fontSize: 11, color: "#10b981", fontWeight: 700, fontFamily: "'DM Mono',monospace" }}>✓ Pronto</span>
        )}
      </div>
    </div>
  );
}

// ─── Column ───────────────────────────────────────────────────────────────────
function Column({ statusKey, cards, usuarios, atividades, onTransition }) {
  const meta = STATUS_MAP[statusKey];
  return (
    <div style={{
      flex: 1, minWidth: 280, maxWidth: 400,
      background: "rgba(255,255,255,0.018)", border: "1px solid rgba(255,255,255,0.055)",
      borderRadius: 18, padding: "16px 14px",
      backdropFilter: "blur(10px)",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
        <span style={{ fontSize: 18, opacity: 0.5 }}>{meta.icon}</span>
        <h2 style={{
          margin: 0, fontSize: 13, fontWeight: 800, letterSpacing: ".1em",
          textTransform: "uppercase", color: "rgba(255,255,255,.8)",
          fontFamily: "'Cabinet Grotesk','Syne',sans-serif",
        }}>{meta.label}</h2>
        <div style={{
          marginLeft: "auto", width: 8, height: 8, borderRadius: "50%",
          background: meta.color, boxShadow: `0 0 8px ${meta.color}`,
        }} />
        <span style={{
          fontSize: 11, fontWeight: 700, fontFamily: "'DM Mono',monospace",
          background: "rgba(255,255,255,.07)", color: "rgba(255,255,255,.4)",
          padding: "2px 9px", borderRadius: 20,
        }}>{cards.length}</span>
      </div>

      <div style={{ maxHeight: "62vh", overflowY: "auto", paddingRight: 2 }}>
        {cards.length === 0 ? (
          <div style={{
            textAlign: "center", padding: "48px 0",
            color: "rgba(255,255,255,.13)", fontSize: 12, fontFamily: "'DM Mono',monospace",
          }}>— vazio —</div>
        ) : cards.map(p => (
          <KanbanCard
            key={`${p.aluno_id}-${p.atividade_id}`}
            progresso={p}
            atividade={atividades.find(a => a.id === p.atividade_id)}
            aluno={usuarios.find(u => u.id === p.aluno_id)}
            onTransition={onTransition}
          />
        ))}
      </div>
    </div>
  );
}

// ─── Modal: Novo Usuário ──────────────────────────────────────────────────────
function ModalUsuario({ onClose, onSaved, toast }) {
  const [form, setForm] = useState({ nome: "", tipo: "aluno", email: "", senha: "" });
  const [saving, setSaving] = useState(false);

  async function submit() {
    if (!form.nome || !form.email || !form.senha) return toast("Preencha todos os campos");
    setSaving(true);
    try {
      await apiFetch("/usuarios", { method: "POST", body: JSON.stringify(form) });
      toast("Usuário criado! ✅"); onClose(); onSaved();
    } catch (e) { toast("Erro: " + e.message); } finally { setSaving(false); }
  }

  return (
    <Modal title="Novo Usuário" onClose={onClose}>
      <Field label="Nome"><input style={inputStyle} placeholder="ex: Maria Silva" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} /></Field>
      <Field label="Tipo">
        <select style={inputStyle} value={form.tipo} onChange={e => setForm({...form, tipo: e.target.value})}>
          <option value="aluno">Aluno</option>
          <option value="professor">Professor</option>
        </select>
      </Field>
      <Field label="Email"><input style={inputStyle} type="email" placeholder="email@exemplo.com" value={form.email} onChange={e => setForm({...form, email: e.target.value})} /></Field>
      <Field label="Senha"><input style={inputStyle} type="password" placeholder="mínimo 6 caracteres" value={form.senha} onChange={e => setForm({...form, senha: e.target.value})} /></Field>
      <button style={{...btnPrimary, width: "100%", marginTop: 8, opacity: saving ? .6 : 1}} onClick={submit} disabled={saving}>
        {saving ? "Salvando..." : "Criar Usuário"}
      </button>
    </Modal>
  );
}

// ─── Modal: Nova Disciplina ───────────────────────────────────────────────────
function ModalDisciplina({ usuarios, onClose, onSaved, toast }) {
  const profs = usuarios.filter(u => u.tipo === "professor");
  const [form, setForm] = useState({ nome: "", professor_id: profs[0]?.id || "", descricao: "" });
  const [saving, setSaving] = useState(false);

  async function submit() {
    if (!form.nome || !form.professor_id) return toast("Preencha nome e professor");
    setSaving(true);
    try {
      await apiFetch("/disciplinas", { method: "POST", body: JSON.stringify({...form, professor_id: Number(form.professor_id)}) });
      toast("Disciplina criada! ✅"); onClose(); onSaved();
    } catch (e) { toast("Erro: " + e.message); } finally { setSaving(false); }
  }

  return (
    <Modal title="Nova Disciplina" onClose={onClose}>
      <Field label="Nome"><input style={inputStyle} placeholder="ex: Programação Python" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} /></Field>
      <Field label="Professor">
        <select style={inputStyle} value={form.professor_id} onChange={e => setForm({...form, professor_id: e.target.value})}>
          {profs.length === 0 && <option value="">Nenhum professor cadastrado</option>}
          {profs.map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
        </select>
      </Field>
      <Field label="Descrição (opcional)"><input style={inputStyle} placeholder="Descrição da disciplina" value={form.descricao} onChange={e => setForm({...form, descricao: e.target.value})} /></Field>
      <button style={{...btnPrimary, width: "100%", marginTop: 8, opacity: saving ? .6 : 1}} onClick={submit} disabled={saving}>
        {saving ? "Salvando..." : "Criar Disciplina"}
      </button>
    </Modal>
  );
}

// ─── Modal: Nova Atividade ────────────────────────────────────────────────────
function ModalAtividade({ disciplinas, onClose, onSaved, toast }) {
  const tomorrow = new Date(); tomorrow.setDate(tomorrow.getDate() + 1);
  const tStr = tomorrow.toISOString().slice(0, 10);

  const [form, setForm] = useState({ titulo: "", descricao: "", data_entrega: tStr, disciplina_id: disciplinas[0]?.id || "", prioridade: "media" });
  const [saving, setSaving] = useState(false);

  async function submit() {
    if (!form.titulo || !form.disciplina_id) return toast("Preencha título e disciplina");
    setSaving(true);
    try {
      await apiFetch("/atividades", { method: "POST", body: JSON.stringify({...form, disciplina_id: Number(form.disciplina_id)}) });
      toast("Atividade criada! ✅"); onClose(); onSaved();
    } catch (e) { toast("Erro: " + e.message); } finally { setSaving(false); }
  }

  return (
    <Modal title="Nova Atividade" onClose={onClose}>
      <Field label="Título"><input style={inputStyle} placeholder="ex: Criar função recursiva" value={form.titulo} onChange={e => setForm({...form, titulo: e.target.value})} /></Field>
      <Field label="Disciplina">
        <select style={inputStyle} value={form.disciplina_id} onChange={e => setForm({...form, disciplina_id: e.target.value})}>
          {disciplinas.length === 0 && <option value="">Nenhuma disciplina cadastrada</option>}
          {disciplinas.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
        </select>
      </Field>
      <Field label="Prioridade">
        <select style={inputStyle} value={form.prioridade} onChange={e => setForm({...form, prioridade: e.target.value})}>
          <option value="alta">Alta</option>
          <option value="media">Média</option>
          <option value="baixa">Baixa</option>
        </select>
      </Field>
      <Field label="Data de Entrega"><input style={inputStyle} type="date" value={form.data_entrega} onChange={e => setForm({...form, data_entrega: e.target.value})} /></Field>
      <Field label="Descrição (opcional)"><input style={inputStyle} placeholder="Detalhes da atividade" value={form.descricao} onChange={e => setForm({...form, descricao: e.target.value})} /></Field>
      <button style={{...btnPrimary, width: "100%", marginTop: 8, opacity: saving ? .6 : 1}} onClick={submit} disabled={saving}>
        {saving ? "Salvando..." : "Criar Atividade"}
      </button>
    </Modal>
  );
}

// ─── Modal: Matricular Aluno ──────────────────────────────────────────────────
function ModalMatricular({ disciplinas, usuarios, onClose, onSaved, toast }) {
  const alunos = usuarios.filter(u => u.tipo === "aluno");
  const [discId, setDiscId] = useState(disciplinas[0]?.id || "");
  const [alunoId, setAlunoId] = useState(alunos[0]?.id || "");
  const [saving, setSaving] = useState(false);

  async function submit() {
    if (!discId || !alunoId) return toast("Selecione disciplina e aluno");
    setSaving(true);
    try {
      await apiFetch(`/disciplinas/${discId}/matricular?aluno_id=${alunoId}`, { method: "POST" });
      toast("Aluno matriculado! ✅"); onClose(); onSaved();
    } catch (e) { toast("Erro: " + e.message); } finally { setSaving(false); }
  }

  return (
    <Modal title="Matricular Aluno" onClose={onClose}>
      <Field label="Disciplina">
        <select style={inputStyle} value={discId} onChange={e => setDiscId(e.target.value)}>
          {disciplinas.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
        </select>
      </Field>
      <Field label="Aluno">
        <select style={inputStyle} value={alunoId} onChange={e => setAlunoId(e.target.value)}>
          {alunos.length === 0 && <option value="">Nenhum aluno cadastrado</option>}
          {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
        </select>
      </Field>
      <button style={{...btnPrimary, width: "100%", marginTop: 8, opacity: saving ? .6 : 1}} onClick={submit} disabled={saving}>
        {saving ? "Matriculando..." : "Matricular"}
      </button>
    </Modal>
  );
}

// ─── Filtros ──────────────────────────────────────────────────────────────────
function Filters({ disciplinas, usuarios, onChangeDisciplina, onChangeAluno }) {
  return (
    <div style={{ display: "flex", gap: 10, marginBottom: 24, flexWrap: "wrap" }}>
      <select
        onChange={e => onChangeDisciplina(e.target.value ? Number(e.target.value) : null)}
        style={{ ...inputStyle, width: "auto", minWidth: 180 }}
      >
        <option value="">Todas as disciplinas</option>
        {disciplinas.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
      </select>
      <select
        onChange={e => onChangeAluno(e.target.value ? Number(e.target.value) : null)}
        style={{ ...inputStyle, width: "auto", minWidth: 160 }}
      >
        <option value="">Todos os alunos</option>
        {usuarios.filter(u => u.tipo === "aluno").map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
      </select>
    </div>
  );
}

// ─── App principal ────────────────────────────────────────────────────────────
export default function App() {
  const { usuarios, disciplinas, atividades, progressos, loading, error, reload } = useKanban();
  const [toast, setToast] = useState(null);
  const [modal, setModal] = useState(null); // "usuario"|"disciplina"|"atividade"|"matricular"
  const [filterDisc, setFilterDisc]   = useState(null);
  const [filterAluno, setFilterAluno] = useState(null);

  const showToast = (msg) => setToast(msg);

  // Enriquece atividades com nome da disciplina
  const atividadesEnriquecidas = atividades.map(a => ({
    ...a,
    disciplina_nome: disciplinas.find(d => d.id === a.disciplina_id)?.nome,
  }));

  // Filtra progressos
  const progressosFiltrados = progressos.filter(p => {
    const atv = atividades.find(a => a.id === p.atividade_id);
    if (filterDisc  && atv?.disciplina_id !== filterDisc)  return false;
    if (filterAluno && p.aluno_id         !== filterAluno) return false;
    return true;
  });

  async function handleTransition(alunoId, atividadeId, newStatus) {
    try {
      await apiFetch(`/progresso/${alunoId}/${atividadeId}`, {
        method: "PUT",
        body: JSON.stringify({ status: newStatus }),
      });
      const aluno = usuarios.find(u => u.id === alunoId);
      const atv   = atividades.find(a => a.id === atividadeId);
      const msgs  = { FAZENDO: "Atividade iniciada! 🚀", PRONTO: "Atividade concluída! 🎉" };
      showToast(`${aluno?.nome}: "${atv?.titulo}" — ${msgs[newStatus]}`);
      await reload();
    } catch (e) { showToast("Erro: " + e.message); }
  }

  const totalProgress = progressos.length > 0
    ? Math.round((progressos.filter(p => p.status === "PRONTO").length / progressos.length) * 100)
    : 0;

  const statCards = [
    { label: "Alunos",      val: usuarios.filter(u => u.tipo === "aluno").length,     color: "#818cf8" },
    { label: "Professores", val: usuarios.filter(u => u.tipo === "professor").length,  color: "#f472b6" },
    { label: "Disciplinas", val: disciplinas.length,  color: "#34d399" },
    { label: "Atividades",  val: atividades.length,   color: "#fbbf24" },
  ];

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;700;800&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #070d1c; color: #e2e8f0; font-family: 'Syne', sans-serif; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: rgba(99,102,241,.3); border-radius: 4px; }
        select option { background: #0d1420; color: #e2e8f0; }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes toastIn { from { opacity:0; transform:translateX(-50%) translateY(12px); } to { opacity:1; transform:translateX(-50%) translateY(0); } }
        @keyframes modalIn { from { opacity:0; transform:scale(.94) translateY(8px); } to { opacity:1; transform:scale(1) translateY(0); } }
        @keyframes fadeUp { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
      `}</style>

      {/* Background */}
      <div style={{ position: "fixed", inset: 0, zIndex: 0, overflow: "hidden", pointerEvents: "none" }}>
        <div style={{ position: "absolute", top: -300, left: -200, width: 600, height: 600, borderRadius: "50%", background: "radial-gradient(circle,rgba(99,102,241,0.08) 0%,transparent 70%)" }} />
        <div style={{ position: "absolute", bottom: -200, right: -100, width: 500, height: 500, borderRadius: "50%", background: "radial-gradient(circle,rgba(52,211,153,0.05) 0%,transparent 70%)" }} />
        <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(rgba(99,102,241,0.04) 1px, transparent 1px)", backgroundSize: "32px 32px" }} />
      </div>

      <div style={{ position: "relative", zIndex: 1, padding: "32px 28px", maxWidth: 1380, margin: "0 auto" }}>

        {/* ── Header ── */}
        <div style={{ marginBottom: 32, animation: "fadeUp .4s ease" }}>
          <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", flexWrap: "wrap", gap: 16, marginBottom: 24 }}>
            <div>
              <p style={{ fontSize: 10, letterSpacing: ".25em", color: "#6366f1", textTransform: "uppercase",
                fontFamily: "'DM Mono', monospace", marginBottom: 4 }}>Sistema Acadêmico</p>
              <h1 style={{ fontSize: 38, fontWeight: 800, letterSpacing: "-.025em", lineHeight: 1,
                background: "linear-gradient(135deg,#e2e8f0 40%,#818cf8)", WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent" }}>
                Kanban Acadêmico
              </h1>
            </div>

            {/* Progress ring */}
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div>
                <p style={{ fontSize: 10, color: "#475569", fontFamily: "'DM Mono',monospace", marginBottom: 3 }}>Progresso Geral</p>
                <p style={{ fontSize: 26, fontWeight: 800, color: "#818cf8" }}>{totalProgress}%</p>
              </div>
              <svg width="56" height="56" viewBox="0 0 56 56" style={{ transform: "rotate(-90deg)" }}>
                <circle cx="28" cy="28" r="23" fill="none" stroke="rgba(99,102,241,0.12)" strokeWidth="4" />
                <circle cx="28" cy="28" r="23" fill="none" stroke="#6366f1" strokeWidth="4"
                  strokeDasharray={`${2 * Math.PI * 23}`}
                  strokeDashoffset={`${2 * Math.PI * 23 * (1 - totalProgress / 100)}`}
                  strokeLinecap="round" style={{ transition: "stroke-dashoffset .6s ease" }} />
              </svg>
            </div>
          </div>

          {/* Stat strip */}
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 20 }}>
            {statCards.map(s => (
              <div key={s.label} style={{
                background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: 12, padding: "10px 18px", display: "flex", alignItems: "center", gap: 10,
              }}>
                <span style={{ fontSize: 18, fontWeight: 800, color: s.color }}>{s.val}</span>
                <span style={{ fontSize: 11, color: "#475569", fontFamily: "'DM Mono',monospace",
                  textTransform: "uppercase", letterSpacing: ".08em" }}>{s.label}</span>
              </div>
            ))}
          </div>

          {/* Action buttons */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {[
              { label: "+ Usuário",    key: "usuario" },
              { label: "+ Disciplina", key: "disciplina" },
              { label: "+ Atividade",  key: "atividade" },
              { label: "↗ Matricular", key: "matricular" },
            ].map(b => (
              <button key={b.key} onClick={() => setModal(b.key)} style={{
                ...btnPrimary,
                background: b.key === "usuario"
                  ? "linear-gradient(135deg,#6366f1,#818cf8)"
                  : b.key === "disciplina"
                  ? "linear-gradient(135deg,#10b981,#34d399)"
                  : b.key === "atividade"
                  ? "linear-gradient(135deg,#f59e0b,#fbbf24)"
                  : "rgba(255,255,255,0.07)",
                color: b.key === "matricular" ? "#94a3b8" : "#fff",
                border: b.key === "matricular" ? "1px solid rgba(255,255,255,0.1)" : "none",
              }}>{b.label}</button>
            ))}
            <button onClick={reload} style={{
              ...btnPrimary, background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.1)", color: "#94a3b8",
            }}>↻ Atualizar</button>
          </div>
        </div>

        {/* ── Filters ── */}
        <Filters
          disciplinas={disciplinas}
          usuarios={usuarios}
          onChangeDisciplina={setFilterDisc}
          onChangeAluno={setFilterAluno}
        />

        {/* ── API offline warning ── */}
        {error && (
          <div style={{
            background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
            borderRadius: 12, padding: "14px 20px", marginBottom: 20,
            color: "#f87171", fontSize: 13, fontFamily: "'DM Mono',monospace",
          }}>
            ⚠ Não foi possível conectar à API (<code>http://localhost:8000</code>). Certifique-se que o backend está rodando com <code>python main.py</code>.<br/>
            <span style={{ opacity: .7 }}>Erro: {error}</span>
          </div>
        )}

        {/* ── Board ── */}
        {loading ? <Spinner /> : (
          <div style={{ display: "flex", gap: 14, alignItems: "flex-start", flexWrap: "wrap" }}>
            {Object.keys(STATUS_MAP).map(key => (
              <Column
                key={key}
                statusKey={key}
                cards={progressosFiltrados.filter(p => p.status === key)}
                usuarios={usuarios}
                atividades={atividadesEnriquecidas}
                onTransition={handleTransition}
              />
            ))}
          </div>
        )}

        {/* ── Empty state ── */}
        {!loading && !error && progressos.length === 0 && (
          <div style={{
            textAlign: "center", padding: "64px 0",
            color: "rgba(255,255,255,.2)", fontSize: 13, fontFamily: "'DM Mono',monospace",
            lineHeight: 2,
          }}>
            Nenhum progresso encontrado.<br/>
            Crie um usuário → disciplina → atividade → matricule o aluno.<br/>
            O progresso é gerado automaticamente ao matricular e criar atividades.
          </div>
        )}
      </div>

      {/* ── Modals ── */}
      {modal === "usuario"    && <ModalUsuario    onClose={() => setModal(null)} onSaved={reload} toast={showToast} />}
      {modal === "disciplina" && <ModalDisciplina onClose={() => setModal(null)} onSaved={reload} toast={showToast} usuarios={usuarios} />}
      {modal === "atividade"  && <ModalAtividade  onClose={() => setModal(null)} onSaved={reload} toast={showToast} disciplinas={disciplinas} />}
      {modal === "matricular" && <ModalMatricular onClose={() => setModal(null)} onSaved={reload} toast={showToast} disciplinas={disciplinas} usuarios={usuarios} />}

      <Toast msg={toast} onClose={() => setToast(null)} />
    </>
  );
}
npm run dev